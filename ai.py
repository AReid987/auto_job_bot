from pprint import pprint
import requests
import json

model = "llama2:13b-chat"

url = "http://localhost:11434/api/chat"

def chat(messages):
  response = requests.post(
    url,
    json={"model": model, "messages": messages, "stream": True},
  )

  response.raise_for_status()
  output = ""

  for line in response.iter_lines():
    body = json.loads(line)
    if "error" in body:
      raise Exception(body["error"])
    if body.get("done") is False:
      message = body.get("message", "")
      content = message.get("content", "")
      output += content
      # pprint(content)

    if body.get("done", False):
      message["content"] = output
      return message



def main(inputs=None):
  messages = []

  while True:
    for user_input in inputs or []:
      if not user_input:
        exit()
      messages.append({"role": "user", "content": user_input})
      message = chat(messages)
      messages.append(message)
      pprint(message.get("content"))
      return message.get("content")

if __name__ == "__main__":
  main()