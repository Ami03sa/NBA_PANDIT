from nba_agents.search_agent import search_agent
from nba_agents.data_agent import data_agent
from nba_agents.visualization_agent import visualization_agent
from nba_agents.orchestrator_agent import orchestrator_agent
from agents import Runner
import asyncio
from dotenv import load_dotenv
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from vizualization_utils import generate_chart_from_json

# Load environment variables
load_dotenv(override=True)

# ------------------------------------
#   NBA STATS CHATBOT CLASS
# ------------------------------------
class NBAStatsChatbot:
    def __init__(self):
        self.search_agent = search_agent
        self.data_agent = data_agent
        self.viz_agent = visualization_agent
        self.orchestrator = orchestrator_agent
        self.conversation_history = []

        # ✅ Use a single event loop that stays open
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def _run_agent(self, agent, prompt):
        """Run any agent asynchronously and return structured output."""
        result = await Runner.run(agent, prompt)
        return getattr(result, "final_output", result)

    def process_query(self, user_query: str) -> dict:
        """Pipeline: Search → Data → (Viz) → Orchestrator."""
        try:
            print("1️⃣ Running Search Agent...")
            search_response = self.loop.run_until_complete(
                self._run_agent(self.search_agent, user_query)
            )
            search_results = getattr(search_response, "data", str(search_response))

            print("2️⃣ Running Data Agent...")
            data_prompt = f"Extract structured NBA data from these search results:\n\n{search_results}"
            data_response = self.loop.run_until_complete(
                self._run_agent(self.data_agent, data_prompt)
            )
            structured_data = getattr(data_response, "data", str(data_response))

            print("3️⃣ Checking if visualization is needed...")
            needs_viz = self._needs_visualization(user_query)
            viz_json = None
            chart_base64 = None

            if needs_viz:
                print("📊 Visualization requested...")
                viz_prompt = (
                    f"Generate a visualization for: '{user_query}'.\n"
                    f"Use this structured data:\n{structured_data}\n\n"
                    f"Return JSON with 'title', 'type', 'labels', and 'datasets'."
                )
                viz_response = self.loop.run_until_complete(
                    self._run_agent(self.viz_agent, viz_prompt)
                )
                viz_json_raw = getattr(viz_response, "data", str(viz_response))
                viz_json = self._safe_json_parse(viz_json_raw)

                if isinstance(viz_json, dict):
                    if "data" in viz_json and "labels" in viz_json["data"]:
                        viz_json_fixed = {
                            "title": viz_json.get("title", "NBA Visualization"),
                            "labels": viz_json["data"].get("labels", []),
                            "datasets": [
                                {"label": k, "data": v}
                                for k, v in viz_json["data"].items()
                                if k != "labels"
                            ],
                        }
                    else:
                        viz_json_fixed = viz_json

                    try:
                        chart_base64 = generate_chart_from_json(viz_json_fixed)
                    except Exception as chart_err:
                        print(f"⚠️ Chart generation failed: {chart_err}")
                        chart_base64 = None
                else:
                    print("⚠️ Invalid visualization JSON received, skipping chart.")

            print("4️⃣ Running Orchestrator Agent...")
            final_prompt = (
                f"User query: {user_query}\n\n"
                f"Search results: {search_results}\n\n"
                f"Structured data: {structured_data}\n\n"
                f"Visualization JSON: {json.dumps(viz_json, indent=2) if viz_json else 'None'}\n\n"
                f"Provide a concise, factual, conversational summary for the user."
            )
            final_response = self.loop.run_until_complete(
                self._run_agent(self.orchestrator, final_prompt)
            )
            final_answer = getattr(final_response, "data", str(final_response))

            chart_title = viz_json.get("title") if isinstance(viz_json, dict) else ""
            self.conversation_history.append(
                {
                    "query": user_query,
                    "answer": final_answer,
                    "data": structured_data,
                    "visualization": chart_base64,
                    "visualization_title": chart_title,
                }
            )

            return {
                "answer": final_answer,
                "structured_data": structured_data,
                "visualization": chart_base64,
                "search_results": search_results,
                "chart_title": chart_title,
            }

        except Exception as e:
            print(f"❌ Error in process_query: {e}")
            return {
                "answer": f"An error occurred: {e}",
                "structured_data": None,
                "visualization": None,
                "search_results": None,
            }

    def _safe_json_parse(self, raw):
        """Extract valid JSON safely."""
        if isinstance(raw, dict):
            return raw
        json_match = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
        json_string = json_match.group(1).strip() if json_match else raw.strip()
        try:
            parsed = json.loads(json_string)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed.")
            return None

    def _needs_visualization(self, query: str) -> bool:
        """Detect if query needs visualization."""
        keywords = [
            "compare", "vs", "trend", "over time", "chart", "graph",
            "visualize", "plot", "career", "leaders", "ranking",
            "stats", "points", "rebounds", "assists", "shooting", "matchup"
        ]
        return any(k in query.lower() for k in keywords)


# ------------------------------------
#   FLASK SERVER SETUP
# ------------------------------------
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
        return jsonify({
            "reply": result.get("answer", ""),
            "has_visualization": bool(result.get("visualization")),
            "chart_image": result.get("visualization"),
            "chart_title": result.get("chart_title", "")
        })
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🏀 Flask backend running at http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=True)
