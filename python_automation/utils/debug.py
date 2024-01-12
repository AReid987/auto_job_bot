from pprint import pprint
import ipdb
from ai import *
# from ..ai.ai_tools import *
# from .document_ingest import *
# from .custom_csv_loader import *

if __name__ == "__main__":
    AiCrew().run('source_documents/qa_pairs.csv', 'first name')
    ipdb.set_trace()
