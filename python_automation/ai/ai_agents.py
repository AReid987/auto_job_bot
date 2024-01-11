from crewai import Agent
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from .ai_tools import CSVTools

llama2 = Ollama(
  model="llama2:13b",
  callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

class AiAgents():
  def csv_data_analyst(self):
    return Agent(
      role="Expert Data Analyst",
      goal="Search for exact or similar matches in CSV file",
      backstory="""
      As an expert data analyst with extensive experience in data mining and pattern recognition, you have a knack for uncovering hidden insights in complex datasets. Your expertise lies in applying advanced analytical techniques to find meaningful connections, making you an invaluable asset in situations requiring precise and thorough data analysis.You work for a company that excels at finding jobs for Software Developers. When filling out job applications on behalf of a Software Developer, there are some predefined answers stored in a CSV file. You will be given this CSV file and a search query. You need to use the tools available to find an exact or similar match to the search query in the CSV file. When you find a match, you need to respond with the corresponding answer to the prompt. When you do not find a match you will respond simply with 'No matches found' and nothing else.
      """,
      tools=[CSVTools.csv_searcher],
      verbose=True,
      allow_delegation=False,
      llm=llama2
    )

  def job_application_writer(self):
    return Agent(
      role='Job Application Writer',
      goal='Write accurate answers to job applications that match the details of the Software Developer you are working for.',
      backstory="""
      You are an assistant to an expert Software Developer. You will fill out job applications on their behalf. You will answer the questions on the forms as if you were the Software Developer. You specialize in writing accurate, outstanding answers to job applications. You will not make up answers if you do not know. If you do not know, you will say 'I dont't know the answer'. You will provide the most accurate answer possible to the prompts you are given, searching the internet when you need to. You will also fill out the forms with the Software Developer's name and information. Give concise answers when appropriate. For example a question asking how many years of experience you have with a certain technology should be responded to with just a whole number representing the number of years.
      """,
      tools=[CSVTools.generate_experience_number],
      verbose=True,
      allow_delegation=False,
      llm=llama2
    )

  # TODO: enable job application writer to search the internet for answers
