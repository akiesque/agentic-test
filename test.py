import anthropic

client = anthropic.Anthropic()

# This is the fake tool. It doesn't call a real weather API -
# we're isolating the AGENT logic, not weather data.
def get_weather(city):
    fake_data = {
        "Manila": "32°C, humid, chance of rain",
        "Singapore": "30°C, thunderstorms likely",
    }
    return fake_data.get(city, f"No data for {city}")

# This describes the tool to Claude, so it knows the tool EXISTS
# and what arguments it takes. Claude never runs this itself -
# it just decides WHEN to ask for it.
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

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in Manila right now?"}
    ]
)

print(response.stop_reason)
print(response.content)