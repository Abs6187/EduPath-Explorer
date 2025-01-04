import gradio as gr
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model and data
with open("course_emb.pkl", "rb") as f:
    course_emb = pickle.load(f)

df = pd.read_excel("analytics_vidhya_courses_Final.xlsx")
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_courses(query, top_n=5):
    if not query.strip():
        return "Please enter a search query."
    
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, course_emb)
    top_n_idx = similarities[0].argsort()[-top_n:][::-1]
    
    results = []
    for idx in top_n_idx:
        course = df.iloc[idx]
        results.append({
            "title": course["Course Title"],
            "description": course["Course Description"],
            "similarity": float(similarities[0][idx])
        })
    return results

def gradio_interface(query):
    results = search_courses(query)
    if isinstance(results, str):
        return results
    
    # Format results as HTML with updated styling
    html_output = "<div style='font-family: Inter, sans-serif;'>"
    
    for i, course in enumerate(results, 1):
        relevance = int(course['similarity'] * 100)
        html_output += f"""
        <div style='background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);'>
            <h3 style='color: #1a237e; margin: 0 0 12px 0; font-weight: 600;'>#{i}. {course['title']}</h3>
            <div style='color: #3949ab; font-size: 0.9em; margin-bottom: 10px; font-weight: 500;'>Match Score: {relevance}%</div>
            <p style='color: #424242; margin: 0; line-height: 1.6;'>{course['description']}</p>
        </div>
        """
    
    html_output += "</div>"
    return html_output

# Create Gradio interface with improved styling
css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}
.gradio-button {
    background: linear-gradient(135deg, #3949ab, #1a237e) !important;
}
.gradio-button:hover {
    background: linear-gradient(135deg, #1a237e, #3949ab) !important;
}
"""

with gr.Blocks(css=css, theme="soft") as iface:
    gr.Markdown(
        """
        # 😻 Smart Learning Pathfinder
        Unlock your learning potential with AI-powered course recommendations tailored just for you!
        """
    )
    
    with gr.Row():
        query_input = gr.Textbox(
            label="What would you like to master?",
            placeholder="Tell us your learning interests (e.g., 'AI fundamentals' or 'data science for beginners')",
            scale=4
        )
    
    with gr.Row():
        search_button = gr.Button("✨ Discover Courses", variant="primary")
    
    with gr.Row():
        output = gr.HTML(label="Personalized Recommendations")
    
    search_button.click(
        fn=gradio_interface,
        inputs=query_input,
        outputs=output,
    )
    
    gr.Markdown(
        """
        ### 💡 Optimization Tips:
        - Share your current knowledge level
        - Mention specific skills you want to develop
        - Include your learning preferences
        - Specify your target outcomes
        """
    )

# Launch the interface
iface.launch(share=True)
