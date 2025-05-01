import json
import js # Pyodide's JS interface
import micropip
import os # Import os module for path checking

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


# --- Prompter Class --- 
class Prompter:
    def __init__(self):
        # Initialize Jinja environment within the class if needed,
        # or keep it global if it's stateless and safe.
        self.jinja_env = Environment()
        print("Prompter instance initialized.")

    def build_prompt_data(self, system_prompt: str, user_template: str, template_vars: dict) -> dict:
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
            # Use the class's jinja_env
            template = self.jinja_env.from_string(user_template)
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

    def count_tokens(self, text: str, model_name: str) -> int:
        """
        Counts tokens in the given text using tiktoken for the specified model.

        Args:
            text: The text string to count tokens for.
            model_name: The name of the OpenAI/other model (e.g., 'gpt-4o').

        Returns:
            The number of tokens.
        """
        # --- REMOVED TEMPORARY DEBUGGING --- 

        try:
            # Get the appropriate encoding for the model
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback for models not directly mapped (like Cohere models)
            # Attempt to load the common cl100k_base encoding LOCALLY
            try:
                print(f"Warning: No specific tiktoken encoding for model '{model_name}'. Falling back to loading 'cl100k_base' locally. Accuracy may vary.")
                # Define the expected path within Pyodide's filesystem
                # Use an absolute path from Pyodide's perspective
                cl100k_base_path = "/home/pyodide/py/encodings/cl100k_base.tiktoken" 
                # Assuming the server root maps to /home/pyodide, adjust if deployed differently
                # Alternatively, construct relative path carefully if needed.

                # Explicitly check if the file exists in Pyodide's FS
                if not os.path.exists(cl100k_base_path):
                    # If check fails, try relative path as a backup
                    relative_path = "py/encodings/cl100k_base.tiktoken"
                    if not os.path.exists(relative_path):
                         raise FileNotFoundError(f"Neither absolute '{cl100k_base_path}' nor relative '{relative_path}' found.")
                    else:
                        cl100k_base_path = relative_path # Use the working relative path
                        print(f"Found encoding file at relative path: {cl100k_base_path}")
                else:
                     print(f"Found encoding file at absolute path: {cl100k_base_path}")

                # Load the BPE ranks from the local file
                print(f"Attempting to load BPE ranks from: {cl100k_base_path}")
                cl100k_base_ranks = load_tiktoken_bpe(cl100k_base_path)
                print("Successfully loaded BPE ranks.")
                
                # Create the Encoding object manually
                encoding = Encoding(
                    name="cl100k_base_local_fallback",
                    pat_str=r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]++|\s+(?!\S)|\s+",
                    mergeable_ranks=cl100k_base_ranks,
                    special_tokens={"<|endoftext|>": 100257}
                )
                print("Successfully created Encoding object from local file.")

            except FileNotFoundError as e:
                # This error means the file wasn't found by os.path.exists
                raise ValueError(f"Could not get tiktoken encoding for model '{model_name}'. Fallback failed: Local encoding file not found. Please ensure 'py/encodings/cl100k_base.tiktoken' exists in the project structure and was deployed. Details: {e}")
            except Exception as e:
                 # Catch other potential errors during local loading (e.g., parsing the file)
                 raise ValueError(f"Could not get tiktoken encoding for model '{model_name}'. Fallback failed during local load/parse from '{cl100k_base_path}': {e}")
        except Exception as e:
            # Catch errors during the initial encoding_for_model call
            raise ValueError(f"Tiktoken failed for model '{model_name}': {e}")

        token_integers = encoding.encode(text)
        return len(token_integers)

# --- Instantiate and Expose the Class Instance --- 
# Create an instance of the class
prompter_instance = Prompter()

# Expose the single instance to JavaScript
js.globals.set('prompterInstance', prompter_instance)

print("Prompter class instance created and exposed to JS as 'prompterInstance'.")