from langgraph.graph import StateGraph, START, END
from src.ChatBotWebSearch.state.state import State
from src.ChatBotWebSearch.node.basic_chatbot_node import BasicChatbotNode
from src.ChatBotWebSearch.node.chatbot_with_websearch_node import ChatBotNodeWithWebSearch
from src.ChatBotWebSearch.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from src.ChatBotWebSearch.node.chatbot_with_websearch_node import ChatBotNodeWithWebSearch
from src.ChatBotWebSearch.node.ai_news_node import AINewsNode

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
    
    def websearch_chatbot_build_graph(self):
        llm = self.llm
        self.chatbot_node_with_web_search = ChatBotNodeWithWebSearch(self.llm)

        tools = get_tools()
        tool_node = create_tool_node(tools=tools)
        
        self.graph_builder.add_node("chatbot", self.chatbot_node_with_web_search.create_chabot(tools=tools))
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

        self.graph_builder.add_edge("chatbot", END)
        
        return self.graph_builder.compile()
    

    def news_summarizer_node(self):
        ai_news_node = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news )
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")

        self.graph_builder.add_edge("save_result", END)

        return self.graph_builder.compile()
        
    
    def setup_graph(self, user_choices):
        if user_choices["selected_usecase"]=="Basic Chatbot":
            return self.basic_chatbot_build_graph()
        
        elif user_choices["selected_usecase"]=="Chatbot with Web":
            return self.websearch_chatbot_build_graph()
        
        elif user_choices["selected_usecase"]=="AI News Summary":
            return self.news_summarizer_node()