# LLM Prompt Engineering Workbench

[![GitHub Pages Deploy](https://github.com/salah-sal/LLM-Prompt-Engineering-Workbench/actions/workflows/pages/pages-build-deployment/badge.svg)](https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to a user-friendly, browser-based workbench for crafting, testing, and iterating on prompts for Large Language Models (LLMs) like OpenAI and Cohere. The best part? **No server needed!**

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

1.  **Visit the Live Demo:** [https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/](https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/)
2.  **Wait for Initialization:** Pyodide (Python runtime) needs to load first (~10-20MB).
3.  **Configure:** Select Provider and Model.
4.  **Enter API Key:** Paste your API key. **Read the [security warning below](#security-warning-)**!
5.  **Craft Prompt:**
    *   Fill in System Prompt (optional).
    *   Write User Template (e.g., ```jinja
Analyze: {{ input }}
```).
    *   Provide JSON for variables (e.g., ```json
{ "input": "some text" }
```).
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

1.  **Clone:** ```bash
git clone https://github.com/salah-sal/LLM-Prompt-Engineering-Workbench.git
```
2.  **Navigate:** ```bash
cd LLM-Prompt-Engineering-Workbench
```
3.  **Serve Locally:** ```bash
python -m http.server 8000
``` (or any simple HTTP server)
4.  **Access:** Open ```
http://localhost:8000
``` in your web browser
5.  **Modify:** Edit HTML, CSS, [`js/main.js`](js/main.js), [`py/prompt_logic.py`](py/prompt_logic.py). Refresh browser (clear cache if needed).

## License

MIT License. See [LICENSE](LICENSE) file.

## For Junior Developers: Understanding Limitations & Possibilities

If you're new to this type of development, here's what you should know about the limitations and possibilities of this browser-based approach:

### Limitations

1. **Browser Environment Constraints:**
   * Limited access to system resources compared to native applications
   * No direct file system access (except through browser APIs like File System Access API)
   * Memory limitations based on the client's browser
   * No background processing when the browser tab is closed

2. **Pyodide Specific Limitations:**
   * Not all Python packages are compatible with Pyodide
   * Performance overhead compared to native Python
   * Limited threading capabilities
   * Package loading increases initial load time

3. **API Usage Considerations:**
   * Client-side API calls expose your API keys to the client
   * Rate limiting and quotas are tied to individual users
   * Network latency affects user experience

### Exploring Possibilities

To understand what's possible with this approach, check out these resources:

1. **Pyodide Documentation:**
   * [Pyodide Official Docs](https://pyodide.org/en/stable/) - Learn what Python can do in the browser
   * [Using Packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) - See which packages are supported

2. **WebAssembly Resources:**
   * [WebAssembly.org](https://webassembly.org/) - Understand the technology that makes this possible
   * [MDN WebAssembly Guide](https://developer.mozilla.org/en-US/docs/WebAssembly) - Mozilla's comprehensive guide

3. **Alternative Approaches:**
   * [Streamlit](https://streamlit.io/) - For when you need a Python backend
   * [Gradio](https://gradio.app/) - Another option for ML model interfaces
   * [Flask](https://flask.palletsprojects.com/) + [React](https://reactjs.org/) - For more complex applications

4. **Advanced Browser APIs:**
   * [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) - For background processing
   * [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API) - For client-side storage
   * [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) - For offline capabilities

By understanding these limitations and exploring these resources, you'll gain insight into what's possible with browser-based applications and when you might need to consider server-side components.

### Potential Enhancements for Contributors

If you're looking to contribute to this project, here are some ideas to consider:

1. **UI/UX Improvements:**
   * Add a dark mode theme
   * Implement responsive design for mobile devices
   * Create a more intuitive layout for prompt templates

2. **Feature Additions:**
   * Add support for more LLM providers
   * Implement prompt history and saving
   * Create a prompt template library
   * Add visualization tools for response analysis

3. **Performance Optimizations:**
   * Implement caching strategies
   * Optimize Pyodide loading time
   * Add progress indicators for long-running operations


## Acknowledgements

Powered by the awesome [Pyodide](https://pyodide.org/) project.
