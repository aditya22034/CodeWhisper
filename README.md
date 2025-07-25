# CodeWhisper 🧠💬

CodeWhisper is a conversational AI tool that allows users to interact with GitHub repositories using natural language. It's designed to help you explore large codebases faster, understand complex logic, and get answers to your questions without manually digging through files.

## ✨ Overview

Ever felt lost in a new or massive codebase? CodeWhisper is your smart companion for navigating code. By leveraging the power of Large Language Models (LLMs), it provides a chat interface to "talk" to a repository. Ask questions, get summaries, and find code snippets in a flash.

Why it’s useful:
- **Explore large codebases faster:** No need to `grep` or `find` your way around. Just ask!
- **Understand complex code:** Get explanations for functions, classes, or entire files.
- **Onboard new developers:** Helps new team members get up to speed quickly.

## 🧰 Tech Stack

- **Frontend:** React.js for a clean, modern chat UI.
- **Backend:** LangChain orchestrates the logic between the user, the LLM, and the vector store.
- **LLM:** GPT-4.1 nano provides the conversational intelligence.
- **RAG System:** A dynamic Retrieval-Augmented Generation (RAG) system to fetch relevant code context.

## 🔍 Key Features

- **🧠 Intelligent Query Understanding:** Asks smart questions to understand the repo's structure and code.
- **📂 Context-Aware Response Generation:** Uses a dynamic RAG system to provide answers based on the most relevant parts of the codebase.
- **⚡ Fast Repo Exploration:** Quickly get information about any part of the repository.
- **💬 Clean, Modern Chat UI:** A simple and intuitive interface for interacting with the AI.

## 🚀 How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/CodeWhisper.git
cd CodeWhisper
```

### 2. Set Up Backend
```bash
cd backend
pip install -r requirements.txt
# Set up your OpenAI API key
export OPENAI_API_KEY='your-api-key'
# Run the backend server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Set Up Frontend
```bash
cd ../frontend
npm install
# Add your backend API URL to .env
echo "VITE_API_URL=http://localhost:8000" > .env
# Run the frontend development server
npm run dev
```

## ⚙️ Architecture

CodeWhisper is built with a decoupled frontend and backend:
- **Frontend:** A React application that provides the chat interface.
- **Backend:** A FastAPI server that handles user queries.
- **LLM:** GPT-4.1 nano is used for generating responses.
- **Vector Store:** ChromaDB is used to store vector representations of the codebase for efficient retrieval.
- **RAG System:** LangChain's RAG implementation connects the LLM with the vector store to provide context-aware answers.

## 📸 Screenshots

*(placeholder for a GIF of the chat interface in action)*

![CodeWhisper UI](https://i.imgur.com/placeholder.png)

## 📦 Dependencies

- **LangChain:** For building the core RAG pipeline.
- **ChromaDB:** As the vector store for a fast and efficient similarity search.
- **OpenAI API:** To access the GPT-4.1 nano model.
- **React.js:** For the frontend application.
- **FastAPI:** For the backend server.

## 🤖 Example Queries

Here are some questions you can ask CodeWhisper:
- "What does `train.py` do?"
- "Show me all functions that use `load_model()`"
- "Explain the `forward` method in the `ResNet` class."
- "Where is the database connection configured?"

---

Happy coding! 🚀
