import gradio as gr
from access_agent import search_with_gemini
from explain import simplify_with_claude

def accessbot_pipeline(user_query, language):
    raw_info = search_with_gemini(user_query)
    simplified = simplify_with_claude(raw_info, target_language=language.lower())
    return simplified

iface = gr.Interface(
    fn=accessbot_pipeline,
    inputs=[
        gr.Textbox(label="Ask your immigration or rights-related question:"),
        gr.Dropdown(["English", "Hindi", "Spanish", "French", "Bengali", "Tamil", "Telugu"], label="Choose Output Language")
    ],
    outputs="text",
    title="Legalance",
    description="I'm a Legalance Assistant that helps people with immigration queries and rights."
)

if __name__ == "__main__":
    iface.launch(share = True)
