''' # Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://172.17.112.1:1234/v1", api_key="not-needed")

history = [
    {"role": "system", "content": "You are an intelligent market analysis assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

while True:
    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})

    '''
import streamlit as st
from openai import OpenAI
import docx

# Initialize the OpenAI client
client = OpenAI(base_url="http://172.17.112.1:1234/v1", api_key="not-needed")

# Function to convert Word doc to text
def docx_to_text(file):
    doc = docx.Document(file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# Function to get response from Phi-2 model
def get_phi2_response(question, history):
    history.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )
    return response.choices[0].message.content

# Main app function
def main():
    st.title("HR Onboarding Assistant")

    # Context-specific history for each tab
    history_tab1 = []
    history_tab2 = []
    history_tab3 = []

    # Creating tabs
    tab1, tab2, tab3 = st.tabs(["First 3 Days", "First Week", "3-Month Performance Review"])

    with tab1:
        st.header("Basic Policies and Recommendations for Your First 3 Days")
        uploaded_file = st.file_uploader("Upload HR Documents", key="file_uploader1")
        if uploaded_file:
            text = docx_to_text(uploaded_file)
            history_tab1.append({"role": "system", "content": text})
        user_question = st.text_input("Ask a question about your first 3 days:", key="question1")
        if user_question:
            answer = get_phi2_response(user_question, history_tab1)
            st.text_area("Assistant's Response:", value=answer, key="answer1")

    # Repeat similar structure for tab2 and tab3

if __name__ == "__main__":
    main()

