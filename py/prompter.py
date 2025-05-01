import json
import js # Pyodide's JS interface
import micropip
# import os # Removed: No longer needed for path checking

# --- Import dependencies ---
# We assume these were installed via micropip in main.js
try:
    from jinja2 import Environment, TemplateSyntaxError
    # import tiktoken # Removed
    # from tiktoken.load import load_tiktoken_bpe # Removed
    # from tiktoken import Encoding # Removed
except ImportError as e:
    # This error should ideally be caught during the micropip install phase in JS
    print(f"Error importing Python packages: {e}")
    # Optionally raise to signal failure back to JS, though JS checks might be better
    # raise

# --- Initialize Jinja ---
# Using a simple environment, no loaders needed for string templates
# jinja_env = Environment() # Moved into class __init__


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

    # --- Removed count_tokens method --- 
    # def count_tokens(self, text: str, model_name: str) -> int:
    #     """
    #     Counts tokens in the given text using tiktoken for the specified model.
    #     (Method content removed)
    #     """
    #     pass # Removed method body

# --- Instantiate the Class --- 
# Create an instance of the class
prompter_instance = Prompter()

# --- Expose the single instance to JavaScript (REMOVED) --- 

print("Prompter class instance created within Python scope.") 