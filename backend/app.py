from typing import List
from typing_extensions import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, Response
from PyPDF2 import PdfReader, PdfWriter
from zipfile import ZipFile
import io

from ocr import OCR_utilities

app = FastAPI()


@app.post("/files/")
async def create_files(files: Annotated[List[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    result: List[OCR_utilities.File] = []

    for file in files:
        contents = await file.read()
        out = OCR_utilities.ocr_document(io.BytesIO(contents), file.filename)
        print(file.filename, len(contents))
        result.append(OCR_utilities.File(file.filename, out))

        # result.append({
        #     "filename": file.filename,
        #     "content_type": "application/pdf",
        #     "content": out,
        # })

    archive = OCR_utilities.zip_files(result)

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
