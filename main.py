import os
from nba_agents.search_agent import search_agent
from nba_agents.data_agent import data_agent
from nba_agents.visualization_agent import visualization_agent
from nba_agents.orchestrator_agent import orchestrator_agent

import json

class NBAStatsChatbot:
    def __init__(self):
        self.search_agent = search_agent
        self.data_agent = data_agent
        self.viz_agent = visualization_agent
        self.orchestrator = orchestrator_agent
        self.conversation_history = []
    
    def process_query(self, user_query: str) -> dict:
        """
        Process a user query through the agent pipeline
        Returns: dict with answer, data, and visualization
        """
        print(f"\n🏀 Processing query: {user_query}\n")
        
        # Step 1: Search for information
        print("📊 Step 1: Searching for NBA data...")
        search_response = self.search_agent.run(user_query)
        search_results = search_response.messages[-1].content
        print(f"✓ Search complete\n")
        
        # Step 2: Extract and structure data
        print("📋 Step 2: Processing and structuring data...")
        data_prompt = f"Extract structured data from these search results:\n\n{search_results}"
        data_response = self.data_agent.run(data_prompt)
        structured_data = data_response.messages[-1].content
        print(f"✓ Data structured\n")
        
        # Step 3: Determine if visualization is needed and create it
        print("📈 Step 3: Creating visualization...")
        needs_viz = self._needs_visualization(user_query)
        visualization = None
        
        if needs_viz:
            viz_prompt = (
                f"Create appropriate visualization for this query: {user_query}\n\n"
                f"Using this structured data:\n{structured_data}"
            )
            viz_response = self.viz_agent.run(viz_prompt)
            visualization = viz_response.messages[-1].content
            print(f"✓ Visualization created\n")
        else:
            print(f"✓ No visualization needed\n")
        
        # Step 4: Synthesize final response
        print("🎯 Step 4: Generating final response...")
        final_prompt = (
            f"User query: {user_query}\n\n"
            f"Search results: {search_results}\n\n"
            f"Structured data: {structured_data}\n\n"
            f"Visualization: {visualization if visualization else 'None'}\n\n"
            f"Provide a complete, helpful response to the user."
        )
        final_response = self.orchestrator.run(final_prompt)
        final_answer = final_response.messages[-1].content
        print(f"✓ Response ready\n")
        
        # Store in conversation history
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
    
    def _needs_visualization(self, query: str) -> bool:
        """Determine if query would benefit from visualization"""
        viz_keywords = [
            'compare', 'comparison', 'vs', 'versus', 'trend', 'over time',
            'chart', 'graph', 'visualize', 'show me', 'plot',
            'career', 'progression', 'leaders', 'top', 'ranking'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in viz_keywords)
    
    def chat(self):
        """Interactive chat mode"""
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
                
                # Process the query
                result = self.process_query(user_input)
                
                # Display the answer
                print(f"\n🤖 NBA Stats Bot:\n")
                print(result['answer'])
                print("\n" + "="*80 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using NBA Stats Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
                print("Please try again with a different query.\n")


def main():
    # Initialize the chatbot
    bot = NBAStatsChatbot()
    
    # Example queries for testing
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
        # Start interactive chat
        bot.chat()


if __name__ == "__main__":
    main()