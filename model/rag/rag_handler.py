from typing import List
import chromadb
from transformers import AutoTokenizer, AutoModel
from chromadb.config import Settings
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from hazm import *


class RAG:
    def __init__(self,
                 model_name: str = "HooshvareLab/bert-base-parsbert-uncased",
                 collection_name: str = "legal_cases",
                 persist_directory: str = "chromadb_collections/",
                 top_k: int = 2
                 ) -> None:

        self.cases_df = pd.read_csv('processed_cases.csv')

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.normalizer = Normalizer()
        self.top_k = top_k

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

        self.client = chromadb.PersistentClient(path=persist_directory)

        self.collection = self.client.get_collection(name=collection_name)

    def query_pre_process(self, query: str) -> str:
        return self.normalizer.normalize(query)

    def embed_single_text(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()


    def extract_case_title_from_df(self, case_id: str) -> str:

        case_id_int = int(case_id.split("_")[1])

        try:
            case_title = self.cases_df.loc[case_id_int, 'title']
            return case_title
        except KeyError:
            return "Case ID not found in DataFrame."

    def extract_case_text_from_df(self, case_id: str) -> str:
        case_id_int = int(case_id.split("_")[1])

        try:
            case_text = self.cases_df.loc[case_id_int, 'text']
            return case_text
        except KeyError:
            return "Case ID not found in DataFrame."

    def retrieve_relevant_cases(self, query_text: str) -> List[str]:
        normalized_query_text = self.query_pre_process(query_text)

        query_embedding = self.embed_single_text(normalized_query_text)
        query_embedding_list = query_embedding.tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding_list],
            n_results=self.top_k
        )

        retrieved_cases = []
        for i in range(len(results['metadatas'][0])):
            case_id = results['ids'][0][i]
            case_text = self.extract_case_text_from_df(case_id)
            case_title = self.extract_case_title_from_df(case_id)
            retrieved_cases.append({
                "text": case_text,
                "title": case_title
            })

        return retrieved_cases

    def get_information(self, query: str) -> List[str]:
        return self.retrieve_relevant_cases(query)