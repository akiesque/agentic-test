import ollama

def get_weather(city):
    fake_data = {
        "Manila": "32°C, humid, chance of rain",
        "Singapore": "30°C, thunderstorms likely",
        "Tokyo": "18°C, clear skies",
    }
    return fake_data.get(city, f"No data for {city}")

# Ollama uses the OpenAI-style tool format, not Anthropic's -
# note "type": "function" wrapping, and "parameters" instead of "input_schema"
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "Compare the weather in Manila and Tokyo. Which is nicer right now?"}
]

while True:
    response = ollama.chat(
        model="llama3.2",   # or "llama3.2" - swap to test the difference
        messages=messages,
        tools=tools
    )

    msg = response["message"]
    messages.append(msg)  # append the whole message, same idea as before

    # No "stop_reason" field in Ollama - instead, check if tool_calls exists
    if not msg.get("tool_calls"):
        print("FINAL ANSWER:", msg["content"])
        break

    # Ollama can also return multiple tool_calls in one message
    for call in msg["tool_calls"]:
        name = call["function"]["name"]
        args = call["function"]["arguments"]  # already a dict, no JSON parsing needed
        print(f"  -> model wants to call {name}({args})")

        result = get_weather(args["city"]) if name == "get_weather" else f"Unknown tool {name}"
        print(f"     result: {result}")

        # Ollama's tool-result message is simpler - no tool_use_id matching needed,
        # just role "tool" + content + which tool it came from
        messages.append({"role": "tool", "content": result, "name": name})