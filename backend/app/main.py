from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from git import Repo, GitCommandError
from .schema.user_request import UserStartRequest, UserChatRequest
import os
import shutil
from langchain_core.messages import SystemMessage
from .utils.ingest_repo import ingest_repo
import stat
from .utils.chat import SYSTEM_PROMPT,LLM_OUTPUT,format_file_symbol_table
from fastapi.middleware.cors import CORSMiddleware


CHAT_HISTORY=[]
FILE_SYMBOL_TABLE=[]
file_table_str=""
app = FastAPI(
    title="Codebase Chatbot API",
    description="Ask questions about code repos using RAG & Advanced LLM Reasoning.",
    version="1"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def on_rm_error(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
    func(path)

def cleanup():
    workspace_dir = os.path.abspath("workspace")
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir, onerror=on_rm_error)
    
    chroma_code_path = os.path.abspath("/chroma_code_db")
    chroma_noncode_path = os.path.abspath("/chroma_noncode_db")
    for path in [chroma_code_path, chroma_noncode_path]:
        if os.path.exists(path):
            shutil.rmtree(path, onerror=on_rm_error)



@app.get("/")
def home():
    return JSONResponse(status_code=200,content="API For Chatting With Any Public Github Repo!")


@app.get('/memory')
def memory():
    total, used, free = shutil.disk_usage("/")
    disk_info = {
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
    }

    workspace_dir = os.path.abspath("workspace")
    files = []
    for root, dirs, file_list in os.walk(workspace_dir):
        for file in file_list:
            file_path = os.path.join(root, file)
            files.append(file_path)

    return JSONResponse(
        status_code=200,
        content={
            "disk": disk_info,
            "files_in_workspace": files
        }
    )

    


@app.post("/init-chat")
def init(request : UserStartRequest):
    CHAT_HISTORY.clear()
    global FILE_SYMBOL_TABLE
    global file_table_str
    FILE_SYMBOL_TABLE.clear()
    CHAT_HISTORY.append(SystemMessage(content=SYSTEM_PROMPT))

    repo_url = request.repo_url
    repo_name = str(repo_url).rstrip("/").split("/")[-1]

    cleanup()

    workspace_dir = os.path.abspath("workspace")
    new_repo_path = os.path.join(workspace_dir, repo_name)

    try:
        Repo.clone_from(repo_url, new_repo_path, depth=1)
        FILE_SYMBOL_TABLE=ingest_repo(new_repo_path)
        file_table_str = format_file_symbol_table(FILE_SYMBOL_TABLE)
        return {
            "message": "Repository cloned successfully",
            "local_path": new_repo_path
        }
    except GitCommandError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Repository not found or private")
        elif "authentication" in str(e).lower():
            raise HTTPException(status_code=401, detail="Authentication failed")
        else:
            raise HTTPException(status_code=400, detail=f"Git error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
    

@app.post("/start-chat")
def start(request : UserChatRequest):
    query = request.query
    try:
        result = LLM_OUTPUT(query,CHAT_HISTORY,FILE_SYMBOL_TABLE,file_table_str)
        return {
            "message": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
   
