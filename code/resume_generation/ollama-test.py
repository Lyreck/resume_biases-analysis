from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='mistral-small', messages=[
  {
    'role': 'user',
    'content': 'Print just one random letter of the alphabet (just print the letter, nothing else)',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)