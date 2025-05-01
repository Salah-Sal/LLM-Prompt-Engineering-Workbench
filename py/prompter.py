import json
import js # Pyodide's JS interface
import micropip

# --- Import dependencies ---
# We assume these were installed via micropip in main.js
try:
    from jinja2 import Environment, TemplateSyntaxError
    import tiktoken
except ImportError as e:
    # This error should ideally be caught during the micropip install phase in JS
    print(f"Error importing Python packages: {e}")
    # Optionally raise to signal failure back to JS, though JS checks might be better
    # raise

# --- Initialize Jinja ---
# Using a simple environment, no loaders needed for string templates
jinja_env = Environment()

# --- Core Functions (to be called from JS) ---

def build_prompt_data(system_prompt: str, user_template: str, template_vars: dict) -> dict:
    """
    Renders the user template with variables and structures the prompt data.

    Args:
        system_prompt: The system prompt string.
        user_template: The Jinja2 template string for the user message.
        template_vars: A dictionary of variables for the template.

    Returns:
        A dictionary containing 'system_prompt' and 'final_user_message'.
    """
    final_user_message = ""
    try:
        template = jinja_env.from_string(user_template)
        final_user_message = template.render(template_vars)
        # print(f"Rendered message: {final_user_message}") # Debugging
    except TemplateSyntaxError as e:
        # Raise error clearly indicating Jinja syntax issue
        raise ValueError(f"Jinja template error: {e.message} at line {e.lineno}")
    except Exception as e:
        # Catch other potential rendering errors
        raise ValueError(f"Failed to render template: {e}")

    # Return structured data useful for API calls
    return {
        "system_prompt": system_prompt,
        "final_user_message": final_user_message
        # Could add formatted few-shot examples here in the future
    }

def count_tokens(text: str, model_name: str) -> int:
    """
    Counts tokens in the given text using tiktoken for the specified model.

    Args:
        text: The text string to count tokens for.
        model_name: The name of the OpenAI/other model (e.g., 'gpt-4o').

    Returns:
        The number of tokens.
    """
    try:
        # Get the appropriate encoding for the model
        # tiktoken should handle mapping model names to encodings
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fallback or attempt a default if model name isn't specific
        try:
            print(f"Warning: No specific encoding for model '{model_name}'. Falling back to 'cl100k_base'.")
            encoding = tiktoken.get_encoding("cl100k_base") # Common default
        except Exception as e:
             raise ValueError(f"Could not get tiktoken encoding for model '{model_name}' or fallback: {e}")
    except Exception as e:
        raise ValueError(f"Tiktoken failed for model '{model_name}': {e}")

    token_integers = encoding.encode(text)
    return len(token_integers)

# --- Expose functions to JavaScript ---
# Make Python functions callable from JS using pyodide.globals.get('function_name')
# js.globals.set('build_prompt_data', build_prompt_data)
# js.globals.set('count_tokens', count_tokens)

# No longer needed when importing the module via pyimport in JS

print("prompter.py loaded. Functions NOT exposed via js.globals for debugging.")