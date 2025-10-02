#Group No : 24
# Author: Rohanpreet Singh: Preparing Text & Image Model Wrappers. 
# Purpose: Implement the two specific AI models (Text and Vision) by inheriting from BaseModelManager.

from oop_logic import BaseModelManager, time_and_log_activity
from PIL import Image # Used for handling image files for the Vision model

# MODEL 1: TEXT GENERATOR (NLP Category) ---
class TextGenerator(BaseModelManager):
    """
    Handles text generation, inheriting setup logic and overriding the run method.
    """
    def __init__(self):
        # INHERITANCE: Calls the parent constructor
        super().__init__(
            model_name="gpt2", # Small, fast model for creative text generation
            category="Text Generation (NLP)",
            purpose="Generates coherent text to complete a short prompt or idea."
        )
        # INHERITANCE: Uses the inherited loading method
        self.initialize_hf_pipeline("text-generation")

    # METHOD OVERRIDING (Polymorphism)
    @time_and_log_activity
    def run_model(self, input_text):
        """Executes the specific text generation task."""
        if not self._is_loaded:
            return "Execution failed: Text model is not loaded correctly."
        
        try:
            output = self._pipeline_object(
                input_text, 
                max_new_tokens=60, 
                num_return_sequences=1,
                truncation=True, 
                do_sample=True,
                temperature=0.7 
            )
            generated_text = output[0].get('generated_text', "Error generating text.")
            
            # Remove the original input text for a cleaner output display
            return generated_text.replace(input_text, "").strip()

        except Exception as e:
            return f"Model execution error: Check if the prompt format is correct. Details: {e}"


#  MODEL 2: IMAGE CLASSIFIER (Vision Category) ---
class ImageClassifier(BaseModelManager):
    """
    Handles zero-shot image classification.
    """
    def __init__(self):
        # INHERITANCE: Calls the parent constructor
        super().__init__(
            model_name="openai/clip-vit-base-patch32", # CLIP model for zero-shot classification
            category="Zero-Shot Image Classification (Vision)",
            purpose="Classifies an image against a user-defined list of potential labels."
        )
        # INHERITANCE: Uses the inherited loading method
        self.initialize_hf_pipeline("zero-shot-image-classification")

    # METHOD OVERRIDING (Polymorphism)
    @time_and_log_activity
    def run_model(self, image_file_path):
        """Executes the specific image classification task, requiring a file path."""
        if not self._is_loaded:
            return "Execution failed: Image model is not loaded correctly."

        try:
            # 1. Open the image file using the PIL library
            image_data = Image.open(image_file_path)
            
            # 2. Define the candidate labels (the options the model chooses from)
            candidate_labels = [
                "a picture of a domestic cat", 
                "a photograph of a dog", 
                "a beautiful outdoor landscape", 
                "a building or structure",
                "a drawing or cartoon"
            ]
            
            # 3. Run the classification pipeline
            output = self._pipeline_object(image_data, candidate_labels=candidate_labels)

            # 4. Format the top result
            top_prediction = output[0]['label']
            confidence = f"{output[0]['score']:.2%}" 
            
            return f"CLASSIFICATION SUCCESS!\n\nConfidence: {confidence}\nModel's Top Prediction: {top_prediction}"

        except FileNotFoundError:
            return "Input Error: Image file not found. Please check the file path entered."
        except Exception as e:
            return f"Model execution error: Ensure the file is a valid image (JPG/PNG). Details: {e}"