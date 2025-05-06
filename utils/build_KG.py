"""
The inspiration of this functions script is from <https://github.com/JesseYule/KnowledgeGraphBeginner>
"""

import json
from tqdm import tqdm
from py2neo import Node, Relationship, NodeMatcher

def read_files(graph_ori_path):
    """
    Read all dicts in the file:
    - build sets of all the nodes we need -> set()
    - save relations -> list()

    Args:
        graph_ori_path ( str ): the path of the file in which save informations needed in building KG

    Returns:
        dict, dict: unique values (nodes) of each keys, unique values ([subject, object]) of each keys (relation)
    """

    with open (graph_ori_path, encoding='utf-8') as f:
        data_list = json.load(f)
    
    # get unique keys
    unique_keys = set()
    for d in data_list:
        for key in d.keys():
            unique_keys.add(key)
    unique_keys = list(unique_keys)

    # create a dict to store unique values (nodes) of each keys
    nodes = {
        key : set() for key in unique_keys
    }

    # create a dict to store unique values ([subject, object]) of each keys (relation)
    relations_part1 = {
        key : [] for key in unique_keys if key != "disease"
    }
    # the value of "subdepartment" stores the relations between small and big departments
    relations = {**relations_part1, "subdepartment": []}

    # add information
    for data_dict in data_list:

        this_disease = data_dict["disease"]
        
        for key in data_dict.keys():
            value = data_dict[key]

            if isinstance(value, str):
                nodes[key].add(value)
                if key != "disease" and key != "cure_department":
                    relations[key].append([this_disease, value])
                elif key == "cure_department":
                    relations[key].append([value, this_disease])
    
            elif isinstance(value, list):
                if key == "cure_department":
                    big_department = value[0]
                    small_department = value[1]
                    nodes[key].add(big_department)
                    nodes[key].add(small_department)
                    relations[key].append([small_department, this_disease])
                    relations["subdepartment"].append([big_department, small_department])

                else:
                    for v in value:
                        nodes[key].add(v)
                        relations[key].append([this_disease, v])

    return nodes, relations


# Create nodes by using py2neo
def create_nodes(logger, graph, nodes):

    for key in tqdm(nodes.keys(), desc="Creating nodes"):
        for unique_node in nodes[key]:
            node = Node(key, detail = unique_node)
            graph.create(node)
    logger.info(f"Create nodes successfully!")


# Create relations by using py2neo
def create_relations(logger, graph, relations):

    node_matcher = NodeMatcher(graph)
    for key in tqdm(relations.keys(), desc="Creating relations"):
        if key != "subdepartment" and key != "cure_department":
            for unique_relation in relations[key]:
                head = node_matcher.match("disease").where(detail=unique_relation[0]).first()
                tail = node_matcher.match(key).where(detail=unique_relation[1]).first()
                relation = Relationship(head, key, tail)
                graph.create(relation)
        elif key == "cure_department":
            for unique_relation in relations[key]:
                head = node_matcher.match(key).where(detail=unique_relation[0]).first()
                tail = node_matcher.match("disease").where(detail=unique_relation[1]).first()
                relation = Relationship(head, key, tail)
                graph.create(relation)
        else:
            for unique_relation in relations[key]:
                head = node_matcher.match("cure_department").where(detail=unique_relation[0]).first()
                tail = node_matcher.match("cure_department").where(detail=unique_relation[1]).first()
                relation = Relationship(head, key, tail)
                graph.create(relation)
    logger.info(f"Create relations successfully!")


# Create nodes in the graph using functions defined before
def create_graph(logger, graph, knowledge_path = 'data/medical_default.json'):

    logger.info(f"Creating KG ···")

    unique_nodes, unique_relations = read_files(knowledge_path)
    
    create_nodes(logger, graph, unique_nodes)
    create_relations(logger, graph, unique_relations)

