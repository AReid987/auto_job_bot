import csv
from typing import List
from langchain.docstore.document import Document
import ipdb
from dotenv import dotenv_values

config = dotenv_values()


class CustomCSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def replace_placeholders(self, text):
        for env_key, env_value in config.items():
            placeholder = f"{{{env_key}}}"
            # ipdb.set_trace()
            print(f"placeholder: {placeholder}")
            if placeholder in text:
                text = text.replace(placeholder, env_value)
        print(f"text: {text.strip().strip()}")
        return text.strip().strip()

    def process_csv_for_loader(self, file_path: str) -> List[Document]:
        processed_data = []

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            processed_data.append(headers)
            for row in reader:
                question = row[0]
                answer = row[1]
                # Replace placeholders in the answer
                processed_answer = self.replace_placeholders(answer)

                processed_row = [question, processed_answer]
                processed_data.append(processed_row)

        # processed_document = [Document(page_content=str(",".join(row)), metadata={
        #                                "source": file_path}) for row in processed_data]
        print(f"processed_document: {processed_data}")
        return processed_data

    def load(self):
        doc = Document(page_content=str(self.process_csv_for_loader(
            self.file_path)), metadata={"source": self.file_path})
        # ipdb.set_trace()
        return [doc]
