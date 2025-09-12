from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self, llm):
        self.llm = llm
        self.tavily = TavilyClient()
        self.state = {}
    
    def fetch_news(self, state):
        frequency = state["messages"][0].content.lower()
        query = state["messages"][1].content.lower()
        self.state["frequency"] = frequency
        time_range_map = {'daily':'d', 'weekly':'w', 'monthly':'m'}
        days_map = {'daily':1, 'weekly':7, 'monthly':30}

        response = self.tavily.search(
            query = query,
            topic="news",
            time_range=time_range_map[frequency],
            include_answer='advanced',
            max_results=15,
            days=days_map[frequency]
        )        
        state["news_result"] = response.get('results', [])
        self.state['news_result']=state['news_result']
        return self.state

    def summarize_news(self, state):
        news_data = self.state['news_result']
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Summarize given news result"),
            ("user", "{articles}")]
        )
        state["summary"] = self.llm.invoke(prompt_template.format(articles = news_data)).content
        self.state["summary"] = state["summary"]
        return self.state
    
    def save_result(self, state):
        frequency = self.state["frequency"]
        summary = self.state["summary"]
        filename = f"./AINews/{frequency}_summary.md"

        with open(file=filename,mode="w") as f:
            f.write(summary)
        self.state["filename"] = filename
        
        return self.state
