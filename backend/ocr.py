import csv
import requests
import uuid
from pypdf import PdfReader, PdfWriter
from fastapi import File, UploadFile
import os
import sys
import io
import ocrmypdf
from zipfile import ZipFile
from typing import List, Dict


class OCR_utilities:

    class File:
        def __init__(self, filename: str, content: bytes, language: str = "eng"):
            self.filename = filename
            self.content = content
            self.language = language

    @staticmethod
    async def ocr_document(input_bytes: io.BytesIO, file_name: str, language: str = "eng") -> io.BytesIO:
        TEMP_FOLDER = 'temp'
        RANDOM_TEMP_NAME = uuid.uuid4().hex
        INPUT_TEMP_FILE = f'temp/{RANDOM_TEMP_NAME}.pdf'
        OUTPUT_TEMP_FILE = f'temp/{RANDOM_TEMP_NAME}_ocred.pdf'

        # create temporary folder if it doesn't exist
        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)

        with open(INPUT_TEMP_FILE, 'wb') as f:
            if type(input_bytes) == bytes:
                reader = PdfReader(io.BytesIO(input_bytes), strict=False)
            else:
                reader = PdfReader(input_bytes, strict=False)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.write(f)

        try:
            ocrmypdf.ocr(INPUT_TEMP_FILE, OUTPUT_TEMP_FILE,
                         language=language, output_type='pdf', use_threads=True)
        except ocrmypdf.PriorOcrFoundError:
            print('Prior OCR found, skipping')
            os.remove(INPUT_TEMP_FILE)
            if type(input_bytes) == bytes:
                return input_bytes
            else:
                return input_bytes.getvalue()
        except ocrmypdf.SubprocessOutputError:
            print('Subprocess error')
            os.remove(INPUT_TEMP_FILE)
            if type(input_bytes) == bytes:
                return input_bytes
            else:
                return input_bytes.getvalue()

        with open(OUTPUT_TEMP_FILE, 'rb') as f:
            # f.name = f'{file_name}_ocred.pdf'
            out_bytes = f.read()

        os.remove(INPUT_TEMP_FILE)
        os.remove(OUTPUT_TEMP_FILE)

        return out_bytes

    @classmethod
    def zip_files(cls, files: List[File]) -> io.BytesIO:
        archive = io.BytesIO()

        with ZipFile(archive, 'w') as zip:
            for file in files:
                zip.writestr(file.filename, file.content)

        return archive

    @classmethod
    def unzip_files(cls, file: io.BytesIO) -> List[File]:
        files: List[cls.File] = []

        with ZipFile(file) as zip:
            for name in zip.namelist():
                with zip.open(name) as f:
                    files.append(OCR_utilities.File(name, f.read()))

        return files

    @classmethod
    def fetch_metadata_file(link: str) -> io.BytesIO:
        # gviz/tq?tqx=out:csv
        response = requests.get(
            "/".join([*link.split('/')[0:-1], 'gviz/tq?tqx=out:csv']))
        return io.BytesIO(response.content)

    @classmethod
    def parse_metadata_file(cls, csv_file: io.BytesIO) -> List[File]:
        extracted_data: List[cls.File] = []
        # TEMP_FILE_PATH = "temp/metadata.csv"

        reader = csv.reader(csv_file.getvalue().decode('utf-8').splitlines())

        headers = next(reader)

        try:
            filename_full_index = headers.index("Access Identifier")
        except ValueError:
            filename_full_index = headers.index("accessIdentifier")

        language_index = headers.index("language")
        for row in reader:
            filename_full = f'{row[filename_full_index]}.pdf'
            language = row[language_index] if row[language_index] != "" else "eng"

            extracted_data.append(cls.File(filename_full, None, language))

        return extracted_data

    @classmethod
    def process_collection(cls, metadata: List[File], collection: List[File]):

        processed_collection: List[File] = collection

        for collection_file_index in range(len(collection)):
            for metadata_file in metadata:
                parsed_filename = collection[collection_file_index].filename.split(
                    "/")[-1]
                if metadata_file.filename == parsed_filename:
                    # print(
                    #     f"parsed_filename: {parsed_filename}, metadata_file.filename: {metadata_file.filename}")
                    processed_collection[collection_file_index] = cls.File(
                        collection[collection_file_index].filename,
                        cls.ocr_document(
                            collection[collection_file_index].content, collection[collection_file_index].filename, metadata_file.language),
                        metadata_file.language
                    )

        return processed_collection
