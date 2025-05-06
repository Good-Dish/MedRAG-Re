from py2neo import NodeMatcher
import json


def build_subgraph(logger, graph, leaf_nodes, mapping_file = 'data/keys_language_map_default.json'):
    logger.info(f"Building subgraph based on your query···")

    with open (mapping_file, encoding='utf-8') as f:
        mapping = json.load(f)

    subgraph_info = []

    node_matcher = NodeMatcher(graph)

    processed_diseases = set()
    visited_nodes = set()
    queue = []
    
    # fine original leaf nodes
    for key in leaf_nodes.keys():
        match_names = leaf_nodes[key]
        for name in match_names:
            the_node = node_matcher.match(key, detail=name).first()
            queue.append(the_node)
            visited_nodes.add(the_node.identity)

    while queue:
        current_node = queue.pop(0)

        if current_node.identity not in processed_diseases:

            processed_diseases.add(current_node.identity)
        
            incoming_relationships = list(graph.match(nodes=(None, current_node), r_type=None))
            
            if incoming_relationships:
            
                for rel in incoming_relationships:
                    parent_node = rel.start_node
                    rel_str = f"{parent_node['detail']}{mapping[type(rel).__name__]}{current_node['detail']}"
                    subgraph_info.append(rel_str)
                    
                    if parent_node.identity not in visited_nodes:
                        queue.append(parent_node)
                        visited_nodes.add(parent_node.identity)
                    
                if 'disease' in current_node.labels:
                    outgoing_relationships = list(graph.match(nodes=(current_node, None), r_type=None))
                    for out_rel in outgoing_relationships:
                        child_node = out_rel.end_node
                        if child_node.identity not in visited_nodes:
                            # 添加扩充的关系字符串
                            exp_rel_str = f"{current_node['detail']}{mapping[type(out_rel).__name__]}{child_node['detail']}"
                            subgraph_info.append(exp_rel_str)
                            visited_nodes.add(child_node.identity)
    
    return subgraph_info