from langgraph.graph import StateGraph, START, END
from src.ChatBotWebSearch.state.state import State
from src.ChatBotWebSearch.node.basic_chatbot_node import BasicChatbotNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
        return self.graph_builder.compile()
    
    def setup_graph(self, user_choices):
        if user_choices["selected_usecase"]=="Basic Chatbot":
            return self.basic_chatbot_build_graph()