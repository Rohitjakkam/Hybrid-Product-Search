import chromadb
import configparser
import pandas as pd
import streamlit as st
from scripts.db import get_mysql_conn
from sentence_transformers import SentenceTransformer

config = configparser.ConfigParser()
config.read("config.ini")

chroma_directory = config['chroma']['chroma_directory']
collection_name = config['chroma']['collection_name']
num_of_results = int(config['chroma']['num_of_results'])
embedding_model = config['chroma']['embedding_model']

chroma_client = chromadb.PersistentClient(path = chroma_directory)
collection = chroma_client.get_collection(collection_name)

embedding_model = SentenceTransformer(embedding_model)

conn = get_mysql_conn()

st.set_page_config(
    page_title="Hybrid Product Search",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.sidebar.header("Semantic Search")
st.sidebar.image("images/search.png", use_column_width=True, 
                 caption="Product Semantic Search")
st.header("Hybrid Product Semantic Search")
query_type = st.selectbox("Search by:", ["Product Name", "Description", 
                                         "Price Range"])

if query_type == "Product Name":
    product_name = st.text_input("Enter product name:")
    if st.button("Search"):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", 
                           ('%' + product_name + '%',))
            results = cursor.fetchall()
            if results:
                columns = ['ID', 'Name', 'Price', 'Category', 'Description']
                df_results = pd.DataFrame(results, columns=columns)
                st.subheader("Results from MySQL:")
                st.table(df_results)
            else:
                st.write("No products found.")

elif query_type == "Description":
    description_query = st.text_input("Enter product description:")
    if st.button("Search"):
        query_vector = embedding_model.encode(description_query)
        results = collection.query(query_vector, n_results = num_of_results)
        st.write("Results from Chroma DB:")
        for result in results['metadatas']:
            st.table(result)

elif query_type == "Price Range":
    min_price = st.number_input("Minimum Price:", min_value=0.0)
    max_price = st.number_input("Maximum Price:", min_value=0.0)
    if st.button("Search"):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE price BETWEEN %s AND %s", 
                           (min_price, max_price))
            results = cursor.fetchall()
            if results:
                columns = ['ID', 'Name', 'Price', 'Category', 'Description']
                df_results = pd.DataFrame(results, columns=columns)
                st.subheader("Results from MySQL:")
                st.table(df_results)
            else:
                st.write("No products found.")