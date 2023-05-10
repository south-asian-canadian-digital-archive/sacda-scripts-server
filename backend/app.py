from typing import List, Optional, Union
from typing_extensions import Annotated
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, Response
import io

from ocr import OCR_utilities

app = FastAPI()


@app.post("/test/")
async def create_files(zip_file: UploadFile):
    contents = await zip_file.read()

    unzipped: List[OCR_utilities.File] = OCR_utilities.unzip_files(
        io.BytesIO(contents))

    print(unzipped[0].filename)

    return {"file_names": [file.filename for file in unzipped]}


@app.post("/ocr-files/")
async def create_upload_files(files: List[UploadFile], language: Union[str, None] = None, output_type: Union[str, None] = None):
    result: List[OCR_utilities.File] = []

    try:
        for file in files:
            contents = await file.read()
            out = OCR_utilities.ocr_document(
                io.BytesIO(contents), file.filename)
            print(file.filename, len(contents))
            result.append(OCR_utilities.File(file.filename, out))
    except Exception as e:
        print(e)
        return Response(content=e.__str__(), media_type="text/plain")

    archive = OCR_utilities.zip_files(result)

    response = Response(
        content=archive.getvalue(), media_type="application/x-zip-compressed")

    return response


@app.post("/ocr-collection/")
async def process_collection(
    collection_zip: Annotated[UploadFile, File()],
    metadata_file: Union[Annotated[UploadFile, File()], None] = None,
    metadata_file_link: Union[Annotated[str, Form()], None] = None,
    metadata_type: Union[str, None] = None,
):

    if metadata_file_link:
        metadata_file = OCR_utilities.fetch_metadata_file(
            metadata_file_link)
    metadata_contents = await metadata_file.read()
    collection_contents = await collection_zip.read()

    unzipped_collection: List[OCR_utilities.File] = OCR_utilities.unzip_files(
        io.BytesIO(collection_contents))
    parsed_metadata: io.BytesIO = OCR_utilities.parse_metadata_file(
        io.BytesIO(metadata_contents))
    # metadata_contents)

    processed_collection: List[OCR_utilities.File] = OCR_utilities.process_collection(
        parsed_metadata, unzipped_collection)

    print(len(processed_collection), len(unzipped_collection))

    zipped: io.BytesIO = OCR_utilities.zip_files(processed_collection)

    return Response(content=zipped.getvalue(), media_type="application/x-zip-compressed")


@app.get("/")
async def main():
    content = """
<body>
<form action="/test/" enctype="multipart/form-data" method="post">
<input name="zip_file" type="file">
<input type="submit">
</form>
<hr>
<form action="/ocr-files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<hr>

<form action="/ocr-collection/" enctype="multipart/form-data" method="post">
<input name="metadata_file" type="file">
<input name="collection_zip" type="file">
<input type="submit">
</form>

</body>
    """
    return HTMLResponse(content=content)
