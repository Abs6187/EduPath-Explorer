import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

with open("course_emb.pkl", "rb") as f:
    course_emb = pickle.load(f)

df = pd.read_excel("analytics_vidhya_courses_Final.xlsx")

model = SentenceTransformer('all-MiniLM-L6-v2')

def search_courses(query, top_n=5):
    query_embedding = model.encode([query])
    
    similarities = cosine_similarity(query_embedding, course_emb)
    
    top_n_idx = similarities[0].argsort()[-top_n:][::-1]
    
    return df.iloc[top_n_idx][["Course Title", "Course Description"]]

query = input("Enter your search query: ")
top_courses = search_courses(query)

print("\nTop relevant courses:")
for idx, row in top_courses.iterrows():
    print(f"Title: {row['Course Title']}")
    print(f"Description: {row['Course Description']}\n")
