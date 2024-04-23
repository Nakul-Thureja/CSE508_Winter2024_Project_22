import streamlit as st
import openai
openai.api_key = ''

class ReviewChatbot:
    def __init__(self, reviews):
        self.reviews = reviews
        self.system_prompt = "You are a helpful assistant that summarizes and answers questions about product reviews."

    def get_contents(self, message, role):
        return [{"role": role, "content": content} for content in message]

    def chat(self, message):
        messages = self.get_contents(self.reviews, "user")
        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                *messages,
            ],
            max_tokens=150,
            temperature=0.7,
        )

        return response.choices[0].message['content']


st.markdown('### Group 22 IR Project')
st.markdown('#### E-Commerce Competitive Analysis System')
st.markdown('Review Analysis by ReviewBot')
params = st.query_params['param']
# param = params['param'] if 'param' in params else ' '
st.markdown(f'Ask a question about your product: {params}')

    # if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = [] 
f = open("reviews.txt", "r", encoding='utf-8')
reviews = f.read()
# file = open('reviews.txt', 'w').close()
#     with open('reviews.txt', 'w') as f:
#         for line in all_detail_product[max_index][5]:
#             f.write(f"{line}\n")

#     f.close()
reviews = reviews.split('\n')
f.close()
chatbot = ReviewChatbot('I love this product! It is the best thing I have ever bought. It is so useful and convenient. I would recommend it to everyone.')
# user_input = st.text_input('Enter your question:', key='user_input')
messages = st.container(height=600)
if prompt := st.chat_input("Say something"):
    messages.chat_message("user").write(prompt)
    # answer = chatbot.chat(prompt)
    # answer = "Chal oye"
    answer = reviews[0]
    messages.chat_message("assistant").write(f"ReviewBot: {answer}")