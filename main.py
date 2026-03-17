import warnings
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from src.graph import MultiAgentGraph

warnings.filterwarnings("ignore")

def main():
    print(f"""Welcome. This is a Multi-Agent Systems designed to write formal reports from web research through the three different AI agents: Researcher, Analyzer and Writer.""")
    print("Please tell what would you like your report to be written on:")
    
    user_query = input()
    initial_state = {
        "initial_query": user_query,
        "messages": [],
        "is_sufficient": False
    }
    graph = MultiAgentGraph()
    result = graph.run(initial_state)


    # File Saving Logic
    # Make the script able to save the created reports inside the 'reports' folder as .md files      
    report_content = result["final_report"]

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Optional, to save better the names
    safe_query = "_".join(user_query.split()[:3]).replace("?", "").replace("!", "").lower()
    filename = f"reports/report_{safe_query}_{timestamp}.md"

    with open(filename, "w", encoding='utf-8') as f:
        f.write(report_content)

    print(f"Finished! Report correctly saved in {filename}")

    # print('\n', result["final_report"])

    


if __name__ == "__main__":
    main()