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


def seek_answer_IBM():
    rag = get_rag_main_ibm()

    # [1:-1] To remove the double quotes
    print("DECODED: " + str(jwt.decode(jwtToken[1:-1], SECERT_KEY, algorithms=[ALGORITHM])), flush=True)
    user_sending_question = str(jwt.decode(jwtToken[1:-1], SECERT_KEY, algorithms=[ALGORITHM]))

    response = dict(rag.rag(question, answerGeneration=True))
    print(response)

    merged_results = {}
    for set in response['debugInfo']['WDresponce']:
        asset_id = set['WD_document_filename']
        merged_results[asset_id] = {"count": 1, "uri_source": set['WD_document_filename'], "title": set['WD_document_filename'], "chunk": {}}
        merged_results[asset_id]['chunk_number'] = asset_id
        merged_results[asset_id]['chunk'][1] = {}
        merged_results[asset_id]['chunk'][1]['relevancy_score'] = set['WD_document_confidence'] * 10.0
        for passage in set['WD_document_passages']:
            merged_results[asset_id]['chunk'][1]['text'] = passage['passage_text']

    merged_results['answer'] = response['generatedText']
    print(response['generatedText'])

    return JSONResponse(content=jsonable_encoder(merged_results), status_code=status.HTTP_200_OK)
