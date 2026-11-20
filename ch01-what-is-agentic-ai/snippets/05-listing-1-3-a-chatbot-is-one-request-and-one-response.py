import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    messages=[{"role": "user",
               "content": "Explain what a Python generator is."}],
)
# The reply is a list of blocks; keep only the text ones.
print("".join(b.text for b in response.content if b.type == "text"))
