# --- Step 5: run the tools Claude asked for, send the results back ---
messages.append({"role": "assistant", "content": response.content})

results = []
for block in response.content:
    if block.type == "tool_use":
        output = TOOLS[block.name](**block.input)      # we do the work
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,                   # match the request
            "content": output,
        })
messages.append({"role": "user", "content": results})

print("\n--- second call ---")
show(ask_claude(messages))
