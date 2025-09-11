import streamlit as st
import os

from src.ChatBotWebSearch.ui.uiconfigfile import Config

class LoadUI:
    def __init__(self):
        self.config = Config()
        self.user_choices = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title())
        st.header(self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            use_case_options = self.config.get_usecase_options()

            self.user_choices["selected_llm"]=st.selectbox("Select LLM", llm_options)
            
            if self.user_choices["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_choices["selected_groq_model"]=st.selectbox("Select Model", model_options)
                self.user_choices["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API Key", type='password')
            self.user_choices["selected_usecase"]=st.selectbox("Select Usecases", use_case_options)

            if self.user_choices["selected_usecase"] == "Chatbot with Web" or self.user_choices["selected_usecase"] == "AI News Summary":
                os.environ["TAVILY_API_KEY"] = self.user_choices["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY", type="password")

            if self.user_choices["selected_usecase"] == "AI News Summary":
                st.subheader("AI News Summary")

                with st.sidebar:
                    time_frame = st.selectbox("Select Time Frame", ["Daily", "Weekly", "Monthly"], index=0)

                if st.button("Fetch News"):
                    st.session_state.time_frame = time_frame
                    st.session_state.IsFetchButtonPressed = True 

        return self.user_choices