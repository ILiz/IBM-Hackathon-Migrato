from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from Backend.IBM.RAGmain import RAGmain
from Backend.IBM.SetVariables import SetVariables

varNames = [
    "WXAPIkey",
    "WXAPIurl",
    "WXprojectID"
]
VARS = SetVariables(varNames, shFileName='IBM/config.sh')
variables = VARS.getVariables()


def get_rag_main_ibm():
    return RAGmain(
        WXAPIkey=variables["WXAPIkey"],
        WXAPIurl=variables["WXAPIurl"],
        WXprojectID=variables["WXprojectID"]
    )


def seek_answer_IBM(question):
    rag = get_rag_main_ibm()

    response = dict(rag.rag(question, answerGeneration=True))
    print(response)

    merged_results = {'answer': response['generatedText']}

    print(response['generatedText'])

    return JSONResponse(content=jsonable_encoder(merged_results), status_code=status.HTTP_200_OK)
