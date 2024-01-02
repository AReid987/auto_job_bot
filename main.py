from pprint import pprint
import time
import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
  'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
  conversation_history.append(prompt)

  full_prompt = "\n".join(conversation_history)

  data = {
    "model": "antonio",
    "stream": False,
    "prompt": full_prompt,
  }

  response = requests.post(url, headers=headers, data=json.dumps(data))

  if response.status_code == 200:
    response_text = response.text
    data = json.loads(response_text)
    actual_response = data["response"]
    conversation_history.append(actual_response)
    pprint(actual_response)
    return actual_response
  else:
    pprint("Error: ", response.status_code, response.text)

try:
  while True:
    prompt = input("Enter a command: ")
    if prompt == "exit":
      break
    generate_response(prompt)
    time.sleep(1)
except KeyboardInterrupt:
  pass
finally:
  pass