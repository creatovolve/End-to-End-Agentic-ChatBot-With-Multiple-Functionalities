import streamlit as st
from src.ChatBotWebSearch.ui.streamlitui.loadui import LoadUI
from src.ChatBotWebSearch.LLMS.groqllm import groqLLM
from src.ChatBotWebSearch.graph.graph_builder import GraphBuilder
from src.ChatBotWebSearch.ui.display_result import DisplayResult

def load_agenticai_app():
    ui = LoadUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Failed To Load UI Selections")
        return
    
    user_message = st.chat_input("Enter your message")

    if user_message:
        try:
            obj_groq_config = groqLLM(user_choices=user_input)
            model = obj_groq_config.get_llm_model()

            if not model:
                st.error("Model Could not be loaded")
                return
            usecase = user_input["selected_usecase"]
            
            if not usecase:
                st.error("No usecase selected")
                return
            graph_builder = GraphBuilder(model=model)
            try:
                graph = graph_builder.setup_graph(user_choices=user_input)
                DisplayResult(usecase=usecase, graph=graph, user_message=user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph loading failed : {e}")
                return

        except Exception as e:
            print("Exception occured while loading graph: {e}")