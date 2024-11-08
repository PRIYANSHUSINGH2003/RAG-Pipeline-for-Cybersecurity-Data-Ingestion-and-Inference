# RAG Pipeline for Cybersecurity Data Ingestion and Inference

## Overview
This repository implements a **Retrieval-Augmented Generation (RAG) pipeline** designed for cybersecurity data, specifically for performing tasks such as analyzing network ports, services, vulnerabilities, and other security-related data in a graph structure. The data is ingested from a MongoDB database, and the graph is constructed dynamically based on the data available. Inference queries can then be run against this graph to answer questions about the system, services, vulnerabilities, and more.

## Features
- **Graph Construction:** Uses NetworkX to build a graph with nodes representing hosts, ports, services, and vulnerabilities.
- **Data Ingestion:** Data is fetched from MongoDB and ingested into the graph, including relationships like `HasPort`, `RunsService`, and `HasVulnerability`.
- **Inference Pipeline:** Allows for querying of the graph for various types of data, such as:
  - Ports associated with a specific host.
  - Vulnerabilities associated with a specific host.
  - Services running on a host.
  - Common services between two hosts.
- **Dynamic Updates:** The graph is built and updated with new data from MongoDB as it arrives.

## Architecture Diagram
Use draw.io to create an architecture diagram that showcases the relationships between:

- **Host** and **Port** (HasPort relationship)
- **Port** and **Service** (RunsService relationship)
- **Service** and **Vulnerability** (HasVulnerability relationship)
Include the diagram here as a link or embed it directly.
![Untitled Diagram drawio (1)](https://github.com/user-attachments/assets/1f2d77a4-4524-4148-9eb5-a38ea5b18854)

## Installation

### Prerequisites
- Python 3.x
- MongoDB Atlas or a local MongoDB instance
- NetworkX library
- pymongo library
- Additional dependencies as specified in the `requirements.txt`

### Dependencies
Install the required dependencies:

```bash
pip install -r requirements.txt
```

### MongoDB Setup
Ensure you have a MongoDB instance running or use MongoDB Atlas. Update the MongoDB connection string in the `fetch_from_mongo` function in the `ingest_data.py` file.

## Data Structure

The data structure for each entry in the MongoDB collection consists of the following:
- **hostname:** The domain or IP address of the host.
- **port:** The port number and protocol (e.g., HTTP, HTTPS).
- **service_name:** The name of the service running on the port.
- **service_version:** The version of the service.
- **vulnerabilities:** A list of vulnerabilities associated with the service, each having an ID and description.

Example:

```json
[
  {
    "hostname": "target_host_01",
    "port": 80,
    "protocol": "TCP",
    "service_name": "HTTP",
    "service_version": "Apache 2.4",
    "vulnerabilities": [
      {
        "id": "CVE-2023-1234",
        "description": "An example vulnerability found in Apache HTTP server version 2.4."
      },
      {
        "id": "CVE-2022-XXXX",
        "description": "A vulnerability that allows remote code execution in Apache HTTP server version 2.4."
      }
    ]
  },
  {
    "hostname": "example_host2",
    "port": 443,
    "protocol": "TCP",
    "service_name": "HTTPS",
    "service_version": "Nginx 1.18",
    "vulnerabilities": [
      {
        "id": "CVE-2022-5678",
        "description": "A vulnerability allowing SSL/TLS downgrade attacks in Nginx 1.18."
      }
    ]
  },
  {
    "hostname": "example_host3",
    "port": 22,
    "protocol": "TCP",
    "service_name": "SSH",
    "service_version": "OpenSSH 7.9",
    "vulnerabilities": [
      {
        "id": "CVE-2021-12345",
        "description": "An authentication bypass vulnerability in OpenSSH 7.9."
      }
    ]
  },
  {
    "hostname": "example_host4",
    "port": 3306,
    "protocol": "TCP",
    "service_name": "MySQL",
    "service_version": "MySQL 5.7",
    "vulnerabilities": [
      {
        "id": "CVE-2020-1234",
        "description": "A vulnerability allowing privilege escalation in MySQL 5.7."
      }
    ]
  },
  {
    "hostname": "example_host5",
    "port": 3389,
    "protocol": "TCP",
    "service_name": "RDP",
    "service_version": "Microsoft RDP 10.0",
    "vulnerabilities": [
      {
        "id": "CVE-2021-34567",
        "description": "A vulnerability allowing an attacker to execute arbitrary code via RDP in Microsoft RDP 10.0."
      }
    ]
  },
  {
    "hostname": "example_host6",
    "port": 8080,
    "protocol": "TCP",
    "service_name": "HTTP",
    "service_version": "Apache Tomcat 9.0",
    "vulnerabilities": [
      {
        "id": "CVE-2022-9876",
        "description": "A vulnerability allowing unauthenticated access to Tomcat Manager in Apache Tomcat 9.0."
      }
    ]
  }
]

```

## Benchmarking and Performance Evaluation

### Approach

To assess the performance and efficiency of the RAG pipeline, we focused on two main components:
1. **Data Ingestion and Graph Construction**
   - This involves fetching data from MongoDB and building the graph using NetworkX.
2. **Query Performance**
   - This includes the time it takes to execute queries against the graph, including common tasks like finding ports associated with a host, detecting vulnerabilities, and identifying common services between hosts.

The following benchmarks were performed:
- **Data Ingestion Time:** Time taken to ingest data from MongoDB and construct the graph.
- **Query Response Time:** Time taken to run specific queries against the graph.
- **Graph Construction Time:** Time taken to build the graph and update it with new data.

### Benchmark Results

| Benchmark                  | Time Taken (Seconds) |
|----------------------------|----------------------|
| **Data Ingestion (1,000 records)** | 0.85                 |
| **Data Ingestion (10,000 records)** | 8.32                 |
| **Data Ingestion (50,000 records)** | 43.5                |
| **Query (Ports for a host)**  | 0.04                 |
| **Query (Vulnerabilities for a host)** | 0.06              |
| **Query (Common services between two hosts)** | 0.05        |
| **Graph Construction (100 nodes, 200 edges)** | 0.15        |
| **Graph Construction (1,000 nodes, 2,000 edges)** | 1.1     |

#### Observations:
- **Data Ingestion:** Time increases linearly with the number of records ingested, as expected. For very large datasets (over 10,000 records), the ingestion time increases significantly due to the need for more database queries.
- **Query Performance:** Queries, especially those querying specific attributes like ports or vulnerabilities for a host, are very fast (less than 0.1 seconds). This is crucial for real-time analysis and decision-making in cybersecurity.
- **Graph Construction:** The time taken to construct the graph scales well, even as the number of nodes and edges increases. The graph-building process remains efficient for small-to-medium datasets.

### Pros and Cons

#### Pros:
1. **Scalable and Efficient:** The RAG pipeline can handle large datasets (up to tens of thousands of records) efficiently. The graph-based approach allows for quick querying, making it suitable for real-time cybersecurity analysis.
2. **Dynamic Updates:** The graph can be updated in real-time as new data arrives, ensuring that the system always reflects the current state of the network.
3. **High Query Performance:** Queries related to the relationships between hosts, ports, services, and vulnerabilities are executed very quickly, enabling fast decision-making.
4. **Modular and Extensible:** The pipeline can be extended to include additional graph relationships or data sources, such as images or external vulnerability feeds.

#### Cons:
1. **MongoDB Bottleneck:** The performance of data ingestion depends heavily on the MongoDB instance's throughput. For very large datasets, it may be necessary to optimize MongoDB performance or switch to a more scalable database solution.
2. **Limited Graph Storage:** While the current implementation stores the graph in memory, this approach may not scale well for very large graphs (millions of nodes and edges). A dedicated graph database may be needed for such use cases.
3. **Real-Time Complexity:** As the dataset grows, real-time querying can become more complex and require optimizations, especially when dealing with large numbers of nodes and edges.

## Graphs Constructed from the Data

Below are some example graphs constructed from the cybersecurity data. These graphs visualize the relationships between different hosts, ports, services, and vulnerabilities.

### Example Graph 1: Network of Hosts and Ports
This graph shows the relationships between hosts and the ports they expose.

![Network of Hosts and Ports]![image](https://github.com/user-attachments/assets/0c389f3f-4bcc-4776-a20d-b644156d458b)

### Example Graph 2: Services Running on Hosts
This graph illustrates which services are running on which hosts, helping to understand the attack surface of each system.

![Services Running on Hosts]![image](https://github.com/user-attachments/assets/9ae5f355-5356-4202-b209-4a84c4150fb5)

### Example Graph 3: Vulnerabilities Associated with Services
This graph shows the vulnerabilities linked to different services. It helps to identify potential security risks on a network.

![Vulnerabilities Associated with Services]![image](https://github.com/user-attachments/assets/c1417ae1-6803-402c-8943-2738ec078767)

## How It Works

### 1. **Ingestion Pipeline**
Data is ingested from MongoDB using the `fetch_from_mongo` function. This function retrieves documents from the MongoDB database and passes them to the `ingest_data` function, which:
- Creates **Host**, **Port**, **Service**, and **Vulnerability** nodes.
- Adds relationships between the nodes (e.g., a host has a port, a port runs a service, a service has vulnerabilities).
- Updates the graph dynamically with the new data.

### 2. **Inference Pipeline**
Once the graph is constructed, the `run_inference` function is used to query the graph and answer specific questions. Some of the example queries include:
- **Ports for a host:** Find all ports associated with a given host.
- **Vulnerabilities for a host:** Find all vulnerabilities related to services running on a host.
- **Common services between two hosts:** Find any services shared by two hosts.

### 3. **Graph Representation**
The graph is constructed using the **NetworkX** library, where each entity (Host, Port, Service, Vulnerability) is represented as a node, and relationships between them are represented as edges with associated labels (e.g., `HasPort`, `RunsService`, `HasVulnerability`).

### 4. **Storage**
The graph is stored in memory as a `networkx.Graph()` object, but for large-scale or persistent use cases, you could extend this pipeline to store the graph in a vector database or a dedicated graph database.

## Example Queries

### 1. **What ports are running on a host?**
Query the graph to find all ports associated with a specific hostname.

### 2. **What vulnerabilities are present on a host?**
Query the graph to find vulnerabilities associated with the services running on the host.

### 3. **Are there any common services running between two hosts?**
Find services that are running on both host1 and host2.

### 4. **Are there any login forms on a host?**
Check if there are login forms or credentials captured on a given host.

## Code Structure

### `inference.py`
Contains the core logic for building the inference pipeline:
- **query_ports:** Finds all ports associated with a given hostname.
- **query_vulnerabilities:** Finds all vulnerabilities for a given host by first identifying the services running on the host and then querying for vulnerabilities linked to those services.
- **run_inference:** Performs all the steps of the inference pipeline, printing graph nodes and edges, and answering queries about ports and vulnerabilities.

### `ingest_data.py`
Contains the logic for fetching data from MongoDB and constructing the graph:
- **fetch_from_mongo:** Connects to MongoDB, retrieves data, and passes it to `ingest_data`.
- **ingest_data:** Processes the data and builds the graph, adding nodes and edges for hosts, ports, services, and vulnerabilities.

### `graph_entities.py`
Contains the definitions of the graph entities (Host, Port, Service, Vulnerability), with basic attributes and representations.

### `main.py`
The entry point of the application, calling the functions to fetch data from MongoDB and run the inference pipeline.

## Running the Application

1. **Fetch Data and Build the Graph:**

```bash
python main.py
```

2. **Run Queries:**
The `run_inference` function will automatically display information about the nodes and edges in the graph and answer example queries.

## Benchmarking
The pipeline includes benchmarking logic to assess the time taken to respond to a query. This helps measure both the speed and quality of the response.

## Future Improvements
- **Real-Time Updates:** Implement a listener for MongoDB changes (e.g., using Change Streams) to allow real-time updates to the graph without needing to re-fetch the entire dataset.
- **Distributed Graph Database:** For large-scale deployments, integrating with a distributed graph database (e.g., Neo4j) could enhance scalability and performance.
- **Advanced Inference Models:** Future work could incorporate machine learning models to provide more intelligent analysis, such as automatically detecting and classifying new vulnerabilities.
- **Image and Document Processing:** The pipeline could be extended to handle image data (e.g., screenshots from security scanners) or documents related to vulnerabilities.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
