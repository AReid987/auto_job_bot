# Auto Job Bot

## Quickstart

### Requirements

#### ollama

- Download ollama: [https://ollama.ai/download](https://ollama.ai/download)

- After downloading ollama, you can execute AI agents via the command line on your local machine by running _ollama run model_name_

- _Examples_:

  - `ollama run llama2:13b`
  - `ollama run mistral`

- _Note_: Feel free to experiment with different AI models: [https://ollama.ai/library](https://ollama.ai/library)

#### .env

- Create a _.env_ file with the following variables:

  - NestJS API variables

    - PORT= (3000 is default)

    - DATABASE_URL="postgresql://"user_name":"password"@db:5432/auto_job_db"

  - PostgreSQL DB variables

    - POSTGRES_USER='' -- PostgresDB user name
    - POSTGRES_PASSWORD='' == PostgresDB password
    - PGADMIN_DEFAULT_EMAIL='' PGAdmin4 email to log in to DB GUI -- default is "<admin@admin.com>"
    - PGADMIN_DEFAULT_PASSWORD='' PGAdmin4 password -- default is pgadmin4

  - Python Automation variables
    - FIRST_NAME='' -- Your first name
    - LAST_NAME='' -- Your last name
      -- DOB='' -- Date of Birth format: MM/DD/YYYY
    - LINKEDIN_USERNAME='' -- Email address for your LinkedIn Profile: <email@example.com>
    - LINKEDIN_PASSWORD='' -- Your LinkedIn password
    - PHONE_NUMBER='' -- Your phone number format: 55555555555

#### Docker

- Download Docker desktop if you do not already have it: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

- Ensure nothing is running on port :5432

  - `sudo lsof -i :5432`
  - `kill -9 <PID>`

- From the project root directory (auto_job_app)

  - run `docker compose build`
  - run `docker compose up`

- The NestJS API should start up on <http://localhost:3000> unless you specified a different port in the .env file

- You can check the logs within Docker desktop "Containers" view for the container or individual images.
- You can also inspect the files within each container by:
  - clicking the container 'auto_job_app'
  - Clicking the container for image you wish to inspect
  - Clicking the "Files" menu in the image container

#### PGAdmin4

- After running `docker compose up`
  - PGAdmin4 GUI will be available at <http://localhost:5050:80>
  - Login using the default values for email and password or
  - Login using the values you set in the .env file for email and password.
  - In the left-hand sidebar click `Servers`
  - Right-click on `Servers` and select `Register` -> `Server`.
  - In the `General` tab of the `Create - Server` dialog give the server the name: 'auto_job_db'
  - In the `Connection` tab, fill in the following details:
    - Host name/address: **db**
    - Port: **5432**
    - Maintenance database: **postgres**
    - Username: **.env file -> POSTGRES_USER**
    - Password: **.env file -> POSTGRES_PASSWORD**
  - Click `Save`
