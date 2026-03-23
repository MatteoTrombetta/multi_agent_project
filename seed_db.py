from dotenv import load_dotenv
from langchain_core.documents import Document
from src.db_connection import VectorDBConnection

# necessary to perform authentication in OpenAIEmbeddings inside VectorDBConnection
load_dotenv()

policies: list[Document] = [
    Document(page_content="Every task must always have one clearly assigned owner who is responsible for its progress and completion. If a task is created without an owner, responsibility should be assigned as soon as possible, and unresolved ownership should be escalated."),
    Document(page_content="All tasks should be completed within their defined deadlines. If a task risks missing its deadline or becomes overdue, it should be flagged, prioritized, and escalated to ensure timely resolution."),
    Document(page_content="All incoming and processed data must be complete, accurate, and aligned with expected formats. Any data that appears incorrect, incomplete, or inconsistent should be identified, rejected, or corrected before being used in further steps."),
    Document(page_content="A process should only be considered complete when all required tasks have been fully executed and verified. Upon completion, a record of actions, decisions, and responsible parties should be documented for traceability."),
]

connection_db = VectorDBConnection()
db = connection_db.get_db()
db.add_documents(documents=policies)

