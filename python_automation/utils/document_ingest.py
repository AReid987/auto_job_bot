
import os
import glob
from typing import List, Dict
from multiprocessing import Pool
from tqdm import tqdm
import ipdb

from .custom_pdf_loader import CustomPDFLoader
from .custom_csv_loader import CustomCSVLoader
import hashlib

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from .constants import CHROMA_SETTINGS

cwd = os.getcwd()
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
parent_directory = os.path.dirname(current_directory)
parent_directory_name = os.path.basename(parent_directory)
source_documents = os.environ.get('SOURCE_DIRECTORY', 'source_documents')
persist_db = os.environ.get('PERSIST_DIRECTORY', 'db')

embeddings_model_name = os.environ.get(
    'EMBEDDINGS_MODEL_NAME', 'all-MiniLM-L6-v2')


class DocumentLoader():
    # Load environment variables
    def __init__(self) -> None:
        self.source_directory = f'{cwd}/{parent_directory_name}/{source_documents}'
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.embeddings_model_name = embeddings_model_name
        self.persist_directory = f'{cwd}/{parent_directory_name}/{persist_db}'

    # Map files extensions to document loaders and their arguments
    def loader_mapping(self) -> Dict:
        LOADER_MAPPING = {
            ".csv": (CustomCSVLoader, {}),
            ".pdf": (CustomPDFLoader, {}),
        }
        return LOADER_MAPPING

    def compute_document_uid(self, document: Document) -> str:
        document_text = document.page_content
        return hashlib.sha256((document_text.encode())).hexdigest()

    def load_single_document(self, file_path: str) -> List[Document]:
        ext = "." + file_path.rsplit(".", 1)[-1]
        if ext in self.loader_mapping():
            # if 'qa_pairs.csv' in file_path:
            #     process_csv(file_path)
            loader_class, loader_args = self.loader_mapping()[ext]
            # ipdb.set_trace()
            loader = loader_class(file_path, **loader_args)
            print(f"loader: {loader}")
            return loader.load()

        raise ValueError(f"Unsupported file extension '{ext}'")

    def load_documents(self, source_dir: str, ignored_files: List[str] = []) -> List[Document]:
        """
        Loads all documents from the source documents directory, ignoring specified files
        """
        all_files = []
        for ext in self.loader_mapping():
            all_files.extend(
                glob.glob(os.path.join(
                    source_dir, f"**/*{ext}"), recursive=True)
            )
        filtered_files = [
            file_path for file_path in all_files if file_path not in ignored_files]
        with Pool(processes=os.cpu_count()) as pool:
            results = []
            with tqdm(total=len(filtered_files), desc="Loading new documents", ncols=80) as pbar:
                for i, docs in enumerate(pool.imap_unordered(self.load_single_document, filtered_files)):
                    results.extend(docs)
                    pbar.update()
        return results

    def process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        """
        Load documents and split into chunks
        """
        print(f"Loading documents from {self.source_directory}")
        documents = self.load_documents(self.source_directory, ignored_files)

        if not documents:
            print("No new documents to load")
            exit(0)
        print(
            f"Loaded {len(documents)} new documents from {self.source_directory}")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        texts = text_splitter.split_documents(documents)
        print(
            f"Split into {len(texts)} chunks of text(max. {self.chunk_size} tokens each)")
        return texts

    def does_vectorstore_exist(self, persist_directory: str) -> bool:
        """
        Checks if vectorstore exists
        """

        db_directory = os.listdir(persist_directory)
        sub_directories = [d for d in db_directory if os.path.isdir(
            os.path.join(persist_directory, d))]

        for subdir in sub_directories:
            if os.path.exists(os.path.join(self.persist_directory, subdir)):
                list_index_files = glob.glob(os.path.join(
                    self.persist_directory, f"{subdir}/*.bin"))
                list_index_files += glob.glob(os.path.join(
                    self.persist_directory, f"{db_directory}/*.pkl"))
                # AT least 3 documents needed in a working vectorstore
                if len(list_index_files) > 3:
                    return True
        return False

    def main(self):
        # ipdb.set_trace()
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embeddings_model_name)

        if self.does_vectorstore_exist(self.persist_directory):
            # Update adn store locally vectorestore
            print(
                f"Appending to existing vectorestore at {self.persist_directory}")
            db = Chroma(persist_directory=self.persist_directory,
                        embedding_function=embeddings)
            collection = db.get()
            existing_uids = set(id
                                for id in collection['ids'])
            texts = self.process_documents()
            processed_texts = [
                (text, self.compute_document_uid(text)) for text in texts]
            new_texts = [
                text for text, uid in processed_texts if uid not in existing_uids]
            if new_texts:
                print(
                    'Creating embeddings for existing vectorestore. This might take a while...')
                db.add_documents(new_texts)
                db.persist()
            else:
                print('No new texts found. exiting to avoid duplication.')
        else:
            # Create and store vectorstore locally
            print("Creating new vectorestore")
            texts = self.process_documents()
            ids = [self.compute_document_uid(text) for text in texts]
            unique_ids = list(set(ids))

            seen_ids = set()

            unique_docs = [text for text, id in zip(
                texts, ids) if id not in seen_ids and (seen_ids.add(id) or True)]
            print('Creating embeddings. This might take a while...')
            db = Chroma.from_documents(
                documents=unique_docs, embedding=embeddings, ids=unique_ids, persist_directory=self.persist_directory)
            db.persist()
        print("Ingestion complete! You can now give your CrewAI agent your identity.")


if __name__ == "__main__":
    DocumentLoader().main()
