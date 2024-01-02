# Auto Job Bot

## Quickstart

### Requirements

#### ollama

- Download ollama: [https://ollama.ai/download](https://ollama.ai/download)

- After downloading ollama, you can execute AI agents via the command line on your local machine by running _ollama run model_name_

- _Examples_:
  - `ollama run llama2:13b`
  - `ollama run mistral`

#### .env

- Create a _.env_ file with the following variables:

  - `PROMPT_PERSONA=""`

    - The _PROMPT_PERSONA_ is used by the _Modelfile_ to instruct the AI agent on how to respond and who to respond as.
    - Write a prompt persona that describes who you are, providing relevant details about yourself.
    - You should also include the explicit instructions to _only answer as "YOUR NAME"_

  - `LINKEDIN_USERNAME=`

    - The email address for the LinkedIn account you wish to use

  - `LINKEDIN_PASSWORD=`
    - The password for the LinkedIn account you wish to use

- _Note_: Feel free to experiment with different AI models: [https://ollama.ai/library](https://ollama.ai/library)

- After completing the _.env_ file, create the model by running in the terminal:

  - `ollama create "MODEL NAME" -f ./Modelfile`

#### Install the requirements

- `pipenv install -r requirements.txt`
- `pipenv shell`

#### Execute the main script

- `python main.py`
