import os
import ipdb
from python_automation.utils.document_ingest import DocumentLoader
from python_automation.ai.ai_crew import *
def find_root():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_directory)
    return project_root
if __name__ == "__main__":
    project_root = find_root()

    # Change working directory to project root
    os.chdir(project_root)

    # Import after modifying sys.path
    print(f"root: {project_root}")

    # Create or add to the Chroma DB
    # and ingest the users source_documents
    # docs = DocumentLoader()
    # docs.main()

    # ipdb.set_trace()
    # Create AI crew and give identities

    ai_crew = AiCrew()
    ai_crew.run('qa_pairs.csv', 'first name')

