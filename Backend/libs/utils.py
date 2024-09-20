import re
import traceback
import uuid

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

from Backend.libs import ElasticSearch


def load_model(model_name):
    return SentenceTransformer(model_name)


def model_encoding(text_2, loaded_model):
    return loaded_model.encode(text_2)


def text_tokens(text_2):
    tokens = tokenizer(text_2, return_tensors='pt')
    tokens_size = tokens["input_ids"].size(1)
    print(f'Tokens    : {tokens_size}')
    if tokens_size > 512:
        print("issue")


def pre_processingtext(text_data):
    pattern = r'\{\s*:\s*[\w#-]+\s*\}|\{\s*:\s*\w+\s*\}|\n\s*\n'
    replaced = re.sub(pattern, '', text_data)
    replaced = re.sub("\{{ .*?\}}", "", replaced)
    replaced = re.sub("\{: .*?\}", "", replaced)
    replaced = re.sub("\(.*?\)|\[.*?\] |\{.*?\}", "", replaced)
    replaced = re.sub("</?div[^>]*>", "", replaced)
    replaced = re.sub("</?p[^>]*>", "", replaced)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("</?href*>", "", replaced)
    replaced = replaced.replace("}", "")
    replaced = replaced.replace("##", "")
    replaced = replaced.replace("###", "")
    replaced = replaced.replace("#", "")
    replaced = replaced.replace("*", "")
    replaced = replaced.replace("<strong>", "")
    replaced = replaced.replace("</strong>", "")
    replaced = replaced.replace("<ul>", "")
    replaced = replaced.replace("</ul>", "")
    replaced = replaced.replace("<li>", "")
    replaced = replaced.replace("</li>", "")
    replaced = replaced.replace("<ol>", "")
    replaced = replaced.replace("</ol>", "")
    replaced = replaced.replace("\n", " ")
    replaced = replaced.replace("}", " ")
    replaced = replaced.replace("{", " ")
    replaced = replaced.replace("<", " ")
    replaced = replaced.replace(">", " ")
    replaced = replaced.replace("/", " ")
    replaced = replaced.replace("\"", " ")
    replaced = replaced.replace("  ", " ")
    return replaced


tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
model = load_model('intfloat/multilingual-e5-large')


def upload_to_index(filename: str, title: str, text: str):
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=20,
        length_function=lambda x: len(tokenizer(x)['input_ids']),
        is_separator_regex=False,
    )

    idC = 0
    json_data = []
    try:
        doc_id = uuid.uuid4().hex
        text = text.replace('"', '').replace("\\", "\\\\")

        chunks = textSplitter.split_text(text)
        chunkNumber = 0
        for chunk in chunks:
            try:
                chunk_text = chunk
                dense_vector = model_encoding(chunk_text, model)
                json_data.append(f'{{\"index\": {{\"_id\": \"{str(doc_id) + "_" + str(chunkNumber)}\"}}}}')
                json_data.append(
                    f'{{\"my_vector\": {dense_vector.tolist()}, \"Text\": \"{str(chunk_text)}\", \"Title\": \"{str(title)}\", \"Course\": \"{str(filename)}\"}}')
                chunkNumber += 1
            except Exception as e:
                print(e)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    print(str(idC) + " - " + str(len(json_data)))
    idC += 1

    print("preparation complete")

    data_string = ""
    for i in range(len(json_data)):
        data_string += (json_data[i]
                        .replace("\r\n", " ")
                        .replace("\r", " ")
                        .replace("\n", " ")
                        .replace("\t", " ")
                        .replace("'", "") + "\n")
        ElasticSearch.send_data_bulk(data_string)
        data_string = ""
        print("data sent to elasticsearch")
