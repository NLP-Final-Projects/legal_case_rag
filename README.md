# Legal Case RAG

## Overview
This project focuses on developing a **Retrieval-Augmented Generation (RAG)** model applied to legal cases to answer legal queries based on existing judicial decisions. By utilizing both retrieval systems and Large Language Models (LLMs), the model can generate precise and context-aware responses to legal questions by referring to similar prior rulings.

The project integrates **Natural Language Processing (NLP)** techniques like **Prompt Engineering** and advanced retrieval systems to enhance legal case analysis and automate legal question-answering based on past legal precedents.

## Features
- **Legal Case Retrieval**: Pulls relevant judicial decisions (court rulings) from a database to answer legal questions.
- **RAG (Retrieval-Augmented Generation)**: Combines retrieved legal documents with LLMs to generate accurate, context-aware answers.
- **Prompt Engineering**: Tailors the model prompts for legal-specific contexts, enhancing response accuracy.
- **Data Handling**: Handles more than 25,000 anonymized judicial decisions.

## Data Sources
The project uses two main datasets:
1. **Legal Codes**: Extracted from publicly available sources, including national legal archives.
2. **Court Rulings (Judgments)**: Collected through web scraping from judicial decision databases. These datasets consist of over 25,000 anonymized judgments, processed for analysis.

## Model Workflow
1. **Data Retrieval**: The retrieval system uses a pre-trained **ParsBERT** model to encode legal documents, storing vector representations in a Chroma database.
2. **Query Encoding**: User queries are encoded, and the model retrieves the most relevant legal documents using cosine similarity.
3. **Response Generation**: The retrieved documents and the user query are combined into a prompt, which is passed to an OpenAI GPT-based model to generate a detailed legal response.

## Installation

### Prerequisites
- Python 3.x
- Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
To run the project and query the legal RAG model:
```bash
python run_query.py --case "Describe the legal question here"
```

The response will be generated based on the most relevant legal cases and statutes.

## Data Preprocessing
- **Judicial Rulings**: Texts are cleaned and preprocessed to remove anonymized information, dates, and other non-relevant metadata. The documents are divided into smaller chunks for tokenization, ensuring efficient retrieval and processing.
- **Vector Encoding**: Each legal document is encoded using ParsBERT to facilitate similarity-based retrieval during query processing.

## Evaluation Metrics
The model is evaluated using:
1. **BLEU Score**: Measures the accuracy of generated answers against human references.
2. **BERT Score**: Evaluates the semantic similarity between the model’s responses and reference texts.

**BLEU-4**: 10.6%  
**BERT F1**: 91.5%

## Roadmap
- Enhance data retrieval efficiency and scale the model to handle a broader range of legal queries.
- Incorporate multi-agent RAG to handle complex multi-step legal reasoning.
- Improve the database of judicial decisions with continuous updates.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.