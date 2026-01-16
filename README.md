# Delhi Career Navigator - Backend Setup

This guide explains how to run the backend, configure the AI model (Ollama or Gemini), and use mock mode for testing.

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) (installed and running)
- `pip` (Python package manager)

## 1. Setup & Installation

1.  **Navigate to the backend directory:**
    ```bash
    cd backend/delhi_navigator
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations (if needed):**
    ```bash
    python manage.py migrate
    ```

## 2. Running the Application

1.  **Start Ollama (if using local AI):**
    Open a terminal and run:
    ```bash
    ollama serve
    ```
    Make sure you have pulled a model (e.g., `ollama pull mistral-nemo`).

2.  **Start the Django Server:**
    ```bash
    python manage.py runserver
    ```
    The server will start at `http://127.0.0.1:8000/`.

## 3. Configuration (Changing Models & Providers)

All configurations are managed via the `.env` file located in `backend/delhi_navigator/.env`.

### A. Using Ollama (Local AI - Free)

To use a local Ollama model (recommended to save API quota):

1.  Open `.env`.
2.  Set `AI_PROVIDER` to `ollama`.
3.  Set `OLLAMA_MODEL` to your desired model tag (check available models with `ollama list`).

**Example `.env`:**
```ini
AI_PROVIDER=ollama
OLLAMA_MODEL=mistral-nemo:latest
# OLLAMA_MODEL=llama3:latest  <-- To switch to Llama 3
# OLLAMA_MODEL=mistral:latest <-- To switch to standard Mistral
```

### B. Using Google Gemini (Cloud AI)

To use Google's Gemini API:

1.  Open `.env`.
2.  Set `AI_PROVIDER` to `gemini`.
3.  Ensure `GEMINI_API_KEY` is set.

**Example `.env`:**
```ini
AI_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
```

## 4. Using Mock Mode (Testing)

Mock mode returns static/pre-defined data without calling any AI model. This is useful for UI testing or when you don't have internet/Ollama access.

1.  Open `.env`.
2.  Set `USE_MOCK_AI` to `true`.

**Example `.env`:**
```ini
USE_MOCK_AI=true
```

**Note:** When `USE_MOCK_AI` is true, the `AI_PROVIDER` setting is ignored.

## Summary of Config Options

| Setting | Value | Description |
| :--- | :--- | :--- |
| `AI_PROVIDER` | `ollama` | Uses local Ollama instance (requires `requests`). |
| | `gemini` | Uses Google Gemini API (requires `google-genai`). |
| `OLLAMA_MODEL` | `model_name` | Specific model to use (e.g., `mistral`, `llama3`). |
| `OLLAMA_BASE_URL`| `url` | URL for Ollama (default: `http://localhost:11434`). |
| `USE_MOCK_AI` | `true` | returns fake data (no AI call). |
| | `false` | Uses the configured `AI_PROVIDER`. |