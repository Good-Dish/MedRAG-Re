import math
import json
from collections import defaultdict
import jieba
import os
import re

# Read the json file which stores the knowledge
def read_json_file(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# Extract the attributes ('desc', 'cause', 'symptom') of each disease
def extract_text(data):

    texts = []
    for item in data:
        texts.append(item.get('desc', ''))
        texts.append(item.get('cause', ''))
        texts.extend(item.get('symptom', []))
    return texts


# Calculate the IDF value
def calculate_idf(texts):

    # Count how many documents each word appears in
    document_frequency = defaultdict(int)
    for doc in texts:
        words = set(jieba.lcut(doc))
        filtered_words = [word for word in words if re.match(r'^[\u4e00-\u9fa5]+$', word)]
        for word in filtered_words:
            document_frequency[word] += 1

    # Calculate the total number of documents in the corpus
    N = len(texts)

    # Calculate the IDF value for each word
    idf_values = {}
    for word, df in document_frequency.items():
        idf = math.log(N / (1 + df))
        idf_values[word] = idf
    return idf_values


# Generate IDF file
def generate_file(logger, idf_values, knowledge_name):

    idf_file_path = os.path.join('data', f"{knowledge_name}_IDF.txt")
    with open(idf_file_path, 'w', encoding='utf-8') as f:
        for word, idf in idf_values.items():
            f.write(f"{word} {idf}\n")
    
    logger.info(f"Create IDF file successfully!")


# Read the data file and generate the IDF file
def generate_idf_file(logger, knowledge_name = "default"):

    logger.info(f"Creating IDF file···")
    
    knowledge_file_path = os.path.join('data', f"medical_{knowledge_name}.json")

    data = read_json_file(knowledge_file_path)
    texts = extract_text(data)
    idf_values = calculate_idf(texts)
    generate_file(logger, idf_values, knowledge_name)