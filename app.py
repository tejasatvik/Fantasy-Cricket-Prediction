import gradio as gr
from cricket_api import get_current_matches, get_series, search_player
from rag_chain import build_qa_chain

# Helper to generate Gemini output for a given context and query
def generate_rag_response(context, query):
    try:
        qa_chain = build_qa_chain(context)
        return qa_chain.run(query)
    except Exception as e:
        return f"Gemini RAG failed: {str(e)}"

# Fetch enriched context from individual API call
def get_context_for_option(option, query):
    if option == "Current Matches":
        return get_current_matches()
    elif option == "Series Info":
        return get_series()
    elif option == "Search Player":
        return search_player(query)
    else:
        return get_current_matches() + "\n" + get_series()

# Chatbot logic with Gemini RAG response always

def chatbot_interface(option, query):
    context = get_context_for_option(option, query)
    if not context.strip():
        return "No data available."

    return generate_rag_response(context, query)

# Gradio UI
options = ["Current Matches", "Series Info", "Search Player", "Ask Anything (RAG)"]

demo = gr.Interface(
    fn=chatbot_interface,
    inputs=[
        gr.Dropdown(choices=options, label="Choose Action"),
        gr.Textbox(label="Enter your question (match, series, player)")
    ],
    outputs=gr.Textbox(label="Response"),
    title="🏏 Live Cricket Chatbot with Gemini",
    description="Get match updates, series info, or ask questions using real-time cricket data."
)

demo.launch()
