from agents import Agent , WebSearchTool, ModelSettings


INSTRUCTIONS = (
    "You are an NBA stats research assistant. Given a query about anything from the NBA, "
    "search the web for that question and summarize accurately in concise bullet points. "
    "Always prioritize official or authoritative basketball sources like statmuse.com, nba.com, espn.com, "
    "basketball-reference.com, theathletic.com, and bleacherreport.com. "
    "Your goal is to return only the essential information that answers the query clearly and precisely, "
    "with no filler or unrelated data. Keep it short and factual."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)