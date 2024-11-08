# inference.py
from rag_pipeline import graph, Host, Port, Service, Vulnerability

def query_ports(hostname):
    ports = []
    for edge in graph.edges(data=True):
        # Check if the host matches the hostname and relation is HasPort
        if isinstance(edge[0], Host) and edge[0].hostname == hostname and edge[2]['relation'] == "HasPort":
            port = edge[1]
            if isinstance(port, Port):
                ports.append(port.port_number)
    return ports

def query_vulnerabilities(hostname):
    vulnerabilities = []
    
    # First, find all services linked to the host
    services = []
    for edge in graph.edges(data=True):
        if isinstance(edge[0], Host) and edge[0].hostname == hostname and edge[2]['relation'] == "HasPort":
            port = edge[1]
            # Find all services running on this port
            for service_edge in graph.edges(data=True):
                if service_edge[0] == port and service_edge[2]['relation'] == "RunsService":
                    service = service_edge[1]
                    if isinstance(service, Service):
                        services.append(service)
    
    # Now, find all vulnerabilities linked to the services
    for service in services:
        for vuln_edge in graph.edges(data=True):
            if vuln_edge[0] == service and vuln_edge[2]['relation'] == "HasVulnerability":
                vulnerability = vuln_edge[1]
                if isinstance(vulnerability, Vulnerability):
                    vulnerabilities.append(vulnerability.vuln_id)
    
    return vulnerabilities

# Example queries for testing with formatted output
def run_inference():
    print("\nNodes in the graph:")
    print(f"{'Type':<15}{'Details':<40}")
    print("=" * 55)
    for node, data in graph.nodes(data=True):
        print(f"{type(node).__name__:<15}{str(node):<40}")
    
    print("\nEdges in the graph:")
    print(f"{'Source':<25}{'Destination':<25}{'Relation':<15}")
    print("=" * 65)
    for src, dst, relation in graph.edges(data=True):
        relation_type = relation.get('relation', 'N/A')
        print(f"{str(src):<25}{str(dst):<25}{relation_type:<15}")
    
    test_host = "target1.example.com"  # Update this as needed
    
    print(f"\nPorts for '{test_host}':")
    ports = query_ports(test_host)
    if ports:
        print(", ".join(map(str, ports)))
    else:
        print("No ports found.")
    
    print(f"\nVulnerabilities for '{test_host}':")
    vulnerabilities = query_vulnerabilities(test_host)
    if vulnerabilities:
        print(", ".join(vulnerabilities))
    else:
        print("No vulnerabilities found.")