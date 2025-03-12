# Context-Aware Conversational Search System

## Overview
The **Context-Aware Conversational Search System** is an advanced search tool designed to enhance user interaction by retaining search context, recognizing intent, and integrating knowledge graphs for more accurate and meaningful results. It leverages **Sentence Transformers for semantic search**, **Redis for caching**, and **Flask for the web interface**, providing a seamless conversational search experience.

## Features

### 1. **Semantic Search**
- Utilizes **Sentence Transformers** to generate high-quality sentence embeddings.
- Computes **cosine similarity** to rank and retrieve the most relevant results.

### 2. **Context Retention**
- Stores previous user queries to maintain **conversational context**.
- Enables users to **revisit past searches** and continue interactions smoothly.

### 3. **Intent Recognition & Query Expansion**
- Uses NLP techniques to **understand user intent** and expand queries.
- Enhances search accuracy by **matching similar phrases and synonyms**.

### 4. **Knowledge Graph Integration**
- Structures search data using **Neo4j graph database**.
- Allows for **semantic relationships** between search entities.

### 5. **Recommendation System**
- Suggests related content based on **user search behavior and interactions**.
- Improves search relevance over time through **adaptive learning**.

### 6. **Efficient Caching with Redis**
- Stores previously computed results to **speed up repeated queries**.
- Reduces backend load and improves response times.

### 7. **User Interface (UI) Features**
- **Chat History Dropdown:** Displays past queries for easy reference.
- **Dynamic Search Filters:** Allows filtering by categories, keywords, and metadata.
- **Interactive UI:** Designed with **TailwindCSS** for a clean and responsive layout.

---

## Getting Started

### Prerequisites
Ensure the following dependencies are installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **Redis server** (for caching)
- **Neo4j database** (for knowledge graph storage)
- **Git** (for version control)

### Setup Instructions

#### **1. Clone the Repository**
```bash
git clone <REPO_URL>
cd <REPO_NAME>
```

#### **2. Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **4. Start Redis Server** (if not already running)
```bash
redis-server
```

#### **5. Run the Flask Application**
```bash
python src/app.py
```
The application will be accessible at: **http://localhost:5000**

---

## Dependencies

- **Flask** - Backend framework for serving the web application.
- **Sentence Transformers** - Generates semantic embeddings for search queries.
- **scikit-learn** - Computes cosine similarity between sentence embeddings.
- **Redis** - Caches search results for improved performance.
- **Neo4j** - Stores structured knowledge graphs for better search accuracy.
- **TailwindCSS** - Styles the front-end interface.
- **JavaScript** - Handles dynamic content like search results and chat history.

---

## Why Choose Sentence-Transformers for Semantic Search?

### **1. Optimized for Sentence-Level Embeddings**
Unlike traditional models like **Word2Vec**, which work at the word level, **Sentence-Transformers** generates embeddings that capture the meaning of **entire sentences**, making them ideal for search applications.

### **2. State-of-the-Art Performance**
- Built on transformer models like **BERT**, but optimized for **semantic similarity**.
- Directly produces embeddings that can be compared using **cosine similarity**.

### **3. Pretrained Models for Various Use Cases**
- Supports models fine-tuned for **document retrieval**, **paraphrase identification**, and **semantic search**.

### **4. Faster and More Efficient**
- Uses pooling techniques to **reduce computational cost** while maintaining accuracy.
- Handles **large-scale search queries** efficiently.

### **5. Excellent for Query Expansion & Paraphrase Detection**
- Enhances search results by recognizing **synonyms and related phrases**.
- Ensures that **different phrasings of a query** return consistent results.

### **6. Fine-Tuning for Domain-Specific Tasks**
- Can be trained on **custom datasets** for specialized applications like **legal document search**, **e-commerce product recommendations**, etc.

---

## Caching with Redis

To **optimize performance**, the system caches results in Redis. When a query is performed:
1. The result is **computed and stored** in Redis.
2. For repeated queries, **Redis returns the cached data** instead of recomputing.

### **Benefits of Caching**
✅ **Faster Responses:** Cached results are retrieved instantly.
✅ **Reduced Server Load:** Limits the number of redundant computations.
✅ **Improved Scalability:** Allows handling of a larger number of users efficiently.

---

## Troubleshooting

### **Redis Server Not Starting?**
Check if Redis is running:
```bash
redis-cli ping
```
If it responds with `PONG`, Redis is running correctly.

### **Application Not Displaying Correctly?**
- Ensure **TailwindCSS** is loading properly.
- Check for JavaScript errors in the browser (Press **F12 → Console Tab**).

### **Slow Queries?**
- Verify that **Redis caching** is being utilized.
- Check the logs to see if queries are being recomputed unnecessarily.

---

## Conclusion

The **Context-Aware Conversational Search System** provides a robust and efficient way to perform **semantic search** with advanced **context retention, query expansion, and structured knowledge graph integration**. By leveraging **Sentence Transformers**, **Redis caching**, and a **dynamic UI**, this system ensures **fast, accurate, and context-aware search experiences** for users.

---

🔹 **Future Enhancements**:
- **Multi-language support** for internationalization.
- **Personalized recommendations** based on user history.
- **Real-time search suggestions** using AI-driven auto-complete.

🚀 **Start using the system today and experience the power of intelligent conversational search!**

