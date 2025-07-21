# Doc-RAG: Document Retrieval-Augmented Generation System

A comprehensive document retrieval and generation system that combines the power of large language models with vector-based document retrieval to provide accurate, context-aware responses.

## 🏗️ Architecture Overview

The system is built with a modular architecture consisting of six core components:

```
src/
├── llms/           # Language Model implementations
├── rag/            # Vector database and retrieval logic
├── agents/         # Conversational agents
├── services/       # Business logic services
├── prompts/        # Prompt templates and management
└── web/routers/    # API endpoints
```

## 🧠 Core Components

### 1. LLMs (Language Models)

The `src/llms/` directory contains implementations for different language model providers:

### 2. Vector Database

The `src/rag/` directory handles document indexing and retrieval:

- **ChromaDB Integration**: Primary vector database for storing embeddings
- **Document Indexing**: Automatic processing and embedding of documents
- **Similarity Search**: Efficient retrieval of relevant documents
- **Embedding Models**: Support for various embedding models (default: all-MiniLM-L6-v2)

### 3. Agents

The `src/agents/` directory contains conversational AI agents:

- **Chat Agent**: Main conversational interface
- **Agent State**: Manages conversation state and context
- **LangGraph Integration**: Workflow orchestration for complex interactions
- **Follow-up Questions**: Automatic generation of relevant follow-up questions

**Key Features:**
- Stateful conversations with memory
- Context-aware responses
- Integration with retrieval system
- Customizable conversation flows

### 4. Prompts

The `src/prompts/` directory contains the prompt template library:

- **Prompt Templates**: Structured templates for different conversation types
- **Prompt Management**: Centralized prompt configuration and versioning
- **Dynamic Prompts**: Context-aware prompt generation
- **Prompt Files**: YAML-based prompt definitions for easy modification

**Key Features:**
- Centralized prompt management
- Template-based prompt generation
- Easy prompt modification without code changes
- Version control for prompt iterations
- Context injection for personalized responses

### 5. Services

The `src/services/` directory provides business logic layer:

- **Index Service**: Document indexing and management
- **Search Service**: Query processing and retrieval
- **Chat Service**: Conversation management

**Key Features:**
- Clean separation of concerns
- Reusable business logic
- Error handling and validation

### 6. Routers (API Endpoints)

The `src/web/routers/` directory contains FastAPI route definitions:

- **Chat Router**: Conversation endpoints
- **Index Router**: Document management endpoints
- **Health Router**: System health checks


## ⚙️ Configuration

The system uses a YAML-based configuration file located at `src/config.yaml`. This file controls all aspects of the system:

### Configuration Structure

```yaml
app:
  name: doc-rag
  version: 0.1.0
  description: A document retrieval and generation system
  data_path: ./data                    # Data storage directory
  prompt_dir: ./src/prompts/prompt_files

# Language Model Settings
llm:
  open_ai_gpt4o:
    type: openai
    model_name: gpt-4o
    api_key: your_openai_api_key_here
  
  anthropic_claude:
    type: anthropic
    model_name: claude-3-5-sonnet-20240620
    api_key: your_anthropic_api_key_here

# Vector Database Settings
vector_db:
  chromadb:
    type: chromadb
    in_memory: false                   # Use persistent storage

# Chat Configuration
chat:
  llm: open_ai_gpt4o                  # Which LLM to use
  max_history: 5                      # Conversation history length
  generate_followup: true             # Auto-generate follow-up questions

# RAG Knowledge Settings
rag_knowledge:
  vector_db: chromadb                 # Which vector DB to use
  embedding_model: all-MiniLM-L6-v2   # Embedding model
  top_k: 4                           # Number of documents to retrieve

# FastAPI Server Settings
fast_api_server:
  host: 0.0.0.0
  port: 2000
  api:
    prefix: /api/v1
```

### Configuration Options

#### LLM Configuration
- **type**: Provider type (`openai`, `anthropic`)
- **model_name**: Specific model to use
- **api_key**: Authentication key for the provider

#### Vector Database Configuration
- **type**: Database type (`chromadb`, `pinecone`)
- **in_memory**: Whether to use in-memory storage (false for persistence)

#### RAG Configuration
- **embedding_model**: Model for generating embeddings
- **top_k**: Number of relevant documents to retrieve per query

#### Chat Configuration
- **llm**: Which LLM to use for chat, select one from the llm configuration
- **max_history**: Conversation history length
- **generate_followup**: Whether to auto-generate follow-up questions

#### Server Configuration
- **host**: Server bind address
- **port**: Server port
- **api.prefix**: API route prefix
- **data_path**: Data storage directory - Persistant vector database will be stored here
- **prompt_dir**: Prompt files directory - Prompt files for chat agent are stored here


## 🚀 Running the Application

### Prerequisites

1. **Python 3.11+**
2. **Dependencies**: Install from requirements.txt
3. **API Keys**: Configure OpenAI/Anthropic API keys in config.yaml

### Python Environment Setup

**⚠️ Important**: Always use a virtual environment to avoid conflicts with your system Python and other projects.

#### Option 1: Using venv (Built-in Python)

```bash
# Create virtual environment
python -m venv doc-rag-env

# Activate virtual environment
# On macOS/Linux:
source doc-rag-env/bin/activate

# On Windows:
# doc-rag-env\Scripts\activate

# Verify you're in the virtual environment
which python  # Should show path to virtual environment
python --version  # Should show Python 3.11+
```

#### Option 2: Using conda (Recommended)

```bash
# Create conda environment with Python 3.11
conda create -n doc-rag python=3.11 -y

# Activate conda environment
conda activate doc-rag

# Verify environment
which python  # Should show conda environment path
python --version  # Should show Python 3.11+
```

#### Option 3: Using pyenv + virtualenv

```bash
# Install Python 3.11 if not available
pyenv install 3.11.0

# Create virtual environment
pyenv virtualenv 3.11.0 doc-rag

# Activate environment
pyenv activate doc-rag

# Set local Python version for project
pyenv local doc-rag
```

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd doc-rag

# Ensure your virtual environment is activated
# (see Python Environment Setup above)

# Upgrade pip to latest version
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```


### Running with Python

Using the run_server script

```bash

# Run the server
python src/web/run_server.py
```


### Access Points

Once running, the application will be available at:

- **API Base**: http://localhost:2000
- **API Documentation**: http://localhost:2000/docs
- **Health Check**: http://localhost:2000/health
- **Chat Endpoint**: http://localhost:2000/api/v1/chat
- **Index Endpoint**: http://localhost:2000/api/v1/index


### Loading Knowledge into the System

**📚 Important**: Before calling any chat endpoint, you need to load documents into the vector database for retrieval.

#### Using the Index Script

The system includes a convenient `index_file.py` script to load documents:

```bash
# There are already some precreated files in the knowledge folder
# Copy your markdown files to the knowledge folder
cp /path/to/your/documents/*.md data/knowledge/

# Run the indexing script
python index_file.py
```

#### Supported Document Formats

Currently, the indexing script supports:
- **Markdown files (*.md)**: Documentation, notes, articles
- **Text files**: Can be easily extended for other formats


#### Manual Document Loading

You can also load documents using the "http://localhost:2000/api/v1/index" API endpoint once the server is running:

Example response:
{"num_chunks": 15}

#### Call Chat Endpoint

First create a new chat POST request: http://0.0.0.0:2000/api/v1/chat/new

This will return a chat id which you can use to call the chat message endpoint.

The chat message endpoint is a POST request: http://0.0.0.0:2000/api/v1/chat/message
Body is a json with the following format:

{
    "chat_id": "<chat_id>",
    "message": "<message>"
}

You can also view chat history by calling GET request: http://0.0.0.0:2000/api/v1/chat/history


## 📊 Evaluation and Experiments
The test_eval_rag.ipynb notebook can be used to evaluate the system.
It uses the test_eval_dataset.json file to evaluate the system.

Note that usinf the test_eval_rag.ipynb or the test_run_rag.ipynb will require langsmith keys to be set. 

You can do this by setting the following environment variables in a .env file:

```bash
# LangSmith API key (replace with your actual key)
LANGCHAIN_API_KEY=<your_langsmith_api_key>

# (Optional) Organization, if you have one
LANGCHAIN_PROJECT=doc-rag
LANGCHAIN_TRACING_V2=true
OPENAI_API_KEY=<your_openai_api_key>

```