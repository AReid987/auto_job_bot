from .utils.document_ingest import *

if __name__ == "__main__":
    # Create or add to the Chroma DB
    # and ingest the users source_documents
    docs = DocumentLoader()
    docs.main()
