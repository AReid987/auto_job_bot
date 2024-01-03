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

  - `FIRST_NAME=""`

  - `LAST_NAME=""`

  - `DOB=""`

    - Use the format: MM/DD/YYYY

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
