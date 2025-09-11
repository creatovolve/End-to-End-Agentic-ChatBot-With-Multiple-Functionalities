import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

class DisplayResult:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message


    def display_result_on_ui(self):
        if self.usecase == "Basic Chatbot":
            for event in self.graph.stream({"messages":("user", self.user_message)}):
                print("\n\nevent_values :", event.values())
                for value in event.values():
                    print(f"val {value}")
                    with st.chat_message("user"):
                        st.write(self.user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif self.usecase == "Chatbot with Web":
            response = self.graph.invoke({"messages":[self.user_message]})
            for msg in response["messages"]:
                if type(msg)==HumanMessage:
                    with st.chat_message("user"):
                        st.write(msg.content)
                elif type(msg)==ToolMessage:
                    with st.chat_message("Tavily Web Search"):
                        st.write("Tool Call Start")
                        st.write(msg.content)
                        st.write("Tool Call End")
                elif type(msg) == AIMessage and msg.content:
                    with st.chat_message("Assistant"):
                        st.write(msg.content)
