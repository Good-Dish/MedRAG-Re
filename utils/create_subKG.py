from py2neo import NodeMatcher, Relationship
import json

def match_nodes(graph, nodes_info):

    node_matcher = NodeMatcher(graph)

    nodes = []
    for key in nodes_info.keys():
        value = nodes_info[key]
        for v in value:
            n = node_matcher.match(key).where(detail=v).first()
            nodes.append(n)
    
    return nodes


def build_subgraph(graph, leaf_nodes, mapping_file = 'data\keys_language_map_default.json'):

    with open (mapping_file, encoding='utf-8') as f:
        mapping = json.load(f)

    subgraph_info = []


    for leaf_node in leaf_nodes:
            
            query = f"MATCH p=(n {{detail: '{leaf_node['detail']}'}})-[:PARENT*]->(root) WHERE NOT (root)-[:PARENT]->() RETURN p"
            paths = graph.run(query)

            for path in paths:
                for rel in path[0].relationships:
                    start_node = rel.start_node
                    end_node = rel.end_node
                    relation_type = rel.type
                    sentence = f"{start_node['detail']}{mapping[relation_type]}{end_node['detail']}"
            
                    subgraph_info.append(sentence)

                    parent = end_node
                    child_query = f"MATCH (p {{detail: '{parent['detail']}'}})-[:PARENT]->(child) RETURN child"
                    children = graph.run(child_query)
                    for child in children:
                        child_node = child[0]
                        relationship = graph.match((parent, child_node)).first().type
                        sentence = f"{parent['detail']}{mapping[relationship]}{child_node['detail']}"
                        subgraph_info.append(sentence)
    
    return subgraph_info