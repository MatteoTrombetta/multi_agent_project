from dotenv import load_dotenv
load_dotenv()

from src.graph import MultiAgentGraph

def main():
    print(f"""Welcome. This is a Multi-Agent Systems designed to write formal reports from web research through the three different AI agents: Researcher, Analyzer and Writer.""")
    print("Please tell what would you like your report to be written on:")
    
    user_query = input()
    initial_state = {
        "initial_query": user_query,
        "chronology": [],
        "is_sufficient": False
    }
    graph = MultiAgentGraph()
    result = graph.run(initial_state)

    print('\n', result["final_report"])

    #IMPROVE: Make the script able to save the created reports inside the 'reports' folder as .md files      


if __name__ == "__main__":
    main()