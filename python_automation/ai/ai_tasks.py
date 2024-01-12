from crewai import Task
from textwrap import dedent

class AiTasks():
  def analysis(self, agent):
    return Task(
      description="""
      Analyze a CSV for matches to a given prompt and respond appropriately. Log new matches to a separate CSV file.
      """,
      agent=agent
    )

  def check_csv(self, agent):
    return Task(description=dedent("""
        Analyze a CSV file's 'Prompt' column for matches to a given search query. I a match is found respond with the value from the 'Answer' column for the matching row. When no matches are found, log the search query to a separate CSV file.
      """),
      agent=agent
    )

  def answer_form(self, agent):
    return Task(description=dedent("""
        Generate accurate answers for the following prompt on a job application on behalf of a Software Developer as the Software Developer:
        '{form_prompt}'.
    """),
    agent=agent
    )