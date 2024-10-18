import chromadb
import configparser
from db import get_mysql_conn
from sentence_transformers import SentenceTransformer

config = configparser.ConfigParser()
config.read("config.ini")

chroma_directory = config['chroma']['chroma_directory']
collection_name = config['chroma']['collection_name']
embedding_model = config['chroma']['embedding_model']

model = SentenceTransformer(embedding_model)

# Initialize Chroma DB
chroma_client = chromadb.PersistentClient(path = chroma_directory)
collection = chroma_client.create_collection(collection_name)

# Get MySQL connection
conn = get_mysql_conn()

with conn.cursor() as cursor:
    cursor.execute("SELECT id, name, price, category, description FROM products")
    products = cursor.fetchall()

    # Add embeddings to Chroma
    for product in products:
        product_id, name, price, category, description = product
        embedding = model.encode(description)
        collection.add(
            ids=[str(product_id)],
            embeddings=[embedding],
            metadatas=[{"id":product_id,"name": name, 
                        "price": str(price), "category": category, 
                        "description":description}]
        )
        print(f"Product{product_id} embeddings created")

print("Embeddings added to Chroma DB.")
conn.close()