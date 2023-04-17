from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from fastapi import File, UploadFile
import os
import sys
import io
import ocrmypdf
from zipfile import ZipFile
from typing import List, Dict
# import base64
# base64.encodestring = base64.encodebytes
# base64.decodestring = base64.decodebytes


class OCR_utilities:

    class File:
        def __init__(self, filename: str, content: bytes):
            self.filename = filename
            self.content = content

    @staticmethod
    def ocr_document(input_bytes: io.BytesIO, file_name: str) -> io.BytesIO:
        TEMP_FOLDER = 'temp'
        INPUT_TEMP_FILE = f'temp/{file_name}.pdf'
        OUTPUT_TEMP_FILE = f'temp/{file_name}_ocred.pdf'

        # create temporary folder if it doesn't exist
        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)

        with open(f'temp/{file_name}.pdf', 'wb') as f:
            reader = PdfReader(input_bytes)
            writer = PdfWriter()

            # print(len(reader.pages))
            for page in reader.pages:
                writer.add_page(page)

            writer.write(f)

        ocrmypdf.ocr(INPUT_TEMP_FILE, OUTPUT_TEMP_FILE, force_ocr=True,
                     language='eng', output_type='pdf', use_threads=True)

        with open(OUTPUT_TEMP_FILE, 'rb') as f:
            # output = io.FileIO(f.read())
            out_bytes = f.read()

        os.remove(INPUT_TEMP_FILE)
        os.remove(OUTPUT_TEMP_FILE)

        return out_bytes

    @staticmethod
    def zip_files(files: List[File]) -> io.BytesIO:
        archive = io.BytesIO()

        with ZipFile(archive, 'w') as zip:
            for file in files:
                zip.writestr(file.filename, file.content)

        return archive


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         with open(sys.argv[1], 'rb') as f:
#             # inbytes = io.FileIO(f.read())
#             print(len(f.read()), len(PdfReader(f).pages))
#             output = ocr(f, test=True)

#     else:
#         print("Please provide a file path as an argument.")
