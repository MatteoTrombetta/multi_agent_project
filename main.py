import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from src.graph import MultiAgentGraph


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

    config = {"configurable": {"thread_id": "1"}}

    partial_state = graph.run(initial_state, config)
    # Extracting last message from the analyzer
    analyzer_reasoning = partial_state["messages"][-1].content

    print("\n======================================================")
    print("> THE SYSTEM REQUIRES MANUAL APPROVATION TO CONTINUE.")
    print("> Data is considered sufficient by the Analyzer.")
    print("==================================================")
    print(f"\n> Analysis of the found information:\n{analyzer_reasoning}\n")

    check = False
    while not check:
        print(f"""> Do you want to continue by generating the report? (Y/N)""")
        approval = input().lower()
        if approval == "n":
            check = True
            print("> Permission denied. Process aborted by the user.")
            exit()
        elif approval == "y":
            check = True
            print("> Permission granted. Moving to the Writer...")
        else:
            print("> Input Error. Please provide a valid input (Y/N).")
    
    result = graph.run(None, config) # None as input state allows to continue execution from last thread_id used


    # File Saving Logic.
    # Make the script able to save the created reports inside the 'reports' folder as .md files      
    report_content = result["final_report"]

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Optional, to save better the names (needs improvement)
    safe_query = "_".join(user_query.split()[:3]).replace("?", "").replace("!", "").lower()
    filename = f"reports/report_{safe_query}_{timestamp}.md"

    with open(filename, "w", encoding='utf-8') as f:
        f.write(report_content)

    print(f"Finished! Report correctly saved in {filename}")

    # print('\n', result["final_report"])

    


if __name__ == "__main__":
    main()