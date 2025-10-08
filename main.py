from nba_agents.search_agent import search_agent
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
        """Run agent asynchronously and return final output"""
        result = await Runner.run(agent, prompt)
        # If agent returns an object with .final_output, use it
        return getattr(result, 'final_output', result)

    def process_query(self, user_query: str) -> dict:
        """Process a user query through the agent pipeline"""
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
    main()
