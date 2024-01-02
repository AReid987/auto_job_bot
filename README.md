# To run the app

Requirements:

ollama
Download ollama: [https://ollama.ai/download](https://ollama.ai/download)

After downloading ollama, you can execute AI agents via the command line on your local machine by running "ollama run model_name"

For example: "ollama run llama2:13b"

.env
Create a .env file. Add the following variables
PROMPT_PERSONA=""
The PROMPT_PERSONA is used by the Modelfile to instruct the AI agent on how to respond and who to respond as. Write a prompt persona that describes who you are, providing key details. You should also include the explicit instructions to only answer as "NAME"

LINKEDIN_USERNAME=
The email address for the LinkedIn account you wish to use

LINKEDIN_PASSWORD=
The password for the LinkedIn username you wish to use

Feel free to experiment with different AI models: [https://ollama.ai/library](https://ollama.ai/library)

After completing the .env file create the model by running in the terminal:

ollama create "NAME" -f ./Modelfile

Install the requirements:
pipenv install -r requirements.txt
pipenv shell

execute the script with "python main.py"
