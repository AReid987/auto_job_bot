
from crewai import Crew
from .ai_agents import AiAgents
from .ai_tasks import AiTasks
from utils.logger import Logger
import ipdb

logger = Logger('ai_crew_logger', 'ai_crew_logger.log').get_logger()


class AiCrew:
    def run(self, csv_file_path, search_query):
        agents = AiAgents()
        tasks = AiTasks()

        csv_data_analyst = agents.csv_data_analyst()
        job_application_writer = agents.job_application_writer()

        check_csv_task = tasks.check_csv(csv_data_analyst)
        answer_form_task = tasks.answer_form(job_application_writer)

        task_input = f"{csv_file_path}|{search_query}"
        check_csv_task.description = task_input

        crew_for_csv = Crew(
            agents=[csv_data_analyst],
            tasks=[check_csv_task],
            verbose=True,
        )
        csv_search_result = crew_for_csv.kickoff()
        logger.info(f'CSV Search Result: {csv_search_result}')
        if "No matches found".lower() in csv_search_result.lower():
            answer_form_task.description = search_query

            crew_for_job_application = Crew(
                agents=[job_application_writer],
                tasks=[answer_form_task],
                verbose=True,
            )
            job_application_result = crew_for_job_application.kickoff()
            return job_application_result

        return csv_search_result
