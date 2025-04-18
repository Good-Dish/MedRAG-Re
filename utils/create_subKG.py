from py2neo import Node, Relationship, NodeMatcher

def match_nodes(graph, nodes_info):

    node_matcher = NodeMatcher(graph)

    nodes = []
    for key in nodes_info.keys():
        value = nodes_info[key]
        for v in value:
            n = node_matcher.match(key).where(detail=v).first()
            nodes.append(n)
    
    return nodes