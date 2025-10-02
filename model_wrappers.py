# Rohanpreet Singh: Preparing Text & Image Model Wrappers. 
from oop_logic import BaseModelManager, time_and_log_activity
from PIL import Image # Required for ImageClassifier

# --- CONCRETE MODEL 1: TEXT GENERATOR (NLP) ---
class TextGenerator(BaseModelManager):
    """
    Wraps a sophisticated Text Generation model (Text Generation is NLP). 
    Demonstrates INHERITANCE and METHOD OVERRIDING.
    """
    def __init__(self):
        super().__init__(
            model_name="gpt2",
            category="Text Generation (NLP)",
            purpose="Generates creative or coherent text based on a user's prompt (Auto-Regressive)."
        )
        self.initialize_hf_pipeline("text-generation")

    # METHOD OVERRIDING (Polymorphism in action)
    @time_and_log_activity
    def run_model(self, input_text):
        """Executes the specific text generation task."""
        if not self._is_loaded:
            return "Execution failed: Model pipeline is not loaded."
        
        try:
            output = self._pipeline_object(
                input_text, 
                max_new_tokens=60, 
                num_return_sequences=1,
                truncation=True,
                do_sample=True,
                temperature=0.8
            )
            generated_text = output[0].get('generated_text', input_text)
            
            # Clean output by removing the prompt for a cleaner result
            return generated_text.replace(input_text, "").strip()

        except Exception as e:
            return f"Model execution error: {e}"


# --- CONCRETE MODEL 2: IMAGE CLASSIFIER (VISION) ---
class ImageClassifier(BaseModelManager):
    """
    Wraps the 'CLIP' model for zero-shot image classification (Vision).
    """
    def __init__(self):
        super().__init__(
            model_name="openai/clip-vit-base-patch32",
            category="Zero-Shot Image Classification (Vision)",
            purpose="Classifies an image against user-provided labels at runtime (Zero-Shot)."
        )
        self.initialize_hf_pipeline("zero-shot-image-classification")

    # METHOD OVERRIDING (Polymorphism in action)
    @time_and_log_activity
    def run_model(self, image_file_path):
        """Executes the specific image classification task."""
        if not self._is_loaded:
            return "Execution failed: Model pipeline is not loaded."

        try:
            image_data = Image.open(image_file_path)
            
            # Smart, specific labels for high-quality classification
            candidate_labels = [
                "a picture of a domestic cat", 
                "a photograph of an outdoor nature landscape", 
                "a close-up shot of a dog", 
                "a picture of a person driving a vehicle"
            ]
            
            output = self._pipeline_object(image_data, candidate_labels=candidate_labels)

            top_prediction = output[0]['label']
            confidence = f"{output[0]['score']:.2%}"
            
            return f"SUCCESS! The model is {confidence} confident the image is: {top_prediction}"

        except FileNotFoundError:
            return "Input Error: Image file not found. Please check the path."
        except Exception as e:
            return f"Model execution error: Ensure the path leads to a valid image. Details: {e}"