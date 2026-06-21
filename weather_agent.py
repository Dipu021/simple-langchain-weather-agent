from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import os
import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================
#              TOOLS
# ============================================

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    weather_options = ["Sunny ☀️", "Rainy 🌧️", "Cloudy ⛅", "Snowy ❄️", "Windy 🌬️"]
    temp = random.randint(15, 35)
    condition = random.choice(weather_options)
    return f"Weather in {city}: {condition}, {temp}°C"

@tool
def get_current_time(timezone: str) -> str:
    """Get the current date and time."""
    now = datetime.datetime.now()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression like '25 * 4 + 10'."""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def tell_joke(topic: str) -> str:
    """Tell a fun joke about a given topic."""
    jokes = {
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "math": "Why was the math book sad? Because it had too many problems! 📚",
        "ai": "Why did the AI go to school? To improve its learning rate! 🤖",
    }
    return jokes.get(topic.lower(), f"Why did the {topic} cross the road? To get to the other side! 😄")

# ============================================
#              AGENT SETUP
# ============================================

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
tools = [get_weather, get_current_time, calculate, tell_joke]
llm_with_tools = llm.bind_tools(tools)
tool_map = {t.name: t for t in tools}

# ============================================
#              AGENT RUNNER
# ============================================

def run_agent(user_input: str):
    print(f"\n👤 You: {user_input}")
    print("-" * 40)

    messages = [
        SystemMessage(content="""You are a smart helpful assistant. 
        Use tools when needed to answer questions accurately."""),
        HumanMessage(content=user_input)
    ]

    # Agentic loop — keeps running until no more tool calls
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If no tool calls, we have the final answer
        if not response.tool_calls:
            print(f"🤖 Assistant: {response.content}")
            break

        # Process each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"🔧 Using tool: {tool_name} with {tool_args}")

            result = tool_map[tool_name].invoke(tool_args)
            print(f"✅ Tool result: {result}")

            messages.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            ))

# ============================================
#              RUN IT
# ============================================

if __name__ == "__main__":
    run_agent("What's the weather in Nepal and what time is it in Nepal?")
    run_agent("What is 1234 * 5678?")
    run_agent("Tell me a joke about AI")