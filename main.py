from utils import *
from py2neo import Graph
import yaml
import os
import argparse


if __name__ == '__main__':

    # args
    parser = argparse.ArgumentParser(description='MedRAG_Rebuild')
    parser.add_argument('--log_dir', type=str, default='logs')
    parser.add_argument('--query', type=str, required=True)
    parser.add_argument('--config_path', type=str, default='config\CH.yaml')
    args = parser.parse_args()

    # create a logger
    log_dir = args.log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    this_logger = ColorLogger(log_dir)

    # read the config file
    with open(args.config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    this_knowledge_name = config["knowledge"]["knowledge_name"]
    this_knowledge_path = os.path.join('data', f"medical_{this_knowledge_name}.json")


    # link to your database
    this_graph = Graph(config['database']['URI'], 
                  auth=(config['database']['user'], config['database']['password']))

    try:
        this_graph.run("RETURN 1")
        this_logger.info(f"Link to the database successfully!")
    except Exception as e:
        this_logger.error(f"Link to the database unsuccessfully: {e}")

    # create KG
    create_graph(logger = this_logger,
                 graph = this_graph,
                 knowledge_path = this_knowledge_path)
    
    # generate IDF file to extracte keywords from patient's query
    if os.path.exists(os.path.join('data', f"{this_knowledge_name}_IDF.txt")):
        generate_idf_file(logger = this_logger,
                          knowledge_name = this_knowledge_name, 
                          idf_file_dir = 'data')
    
    # extracte keywords from patient's query
    keywords_list = extract_keywords(text = args.query, 
                                     topk = config["extract"]["topk"], 
                                     idf_path = os.path.join('data', f"{this_knowledge_name}_IDF.txt"))