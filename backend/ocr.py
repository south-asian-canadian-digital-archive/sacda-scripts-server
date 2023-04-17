from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from fastapi import File, UploadFile
import os
import sys
import io
import ocrmypdf
import base64
base64.encodestring = base64.encodebytes
base64.decodestring = base64.decodebytes


def ocr(input_bytes: UploadFile, test=False) -> io.BytesIO:

    TEMP_FOLDER = 'temp'
    OUTPUT_TEMP_FILE = 'temp/temp_ocred.pdf'

    # create temporary folder if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')

    input_file_name = 'temp/temp.pdf'
    with open(input_file_name, 'wb') as f:
        # with io.FileIO(input_bytes) as f2:

        reader = PdfReader(input_bytes)
        writer = PdfWriter()

        print(len(reader.pages))

        for page in reader.pages:
            writer.add_page(page)

        writer.write(f)

    ocrmypdf.ocr(input_file_name, OUTPUT_TEMP_FILE, force_ocr=True,
                 language='eng', output_type='pdf', use_threads=True)

    with open(OUTPUT_TEMP_FILE, 'rb') as f:
        output = io.FileIO(f.read())

        return output


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         with open(sys.argv[1], 'rb') as f:
#             # inbytes = io.FileIO(f.read())
#             print(len(f.read()), len(PdfReader(f).pages))
#             output = ocr(f, test=True)

#     else:
#         print("Please provide a file path as an argument.")
