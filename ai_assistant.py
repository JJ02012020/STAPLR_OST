import ollama

def chat_with_mistral(query: str) -> str:
    """
    Chat with the Mistral model under Staplr's restricted behavior.
    - Responds only if the query relates to predefined Staplr functions.
    - Otherwise, returns a warning message.
    """

    system_prompt = (
        "You are an AI assistant named Staplr. "
        "You can only assist using the functions defined in Staplr.py. "
        "If the query is unrelated, reply exactly with: "
        "'⚠️ I can only assist with predefined functions in Staplr.'"
    )

    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.strip()}
            ]
        )

        # Safely extract the response content
        return response.get("message", {}).get("content", "⚠️ No valid response received from Mistral.")

    except Exception as e:
        return f"⚠️ An error occurred while processing your request: {e}"
