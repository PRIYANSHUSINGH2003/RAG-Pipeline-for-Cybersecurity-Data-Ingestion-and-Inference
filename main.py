from rag_pipeline import fetch_from_mongo
from inference import run_inference

def main():
    # Fetch data from MongoDB and build the graph
    fetch_from_mongo()
    
    # Run inference queries
    run_inference()

if __name__ == "__main__":
    main()
