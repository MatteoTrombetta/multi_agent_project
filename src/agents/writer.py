from langchain_openai import ChatOpenAI
from src.state import State
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class WriterAgent:
    """Takes the insights and information provided by the researcher and
     checked by the analyzer, then creates the final formal report"""
    
    def __init__(self):
        
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4) # 0.4 for a little bit of fluent speaking

        # Could be improved (also with images, graphs maybe)
        self.agent_prompt = f"""You are an experienced report writer. You will write
        the report according to the information provided to you by a researcher and
        checked by an analyzer, following an initial query provided by the user. You will write your report in Markdown, clearly citing the
        sources and building it according to these sections:
        - Front matter: establishes the authority of the report, intended audience, and key concepts.
        - Body: short introduction, background, purpose or problem statement, evaluation, possible solution (if necessary).
        - Conclusion: finishes the body of the report by summarizing the major ideas of the report. While not the same as an executive summary, 
        it has a similar feel as it provides the report\'s key concepts. A conclusion should never introduce a fact or idea not presented earlier in the report.
        """

    def run(self, state: State) -> dict:
        
        context = [
            SystemMessage(content=self.agent_prompt),
            HumanMessage(content=f"Original query from the user: {state["initial_query"]}")
        ] + state["chronology"]

        answer = self.llm.invoke(context)
        return {
            "final_report": answer.content
        }