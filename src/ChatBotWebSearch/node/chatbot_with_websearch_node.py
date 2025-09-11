from src.ChatBotWebSearch.state.state import State

class ChatBotNodeWithWebSearch:
    def __init__(self, model):
        self.llm = model

    def process(self, state: State):
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response =  self.llm.invoke({"role":"user", "content": user_input})
        tool_response = f"Tool integration for {user_input} is :"

        return {"messages":[llm_response, tool_response]}
    
    def create_chabot(self, tools): 
        llm_with_tool = self.llm.bind_tools(tools)
        def chatbot_node(state: State):
            return {"messages": [llm_with_tool.invoke(state["messages"])]}
        
        return chatbot_node