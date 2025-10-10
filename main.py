from nba_agents.search_agent import search_agent
from nba_agents.data_agent import data_agent
from nba_agents.visualization_agent import visualization_agent
from nba_agents.orchestrator_agent import orchestrator_agent
from agents import Runner
import asyncio
from dotenv import load_dotenv
import gradio as gr
from vizualization_utils import generate_chart_from_json
import json
import re 
import os 


load_dotenv(override=True)


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
        # Create a new event loop for synchronous calls (necessary for non-async main function)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Step 1: Search
            print("1. Running Search Agent...")
            search_response = loop.run_until_complete(self._run_agent(self.search_agent, user_query))
            search_results = getattr(search_response, 'data', str(search_response))

            # Step 2: Data extraction
            print("2. Running Data Extraction Agent...")
            data_prompt = f"Extract structured data from these search results:\n\n{search_results}"
            data_response = loop.run_until_complete(self._run_agent(self.data_agent, data_prompt))
            structured_data = getattr(data_response, 'data', str(data_response))

            # Step 3: Visualization
            needs_viz = self._needs_visualization(user_query)
            viz_json = None
            chart_image = None
            viz_json_raw = None

            if needs_viz:
                print("3. Running Visualization Agent...")
                
                # --- FINAL FIXED VIZ_PROMPT FOR DATA STRUCTURE CLARITY ---
                viz_prompt = (
                    f"Create appropriate visualization for this query: {user_query}\n\n"
                    f"Using this structured data:\n{structured_data}\n\n"
                    f"CRITICAL DATA REMINDER: Ensure the 'data' field in your JSON output "
                    f"contains a key named **'labels'** (for x-axis categories) and additional keys "
                    f"for each data series, where values are lists of numbers aligned with the labels."
                )
                # --- END VIZ_PROMPT FIX ---
                
                viz_response = loop.run_until_complete(self._run_agent(self.viz_agent, viz_prompt))
                viz_json_raw = getattr(viz_response, 'data', str(viz_response))
                
                # --- ROBUST JSON PARSING LOGIC TO HANDLE PROSE/CODE BLOCKS (PREVIOUS FIX) ---
                if isinstance(viz_json_raw, dict):
                    viz_json = viz_json_raw
                elif isinstance(viz_json_raw, str):
                    # Use regex to find and extract the JSON content inside ```json ... ```
                    json_match = re.search(r"```json\s*(.*?)\s*```", viz_json_raw, re.DOTALL)
                    json_string = viz_json_raw

                    if json_match:
                        json_string = json_match.group(1).strip()
                        print("✅ Extracted JSON from Markdown block.")
                    else:
                        json_string = json_string.strip()
                        print("⚠️ No Markdown block found. Attempting to parse raw string.")

                    try:
                        if json_string.startswith('{'): 
                            viz_json = json.loads(json_string)
                            print("✅ Successfully parsed JSON.")
                        else:
                            print(f"❌ Cleaned string does not start with '{{'. Skipping JSON load.")
                            viz_json = None

                    except json.JSONDecodeError as e:
                        print(f"❌ Final JSON decoding failed: {e}. Raw (extracted) string sample: {json_string[:200]}...")
                        viz_json = None
                
                if isinstance(viz_json, dict):
                    chart_image = generate_chart_from_json(viz_json)
                    if chart_image:
                        print("✅ Chart Image successfully generated (PIL Image).")
                    else:
                        print("❌ Chart Image failed to generate (generate_chart_from_json returned None).")
                else:
                    print(f"❌ Visualization JSON is not a dictionary or failed to parse. Skipping visualization.")
            
            # Step 4: Orchestrate final answer
            print("4. Running Orchestrator Agent...")
            final_prompt = (
                f"User query: {user_query}\n\n"
                f"Search results: {search_results}\n\n"
                f"Structured data: {structured_data}\n\n"
                f"Visualization: {viz_json if viz_json else 'None'}\n\n"
                f"Provide a complete, helpful response to the user."
                f"Provide answers only to the requested query in a concise format. Do not include extra narrative."
            )
            final_response = loop.run_until_complete(self._run_agent(self.orchestrator, final_prompt))
            final_answer = getattr(final_response, 'data', str(final_response))

            # Store history
            chart_title = viz_json.get("title") if isinstance(viz_json, dict) else ""
            self.conversation_history.append({
                'query': user_query,
                'answer': final_answer,
                'data': structured_data,
                'visualization': chart_image,
                'visualization_title': chart_title
            })

            return {
                'answer': final_answer,
                'structured_data': structured_data,
                'visualization': chart_image,
                'search_results': search_results
            }

        except Exception as e:
            print(f"An unexpected error occurred in process_query: {e}")
            return {
                'answer': f"An error occurred: {e}",
                'structured_data': None,
                'visualization': None,
                'search_results': None
            }
        finally:
            loop.close()

    def _needs_visualization(self, query: str) -> bool:
        viz_keywords = [
            'compare', 'comparison', 'vs', 'versus', 'trend', 'over time',
            'chart', 'graph', 'visualize', 'show me', 'plot',
            'career', 'progression', 'leaders', 'top', 'ranking'
        ]
        return any(keyword in query.lower() for keyword in viz_keywords)

    def chat(self):
        print("🏀 NBA Stats Chatbot - Ready! Type 'quit' to exit.\n")
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                if not user_input:
                    continue

                result = self.process_query(user_input)
                print(f"\n🤖 NBA Stats Bot:\n{result['answer']}\n")
                if result['visualization']:
                    result['visualization'].show()
                print("="*80 + "\n")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")

# --- Gradio ---
def launch_gradio():
    bot = NBAStatsChatbot()

    def gradio_interface(user_input):
        result = bot.process_query(user_input)
        answer_text = result.get("answer", "")
        chart_image = result.get("visualization", None)
        chart_caption = ""

        if chart_image:
            last_entry = bot.conversation_history[-1]
            chart_caption = f"📊 **{last_entry.get('visualization_title', 'Visualization')}**"
        else:
            chart_caption = "⚠️ **Visualization could not be generated.**" 

        return f"🧠 **Answer:**\n{answer_text}\n\n{chart_caption}", chart_image

    iface = gr.Interface(
        fn=gradio_interface,
        inputs=gr.Textbox(label="Ask about NBA stats:", placeholder="e.g. Compare Curry vs Lillard 3PT %"),
        outputs=[gr.Markdown(label="Answer & Caption"), gr.Image(label="Visualization", type="pil")],
        title="🏀 NBA Stats Chatbot",
        description="Ask anything about NBA players, stats, or comparisons.",
        allow_flagging="never"
    )
    iface.launch()

def main():
    bot = NBAStatsChatbot()
    mode = input("Run in (1) Terminal Mode or (2) Gradio Web Mode? [1/2]: ").strip()
    if mode == "2":
        launch_gradio()
    else:
        bot.chat()

if __name__ == "__main__":
    main()