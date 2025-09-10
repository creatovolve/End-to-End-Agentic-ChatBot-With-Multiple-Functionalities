import os
import streamlit as st
from langchain_groq import ChatGroq

class groqLLM:
    def __init__(self, user_choices):
        self.user_choices = user_choices

    def get_llm_model(self):
        try:
            groq_api_key = self.user_choices["GROQ_API_KEY"]
            groq_model = self.user_choices["selected_groq_model"]
            if groq_api_key=="" and os.environ["GROQ_API_KEY"]=="":
                st.error("Groq API key Must Be provided")
                return
            llm = ChatGroq(api_key=groq_api_key, model=groq_model)
        except Exception as e:
            raise ValueError("Error Occured: {e}")
        
        return llm

