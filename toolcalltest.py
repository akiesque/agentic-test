import anthropic

client = anthropic.Anthropic()

def get_weather(city):
    fake_data = {
        "Manila": "32°C, humid, chance of rain",
        "Singapore": "30°C, thunderstorms likely",
    }
    return fake_data.get(city, f"No data for {city}")

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"}
            },
            "required": ["city"]
        }
    }
]

messages = [
    {"role": "user", "content": "What's the weather in Manila right now?"}
]

# --- First call: Claude decides it needs the tool ---
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    tools=tools,
    messages=messages
)

print("First stop_reason:", response.stop_reason)

# Claude's tool-use request goes into the conversation history
# as if IT said "I want to call this tool" - so we append its
# whole response as an "assistant" turn.
messages.append({"role": "assistant", "content": response.content})

# Find the tool_use block and actually run the real function
tool_use_block = next(b for b in response.content if b.type == "tool_use")
city = tool_use_block.input["city"]
result = get_weather(city)  # <-- your real function runs HERE, not inside Claude

print("Ran get_weather(", city, ") ->", result)

# Now we send the RESULT back, tagged with the same tool_use id
# so Claude knows which call this answers.
messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": tool_use_block.id,
            "content": result
        }
    ]
})

# --- Second call: Claude now has the real data and can answer ---
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    tools=tools,
    messages=messages
)

print("Second stop_reason:", response2.stop_reason)
print("Final answer:", response2.content[0].text)