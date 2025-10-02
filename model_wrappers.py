# Rohanpreet Singh: Preparing Text & Image Model Wrappers. 
from oop_logic import BaseModelManager, time_and_log_activity
from PIL import Image

class TextGenerator(BaseModelManager):
    def __init__(self):
        super().__init__(model_name="gpt2", category="Text Generation (NLP)", purpose="Generates text.")
        self.initialize_hf_pipeline("text-generation")

    @time_and_log_activity
    def run_model(self, input_text):
        # This is the correct text logic
        return f"Draft output for text: {input_text}" 

class ImageClassifier(BaseModelManager):
    def __init__(self):
        super().__init__(model_name="openai/clip-vit-base-patch32", category="Image Classification (Vision)", purpose="Classifies images.")
        self.initialize_hf_pipeline("zero-shot-image-classification")

    @time_and_log_activity
    def run_model(self, image_file_path):
        # PROBLEM: This model should handle an IMAGE, but the draft returns text logic.
        # This violates polymorphism's intended different behaviors.
        return f"Draft output: Image input received, but still running text logic on: {image_file_path}"