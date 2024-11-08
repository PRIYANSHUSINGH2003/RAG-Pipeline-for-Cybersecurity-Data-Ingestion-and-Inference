import networkx as nx

class Host:
    def __init__(self, hostname: str):
        self.hostname = hostname

    def __repr__(self):
        return f"Host({self.hostname})"

class Port:
    def __init__(self, port_number: int, protocol: str):
        self.port_number = port_number
        self.protocol = protocol

    def __repr__(self):
        return f"Port({self.port_number}/{self.protocol})"

class Service:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __repr__(self):
        return f"Service({self.name}, {self.version})"

class Vulnerability:
    def __init__(self, vuln_id: str, description: str):
        self.vuln_id = vuln_id
        self.description = description

    def __repr__(self):
        return f"Vulnerability({self.vuln_id})"
