import requests
import streamlit as st
import streamlit.components.v1 as components
import json
import re

# Function to generate text using Codestral API
def generate_text(prompt):
    api_key = "lHFGShbf91kbUx1vrJ2rqLDIaJnAhYBy"  # Replace with your actual API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "codestral-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3500
    }
    response = requests.post("https://codestral.mistral.ai/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def strip_markdown(text):
    # Remove markdown header markers from the start of lines
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove bold formatting markers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove italic formatting markers
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove underscores used for emphasis
    text = re.sub(r'__(.*?)__', r'\1', text)
    # Remove inline code markers
    text = re.sub(r'`(.*?)`', r'\1', text)
    return text

def clipboard_component(text):
    # Use json.dumps to safely escape the text for embedding in HTML
    escaped_text = json.dumps(text)
    html_code = f"""
    <html>
      <head>
        <meta charset="UTF-8">
        <style>
          #copy-button {{
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
          }}
        </style>
      </head>
      <body>
        <button id="copy-button">Copy to Clipboard</button>
        <textarea id="copy-text" style="position: absolute; left: -9999px;">{text}</textarea>
        <script>
          const copyButton = document.getElementById("copy-button");
          copyButton.addEventListener("click", function() {{
            const textArea = document.getElementById("copy-text");
            textArea.select();
            document.execCommand("copy");
            copyButton.innerText = "Copied!";
            setTimeout(() => {{
              copyButton.innerText = "Copy to Clipboard";
            }}, 2000);
          }});
        </script>
      </body>
    </html>
    """
    # Render the HTML component (adjust the height if needed)
    components.html(html_code, height=120)

def main():
    st.set_page_config(page_title="TFI Research BOT", layout="centered")
    st.title("✍ TFI Research Bot")
    st.write("Enter a topic or text snippet.")
    
    # Initialize session state for generated text if not already set
    if "plain_text" not in st.session_state:
        st.session_state.plain_text = ""
    
    user_input = st.text_area("Enter your text:")

    # Create two columns: one for Submit and one for the Copy button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit"):
            if user_input:
                with st.spinner("Generating text..."):
                    prompt = (f"Expand the following text to 30 lines with detailed explanation and ensure "
                              f"the content is unique and avoids plagiarism: {user_input}")
                    extended_text = generate_text(prompt)
                    plain_text = strip_markdown(extended_text)
                    st.session_state.plain_text = plain_text  # store for later use
            else:
                st.warning("Please enter some text before generating.")
    with col2:
        # Only show the copy button if generated text exists
        if st.session_state.plain_text:
            clipboard_component(st.session_state.plain_text)
    
    # Display the generated text below the buttons if available
    if st.session_state.plain_text:
        st.text_area("Generated Text:", st.session_state.plain_text, height=400)

if __name__ == "__main__":
    main()

