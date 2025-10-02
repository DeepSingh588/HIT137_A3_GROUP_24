# Aryan Rakhra: Initializing OOP Base Class for HD requirements.import time
from transformers import pipeline

# --- MULTIPLE DECORATORS: CUSTOM LOGGER ---
def time_and_log_activity(func):
    """
    A custom decorator to measure and log the execution time of any decorated method.
    This fulfills one part of the 'Multiple Decorators' requirement.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        # Execute the original function (e.g., load_pipeline or run_model)
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"[LOG: {func.__name__}]: Executed in {duration:.3f} seconds.")
        
        return result
    return wrapper

# --- BASE CLASS: ENCAPSULATION & POLYMORPHISM ---
class BaseModelManager:
    """
    The abstract base class for all AI model wrappers.
    
    OOP Focus:
    - ENCAPSULATION: Protects model details and the pipeline object.
    - POLYMORPHISM: Defines the abstract 'run_model' method.
    """
    def __init__(self, model_name, category, purpose):
        # ENCAPSULATION: Using private-convention attributes (single underscore)
        self._model_name = model_name
        self._category = category
        self._purpose = purpose
        self._pipeline_object = None # Protected: holds the Hugging Face pipeline

    # ENCAPSULATION: Public Getter Method
    def get_public_model_info(self):
        """Provides safe, read-only access to the private model details."""
        return {
            "Model Name": self._model_name,
            "Category": self._category,
            "Purpose": self._purpose
        }

    # ENCAPSULATION & MULTIPLE DECORATORS: Load Pipeline Method
    @time_and_log_activity # Custom Decorator
    def initialize_hf_pipeline(self, pipeline_task):
        """Loads the Hugging Face pipeline object for a given task."""
        try:
            self._pipeline_object = pipeline(pipeline_task, model=self._model_name)
            return True
        except Exception as e:
            print(f"FATAL ERROR loading {self._model_name}: {e}")
            self._pipeline_object = None
            return False

    # POLYMORPHISM: Abstract Method (MUST be overridden)
    def run_model(self, user_input_data):
        """
        ABSTRACT METHOD: Subclasses MUST implement their unique execution logic here.
        This enforces the Polymorphism contract across all model wrappers.
        """
        raise NotImplementedError("Concrete model class must implement 'run_model' logic.")