import os
from python_automation.utils import *
from langchain.tools import tool
from langchain.agents import Tool
from langchain.vectorstores import Chroma
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from fuzzywuzzy import fuzz
import ipdb
import random

# Instantiate logger
logger = Logger('ai_tools', 'python_automation/ai/logs/ai_tools.log').get_logger()
embeddings_model_name = os.environ.get(
    'EMBEDDINGS_MODEL_NAME', 'all-MiniLM-L6-v2')


class CSVTools():
    @tool("Search CSV file")
    def csv_searcher(arguments) -> str:
        """
        Tool for searching in CSV files using fuzzy matching.
        Input format: 'file_path|search_query'.
        Returns rows matching a search query or similar matches if an exact match is not found.
        """
        file_path, search_query = arguments.split('|')
        # Process the CSV file and convert it to DataFrame using imported function
        df = make_data_frame_from_csv(file_path)
        # Fuzzy match search
        threshold_similarity = 80

        def is_similar(a, b):
            return fuzz.token_set_ratio(a, b) > threshold_similarity

        similar_matches = df[df['Prompt'].apply(
            lambda x: is_similar(x, search_query))]

        if not similar_matches.empty:
            return similar_matches['Answer'].to_string(index=False)
        else:
            return "No matches found"

    @tool("Check if question is about work experience")
    def generate_experience_number(prompt):
        """
        Tool for checking if question is related to work experience.
        Input format: 'prompt'
        Returns whole number representing the number of years of work experience the Software Developer has with a specific technology.
        """
        if "work experience" in prompt.lower():
            return str(random.randint(1, 10))
        else:
            return "Prompt not related to work experience."


class UserDataTools:
    @tool("Tool to fetch the user data")
    def fetch_user_data(query) -> str:
        """
        Tool for retrieving User uploaded data from the vectorstore.
        """

        embeddings = HuggingFaceEmbeddings(
            model_name=embeddings_model_name)
        # Setup to access Chroma vectorstore
        db = Chroma(persist_directory=CHROMA_SETTINGS.persist_directory,
                    embedding_function=embeddings)
        ipdb.set_trace()
