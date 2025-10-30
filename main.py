from nba_agents.search_agent import search_agent
from nba_agents.data_agent import data_agent
from nba_agents.visualization_agent import visualization_agent
from nba_agents.orchestrator_agent import orchestrator_agent
from agents import Runner
import asyncio
from dotenv import load_dotenv
import json
import re
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from vizualization_utils import generate_chart_from_json

# Load environment variables
load_dotenv(override=True)

# -----------------------------
#   NBA STATS CHATBOT CLASS
# -----------------------------
class NBAStatsChatbot:
    def __init__(self):
        self.search_agent = search_agent
        self.data_agent = data_agent
        self.viz_agent = visualization_agent
        self.orchestrator = orchestrator_agent
        self.conversation_history = []

    async def _run_agent(self, agent, prompt):
        result = await Runner.run(agent, prompt)
        return getattr(result, 'final_output', result)

    def process_query(self, user_query: str) -> dict:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Step 1: Search
            print("1️⃣ Running Search Agent...")
            search_response = loop.run_until_complete(self._run_agent(self.search_agent, user_query))
            search_results = getattr(search_response, 'data', str(search_response))

            # Step 2: Data Extraction
            print("2️⃣ Running Data Agent...")
            data_prompt = f"Extract structured data from these search results:\n\n{search_results}"
            data_response = loop.run_until_complete(self._run_agent(self.data_agent, data_prompt))
            structured_data = getattr(data_response, 'data', str(data_response))

            # Step 3: Visualization (if needed)
            needs_viz = self._needs_visualization(user_query)
            viz_json = None
            chart_image = None

            if needs_viz:
                print("3️⃣ Running Visualization Agent...")
                viz_prompt = (
                    f"Create a visualization for: {user_query}\n"
                    f"Using structured data:\n{structured_data}\n\n"
                    f"Ensure JSON includes 'labels' (x-axis) and numeric lists for each series."
                )

                viz_response = loop.run_until_complete(self._run_agent(self.viz_agent, viz_prompt))
                viz_json_raw = getattr(viz_response, 'data', str(viz_response))

                if isinstance(viz_json_raw, dict):
                    viz_json = viz_json_raw
                elif isinstance(viz_json_raw, str):
                    json_match = re.search(r"```json\s*(.*?)\s*```", viz_json_raw, re.DOTALL)
                    json_string = json_match.group(1).strip() if json_match else viz_json_raw.strip()
                    try:
                        viz_json = json.loads(json_string) if json_string.startswith('{') else None
                    except json.JSONDecodeError:
                        viz_json = None

                if isinstance(viz_json, dict):
                    chart_image = generate_chart_from_json(viz_json)

            # Step 4: Orchestrator Agent
            print("4️⃣ Running Orchestrator Agent...")
            final_prompt = (
                f"User query: {user_query}\n\n"
                f"Search results: {search_results}\n\n"
                f"Structured data: {structured_data}\n\n"
                f"Visualization: {viz_json if viz_json else 'None'}\n\n"
                f"Provide a concise, factual response."
            )
            final_response = loop.run_until_complete(self._run_agent(self.orchestrator, final_prompt))
            final_answer = getattr(final_response, 'data', str(final_response))

            # Save conversation
            chart_title = viz_json.get("title") if isinstance(viz_json, dict) else ""
            self.conversation_history.append({
                "query": user_query,
                "answer": final_answer,
                "data": structured_data,
                "visualization": chart_image,
                "visualization_title": chart_title,
            })

            return {
                "answer": final_answer,
                "structured_data": structured_data,
                "visualization": chart_image,
                "search_results": search_results,
            }

        except Exception as e:
            print(f"❌ Error in process_query: {e}")
            return {
                "answer": f"An error occurred: {e}",
                "structured_data": None,
                "visualization": None,
                "search_results": None,
            }
        finally:
            loop.close()

    def _needs_visualization(self, query: str) -> bool:
        keywords = [
            "compare", "vs", "versus", "trend", "over time", "chart", "graph",
            "visualize", "show me", "plot", "career", "progression", "leaders", "ranking"
        ]
        return any(k in query.lower() for k in keywords)


# -----------------------------
#   FLASK API SETUP
# -----------------------------
app = Flask(__name__)
CORS(app)
bot = NBAStatsChatbot()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "Missing 'message' field"}), 400

        result = bot.process_query(user_input)
        answer = result.get("answer", "")
        has_chart = bool(result.get("visualization"))
        chart_title = bot.conversation_history[-1].get("visualization_title", "") if has_chart else ""

        return jsonify({
            "reply": answer,
            "has_visualization": has_chart,
            "chart_title": chart_title,
        })

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500


# -----------------------------
#   ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    print("🏀 Flask backend running at http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=True)
