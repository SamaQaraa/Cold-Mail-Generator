import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        results = self.collection.query(query_texts=skills, n_results=2)
        all_links = []

        for metadata_list in results.get('metadatas', []):
            for metadata in metadata_list:
                all_links.append(metadata["links"])

        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in all_links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)

        return unique_links
