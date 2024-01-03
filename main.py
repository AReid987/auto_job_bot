import csv
from pprint import pprint
import time
import requests
import json
import csv_formatter
import subprocess
import time

url = "http://localhost:11434/api/generate"

headers = {
  'Content-Type': 'application/json',
}

conversation_history = []

def convert_string_to_bool(input_string):
  input_string = input_string.lower().strip()
  if input_string == 'yes.' or input_string == 'yes':
    return True
  elif input_string == 'no.' or input_string == 'no':
    return False
  else:
    raise ValueError("Input must be 'yes.' or 'no.'")
# ask antonio-llama2 to compare the question and csv_question
def is_question_similar(question, csv_question):
  pprint(f"question: {question}")
  pprint(f"csv question: {csv_question}")
  prompt = f"Answer with one word:'yes' or 'no'. Are the following prompts similar enough to warrant the same answer? 1. {question} 2. {csv_question}"
  answer = generate_response(prompt)
  time.sleep(1)
  try:
    response = convert_string_to_bool(answer)
    pprint(f"response: {response}")
    return response
  except ValueError:
    pprint(f"Unclear response: {answer}")

# look for the question in qa_pairs.csv
def find_answer_in_file(question, qa_pairs):
  pprint(qa_pairs.keys())
  for csv_question in qa_pairs.keys():
    if is_question_similar(question, csv_question):
      pprint(qa_pairs[csv_question])
      return qa_pairs[csv_question]

  return None

def generate_response(prompt):
  # conversation_history.append(prompt)

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
    # conversation_history.append(actual_response)
    pprint(f"actual_response {actual_response}")
    return actual_response
  else:
    pprint("Error: ", response.status_code, response.text)
    return "Error"


def main():
  qa_pairs = csv_formatter.process_csv('qa_pairs.csv')

  try:
    while True:
      prompt = input("Enter a command: ")
      answer = find_answer_in_file(prompt, qa_pairs)
      if prompt == "exit":
        break
      if not answer:
        answer = generate_response(prompt)
      time.sleep(1)
  except KeyboardInterrupt as e:
    pprint("Error: {e}")
  finally:
    pprint("Fin")

if __name__ == "__main__":
  main()

