# LLM Prompt Engineering Workbench

[![GitHub Pages Deploy](https://github.com/salah-sal/LLM-Prompt-Engineering-Workbench/actions/workflows/pages/pages-build-deployment/badge.svg)](https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A browser-based workbench for crafting, testing, analyzing, and iterating on prompts for Large Language Models (LLMs) like those from OpenAI and Cohere. **No server needed!**

**[➡️ Live Demo Here!](https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/)** ## The Core Idea: Serverless Python Power in the Browser! ✨

This project isn't just another LLM tool; it's a demonstration of a powerful development pattern gaining traction in 2025: **running sophisticated Python logic directly in the user's web browser using WebAssembly (WASM) and Pyodide.**

**The Problem We Usually Face:**

Traditionally, if you want to build a web tool that relies on Python's rich ecosystem (for data manipulation, complex logic, specific libraries), you need a backend server. This means:
* **Costs:** Hosting bills, database costs, server maintenance.
* **Maintenance:** Patching operating systems, updating Python dependencies, managing deployments, renewing domains/certificates.
* **Complexity:** Setting up APIs (like FastAPI/Flask), managing state, dealing with scalability.
* **Longevity Issues:** Free tiers disappear (remember Heroku?), servers need upgrades, and abandoned projects often break or get taken down due to cost/effort.

**The "Magic" We're Leveraging Here:**

1.  **WebAssembly (WASM):** Think of WASM as a universal, high-performance runtime built into modern web browsers. It allows code written in languages like C, C++, Rust, and others to run nearly natively within the browser sandbox.
2.  **Pyodide:** This incredible open-source project takes the standard CPython interpreter and compiles *it* (along with many popular scientific and general-purpose Python packages) to WebAssembly. **It literally puts Python, Pandas, NumPy, and much more *inside* the browser.** Furthermore, its `micropip` tool can often install pure-Python packages or pre-compiled WASM wheels directly from PyPI on demand, client-side!

**How This Project Uses It (The "Trick"):**

Instead of a server, we push the work to the client's browser:
* **Complex Templating:** We use the full power of Python's **Jinja2** library for sophisticated prompt templating, running entirely client-side via Pyodide.
* **Accurate Token Counting:** We use the official `tiktoken` library (compiled to WASM and loaded via `micropip`) to get precise, model-specific token counts *before* potentially wasting an API call. This isn't just a JavaScript approximation; it's the real deal.
* **Pythonic Logic:** All the logic for structuring prompts based on inputs, handling variables, and preparing data for the LLM API is written in clean, familiar Python.
* **Direct API Calls:** Standard browser `Workspace` calls are used to interact directly with the OpenAI/Cohere APIs from the client (using the user's provided key).

**Why YOU Should Consider This Approach:**

This isn't just a novelty; it offers tangible benefits, especially for tools, utilities, and demos you want to share freely and have last:
* ✅ **Zero Backend Cost & Hassle:** Deploy your tool as simple static files (HTML, CSS, JS, WASM) on free platforms like **GitHub Pages**, Netlify, Cloudflare Pages, etc. No servers to manage or pay for!
* ✅ **Built to Last:** Reduce dependency on specific server infrastructure or free tiers that might vanish. As long as browsers support WASM and static hosting exists, your tool has a high chance of remaining functional with minimal intervention. This follows the philosophy of building durable "gifts to the world."
* ✅ **Leverage the Python Ecosystem:** Don't rewrite complex logic in JavaScript if a solid Python library already exists and is compatible with Pyodide/WASM. Use the tools you know!
* ✅ **Enhanced Privacy (in some aspects):** For tasks that *don't* require external API calls (like data analysis, visualization, text manipulation), all processing can happen locally in the user's browser, meaning user data never leaves their machine. (Note: *This* specific project still calls external LLM APIs).
* ✅ **Perfect for:** Internal tools, open-source utilities, educational demos, documentation components, data visualization widgets, offline-capable apps (once assets are loaded).

**Think about it:** That useful script, that internal data tool, that cool demo for your library – could it run directly in the browser using this pattern? Give it a try!

## Features

* Select LLM Provider (OpenAI, Cohere) and specific model.
* Input System Prompt and User Message Template.
* Utilize **Jinja2** templating in the User Message with dynamic variables provided as JSON.
* Accurately **estimate token count** client-side using **`tiktoken`** via Pyodide/WASM.
* View the fully rendered prompt before sending.
* Run prompts directly against OpenAI/Cohere APIs from the browser.
* View the LLM response or detailed errors.
* Purely static deployment – no server backend required!

## Usage

1.  **Visit the Live Demo:** [https://salah-sal.github.io/LLM-Prompt-Engineering-Workbench/]
2.  **Wait for Initialization:** The first load downloads Pyodide (~10-20MB) and Python packages (~few MBs). Subsequent visits should be faster due to browser caching. You'll see status messages.
3.  **Configure:** Select the LLM Provider and Model you want to target.
4.  **Enter API Key:** Paste your API key for the selected provider into the designated field. ***Read the security warning below!***
5.  **Craft Your Prompt:**
    * Fill in the System Prompt (optional).
    * Write your User Message Template using Jinja2 syntax (e.g., `Analyze this: {{ input_text }}`).
    * Provide the values for your template variables as a valid JSON object in the "Template Variables" box (e.g., `{ "input_text": "Some text here" }`).
6.  **Estimate Tokens:** Click the "Estimate Tokens" button. This uses `tiktoken` in the browser to calculate the token count for the *rendered user message* based on the selected model.
7.  **Run Prompt:** Click "Run Prompt". The tool will:
    * Render the full prompt using Jinja2.
    * Display the rendered prompt structure.
    * Make a direct API call to the selected LLM provider using your API key.
    * Display the response or any errors.

## !! Security Warning !! 💣

* This tool requires you to **enter your LLM API key** directly into the web page.
* The key is used **ONLY** by the JavaScript code running locally in *your browser* to make a direct API call to the LLM provider (OpenAI/Cohere).
* **This key is NOT stored, logged, or sent anywhere else by this tool.**
* **HOWEVER:** Pasting sensitive credentials like API keys into web applications carries inherent risks. Potential risks include malicious browser extensions, cross-site scripting (XSS) vulnerabilities (though unlikely in a simple static site), or compromises on your local machine.
* **USE WITH CAUTION:**
    * Prefer using API keys with limited permissions and spending caps.
    * Do not use this tool on untrusted computers or networks.
    * Clear the API key field after use or close the browser tab.

## Technology Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
* **Client-Side Python:** [Pyodide](https://pyodide.org/) (CPython compiled to WebAssembly)
* **Python Libraries (via Pyodide/micropip):**
    * [Jinja2](https://jinja.palletsprojects.com/) (Templating)
    * [tiktoken](https://github.com/openai/tiktoken) (Token counting - requires WASM-compatible wheel)
* **Deployment:** Static Files on [GitHub Pages](https://pages.github.com/)

## Development

Want to tinker or contribute?

1.  **Clone:** `git clone https://github.com/salah-sal/LLM-Prompt-Engineering-Workbench.git`
2.  **Navigate:** `cd LLM-Prompt-Engineering-Workbench`
3.  **Serve Locally:** Due to browser security policies (CORS, WASM loading), you need a local HTTP server.
    ```bash
    python -m http.server 8000
    ```
4.  **Access:** Open `http://localhost:8000` in your browser.
5.  **Modify:** Edit the HTML, CSS, `js/main.js`, or `py/prompter.py` files. Changes should reflect after a browser refresh (you might need to clear cache sometimes, especially for JS/Python changes).

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project heavily relies on the amazing work done by the **Pyodide** team and contributors. Their efforts make running Python effectively in the browser possible.