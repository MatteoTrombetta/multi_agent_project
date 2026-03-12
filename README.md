# Project outline
Un sistema "Multi-Agent" in Python, focalizzato sull'automazione della ricerca e dell'analisi dati (es. un Agente che cerca sul web tramite API, un Agente che analizza, un Agente che redige un report).

Il nostro sistema sarà un grafo diretto. Ogni agente sarà un nodo del grafo che riceve lo stato, compie un'azione (o usa un tool), aggiorna lo stato e lo passa al nodo successivo.

Concettualmente, avremo bisogno di questa struttura OOP:

Lo Stato (State): Un oggetto (spesso una TypedDict o un modello Pydantic) che viaggia tra gli agenti. Conterrà la query iniziale, la lista dei documenti trovati, le analisi intermedie e il report finale.

I Tool (Tools): Classi o funzioni isolate (es. WebSearchTool, FileParserTool). Devono avere firme chiare (type hinting) e docstring precise, perché l'LLM le leggerà per capire come usarle (Function Calling).

**Gli Agenti (Nodes)**:

- **ResearcherAgent**: Riceve la query, decide quali termini cercare, usa il tool di ricerca, estrapola i dati grezzi e li appende allo Stato.

- **AnalyzerAgent**: Legge i dati grezzi dallo Stato. Se sono sufficienti, ne estrae gli insight chiave. Se mancano pezzi, rimanda l'esecuzione al Researcher (ecco il loop ciclico!).

- **WriterAgent**: Prende gli insight e redige il report formale.


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

    Per iniziare a sporcarti le mani, prepara il tuo ambiente virtuale (venv o conda) e registra questi account gratuiti (o a basso costo) per recuperare le API key da inserire nel tuo file .env:

OpenAI API: Utilizzeremo gpt-4o-mini (economico e veloce) o gpt-4o per il function calling. OpenAI rimane lo standard industriale di riferimento per la stabilità degli agenti che devono chiamare funzioni.

Tavily API: Tavily è un motore di ricerca progettato specificamente per gli LLM e gli agenti AI. A differenza di una normale API di Google, non restituisce solo link, ma estrae già il contenuto rilevante dalle pagine in modo pulito. È perfetto per il nostro ResearcherAgent.

Librerie Base (requirements.txt):
- langchain-core
- langchain-openai
- langgraph
- tavily-python
- python-dotenv
- pydantic (per la validazione rigorosa dei dati e del function calling)