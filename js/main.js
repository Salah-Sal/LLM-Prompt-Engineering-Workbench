// --- UI Elements ---
const providerSelect = document.getElementById('llm-provider');
const modelSelect = document.getElementById('llm-model');
const apiKeyInput = document.getElementById('api-key');
const systemPromptInput = document.getElementById('system-prompt');
const userTemplateInput = document.getElementById('user-template');
const templateVarsInput = document.getElementById('template-vars');
const estimateTokensBtn = document.getElementById('estimate-tokens-btn');
const runPromptBtn = document.getElementById('run-prompt-btn');
const tokenCountSpan = document.getElementById('token-count');
const renderedPromptOutput = document.getElementById('rendered-prompt-output');
const llmResponseOutput = document.getElementById('llm-response-output');
const errorOutput = document.getElementById('error-output');
const loadingIndicator = document.getElementById('loading-indicator');

// --- Global State ---
let pyodide = null;
let prompter = null; // Will hold Python module/functions

// --- Model Definitions (simplified) ---
const models = {
    openai: ["gpt-4o", "gpt-3.5-turbo"],
    cohere: ["command-r", "command-r-plus"] // Add more as needed
};

// --- Helper Functions ---
function showError(message) {
    errorOutput.textContent = `Error: ${message}`;
    errorOutput.classList.remove('hidden');
    llmResponseOutput.textContent = ''; // Clear previous response on new error
    loadingIndicator.classList.add('hidden');
}

function clearError() {
    errorOutput.classList.add('hidden');
    errorOutput.textContent = '';
}

function showLoading(isLoading) {
    loadingIndicator.classList.toggle('hidden', !isLoading);
    runPromptBtn.disabled = isLoading;
    estimateTokensBtn.disabled = isLoading;
}

function updateModelOptions() {
    const provider = providerSelect.value;
    modelSelect.innerHTML = ''; // Clear existing options
    models[provider].forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        option.textContent = `${model} (${provider})`;
        modelSelect.appendChild(option);
    });
}

// --- Pyodide Initialization ---
async function initializePyodide() {
    console.log("Loading Pyodide...");
    showError("Loading Pyodide runtime... This might take a moment.");
    try {
        pyodide = await loadPyodide();
        console.log("Pyodide loaded.");
        clearError();
        showError("Loading Python dependencies (jinja2, tiktoken)...");

        // Fetch and run the Python prompter code
        const pythonCodeResponse = await fetch('py/prompter.py');
        if (!pythonCodeResponse.ok) {
             throw new Error(`Failed to fetch prompter.py: ${pythonCodeResponse.statusText}`);
        }
        const pythonCode = await pythonCodeResponse.text();

        // Load packages and run the Python script. Use runPythonAsync for top-level await in Python.
        await pyodide.loadPackage(['micropip']);
        const micropip = pyodide.pyimport("micropip");
        await micropip.install(['jinja2', 'tiktoken']); // Ensure tiktoken wheel is available for Pyodide/WASM
        console.log("Python packages installed.");

        // Execute the Python script to define functions
        // Use pyodide.runPythonAsync if the Python script uses await (e.g., for async operations)
        // If prompter.py doesn't use await, runPython is fine.
        await pyodide.runPythonAsync(pythonCode);
        console.log("Python script executed.");

        // Access the Python functions exposed via `js.globals.set` in Python
        prompter = {
            build_prompt_data: pyodide.globals.get('build_prompt_data'),
            count_tokens: pyodide.globals.get('count_tokens')
        };
        
        // Add a check to ensure functions were actually exposed
        if (!prompter.build_prompt_data || !prompter.count_tokens) {
            throw new Error("Failed to access Python functions via js.globals. Check prompter.py.");
        }

        console.log("Python functions ready.");
        clearError();
        estimateTokensBtn.disabled = false;
        runPromptBtn.disabled = false;

    } catch (error) {
        console.error("Pyodide initialization failed:", error);
        showError(`Failed to initialize Python environment: ${error.message}. Try refreshing.`);
        estimateTokensBtn.disabled = true;
        runPromptBtn.disabled = true;
    }
}

// --- Core Logic Functions ---
async function handleEstimateTokens() {
    clearError();
    // Check if prompter object exists
    if (!prompter || !prompter.count_tokens) {
        showError("Python environment or count_tokens function not ready yet.");
        return;
    }

    const userTemplate = userTemplateInput.value;
    const templateVarsRaw = templateVarsInput.value;
    const modelName = modelSelect.value;
    let templateVars = {};

    try {
        templateVars = templateVarsRaw ? JSON.parse(templateVarsRaw) : {};
    } catch (e) {
        showError("Invalid JSON in Template Variables.");
        return;
    }

    try {
        // Call Python function to build just the user message part for token counting
        // NOTE: Adjust Python function if needed to just render the user part
        // Need to convert JS object to Python dict for functions accessed via globals
        const promptDataPy = await prompter.build_prompt_data(
            "", // No system prompt needed for this estimate
            userTemplate,
            pyodide.toPy(templateVars) // Convert JS object to Python dict
        );
        // Convert PyProxy Map to JS object 
        const promptData = promptDataPy.toJs({ dict_converter: Object.fromEntries });

        // Render the prompt for user visibility (even though only user message is counted accurately here)
        renderedPromptOutput.textContent = promptData.final_user_message;

        // Pass JS string directly is fine
        const tokenCount = await prompter.count_tokens(promptData.final_user_message, modelName);
        tokenCountSpan.textContent = `Token Count (User Message): ${tokenCount}`;

    } catch (error) {
        console.error("Token estimation error:", error);
        // Attempt to get Python error message if possible
        const pyError = error.message.includes('PythonError:') ? error.pythonError.message : error.message;
        showError(`Token estimation failed: ${pyError}`);
        tokenCountSpan.textContent = `Token Count: Error`;
    }
}

async function handleRunPrompt() {
    clearError();
    // Check if prompter object exists
    if (!prompter || !prompter.build_prompt_data) {
        showError("Python environment or build_prompt_data function not ready yet.");
        return;
    }

    const apiKey = apiKeyInput.value.trim();
    if (!apiKey) {
        showError("API Key is required.");
        return;
    }

    const provider = providerSelect.value;
    const modelName = modelSelect.value;
    const systemPrompt = systemPromptInput.value;
    const userTemplate = userTemplateInput.value;
    const templateVarsRaw = templateVarsInput.value;
    let templateVars = {};

     try {
        templateVars = templateVarsRaw ? JSON.parse(templateVarsRaw) : {};
    } catch (e) {
        showError("Invalid JSON in Template Variables.");
        return;
    }

    showLoading(true);
    llmResponseOutput.textContent = '';
    renderedPromptOutput.textContent = '';

    try {
        // 1. Build the structured prompt data using Python
        // Need to convert JS object to Python dict for functions accessed via globals
        const promptDataPy = await prompter.build_prompt_data(
            systemPrompt,
            userTemplate,
            pyodide.toPy(templateVars) // Convert JS object to Python dict
        );
        // Convert the PyProxy map back to a JS object
        const promptData = promptDataPy.toJs({ dict_converter: Object.fromEntries });

        renderedPromptOutput.textContent = `System: ${promptData.system_prompt}\nUser: ${promptData.final_user_message}`; // Display rendered parts

        // 2. Call the appropriate LLM API
        const response = await callLLM(apiKey, provider, modelName, promptData);
        llmResponseOutput.textContent = response;

    } catch (error) {
        console.error("Prompt execution error:", error);
         // Attempt to get Python error message if possible
        const pyError = error.message.includes('PythonError:') ? error.pythonError.message : error.message;
        showError(`Prompt execution failed: ${pyError}`);
        llmResponseOutput.textContent = ''; // Clear any partial response
    } finally {
        showLoading(false);
    }
}


// --- API Call Function ---
async function callLLM(apiKey, provider, modelName, promptData) {
    let endpoint = '';
    let headers = {
        'Content-Type': 'application/json',
    };
    let body = {};

    if (provider === 'openai') {
        endpoint = 'https://api.openai.com/v1/chat/completions';
        headers['Authorization'] = `Bearer ${apiKey}`;
        body = {
            model: modelName,
            messages: [
                { role: "system", content: promptData.system_prompt },
                { role: "user", content: promptData.final_user_message }
                // Add logic for history/few-shot examples here if implemented
            ],
            // Add temperature, max_tokens etc. here from UI if implemented
        };
    } else if (provider === 'cohere') {
        endpoint = 'https://api.cohere.ai/v1/chat'; // Verify Cohere API endpoint
         headers['Authorization'] = `Bearer ${apiKey}`;
         headers['Cohere-Version'] = '2022-12-06'; // Check for latest Cohere API version header
         body = {
             model: modelName,
             chat_history: promptData.system_prompt ? [{ role: "SYSTEM", message: promptData.system_prompt }] : [],
             message: promptData.final_user_message,
             // Add connectors, temperature etc. here
         };
    } else {
        throw new Error(`Unsupported provider: ${provider}`);
    }

    console.log("Calling API:", endpoint, "with model:", modelName);
    // console.log("Request Body:", JSON.stringify(body)); // Be careful logging potentially sensitive prompt data

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Failed to parse error response' }));
        console.error("API Error Response:", errorData);
        throw new Error(`API request failed: ${response.status} ${response.statusText} - ${errorData.error?.message || errorData.message || 'Unknown API error'}`);
    }

    const data = await response.json();
    console.log("API Success Response:", data);

    // Extract the response text based on provider structure
    if (provider === 'openai') {
        return data.choices[0]?.message?.content || 'No content received';
    } else if (provider === 'cohere') {
         return data.text || 'No content received'; // Verify Cohere response structure
    } else {
        return JSON.stringify(data); // Fallback
    }
}


// --- Event Listeners ---
providerSelect.addEventListener('change', updateModelOptions);
estimateTokensBtn.addEventListener('click', handleEstimateTokens);
runPromptBtn.addEventListener('click', handleRunPrompt);

// --- Initial Setup ---
document.addEventListener('DOMContentLoaded', () => {
    updateModelOptions(); // Populate models for the default provider
    estimateTokensBtn.disabled = true; // Disabled until Pyodide loads
    runPromptBtn.disabled = true;
    initializePyodide();
});