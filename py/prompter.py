import json
import js # Pyodide's JS interface
import micropip

# --- Import dependencies ---
# We assume these were installed via micropip in main.js
try:
    from jinja2 import Environment, TemplateSyntaxError
    import tiktoken
    from tiktoken.load import load_tiktoken_bpe # Import the BPE loader
    from tiktoken import Encoding # Import Encoding class
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
        # Fallback for models not directly mapped (like Cohere models)
        # Attempt to load the common cl100k_base encoding LOCALLY
        try:
            print(f"Warning: No specific tiktoken encoding for model '{model_name}'. Falling back to loading 'cl100k_base' locally. Accuracy may vary.")
            # Define the expected path within Pyodide's filesystem
            cl100k_base_path = "py/encodings/cl100k_base.tiktoken"
            
            # Load the BPE ranks from the local file
            cl100k_base_ranks = load_tiktoken_bpe(cl100k_base_path)
            
            # Create the Encoding object manually
            # You might need to specify special tokens depending on the model family
            # For a general fallback, we'll use common settings.
            encoding = Encoding(
                name="cl100k_base_local_fallback",
                pat_str=r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]++|\s+(?!\S)|\s+",
                mergeable_ranks=cl100k_base_ranks,
                special_tokens={"<|endoftext|>": 100257} # Example, adjust if needed
            )

        except FileNotFoundError:
             # This error means the user didn't download the file or place it correctly
            raise ValueError(f"Could not get tiktoken encoding for model '{model_name}'. Fallback failed: 'py/encodings/cl100k_base.tiktoken' not found. Please ensure the file is downloaded and placed correctly.")
        except Exception as e:
             # Catch other potential errors during local loading
             raise ValueError(f"Could not get tiktoken encoding for model '{model_name}'. Fallback failed during local load: {e}")
    except Exception as e:
        # Catch errors during the initial encoding_for_model call
        raise ValueError(f"Tiktoken failed for model '{model_name}': {e}")

    token_integers = encoding.encode(text)
    return len(token_integers)

# --- Expose functions to JavaScript ---
# Make Python functions callable from JS using pyodide.globals.get('function_name')
# js.globals.set('build_prompt_data', build_prompt_data)
# js.globals.set('count_tokens', count_tokens)

# No longer needed when importing the module via pyimport in JS

print("prompter.py loaded. Functions NOT exposed via js.globals for debugging.")