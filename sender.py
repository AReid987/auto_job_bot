import subprocess
from sys import stderr, stdin, stdout
import time

# start ollama with llama2 13B
result = subprocess.Popen(
  ["ollama", "run", "llama2:13B"],
  stdin=stdin,
  stdout=stdout,
  stderr=stderr
)

output, error = result.communicate()
print("Output: ", output.decode())
print("Error: ", error.decode())

# Function to send a command to the listener
def send_command(command):
  print(f"Sending command: {command}")
  result.stdin.write(f"{command}\n")
  result.stdin.flush()

try:
  while True:
    command = input("Enter a command: ")
    if command == "exit":
      break
    send_command(command)
    time.sleep(1)
except KeyboardInterrupt:
  pass
finally:
  result.terminate()