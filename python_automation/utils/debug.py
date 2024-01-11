from pprint import pprint
import ipdb
from ..ai import ai_crew as AICrew
from ..ai.ai_tools import *
from .document_ingest import *
from .custom_csv_loader import *

if __name__ == "__main__":
    # match = CSVTools.find_matches('qa_pairs.csv|first name')
    # print(match)
    # loader = CustomCSVLoader(
    #     '/Users/antonioreid/development/code/auto_job_app/source_documents/qa_pairs.csv')
    # loader.load()
    data = UserDataTools()
    data.fetch_user_data('hello')
    ipdb.set_trace()
