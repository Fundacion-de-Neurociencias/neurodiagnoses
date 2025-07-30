# tools/knowledge_graph/hpo_parser.py
import os
import pronto
import networkx as nx
import urllib.request

# Define paths
HPO_URL = 'http://purl.obolibrary.org/obo/hp.obo'
DATA_DIR = 'data'
HPO_OBO_PATH = os.path.join(DATA_DIR, 'hp.obo')
HPO_GRAPH_PATH = os.path.join(DATA_DIR, 'hpo_graph.graphml')

def create_hpo_graph():
    """
    Downloads the HPO ontology (if not present), parses it,
    and saves it as a NetworkX graph.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(HPO_OBO_PATH):
        print(f"Downloading HPO from {HPO_URL}...")
        try:
            urllib.request.urlretrieve(HPO_URL, HPO_OBO_PATH)
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading HPO file: {e}")
            return

    print(f"Loading ontology from {HPO_OBO_PATH}...")
    try:
        hpo = pronto.Ontology(HPO_OBO_PATH)
    except Exception as e:
        print(f"Error parsing HPO file: {e}")
        return

    G = nx.DiGraph()

    print("Building knowledge graph from HPO terms...")
    for term in hpo.terms():
        if term.obsolete:
            continue
        
        G.add_node(term.id, name=term.name, description=getattr(term, 'def', ""))
        
        for parent in term.superclasses(distance=1):
            if not parent.obsolete:
                G.add_edge(term.id, parent.id, type='is_a')

    print(f"Saving graph to {HPO_GRAPH_PATH}...")
    nx.write_graphml(G, HPO_GRAPH_PATH)
    
    print(f"\n✅ Knowledge graph created successfully.")
    print(f"   Nodes: {G.number_of_nodes()}")
    print(f"   Edges: {G.number_of_edges()}")

if __name__ == '__main__':
    create_hpo_graph()
