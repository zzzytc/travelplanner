import gradio as gr 
import requests

FASTAPI_URL = "http://127.0.0.1:8000/travel-plan"

def ask_question(question):
    try:
        response = requests.post(FASTAPI_URL, json={"query": question})
        response.raise_for_status()
        data = response.json()
        answer = data.get("result", "No answer found.")
        return answer
    except Exception as e:
        return f"Error: {str(e)}", None

gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Ask a question", lines=2, placeholder="e.g. Give me a 5 days trip of tokyo. I go from Hong Kong"),
    outputs=gr.Textbox(label="Answer"),
    title="AI Travel Planner",
    description="AI Travel Planner to plan your trip",
).launch()


