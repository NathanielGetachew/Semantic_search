Semantic Search with Context-Aware Chat and Product Filtering
This project is an advanced Semantic Search Tool that provides users with the ability to search and filter products based on descriptions, categories, and features, while also offering a conversational history. It uses Sentence Transformers for semantic embeddings, Redis for caching results, and Flask for the web interface. The system features context-aware search that retains previous queries and integrates a chat history dropdown, enhancing user interaction.

Features
Semantic Search: Uses Sentence Transformers for advanced semantic similarity matching of product descriptions, features, and categories.
Context-Aware Chat: Retains past search queries in a dropdown chat history, allowing users to revisit previous searches.
Product Filtering: Dynamically filter search results based on categories and features, and displays only relevant data.
Bold Product Title & Truncated Info: Product details and titles are displayed in bold, with other information truncated for better UI clarity.
Caching with Redis: Speeds up repeated queries by caching the results.
Dynamic UI: Interactive and simple web interface for seamless product searching and filtering.
Getting Started
Prerequisites
Ensure you have the following installed:

Python 3.8+
pip (Python package manager)
Redis server
Git
Setup Instructions
Clone the Repository

bash
Copy
Edit
git clone <REPO_URL>
cd <REPO_NAME>
Set up the Virtual Environment

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Start Redis Server (if it's not already running)

bash
Copy
Edit
redis-server
Run the Flask Application

bash
Copy
Edit
python src/app.py
The application will be running at http://localhost:5000.

Dependencies
Flask: Backend framework for serving the web application.
Sentence Transformers: For generating semantic embeddings.
scikit-learn: For computing cosine similarity between sentence embeddings.
Redis: For caching search results.
TailwindCSS: For styling the front-end interface.
JavaScript: For handling dynamic content like search results and chat history.
Why Choose Sentence-Transformers Over Other Models (e.g., BERT, Word2Vec, etc.)?
1. Optimized for Sentence Embeddings
Sentence-Transformers is specifically designed for generating sentence-level embeddings, which is essential for semantic search tasks. Unlike models like BERT (which requires additional steps to derive sentence embeddings) or Word2Vec (which operates on word-level embeddings), Sentence-Transformers generates embeddings that directly capture the meaning of entire sentences, making it more efficient and accurate for semantic search.

2. State-of-the-Art Performance for Semantic Search
Built on top of transformer models like BERT, Sentence-Transformers optimizes them for semantic similarity tasks. It directly generates embeddings that can be compared using cosine similarity, facilitating quick and accurate retrieval of semantically similar sentences or documents.

3. Pretrained Models for Various Use Cases
Sentence-Transformers offers a wide range of pretrained models tailored for semantic search, paraphrase identification, and document retrieval. These models are fine-tuned on large datasets to produce high-quality embeddings out-of-the-box.

4. Faster and More Efficient
Sentence-Transformers is designed for faster inference compared to BERT, utilizing techniques like mean-pooling and max-pooling. It is optimized to handle large-scale semantic search tasks more efficiently than traditional models.

5. Easy Integration and Usage
Sentence-Transformers provides a simple API that allows easy generation of sentence embeddings. Unlike BERT, which requires manual tokenization and attention masks, Sentence-Transformers simplifies the process, reducing complexity in your pipeline.

6. Excellent for Paraphrase Detection and Similarity
Sentence-Transformers excels in tasks like paraphrase detection, where understanding the meaning of entire sentences is crucial. This is particularly useful in semantic search applications where queries may be phrased differently, but convey the same intent.

7. Fine-Tuning for Specific Tasks
While Sentence-Transformers works well out-of-the-box, it also allows fine-tuning on domain-specific data, making it even more effective for specialized tasks such as e-commerce product search, legal document retrieval, and more.

User Interface Features
Search Interface: Allows users to input a search query, and results are displayed dynamically. Product titles are bolded, and descriptions are truncated for a cleaner UI.
Chat History Dropdown: Displays past searches in the top-right corner of the page. Users can view their query, timestamp, and the number of search results.
Filtering Options: Filter results based on categories and features.
Product Detail View: Only relevant product details (like title and description) are displayed for each result. Categories and features are truncated to maintain a clean UI.
Caching with Redis
To optimize performance, Redis is used to cache search results for repeated queries. When a query is performed for the first time, the result is computed and stored in Redis. For subsequent queries that match the cached result, Redis will provide the stored data, reducing the computational cost and speeding up the response time.

Benefits of Caching
Faster Responses: By caching previous search results, queries that are repeated will return results much faster.
Reduced Load on the Server: Redis reduces the number of times the backend model needs to run, easing the load on the server.
Troubleshooting
1. Redis Server Not Starting
If Redis doesn't start correctly, ensure it's installed properly and running as a service. You can verify the status with:

bash
Copy
Edit
redis-cli ping
If it responds with PONG, Redis is running.

2. Application Not Displaying Correctly
Ensure the Tailwind CSS file is being loaded properly. Check for any JavaScript errors in the browser’s console (F12 → Console tab).

3. Slow Queries
If queries are running slowly, ensure that the cache is being utilized properly. Check if Redis is being queried for repeated searches, and inspect the server logs for any errors or performance issues.

Conclusion
This semantic search system with context-aware chat, filtering options, and caching provides a robust solution for users looking for an interactive and efficient search experience. By leveraging Sentence-Transformers and Redis, the system ensures fast and accurate results, while the chat history feature allows users to maintain context and revisit previous searches.
