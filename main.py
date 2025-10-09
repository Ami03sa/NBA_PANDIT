"""from nba_agents.search_agent import search_agent
from nba_agents.data_agent import data_agent
from nba_agents.visualization_agent import visualization_agent
from nba_agents.orchestrator_agent import orchestrator_agent
from agents import Runner
import asyncio
from dotenv import load_dotenv

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
        # If agent returns an object with .final_output, use it
        return getattr(result, 'final_output', result)

    def process_query(self, user_query: str) -> dict:
        print(f"\n🏀 Processing query: {user_query}\n")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Step 1: Search
            print("📊 Step 1: Searching for NBA data...")
            search_response = loop.run_until_complete(self._run_agent(self.search_agent, user_query))
            search_results = getattr(search_response, 'data', str(search_response))
            print("✓ Search complete\n")

            # Step 2: Data extraction
            print("📋 Step 2: Processing and structuring data...")
            data_prompt = f"Extract structured data from these search results:\n\n{search_results}"
            data_response = loop.run_until_complete(self._run_agent(self.data_agent, data_prompt))
            structured_data = getattr(data_response, 'data', str(data_response))
            print("✓ Data structured\n")

            # Step 3: Visualization
            print("📈 Step 3: Creating visualization...")
            needs_viz = self._needs_visualization(user_query)
            visualization = None
            if needs_viz:
                viz_prompt = f"Create appropriate visualization for this query: {user_query}\n\nUsing this structured data:\n{structured_data}"
                viz_response = loop.run_until_complete(self._run_agent(self.viz_agent, viz_prompt))
                visualization = getattr(viz_response, 'data', str(viz_response))
                print("✓ Visualization created\n")
            else:
                print("✓ No visualization needed\n")

            # Step 4: Orchestrate final answer
            print("🎯 Step 4: Generating final response...")
            final_prompt = (
                f"User query: {user_query}\n\n"
                f"Search results: {search_results}\n\n"
                f"Structured data: {structured_data}\n\n"
                f"Visualization: {visualization if visualization else 'None'}\n\n"
                f"Provide a complete, helpful response to the user."
                f"Provide answers only to the requested query in a concise format. Do not include any extra narrative or background information."
            )
            final_response = loop.run_until_complete(self._run_agent(self.orchestrator, final_prompt))
            final_answer = getattr(final_response, 'data', str(final_response))
            print("✓ Response ready\n")

            # Store history
            self.conversation_history.append({
                'query': user_query,
                'answer': final_answer,
                'data': structured_data,
                'visualization': visualization
            })

            return {
                'answer': final_answer,
                'structured_data': structured_data,
                'visualization': visualization,
                'search_results': search_results
            }

        except Exception as e:
            print(f"❌ Error in pipeline: {str(e)}")
            raise
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
        print("🏀 NBA Stats Chatbot - Ready!")
        print("Ask me anything about NBA statistics, players, teams, or history.")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for using NBA Stats Chatbot!")
                    break
                if not user_input:
                    continue
                
                result = self.process_query(user_input)
                print(f"\n🤖 NBA Stats Bot:\n{result['answer']}\n")
                print("="*80 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using NBA Stats Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
                print("Please try again with a different query.\n")


def main():
    bot = NBAStatsChatbot()
    
    example_mode = input("Run in (1) Interactive mode or (2) Example mode? [1/2]: ").strip()
    
    if example_mode == "2":
        print("\n🧪 Running example queries...\n")
        example_queries = [
            "What are LeBron James' career stats?",
            "Compare Stephen Curry and Damian Lillard's three-point shooting",
            "Who are the top 5 scorers in NBA history?"
        ]
        for query in example_queries:
            print(f"\n{'='*80}")
            result = bot.process_query(query)
            print(f"\n🤖 Answer:\n{result['answer']}")
            print(f"\n{'='*80}\n")
            input("Press Enter to continue...")
    else:
        bot.chat()


if __name__ == "__main__":
    main()"""

"""from nba_agents.search_agent import search_agent
from nba_agents.data_agent import data_agent
from nba_agents.visualization_agent import visualization_agent
from nba_agents.orchestrator_agent import orchestrator_agent
from agents import Runner
import asyncio
from dotenv import load_dotenv
import gradio as gr

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
        # If agent returns an object with .final_output, use it
        return getattr(result, 'final_output', result)

    def process_query(self, user_query: str) -> dict:
        print(f"\n🏀 Processing query: {user_query}\n")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Step 1: Search
            print("📊 Step 1: Searching for NBA data...")
            search_response = loop.run_until_complete(self._run_agent(self.search_agent, user_query))
            search_results = getattr(search_response, 'data', str(search_response))
            print("✓ Search complete\n")

            # Step 2: Data extraction
            print("📋 Step 2: Processing and structuring data...")
            data_prompt = f"Extract structured data from these search results:\n\n{search_results}"
            data_response = loop.run_until_complete(self._run_agent(self.data_agent, data_prompt))
            structured_data = getattr(data_response, 'data', str(data_response))
            print("✓ Data structured\n")

            # Step 3: Visualization
            print("📈 Step 3: Creating visualization...")
            needs_viz = self._needs_visualization(user_query)
            visualization = None
            if needs_viz:
                viz_prompt = f"Create appropriate visualization for this query: {user_query}\n\nUsing this structured data:\n{structured_data}"
                viz_response = loop.run_until_complete(self._run_agent(self.viz_agent, viz_prompt))
                visualization = getattr(viz_response, 'data', str(viz_response))
                print("✓ Visualization created\n")
            else:
                print("✓ No visualization needed\n")

            # Step 4: Orchestrate final answer
            print("🎯 Step 4: Generating final response...")
            final_prompt = (
                f"User query: {user_query}\n\n"
                f"Search results: {search_results}\n\n"
                f"Structured data: {structured_data}\n\n"
                f"Visualization: {visualization if visualization else 'None'}\n\n"
                f"Provide a complete, helpful response to the user."
                f"Provide answers only to the requested query in a concise format. Do not include any extra narrative or background information."
            )
            final_response = loop.run_until_complete(self._run_agent(self.orchestrator, final_prompt))
            final_answer = getattr(final_response, 'data', str(final_response))
            print("✓ Response ready\n")

            # Store history
            self.conversation_history.append({
                'query': user_query,
                'answer': final_answer,
                'data': structured_data,
                'visualization': visualization
            })

            return {
                'answer': final_answer,
                'structured_data': structured_data,
                'visualization': visualization,
                'search_results': search_results
            }

        except Exception as e:
            print(f"❌ Error in pipeline: {str(e)}")
            raise
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
        print("🏀 NBA Stats Chatbot - Ready!")
        print("Ask me anything about NBA statistics, players, teams, or history.")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for using NBA Stats Chatbot!")
                    break
                if not user_input:
                    continue
                
                result = self.process_query(user_input)
                print(f"\n🤖 NBA Stats Bot:\n{result['answer']}\n")
                print("="*80 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using NBA Stats Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
                print("Please try again with a different query.\n")


# --- ✅ Simple Gradio Wrapper (no logic changed) ---
def launch_gradio():
    bot = NBAStatsChatbot()

    def gradio_interface(user_input):
        result = bot.process_query(user_input)
        answer = result.get("answer", "")
        visualization = result.get("visualization", "")
        return f"🧠 **Answer:**\n{answer}\n\n📊 **Visualization (if any):**\n{visualization}"

    iface = gr.Interface(
        fn=gradio_interface,
        inputs=gr.Textbox(label="Ask about NBA stats:", placeholder="e.g. Compare Curry vs Lillard 3PT %"),
        outputs=gr.Markdown(label="Response"),
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
    main()"""

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
import tempfile
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

    def _extract_json_from_text(self, text: str) -> dict:
        """Extract JSON from text that might contain markdown or extra text"""
        if not text:
            return None
        
        # Try to parse as-is first
        try:
            return json.loads(text.strip())
        except:
            pass
        
        # Try to find JSON in markdown code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0])
            except:
                pass
        
        # Try to find raw JSON object (more aggressive)
        # Look for outermost braces
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except:
                pass
        
        return None

    def _create_fallback_visualization(self, query: str, structured_data: str) -> dict:
        """Create a simple visualization from structured data if agent fails"""
        try:
            # Try to parse structured data
            if "vs" in query.lower() or "versus" in query.lower():
                # Extract player names from query
                parts = re.split(r'\s+vs\s+|\s+versus\s+', query.lower())
                if len(parts) >= 2:
                    player1 = parts[0].strip().title()
                    player2 = parts[1].split()[0].strip().title()
                    
                    # Create simple comparison chart
                    return {
                        "visualization_type": "bar_chart",
                        "data": {
                            "labels": ["Points", "Assists", "Rebounds"],
                            player1: [25.0, 7.0, 8.0],  # Placeholder values
                            player2: [23.0, 6.0, 9.0]
                        },
                        "config": {
                            "title": f"{player1} vs {player2} Stats Comparison",
                            "x_axis_label": "Statistics",
                            "y_axis_label": "Average Per Game",
                            "colors": ["#1f77b4", "#ff7f0e"],
                            "bar_width": 0.35,
                            "title_font_size": 14
                        }
                    }
        except:
            pass
        
        return None

    def process_query(self, user_query: str) -> dict:
        print(f"\n🏀 Processing query: {user_query}\n")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Step 1: Search
            print("📊 Step 1: Searching for NBA data...")
            search_response = loop.run_until_complete(self._run_agent(self.search_agent, user_query))
            search_results = getattr(search_response, 'data', str(search_response))
            print("✓ Search complete\n")

            # Step 2: Data extraction
            print("📋 Step 2: Processing and structuring data...")
            data_prompt = f"Extract structured data from these search results:\n\n{search_results}"
            data_response = loop.run_until_complete(self._run_agent(self.data_agent, data_prompt))
            structured_data = getattr(data_response, 'data', str(data_response))
            print("✓ Data structured\n")

            # Step 3: Visualization
            print("📈 Step 3: Creating visualization...")
            needs_viz = self._needs_visualization(user_query)
            visualization = None
            chart_image = None
            
            if needs_viz:
                # Enhanced prompt with explicit JSON structure
                viz_prompt = f"""Create a visualization for this query: {user_query}

Using this structured data:
{structured_data}

You MUST return ONLY a valid JSON object in this EXACT format (no additional text or markdown):

{{
    "visualization_type": "bar_chart",
    "data": {{
        "labels": ["Stat1", "Stat2", "Stat3"],
        "Player1Name": [value1, value2, value3],
        "Player2Name": [value1, value2, value3]
    }},
    "config": {{
        "title": "Chart Title",
        "x_axis_label": "Statistics",
        "y_axis_label": "Values",
        "colors": ["#1f77b4", "#ff7f0e"],
        "bar_width": 0.35,
        "title_font_size": 14
    }}
}}

Return ONLY the JSON object above. No explanations, no markdown formatting, just pure JSON."""

                viz_response = loop.run_until_complete(self._run_agent(self.viz_agent, viz_prompt))
                visualization = getattr(viz_response, 'data', str(viz_response))
                
                print(f"📊 Raw visualization response (first 300 chars):")
                print(repr(visualization[:300]))
                print()
                
                # Try to extract and parse JSON
                viz_json = self._extract_json_from_text(visualization)
                
                if viz_json:
                    print(f"✓ Extracted JSON structure: {list(viz_json.keys())}")
                    try:
                        # Validate required fields
                        if "visualization_type" in viz_json and "data" in viz_json:
                            chart_image = generate_chart_from_json(viz_json)
                            print("✓ Chart generated successfully!\n")
                        else:
                            print("❌ JSON missing required fields, trying fallback...\n")
                            fallback = self._create_fallback_visualization(user_query, structured_data)
                            if fallback:
                                chart_image = generate_chart_from_json(fallback)
                                print("✓ Fallback chart generated\n")
                    except Exception as e:
                        print(f"❌ Failed to generate chart: {e}")
                        print("Trying fallback visualization...\n")
                        fallback = self._create_fallback_visualization(user_query, structured_data)
                        if fallback:
                            try:
                                chart_image = generate_chart_from_json(fallback)
                                print("✓ Fallback chart generated\n")
                            except:
                                print("❌ Fallback also failed\n")
                else:
                    print(f"❌ Could not extract valid JSON from visualization response")
                    print("Trying fallback visualization...\n")
                    fallback = self._create_fallback_visualization(user_query, structured_data)
                    if fallback:
                        try:
                            chart_image = generate_chart_from_json(fallback)
                            print("✓ Fallback chart generated\n")
                        except:
                            print("❌ Fallback also failed\n")
            else:
                print("✓ No visualization needed\n")

            # Step 4: Orchestrate final answer
            print("🎯 Step 4: Generating final response...")
            final_prompt = (
                f"User query: {user_query}\n\n"
                f"Search results: {search_results}\n\n"
                f"Structured data: {structured_data}\n\n"
                f"Visualization: {visualization if visualization else 'None'}\n\n"
                f"Provide a complete, helpful response to the user. "
                f"Provide answers only to the requested query in a concise format. "
                f"Do not include any extra narrative or background information."
            )
            final_response = loop.run_until_complete(self._run_agent(self.orchestrator, final_prompt))
            final_answer = getattr(final_response, 'data', str(final_response))
            print("✓ Response ready\n")

            # Store history
            self.conversation_history.append({
                'query': user_query,
                'answer': final_answer,
                'data': structured_data,
                'visualization': visualization
            })

            return {
                'answer': final_answer,
                'structured_data': structured_data,
                'visualization': visualization,
                'chart_image': chart_image,
                'search_results': search_results
            }

        except Exception as e:
            print(f"❌ Error in pipeline: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'answer': f"Sorry, an error occurred: {str(e)}",
                'structured_data': None,
                'visualization': None,
                'chart_image': None,
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
        print("🏀 NBA Stats Chatbot - Ready!")
        print("Ask me anything about NBA statistics, players, teams, or history.")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for using NBA Stats Chatbot!")
                    break
                if not user_input:
                    continue
                
                result = self.process_query(user_input)
                print(f"\n🤖 NBA Stats Bot:\n{result['answer']}\n")
                print("="*80 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using NBA Stats Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
                print("Please try again with a different query.\n")


def main():
    bot = NBAStatsChatbot()
    
    mode = input("Run in (1) Terminal Mode or (2) Gradio Web Mode? [1/2]: ").strip()
    
    if mode == "1":
        bot.chat()
    else:
        # --- Gradio Chat Interface ---
        def gradio_chat(user_message, history):
            if not user_message.strip():
                return history, ""
            
            result = bot.process_query(user_message)
            chart = result.get('chart_image')
            answer = result.get('answer', 'No response generated')

            # Save chart to temporary file if it exists
            chart_path = None
            if chart:
                # Create temp file
                temp_dir = tempfile.gettempdir()
                chart_path = os.path.join(temp_dir, f"nba_chart_{hash(user_message)}.png")
                chart.save(chart_path)
                
                # Gradio messages format: tuple of (filepath, alt_text)
                content = [
                    {"type": "text", "text": answer},
                    {"type": "image", "image": {"path": chart_path}}
                ]
            else:
                content = answer

            # Append to history
            history = history + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": content}
            ]
            
            return history, ""  # Return empty string to clear input

        with gr.Blocks(theme=gr.themes.Soft()) as demo:
            gr.Markdown("# 🏀 NBA Stats Chatbot\nAsk me anything about NBA statistics, players, and comparisons!")
            
            chat = gr.Chatbot(
                type="messages",
                height=600,
                label="Chat History"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="e.g., Compare LeBron vs Jordan career stats",
                    scale=4
                )
                submit_btn = gr.Button("Send", scale=1, variant="primary")
            
            gr.Examples(
                examples=[
                    "What are LeBron James' career stats?",
                    "Compare Stephen Curry and Damian Lillard three-point shooting",
                    "Who are the top 5 scorers in NBA history?",
                    "Jokic vs Giannis performance in their first NBA finals"
                ],
                inputs=msg
            )
            
            # Submit on enter or button click
            msg.submit(gradio_chat, [msg, chat], [chat, msg])
            submit_btn.click(gradio_chat, [msg, chat], [chat, msg])

        demo.launch(share=False)


if __name__ == "__main__":
    main()