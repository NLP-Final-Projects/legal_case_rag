

---
## Overview
The **Legal Case Retrieval-Augmented Generation (RAG)** project applies cutting-edge **Natural Language Processing (NLP)** techniques to provide automated, context-aware legal answers by referring to historical judicial decisions. This system combines a **retrieval-based model** with **large language models (LLMs)** to generate accurate responses to legal queries. Through the integration of **Prompt Engineering**, the system enhances legal question-answering by retrieving and analyzing past legal rulings to produce relevant, context-specific answers.

The project manages a database containing over **25,000 anonymized judicial decisions**, providing legal professionals with precise legal case retrieval and efficient query responses.

To use this project online, visit our [Hugging Face Space](https://huggingface.co/spaces/parsi-ai-nlpclass/Legal_RAG).
---

## Key Features
### 1. **Legal Case Retrieval**
The system retrieves relevant legal rulings from a database of judicial decisions. The **ParsBERT** model is used to encode legal documents into vector representations, which are stored in a **Chroma database** for efficient retrieval based on **cosine similarity**. This enables the system to extract judicial decisions that are most relevant to the legal query being processed.

### 2. **RAG (Retrieval-Augmented Generation)**
The RAG model combines the retrieved legal documents with a generative language model, such as OpenAI’s GPT, to generate comprehensive and factually grounded answers. By integrating real legal cases into the generative process, the model can provide legally accurate and contextually appropriate responses.

### 3. **Prompt Engineering**
The system uses **Prompt Engineering** to optimize the generative model for legal contexts. Prompts are designed to include relevant legal terminology and case details, ensuring that the generated responses are tailored to the legal domain. This technique improves the model’s ability to generate useful and legally sound responses to complex queries.

### 4. **Data Handling**
The system is equipped to handle over 25,000 judicial rulings, which have been anonymized and preprocessed to remove non-relevant metadata. The documents are chunked into smaller segments for efficient retrieval and processing, ensuring that the system can quickly respond to legal queries with accurate information.

---

## Data Sources
The project relies on two key types of legal documents:

### 1. **Legal Codes**
These are statutory regulations and codes sourced from public legal archives. Legal codes form the foundation of any legal system, providing a structured framework for decision-making in judicial cases.

### 2. **Court Rulings (Judgments)**
The dataset includes **judicial decisions**, also known as **judgments** or **court rulings**, that are collected via web scraping from judicial databases. These rulings are anonymized and preprocessed for analysis and retrieval. The system leverages these judgments to provide answers grounded in past legal precedents.

---

## Data Types and Extraction Process

### **Data Extraction Process**
For each data category, the extraction process differs slightly. Below is a breakdown of how the data is collected and prepared for use in the system:

#### **Legal Codes**
The legal codes are extracted from various public sources, including the **National Legal System**, **Mehdi Davoodabadi's website**, and **Parliament Research websites**. For this project, the primary source of legal codes is **Mehdi Davoodabadi's website**. Initially, 20 major legal titles are selected as the main legal codes, including:

- **Constitution of the Islamic Republic of Iran**
- **Direct Taxation Law**
- **Labor Law**
- **Dispute Resolution Councils Law**
- **Civil Law**
- **Civil Liability Law**
- **Mandatory Insurance Law for Third-Party Damages**
- **Commercial Law**
- **Administrative Justice Law**
- **Registration of Documents and Properties Law**
- **Islamic Penal Code**
- **Issuance of Check Law**
- **Family Protection Law**
- **Amendment of the Commercial Code**
- **Civil Procedure Code**
- **Law on the Execution of Financial Judgments**
- **Municipal Law**
- **Law on the Enforcement of Civil Judgments**

The texts of these laws are extracted, and the dataset is prepared using a Python script (`model/law_provider.py`). This results in two main files:
- **dataset/law_name.csv**: Contains information about the legal codes.
- **dataset/madeh_df.csv**: Contains the articles (or provisions) of the laws.

In total, **5,882 provisions and principles** have been extracted. To avoid duplication or overlap between repeated provisions, they are listed under the original article number.

#### **Court Rulings (Judgments)**
Approximately **30,000 judicial decisions (court rulings)** have been made available anonymously by the **Judiciary Research Center** in the **National Judgments System**. These rulings serve as the foundation for this project. A custom web scraper (`model/case_crawler.py`) was developed to extract these rulings.

The scraper retrieves judicial decisions from the **National Judgments System**, processes them according to the research needs, and prepares them for use in the system. After running the scraper for **7 hours and 30 minutes**, over **25,000 rulings** were extracted and saved in the **dataset/case_df.csv** file.

---

## Data Preprocessing
Once the court rulings are extracted, several **preprocessing** steps are necessary to clean and prepare the data for the model:

- The dataset includes **25,048 documents**, each of which is examined for length. Of these, **622 documents** contain more than **2,500 words**, and **40 documents** contain fewer than **50 words**.
- The system also ensures that unnecessary metadata such as anonymized names, dates, and non-relevant information are removed.

#### **Preprocessing Judicial Rulings**
The preprocessing of judicial rulings involves:
- **Removing anonymized names, dates, and irrelevant numbers**.
- Splitting the texts into manageable chunks (each containing around **250 words**) to facilitate efficient tokenization and retrieval during query processing.
- Maintaining context across sections by adding a **50-word overlap** between consecutive chunks.

The preprocessing code is available in the script **model/pre_process.ipynb**, and the word distribution across documents is illustrated in a **histogram**, as shown below:

![[Pasted image 20240924220942.png]]
**Figure 3.3**: Histogram showing the distribution of word counts for each document.

---
## Evaluation and Validation
For evaluating the model, an initial **human evaluation** process was conducted to create a **dataset of questions and answers** based on the extracted judicial decisions. To improve the research outcomes, the evaluation dataset was divided into three categories:

1. **Easy**: Questions are generally derived from the title of the case, and the answers can be found directly within the text.
2. **Medium**: Both the questions and answers are extracted from the content of the case.
3. **Hard**: Questions are drawn from a set of similar cases, and the answers are synthesized from the relevant case texts.

The system's performance is evaluated using two main metrics:

### 1. **BLEU Score (Bilingual Evaluation Understudy)**
**BLEU** is an automatic metric for evaluating the quality of machine-generated translations. It compares the **n-grams** in the model-generated responses to reference answers (often human-generated). The BLEU score is a value between **0 and 1**, with scores closer to **1** indicating higher quality. While **BLEU** is widely used due to its simplicity and computational efficiency, it may struggle to capture deeper meanings or complex structures in texts.

### 2. **BERT Score**
**BERT Score** is a more advanced metric that uses **BERT** or similar language models to assess the quality of generated text by comparing **semantic similarity** between the generated response and the reference answer. Instead of comparing **n-grams**, BERT Score measures the similarity of the **word embeddings** generated by the BERT model for each word. This approach typically provides greater accuracy for understanding the meaning and context of a response compared to BLEU.

In summary, **BLEU** focuses more on structural accuracy, while **BERT Score** emphasizes the semantic understanding of the texts.

### **RAG Model Evaluation**
Since the focus of this project is on **RAG**, the generated answers were compared in two categories: one using **RAG** and one without it. By running the evaluation metrics, the following scores were achieved:

---

## Model Workflow
The RAG model workflow consists of several steps:

### 1. **Data Retrieval**
Legal documents are encoded into vectors using the **ParsBERT** model. These vectors are stored in a **Chroma database**, which allows the system to retrieve relevant documents based on the cosine similarity between the user’s query and the stored vectors.

### 2. **Query Encoding**
When a user submits a legal query, the system encodes the query into a vector representation and matches it against the legal document vectors. The most relevant legal documents are retrieved based on their similarity to the query.

### 3. **Response Generation**
The retrieved legal documents and the user query are combined into a **prompt** that is passed to the **GPT** model. The model then generates a context-aware and legally accurate response based on the input query and retrieved documents.

### 4. **Prompt Engineering**
The prompts are fine-tuned for legal queries using **Prompt Engineering** techniques. This ensures that the generated response is tailored to the legal context and is both accurate and relevant to the specific legal question posed.

---

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

The system will retrieve the most relevant legal documents and generate a response based on

 the retrieved information and legal precedents.

---

## Roadmap
- **Improve Retrieval Efficiency**: Further optimize retrieval to make it faster and more accurate.
- **Expand Dataset**: Continuously update the judicial decisions and legal codes to include more recent data.
- **Multi-Agent RAG**: Implement a multi-agent system to handle more complex legal reasoning.

---

## Contributing
We welcome contributions! Please feel free to open issues or submit pull requests.

---

## License
This project is licensed under the **MIT License**.

---

This version now includes detailed **evaluation and validation** processes along with the BLEU and BERT metrics for assessing the RAG model’s performance. Let me know if you need further adjustments!