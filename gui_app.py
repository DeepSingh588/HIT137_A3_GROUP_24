# Mehakpreet Singh: Starting GUI structure and explanation frames.
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk, constants
from model_wrappers import TextGenerator, ImageClassifier

# --- OOP ADVANCED: MIXIN CLASS FOR MULTIPLE INHERITANCE ---
class ExplanationMixin:
    """A Mixin class for handling scrollable text display within a frame."""
    def create_explanation_content(self, title, text_content, height=8):
        # Setup the title and the scrollable text area
        ttk.Label(self, text=title, font=('Arial', 11, 'bold')).pack(pady=(5, 2), anchor='w')
        
        # Use a Text widget for multi-line, scrollable, non-editable content
        self.text_widget = tk.Text(self, wrap=tk.WORD, height=height, width=55, state='normal', 
                                   font=('Courier New', 9), relief=tk.FLAT, borderwidth=0)
        self.text_widget.insert(tk.END, text_content)
        self.text_widget.config(state='disabled', background='#F8F9FA') # Light gray background
        self.text_widget.pack(fill='both', expand=True, padx=5, pady=5)

    def update_content(self, new_text):
        """Updates content dynamically (used for Model Info)."""
        self.text_widget.config(state='normal')
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, new_text)
        self.text_widget.config(state='disabled')

# --- WIDGET: FRAME FOR EXPLANATIONS (MULTIPLE INHERITANCE PROOF) ---
class ExplanationFrame(ttk.Frame, ExplanationMixin):
    """
    Frame demonstrating MULTIPLE INHERITANCE by inheriting from both ttk.Frame
    and ExplanationMixin.
    """
    def __init__(self, parent, title, text_content, **kwargs):
        # Initialize both parent classes
        ttk.Frame.__init__(self, parent, padding="10", **kwargs)
        # Call the mixin method to build the required text area
        ExplanationMixin.create_explanation_content(self, title, text_content)


# --- MAIN APPLICATION CLASS ---
class AIApplicationWindow(tk.Tk):
    """
    The main Tkinter application window with advanced layout management and theme.
    """
    def __init__(self):
        # Initialize with a modern theme 
        self.style = Style(theme='flatly') 
        super().__init__()
        
        self.title("HIT137 AI Model Integrator (HD Design)")
        self.geometry("1200x750") 
        
        # Instantiate the two AI model wrappers
        self.text_model = TextGenerator()
        self.image_model = ImageClassifier()

        self._create_main_layout()

    def _create_main_layout(self):
        """Sets up the primary two-panel layout using PanedWindow."""
        # PanedWindow for resizable sections (HD structure)
        main_pane = ttk.PanedWindow(self, orient=constants.HORIZONTAL)
        main_pane.pack(fill=constants.BOTH, expand=True, padx=15, pady=15)

        # Left side: Input, Output, and Control
        self.left_panel = ttk.Frame(main_pane, padding="10")
        # Right side: Information and Explanations
        self.right_panel = ttk.Frame(main_pane, padding="10")
        
        main_pane.add(self.left_panel, weight=1)
        main_pane.add(self.right_panel, weight=0) 

        self._populate_left_panel()
        self._populate_right_panel()

    def _populate_left_panel(self):
        """Creates the Model Selection, Input, and Output sections using LabelFrames."""
        
        # --- Model Selection and Control (Top Left) ---
        control_frame = ttk.LabelFrame(self.left_panel, text="1. Select AI Model", padding="20", style='primary.TLabelframe')
        control_frame.pack(fill=constants.X, pady=10)
        
        self.model_selection_var = tk.StringVar(value="Model 1: Text Generator")
        model_options = ["Model 1: Text Generator", "Model 2: Image Classifier"]
        
        ttk.Label(control_frame, text="Current Model:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        model_dropdown = ttk.Combobox(
            control_frame, 
            textvariable=self.model_selection_var, 
            values=model_options, 
            state="readonly", 
            width=35
        )
        model_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        self.model_selection_var.trace_add("write", lambda *args: self._update_model_info_display())
        control_frame.grid_columnconfigure(1, weight=1) 

        # --- Input Section (Middle Left) ---
        input_frame = ttk.LabelFrame(self.left_panel, text="2. User Input & Action", padding="20", style='info.TLabelframe')
        input_frame.pack(fill=constants.X, pady=10)

        ttk.Label(input_frame, text="Input Data:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(input_frame, text="Browse Image File", command=self._handle_browse_file, style='secondary.TButton').grid(row=0, column=2, padx=10, pady=5, sticky='e')
        
        # Central Run Button with distinct color
        ttk.Button(input_frame, text="3. RUN SELECTED MODEL", command=self._execute_selected_model, 
                   style='success.TButton', width=40).grid(row=1, column=1, columnspan=2, pady=15, sticky='w')
        
        input_frame.grid_columnconfigure(1, weight=1) 

        # --- Output Section (Bottom Left) ---
        output_frame = ttk.LabelFrame(self.left_panel, text="4. Model Output Display", padding="15", style='dark.TLabelframe')
        output_frame.pack(fill=constants.BOTH, expand=True, pady=10)
        
        # Use a higher contrast background for output
        self.output_text_display = tk.Text(output_frame, height=18, wrap=tk.WORD, state='disabled', font=('Consolas', 10), background='#212529', foreground='#20C997')
        self.output_text_display.pack(fill=constants.BOTH, expand=True, padx=5, pady=5)

    def _populate_right_panel(self):
        """Creates the two required Explanation sections (Right side)."""
        
        # --- Model Information Display (Updates dynamically, top right) ---
        self.model_info_frame = ExplanationFrame(self.right_panel, "Selected Model Information & Status", "", height=5, style='secondary.TLabelframe')
        self.model_info_frame.pack(fill=constants.X, pady=10)
        self._update_model_info_display() 
        
        # --- OOP Explanation Display (Static content, bottom right) ---
        oop_explanation_text = """
        • MULTIPLE INHERITANCE: Achieved by 'ExplanationFrame' inheriting from both 'ttk.Frame' (GUI structure) and 'ExplanationMixin' (text widget utility methods).
        
        • ENCAPSULATION: Enforced in 'BaseModelManager' by using protected attributes (e.g., '_model_name') which are ONLY accessed via the public getter method 'get_public_model_info()'.
        
        • POLYMORPHISM/METHOD OVERRIDING: 'BaseModelManager' defines the abstract 'run_model()' method. This is OVERRIDDEN with unique logic in both 'TextGenerator' and 'ImageClassifier' child classes, executed via a single button click.
        
        • MULTIPLE DECORATORS: The custom '@time_and_log_activity' decorator is applied to key methods (run_model, initialize_hf_pipeline) and runs alongside standard built-in decorators.
        
        • INHERITANCE: 'TextGenerator' and 'ImageClassifier' reuse common setup methods (like initialize_hf_pipeline) from the parent 'BaseModelManager'.
        """
        ExplanationFrame(self.right_panel, "OOP Concepts Explanation (HD Requirement)", oop_explanation_text, style='primary.TLabelframe').pack(fill=constants.BOTH, expand=True, pady=10)

    def _update_model_info_display(self):
        """Fetches info from the currently selected model and updates the GUI frame."""
        model = self.text_model if "Model 1" in self.model_selection_var.get() else self.image_model
            
        info = model.get_public_model_info()
        
        # Using .get() for robustness, as fixed earlier
        info_text = (
            f"• Model Name: {info.get('Model Name', 'N/A')}\n"
            f"• Category: {info.get('Category', 'N/A')}\n"
            f"• Purpose: {info.get('Purpose', 'N/A')}\n"
            f"• Status: {info.get('Status', 'Initialising...')}" 
        )
        
        self.model_info_frame.update_content(info_text)

    def _handle_browse_file(self):
        """Opens a file dialog for the Image Classifier model."""
        if "Model 2" in self.model_selection_var.get():
            filepath = filedialog.askopenfilename(
                title="Select Image File (JPG/PNG)",
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
            )
            if filepath:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, filepath)
        else:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, "Enter text prompt here...")

    def _execute_selected_model(self):
        """Determines which model to run and executes it."""
        input_data = self.input_entry.get()
        
        self.output_text_display.config(state='normal')
        self.output_text_display.delete(1.0, tk.END)
        self.output_text_display.insert(tk.END, "STATUS: Running AI model... (Check terminal for timing log)\n")
        self.update() 

        try:
            if "Model 1" in self.model_selection_var.get():
                if not input_data.strip():
                     final_result = "Input Error: Text prompt cannot be empty."
                else:
                    final_result = self.text_model.run_model(input_data)
            else:
                if not input_data.strip():
                    final_result = "Input Error: Must provide an image file path."
                else:
                    final_result = self.image_model.run_model(input_data)
            
            self.output_text_display.insert(tk.END, f"\n--- MODEL RESULT ---\n{final_result}")

        except Exception as e:
            self.output_text_display.insert(tk.END, f"\nCRITICAL APPLICATION ERROR: {e}")
            
        self.output_text_display.config(state='disabled')