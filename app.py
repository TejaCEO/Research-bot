import requests
import streamlit as st

def generate_text(prompt):
    """
    Uses Mistral's Codestral API to generate extended text based on the input.
    """
    api_key = "lHFGShbf91kbUx1vrJ2rqLDIaJnAhYBy"  # Replace with your actual Mistral API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "codestral-latest",  # Latest Codestral model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3500  # Adjust token limit based on needs
    }

    response = requests.post("https://codestral.mistral.ai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.set_page_config(page_title="TFI Research BOT", layout="centered")
    st.title("✍ TFI Research Bot")
    st.write("Enter a topic or text snippet.")
    
    user_input = st.text_area("Enter your text:")
    if st.button("Submit"):
        if user_input:
            with st.spinner("Generating text..."):
                prompt = f"Expand the following text to 30 lines with detailed explanation and ensure the content is unique and avoids plagiarism: {user_input}"
                extended_text = generate_text(prompt)
                st.text_area("Generated Text:", extended_text, height=400)
        else:
            st.warning("Please enter some text before generating.")

if __name__ == "__main__":
    main()