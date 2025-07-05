import chromadb
from sentence_transformers import SentenceTransformer

# Initialize model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create client only if needed
chroma_client = chromadb.PersistentClient(path="./function_db")
collection = chroma_client.get_or_create_collection("functions")

# Expanded function data
function_data = [
    {"name": "open_chrome", "description": "Launch Google Chrome browser web internet"},
    {"name": "open_calculator", "description": "Open calculator application math compute"},
    {"name": "open_notepad", "description": "Open Notepad text editor write edit"},
    {"name": "open_file_explorer", "description": "Open file manager explorer browse files"},
    {"name": "get_cpu_usage", "description": "CPU usage percentage processor performance"},
    {"name": "get_ram_usage", "description": "RAM memory usage percentage"},
    {"name": "get_system_uptime", "description": "System uptime boot time running"},
    {"name": "get_system_info", "description": "System information specs hardware details"},
    {"name": "run_shell_command", "description": "Execute shell command terminal cmd"},
    {"name": "kill_process", "description": "Kill terminate process application stop"},
    {"name": "list_running_processes", "description": "List running processes applications tasks"},
    {"name": "create_file", "description": "Create new file write save text"},
    {"name": "shutdown_system", "description": "Shutdown turn off computer system"},
    {"name": "restart_system", "description": "Restart reboot computer system"}
]


# Initialize database only if empty
def initialize_db():
    if collection.count() == 0:
        embeddings = model.encode([func["description"] for func in function_data]).tolist()
        collection.add(
            documents=[func["description"] for func in function_data],
            embeddings=embeddings,
            ids=[func["name"] for func in function_data]
        )


# Initialize on import
initialize_db()


def retrieve_function(query):
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    return results["ids"][0][0] if results["ids"] and results["ids"][0] else None


# Quick function mapping for exact matches (faster)
quick_map = {
    "chrome": "open_chrome",
    "calculator": "open_calculator",
    "notepad": "open_notepad",
    "explorer": "open_file_explorer",
    "cpu": "get_cpu_usage",
    "ram": "get_ram_usage",
    "memory": "get_ram_usage",
    "uptime": "get_system_uptime",
    "info": "get_system_info",
    "kill": "kill_process",
    "processes": "list_running_processes",
    "shutdown": "shutdown_system",
    "restart": "restart_system"
}


def get_function(query):
    # Try quick mapping first
    for key, func in quick_map.items():
        if key in query.lower():
            return func

    # Fall back to semantic search
    return retrieve_function(query)