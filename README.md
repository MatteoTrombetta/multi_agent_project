# VERSION 3.0
## 🌟 Core Features

* **Multi-Agent Orchestration:**
  * **Researcher Agent:** Gathers data using web search and internal tools (Function Calling).
  * **Analyzer Agent:** Validates data sufficiency using Structured Outputs (Pydantic).
  * **Writer Agent:** Compiles validated data into formal Markdown reports.
* **Enterprise Design Patterns:**
  * **Factory & Registry Pattern:** Decouples agent instantiation (`AgentFactory`), ensuring the system is strictly Open/Closed for future agent extensions.
  * **Singleton Pattern:** Manages the `VectorDBConnection` to ensure a single, memory-optimized instance of the embedding model and database across the application.
* **Local RAG (Company Knowledge):** Integrates **ChromaDB** to vectorize and retrieve internal company policies using OpenAI's `text-embedding-3-small`.
* **Human-in-the-Loop (Governance):** Utilizes LangGraph's `MemorySaver` and `interrupt_before` to pause execution, allowing for human review and approval of the data before the final report is generated.

## 🛠️ Tech Stack
* **Framework:** LangGraph, LangChain
* **LLM:** OpenAI (`gpt-4o-mini`)
* **Vector DB:** Chroma (Local)
* **Tools:** Tavily Search API, Local Semantic Search
* **Language:** Python 3.x

## 🚀 Quickstart

1. **Environment Setup:** Create a `.env` file with your `OPENAI_API_KEY` and `TAVILY_API_KEY`.
2. **Data Ingestion:** Run the seeding script to populate the local Vector DB with company policies.
   `python seed_db.py`
3. **Run the orchestrator**
`python main.py`
The system will prompt you for a query, search for data, analyze it, and pause for your manual approval before generating the final Markdown report in the /reports folder.



---


# VERSION 2.0
In this new branch we will focus on improving this project aiming to an enterprise-like structure.


## Project outline

Modular, stateful Multi-Agent workflow using Python and LangGraph to automate complex research tasks. The system features a cyclic state machine where a Researcher agent dynamically calls search tools (Tavily API), an Analyzer agent uses structured outputs (Pydantic) to evaluate data sufficiency (Reflection pattern), and a Writer agent drafts the final report. This project demonstrates practical expertise in modern LLM orchestration, Function Calling, and advanced prompt engineering beyond basic RAG implementations.


A single LLM easily lose context and hallucinates, also is not able to do structured auto-correction. A Multi-Agent System divides the tasks (Separation of Concerns) and uses shared memory (the State) in order to iterate until the final result is solid.


Un sistema "Multi-Agent" in Python, focalizzato sull'automazione della ricerca e dell'analisi dati (es. un Agente che cerca sul web tramite API, un Agente che analizza, un Agente che redige un report).

Il nostro sistema sarà un grafo diretto. Ogni agente sarà un nodo del grafo che riceve lo stato, compie un'azione (o usa un tool), aggiorna lo stato e lo passa al nodo successivo.

Struttura OOP:

Lo Stato (State): Un oggetto (spesso una TypedDict o un modello Pydantic) che viaggia tra gli agenti. Conterrà la query iniziale, la lista dei documenti trovati, le analisi intermedie e il report finale.

I Tool (Tools): Classi o funzioni isolate (es. WebSearchTool, FileParserTool). Devono avere firme chiare (type hinting) e docstring precise, perché l'LLM le leggerà per capire come usarle (Function Calling).

**Gli Agenti (Nodes)**:

- **ResearcherAgent**: Riceve la query, decide quali termini cercare, usa il tool di ricerca, estrapola i dati grezzi e li appende allo Stato.

- **AnalyzerAgent**: Legge i dati grezzi dallo Stato. Se sono sufficienti, ne estrae gli insight chiave. Se mancano pezzi, rimanda l'esecuzione al Researcher (ecco il loop ciclico!).

- **WriterAgent**: Prende gli insight e redige il report formale.

```
multi_agent_project/
├── .env                  # Variabili d'ambiente (API keys)
├── requirements.txt
├── main.py               # Entry point, inizializzazione del grafo
└── src/
    ├── __init__.py
    ├── state.py          # Definizione della struttura dello Stato
    ├── agents/           # Le classi per i vari agenti (Researcher, Analyzer, Writer)
    ├── tools/            # Strumenti esterni (ricerca web, I/O file)
    └── graph.py          # La logica di orchestrazione (nodi e archi di LangGraph)
```


Utilizzeremo gpt-4o-mini (economico e veloce) o gpt-4o per il function calling. OpenAI rimane lo standard industriale di riferimento per la stabilità degli agenti che devono chiamare funzioni.

Tavily API: Tavily è un motore di ricerca progettato specificamente per gli LLM e gli agenti AI. A differenza di una normale API di Google, non restituisce solo link, ma estrae già il contenuto rilevante dalle pagine in modo pulito.

Librerie Base (requirements.txt):
- langchain-core
- langchain-openai
- langgraph
- tavily-python
- python-dotenv
- pydantic (per la validazione rigorosa dei dati e del function calling)
- langchain