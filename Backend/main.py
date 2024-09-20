# here we can write all the API connections and link them through to the right backend process
from pathlib import Path

from typing import Annotated
from pypdf import PdfReader

from fastapi import FastAPI, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from Backend.IbmConnections import seek_answer_IBM
from Backend.libs.utils import upload_to_index

# from Backend.libs.utils import upload_to_index

API_VERSION = "1.0.0"
print("API VERSION: " + API_VERSION, flush=True)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, swagger_ui_oauth2_redirect_url=None,
              title="Migrato B.V. Student Rag API", version=API_VERSION)


@app.post('/api/v1/documentSubmitIndexing')
def submit_document_for_indexing(
        file_upload: UploadFile,
        jwtToken: Annotated[str, Form()],
        response: JSONResponse):
    suffix = file_upload.filename.split(".")[1].lower()  # TODO: This can be done better

    if suffix in ["pdf", "txt"]:
        try:
            f_in = open(file_upload.filename, "wb")
            f_in.write(file_upload.file.read())
            f_in.flush()
            f_in.close()
        except Exception as e:
            print(e)

    extracted_text = ""
    if suffix in "pdf":
        reader = PdfReader(file_upload.filename)
        number_of_pages = len(reader.pages)
        for page_number in range(0, number_of_pages):
            page = reader.pages[page_number]
            page_text = page.extract_text()
            extracted_text += page_text + "\n"
    elif suffix in "txt":
        with open(file_upload.filename, 'r') as content_file:
            extracted_text = content_file.read()
    else:
        raise HTTPException(status_code=1234, detail="Unsupported format")

    print(extracted_text, flush=True)
    Path(file_upload.filename).unlink(missing_ok=True)

    upload_to_index(file_upload.filename, file_upload.filename.split(".")[0], extracted_text)

    return "File uploaded and indexed"


@app.post('/api/v1/ragDocumentStreamIBM')
def seek_answer_IBM_API():
    #    question: Annotated[str, Form()],
    #    jwtToken: Annotated[str, Form()],
    #    response: JSONResponse):
    question = "Wie werkt er bij Pratt & Whitney?"
    seek_answer_IBM(question)
    return


seek_answer_IBM_API()
