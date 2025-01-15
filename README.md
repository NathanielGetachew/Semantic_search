# Semantic Search with Filtering and Caching

This project is a **Semantic Search Tool** designed to search and filter products based on their descriptions, categories, and features. It uses **Sentence Transformers** for semantic embeddings, **Redis** for caching results, and a **Flask** web application for the user interface.

## Features
- **Semantic Search:** Leveraging Sentence Transformers to perform advanced semantic similarity matching.
- **Filtering Options:** Dynamically filter search results based on categories and features.
- **Caching with Redis:** Speeds up repeated queries by caching results.
- **Dynamic UI:** Simple web interface for searching and filtering.

---

## Getting Started

### Prerequisites
Make sure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- Redis server
- Git

---

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone <REPO_URL>
cd <REPO_NAME>
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
redis-server
python src/app.py
```
### Dependencies
Flask: Backend framework for serving the web application.
Sentence Transformers: For generating semantic embeddings.
scikit-learn: For computing cosine similarity.
Redis: For caching search results.
TailwindCSS: For styling the front-end.

# Why Choose Sentence-Transformers Over Other Models (e.g., BERT, Word2Vec, etc.)?
When building a semantic search system, the choice of model has a significant impact on performance, efficiency, and accuracy. While popular models like BERT and Word2Vec are widely used, Sentence-Transformers offers several compelling advantages that make it a better choice for many search-related tasks. Here’s why:

### 1. Optimized for Sentence Embeddings
Sentence-Transformers is specifically designed to generate sentence-level embeddings, which makes it ideal for semantic search and retrieval tasks. It produces dense vector representations of entire sentences, paragraphs, or documents, capturing the semantic meaning more effectively compared to token-level embeddings like BERT or Word2Vec.
BERT is a token-level model and requires additional processing, such as pooling or averaging the token embeddings, to obtain sentence embeddings. This can lead to inefficiencies and loss of context when working with entire sentences.
Word2Vec, on the other hand, generates embeddings for individual words, making it unsuitable for tasks that require understanding the relationships between full sentences or documents. Sentence-Transformers directly addresses this limitation by providing embeddings for entire sentences.
### 2. State-of-the-Art Results for Semantic Search
Sentence-Transformers is built on top of BERT and other transformer models, leveraging them as backbones while adding specialized layers to optimize the embeddings for semantic similarity tasks. This makes it highly effective for tasks like semantic search, text similarity, and clustering.
Unlike Word2Vec or traditional models, Sentence-Transformers generates embeddings that can directly be compared using cosine similarity, making it easy to find semantically similar sentences, even if they use different wording.
### 3. Pretrained Models for Various Tasks
Sentence-Transformers provides access to a wide range of pretrained models, tailored for specific tasks such as semantic search, paraphrase identification, and document retrieval. These models have been trained on large datasets specifically designed for generating high-quality sentence embeddings, allowing you to achieve good results with minimal fine-tuning.
BERT models can be fine-tuned for specific tasks, but they are not inherently optimized for sentence embeddings, which means you'll need more effort to adapt them for semantic search applications.
### 4. Faster and More Efficient
Sentence-Transformers is designed to be more efficient than traditional transformer-based models like BERT. It uses techniques like mean-pooling or max-pooling to speed up inference times and reduce the computational load. This makes it much faster and less resource-intensive than BERT for generating sentence embeddings.
Word2Vec is faster for individual word embeddings but requires additional steps to handle sentences or documents, which can still be computationally expensive compared to Sentence-Transformers.
### 5. Easy to Use and Integrate
Sentence-Transformers provides a simple API that makes it incredibly easy to generate embeddings for sentences and documents. You can directly use the encode method to convert sentences into embeddings, without the need for complex tokenization or additional processing.
With BERT, you often need to handle tokenization, padding, and attention masks manually, which adds complexity to the pipeline. Word2Vec also requires you to handle word-level embeddings and often needs additional steps for aggregating word vectors into sentence representations.
### 6. Better Performance for Paraphrase Detection and Textual Similarity
Sentence-Transformers excels in tasks like paraphrase detection and measuring textual similarity, where understanding the meaning of the entire sentence is crucial. This is particularly useful in applications like semantic search, where you need to compare the user's query with a database of product descriptions or documents that may be phrased differently but convey the same meaning.
BERT and Word2Vec are not inherently designed for such tasks and require additional modifications or fine-tuning to achieve similar performance.
### 7. Fine-Tuning Capabilities
Sentence-Transformers allows easy fine-tuning on domain-specific data, enabling it to improve further for specialized tasks like e-commerce search, legal document retrieval, and more. You can fine-tune the model on a custom dataset to improve the quality of semantic search results tailored to your specific use case.
While BERT can also be fine-tuned, the process is often more complex, especially for tasks requiring embeddings or sentence-level understanding. Word2Vec lacks the flexibility needed for such fine-tuning tasks.



