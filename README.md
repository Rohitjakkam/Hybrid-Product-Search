# Hybrid Search Engine: Combining Keyword and Semantic Search

### Overview
This project demonstrates how to build a **hybrid search engine** that combines traditional keyword-based search with semantic search using embeddings. The goal is to improve search accuracy by understanding the meaning of user queries, leveraging both exact keyword matching (with MySQL) and semantic understanding (with ChromaDB).

### Features
- **Keyword Search**: Performs exact matches of product names, categories, or keywords using MySQL.
- **Semantic Search**: Uses **Sentence Transformers** to generate embeddings for product descriptions and allows for context-aware searches using ChromaDB.
- **Hybrid Search Capability**: Combines both search approaches to return more relevant results for user queries.
- **Streamlit UI**: Provides a user-friendly interface for users to perform searches.

### Technologies Used
- **MySQL**: Relational database for storing product information and handling keyword-based queries.
- **ChromaDB**: Vector database used to store and search embeddings for semantic queries.
- **Python**: Core programming language for the backend.
  - **pymysql**: For connecting to MySQL.
  - **chromadb**: For interacting with ChromaDB.
  - **sentence-transformers**: For generating embeddings from product descriptions.
- **Streamlit**: Frontend framework to create the web UI for the search engine.

### Project Structure

```
hybrid_search
│
├── chroma_db/
│   └── (ChromaDB-related files)
│
├── images/
│   └── product_search.png
│
├── scripts/
│   ├── __init__.py
│   ├── db.py                # Handles MySQL connection
│   ├── create_embeddings.py  # Creates embeddings and stores them in ChromaDB
│   ├── query_embeddings.py   # Queries embeddings from ChromaDB
│
├── config.ini                # Configuration settings for MySQL and ChromaDB
├── main.py                   # Main application file for the Streamlit UI
├── products.sql              # SQL script to set up the product table in MySQL
├── readme.md                 # Documentation (this file)
└── requirements.txt          # Python package dependencies
```

### Prerequisites

1. **Python 3.10+**
2. **MySQL Server**: Set up a MySQL database and configure it in the `config.ini` file.
3. **ChromaDB**: Ensure ChromaDB is installed and configured for embedding storage.

### Setup Instructions

#### 1. Clone the repository
```bash
git clone https://github.com/Rohitjakkam/hybrid_search_engine.git
cd hybrid_search_engine
```

#### 2. Install required packages
Install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

#### 3. Set up the MySQL database
- Create a MySQL database using the `products.sql` script:
```sql
# create database
CREATE DATABASE salesdb1;

# use database
USE salesdb1;

# create products table
CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  price DECIMAL(10, 2),
  category VARCHAR(100),
  description TEXT
);

# Insert sample data into the table
INSERT INTO products (name, price, category, description) VALUES
('Wireless Mouse', 25.99, 'Electronics', 'A sleek wireless mouse with ergonomic design.'),
('Laptop Stand', 49.99, 'Accessories', 'Adjustable aluminum stand for laptops.'),
('Bluetooth Speaker', 89.99, 'Electronics', 'Portable Bluetooth speaker with high-quality sound.');
```

#### 4. Configure the `config.ini` file
Edit the `config.ini` file with your MySQL and ChromaDB credentials:
```ini
[mysql]
host = localhost
port = 3306
user = your_username
password = your_password
database_name = salesdb1

[chroma]
num_of_results = 3
collection_name = product_descriptions
chroma_directory = chroma_db
embedding_model = all-MiniLM-L6-v2
```

#### 5. Generate embeddings for semantic search
Run the following script to generate embeddings for the product descriptions and store them in ChromaDB:
```bash
python scripts/create_embeddings.py
```

#### 6. Run the application
Start the Streamlit application by running the following command:
```bash
streamlit run main.py
```

Once the server is running, the application will be accessible in your browser.

### Search Functionality

- **Search by Product Name**: Performs a keyword search in MySQL for product names.
- **Search by Description**: Uses ChromaDB to perform a semantic search based on the description.
- **Search by Price Range**: Allows users to filter products by price using MySQL.

### Example Queries
- **Product Name Search**: Enter "Wireless Mouse" to find exact product matches.
- **Description Search**: Enter "ergonomic design" to find products related to ergonomic features.
- **Price Range Search**: Input a range (e.g., 20 to 50) to filter products within that price.

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing
Feel free to submit issues or pull requests if you want to contribute to this project.

### Contact
For any inquiries, reach out to me via:
- **LinkedIn**: [Rohit Jakkam](https://www.linkedin.com/in/rohitjakkam/)
- **GitHub**: [Rohitjakkam](https://github.com/Rohitjakkam)
