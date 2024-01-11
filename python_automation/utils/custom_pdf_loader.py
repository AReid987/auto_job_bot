from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from typing import List
from langchain.docstore.document import Document

import ipdb
import pypdfium2 as pdfium
from pytesseract import image_to_string


class CustomPDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert_pdf_to_images(self, file_path, scale=300/72):
        pdf_file = pdfium.PdfDocument(file_path)

        page_indices = [i for i in range(len(pdf_file))]

        renderer = pdf_file.render(
            pdfium.PdfBitmap.to_pil,
            page_indices=page_indices,
            scale=scale,
        )

        final_images = []

        for i, image in zip(page_indices, renderer):

            image_byte_array = BytesIO()
            image.save(image_byte_array, format='jpeg', optimize=True)
            image_byte_array = image_byte_array.getvalue()
            final_images.append(dict({i: image_byte_array}))

        return final_images

    def display_images(self, list_dict_final_images):

        all_images = [list(data.values())[0]
                      for data in list_dict_final_images]

        for index, image_bytes in enumerate(all_images):

            image = Image.open(BytesIO(image_bytes))
            plt.figure(figsize=(image.width / 100, image.height / 100))

            plt.title(f"----- Page Number {index+1} -----")
            plt.imshow(image)
            plt.axis("off")
            plt.show()

    def extract_text_with_pytesseract(self, image_dict):
        image_list = [list(data.values())[0] for data in image_dict]
        image_content = []

        for index, image_bytes in enumerate(image_list):
            image = Image.open(BytesIO(image_bytes))
            raw_text = str(image_to_string(image))
            image_content.append(raw_text)
        return "\n".join(image_content)

    def load(self) -> List[Document]:
        image_dict = self.convert_pdf_to_images(self.file_path)
        text_with_pytesseract = self.extract_text_with_pytesseract(image_dict)
        doc = Document(page_content=text_with_pytesseract,
                       metadata={"source": self.file_path})
        return [doc]
