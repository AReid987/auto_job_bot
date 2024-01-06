from pprint import pprint
import time
import requests
import json
import time

url = "http://localhost:11434/api/generate"

headers = {
  'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
  conversation_history.append(prompt)

  # full_prompt = "\n".join(conversation_history)

  data = {
    "model": "antonio-llama2",
    "stream": False,
    "prompt": prompt,
  }

  response = requests.post(url, headers=headers, data=json.dumps(data))

  if response.status_code == 200:
    response_text = response.text
    data = json.loads(response_text)
    actual_response = data["response"].strip().split('\n')[-1]
    conversation_history.append(actual_response)
    pprint(f"actual_response {actual_response}")
    return actual_response
  else:
    pprint("Error: ", response.status_code, response.text)
    return "Error"


def main():
  try:
    while True:
      prompt = input("Enter a command: ")
      if prompt == "exit":
        break

      answer = generate_response(prompt)
      time.sleep(1)
  except KeyboardInterrupt as e:
    pprint("Error: {e}")
  finally:
    pprint("Fin")

if __name__ == "__main__":
  main()

