# Auto Job Bot

## Quickstart

### Requirements

#### ollama

- Download ollama: [https://ollama.ai/download](https://ollama.ai/download)

- After downloading ollama, you can execute AI agents via the command line on your local machine by running _ollama run model_name_

- _Examples_:
  - `ollama run llama2:13b`
  - `ollama run mistral`

#### source_documents

- Add .pdf and .csv files of documents such as:
  - your resume
  - exported PDF of your LinkedIn profile to the source_documents directory

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

#### Install the requirements

- `pipenv install`
- `pipenv shell`

#### Execute the main script

- From the project's root directory `cd ..`
- Then from the project's parent directory `python -m auto_job_app.main`
- Note: to debug load any modules needed into utils/debug.py
  - Then run from the project's parent directory: `python -m auto_job_app.utils.debug`
