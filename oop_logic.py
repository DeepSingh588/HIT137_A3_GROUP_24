#Group No : 24
# Author : Aryan Rakhra: Initializing OOP Base Class for HD requirements
# Purpose: Defines the BaseModelManager (parent class) and the required Custom Decorator.

import time
from transformers import pipeline

# 1. CUSTOM LOGGER ---
def time_and_log_activity(func):
    """
    A custom decorator that measures the execution time of a function.
    This fulfills the 'Multiple Decorators' requirement when used on loading/running methods.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        # Execute the original function (e.g., run_model)
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        # Log the performance to the terminal console
        print(f"[MODEL LOG: {func.__name__}]: Execution time: {duration:.3f} seconds.")
        
        return result
    return wrapper

# --- BASE CLASS: INHERITANCE, ENCAPSULATION & POLYMORPHISM ---
class BaseModelManager:
    """
    The parent class for all AI model wrappers, defining the common interface.
    """
    def __init__(self, model_name, category, purpose):
        # ENCAPSULATION: These attributes are protected (single underscore convention).
        # They hold the model's core state (name, category, status)
        self._model_name = model_name
        self._category = category
        self._purpose = purpose
        self._pipeline_object = None # The Hugging Face pipeline object
        self._is_loaded = False

    # ENCAPSULATION: Public Getter Method
    def get_public_model_info(self):
        """
        Returns a dictionary of public information. This is the only controlled
        way for the GUI to safely read the model's protected state.
        """
        return {
            "Model Name": self._model_name,
            "Category": self._category,
            "Purpose": self._purpose,
            "Status": "Ready" if self._is_loaded else "Loading Error"
        }

    # Model Initialization Method (Uses the custom decorator)
    @time_and_log_activity
    def initialize_hf_pipeline(self, pipeline_task, **kwargs):
        """Loads the Hugging Face model pipeline."""
        try:
            # Load the model, specifying 'cpu' for wide compatibility
            self._pipeline_object = pipeline(pipeline_task, model=self._model_name, device="cpu", **kwargs)
            self._is_loaded = True
            return True
        except Exception as e:
            print(f"[FATAL ERROR]: Could not load model '{self._model_name}'. Error: {e}")
            self._pipeline_object = None
            self._is_loaded = False
            return False

    # POLYMORPHISM: Abstract Method
    def run_model(self, user_input_data):
        """
        ABSTRACT METHOD: Child classes MUST override this method.
        This rule enforces Polymorphism: the GUI calls 'run_model' regardless of the model type.
        """
        raise NotImplementedError("Concrete model class must implement its own 'run_model' logic.")