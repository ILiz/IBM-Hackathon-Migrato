# here we can write all the API connections and link them through to the right backend process
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

from Backend.IbmConnections import seek_answer_IBM

API_VERSION = "1.0.0"
print("API VERSION: " + API_VERSION, flush=True)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, swagger_ui_oauth2_redirect_url=None,
              title="Migrato B.V. NLP API", version=API_VERSION)


@app.post('/api/v1/ragDocumentStreamIBM')
def seek_answer_IBM_API():
    #    question: Annotated[str, Form()],
    #    jwtToken: Annotated[str, Form()],
    #    response: JSONResponse):
    question = "Wie werkt er bij Pratt & Whitney?"
    seek_answer_IBM(question)
    return


seek_answer_IBM_API()
