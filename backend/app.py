from typing import List
from typing_extensions import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, Response
from PyPDF2 import PdfReader, PdfWriter
from zipfile import ZipFile
import ocrmypdf
import io
import os

app = FastAPI()


def ocr(input_bytes: UploadFile, file_name: str) -> io.BytesIO:

    TEMP_FOLDER = 'temp'
    INPUT_TEMP_FILE = f'temp/{file_name}.pdf'
    OUTPUT_TEMP_FILE = f'temp/{file_name}_ocred.pdf'

    # create temporary folder if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')

    with open(f'temp/{file_name}.pdf', 'wb') as f:

        reader = PdfReader(input_bytes)
        writer = PdfWriter()

        print(len(reader.pages))

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


@app.post("/files/")
async def create_files(files: Annotated[List[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    result = []

    for file in files:
        contents = await file.read()
        out = ocr(io.BytesIO(contents), file.filename)
        print(file.filename, len(contents))
        # result[file.filename] = out
        result.append({
            "filename": file.filename,
            "content_type": "application/pdf",
            "content": out,
        })

    archive = io.BytesIO()

    with ZipFile(archive, 'w') as zip:
        for file in result:
            zip.writestr(file['filename'], file['content'])

    response = Response(
        content=archive.getvalue(), media_type="application/x-zip-compressed")

    return response


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
