# Replace the simulated response with:
import openai

# In the sendMessage function:
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
)
ai_message = response.choices[0].message['content']
