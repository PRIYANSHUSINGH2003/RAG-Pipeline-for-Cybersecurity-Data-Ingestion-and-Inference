from pymongo import MongoClient
import networkx as nx
from graph_entities import Host, Port, Service, Vulnerability

# Initialize the graph
graph = nx.Graph()

# Ingest data into the graph
def ingest_data(data):
    for entry in data:
        host = Host(entry['hostname'])
        port = Port(entry['port'], entry['protocol'])
        service = Service(entry['service_name'], entry['service_version'])

        # Add nodes and edges for relationships
        graph.add_node(host)
        graph.add_node(port)
        graph.add_edge(host, port, relation="HasPort")
        graph.add_edge(port, service, relation="RunsService")

        for vuln in entry.get('vulnerabilities', []):
            vulnerability = Vulnerability(vuln['id'], vuln['description'])
            graph.add_node(vulnerability)
            graph.add_edge(service, vulnerability, relation="HasVulnerability")

# Connect to MongoDB and fetch data
def fetch_from_mongo():
    client = MongoClient("mongodb+srv://priyanshusingh00004:110044@cluster0.tcvez.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["cyber_db"]
    collection = db["walkthroughs"]
    data = list(collection.find())
    ingest_data(data)
