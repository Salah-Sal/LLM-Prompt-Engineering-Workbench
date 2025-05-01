# LLM Prompt Engineering Workbench

[![GitHub Pages Deploy](https://github.com/salah-sal/LLM-Prompt-Engineering-Workbench/actions/workflows/pages/pages-build-deployment/badge.svg)](https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A browser-based workbench for crafting, testing, and iterating on prompts for Large Language Models (LLMs) like OpenAI and Cohere. **No server needed!**

**[➡️ Live Demo Here!](https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/)**

## How it Works

This tool runs Python (specifically Jinja2 for templating) directly in your browser using [Pyodide](https://pyodide.org/) and WebAssembly. This means:
*   **No Backend:** Everything runs client-side.
*   **Static Deployment:** Can be hosted easily on platforms like GitHub Pages.
*   **Direct API Calls:** Your browser calls the LLM APIs directly using the key you provide.

## Features

*   Select LLM Provider (OpenAI, Cohere) and model.
*   Input System Prompt and User Message Template.
*   Use **Jinja2** templating with JSON variables.
*   View the rendered prompt.
*   Run prompts directly against LLM APIs.
*   View LLM responses or errors.

## Usage

1.  **Visit the Live Demo:** [https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/]
2.  **Wait for Initialization:** Pyodide (Python runtime) needs to load first (~10-20MB).
3.  **Configure:** Select Provider and Model.
4.  **Enter API Key:** Paste your API key. **Read the security warning below!**
5.  **Craft Prompt:**
    *   Fill in System Prompt (optional).
    *   Write User Template (e.g., `Analyze: {{ input }}`).
    *   Provide JSON for variables (e.g., `{ "input": "some text" }`).
6.  **Run Prompt:** Click the button to see the rendered prompt and the LLM response.

## !! Security Warning !! 💣

*   This tool uses your **LLM API key** directly from your browser to call the LLM API.
*   **It is NOT stored or sent anywhere else.**
*   **RISKS:** Pasting keys into web apps has risks (malicious extensions, etc.).
*   **CAUTION:** Use keys with limited permissions/spending caps. Use on trusted devices/networks. Clear the key field after use.

## Technology Stack

*   **Frontend:** HTML5, CSS3, Vanilla JavaScript
*   **Client-Side Python:** [Pyodide](https://pyodide.org/) + WebAssembly
*   **Python Libs:** [Jinja2](https://jinja.palletsprojects.com/)
*   **Deployment:** Static files on [GitHub Pages](https://pages.github.com/)

## Development

1.  **Clone:** `git clone https://github.com/salah-sal/LLM-Prompt-Engineering-Workbench.git`
2.  **Navigate:** `cd LLM-Prompt-Engineering-Workbench`
3.  **Serve Locally:** `python -m http.server 8000` (or any simple HTTP server)
4.  **Access:** Open `http://localhost:8000`
5.  **Modify:** Edit HTML, CSS, `js/main.js`, `py/prompt_logic.py`. Refresh browser (clear cache if needed).

## License

MIT License. See [LICENSE](LICENSE) file.

## Acknowledgements

Powered by the awesome [Pyodide](https://pyodide.org/) project.