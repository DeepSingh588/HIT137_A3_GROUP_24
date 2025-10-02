#Group No : 24
#Author: Mehakpreet Singh: Starting GUI structure and explanation frames.
#Purpose: Create the advanced, professional GUI interface using ttkbootstrap, including Multiple Inheritance.

import tkinter as tk
from tkinter import filedialog
from model_wrappers import TextGenerator, ImageClassifier
from ttkbootstrap import Style, ttk, constants

# --- MIXIN CLASS FOR MULTIPLE INHERITANCE ---
class ExplanationMixin:
    """
    A utility class (Mixin) providing methods for creating and managing a styled text display.
    """
    def create_explanation_content(self, title, text_content, height=8):
        # Create a title label for the frame
        ttk.Label(self, text=title, font=('Arial', 11, 'bold')).pack(pady=(5, 2), anchor='w')
        
        # Text widget for multi-line display
        self.text_widget = tk.Text(self, wrap=tk.WORD, height=height, width=55, state='normal', 
                                   font=('Courier New', 9), relief=tk.FLAT, borderwidth=0)
        self.text_widget.insert(tk.END, text_content)
        self.text_widget.config(state='disabled', background='#F8F9FA') # Styled background
        self.text_widget.pack(fill='both', expand=True, padx=5, pady=5)

    def update_content(self, new_text):
        """Allows safe, dynamic update of the text widget content (used for Model Info)."""
        self.text_widget.config(state='normal')
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, new_text)
        self.text_widget.config(state='disabled')

#  MULTIPLE INHERITANCE ---
class ExplanationFrame(ttk.Frame, ExplanationMixin):
    """
    This widget inherits from two distinct parents:
    1. ttk.Frame: Provides the base GUI container functionality.
    2. ExplanationMixin: Provides the text utility functions.
    """
    def __init__(self, parent, title, text_content, **kwargs):
        # Initialize the primary GUI parent (Frame)
        ttk.Frame.__init__(self, parent, padding="10", **kwargs)
        # Use the utility method inherited from the Mixin
        ExplanationMixin.create_explanation_content(self, title, text_content)


# --- MAIN APPLICATION CLASS ---
class AIApplicationWindow(tk.Tk):
    """
    The central application window class, managing the GUI and model interaction.
    """
    def __init__(self):
        # Initialize with a modern, professional theme for HD appearance
        self.style = Style(theme='flatly') 
        super().__init__()
        
        self.title("HIT137 AI Model Integrator (HD Professional Interface)")
        self.geometry("1200x750") 
        
        # Instantiate the two model classes, triggering pipeline loading
        self.text_model = TextGenerator()
        self.image_model = ImageClassifier()

        self._create_main_layout()

    # --- Layout Setup ---

    def _create_main_layout(self):
        """Sets up the primary two-column, resizable layout using PanedWindow."""
        # PanedWindow allows users to drag and resize the left and right panels
        main_pane = ttk.PanedWindow(self, orient=constants.HORIZONTAL)
        main_pane.pack(fill=constants.BOTH, expand=True, padx=15, pady=15)

        self.left_panel = ttk.Frame(main_pane, padding="10")
        self.right_panel = ttk.Frame(main_pane, padding="10")
        
        main_pane.add(self.left_panel, weight=1) # Left panel expands
        main_pane.add(self.right_panel, weight=0) # Right panel keeps its size

        self._populate_left_panel()
        self._populate_right_panel()

    def _populate_left_panel(self):
        """Creates the Model Selection, Input, and Output areas."""
        
        # 1. Model Selection Frame (Styled for HD)
        control_frame = ttk.LabelFrame(self.left_panel, text="1. Select AI Model", padding="20", style='primary.TLabelframe')
        control_frame.pack(fill=constants.X, pady=10)
        
        self.model_selection_var = tk.StringVar(value="Model 1: Text Generator")
        model_options = ["Model 1: Text Generator", "Model 2: Image Classifier"]
        
        ttk.Label(control_frame, text="Current Model:", font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        model_dropdown = ttk.Combobox(
            control_frame, 
            textvariable=self.model_selection_var, 
            values=model_options, 
            state="readonly", 
            width=35,
            font=('Arial', 10)
        )
        model_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        model_dropdown.bind("<<ComboboxSelected>>", self._handle_model_switch) 

        control_frame.grid_columnconfigure(1, weight=1) 

        # 2. Input Section Frame (Styled for HD)
        input_frame = ttk.LabelFrame(self.left_panel, text="2. User Input & Action", padding="20", style='info.TLabelframe')
        input_frame.pack(fill=constants.X, pady=10)

        ttk.Label(input_frame, text="Input Data:", font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.input_entry = ttk.Entry(input_frame, width=50, font=('Arial', 10))
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.input_entry.insert(0, "Enter your prompt or image file path...")

        # Advanced Button Styling
        ttk.Button(input_frame, text="Browse Image File", command=self._handle_browse_file, style='secondary.TButton').grid(row=0, column=2, padx=10, pady=5, sticky='e')
        
        # Main execution button (Prominent Styling)
        ttk.Button(input_frame, text="3. RUN SELECTED MODEL", command=self._execute_selected_model, 
                   style='success.TButton', width=40, cursor='hand2').grid(row=1, column=1, columnspan=2, pady=15, sticky='w')
        
        input_frame.grid_columnconfigure(1, weight=1) 

        # 3. Output Section Frame (Styled for HD - Console look)
        output_frame = ttk.LabelFrame(self.left_panel, text="4. Model Output Display", padding="15", style='dark.TLabelframe')
        output_frame.pack(fill=constants.BOTH, expand=True, pady=10)
        
        # Console-style Text widget for output clarity
        self.output_text_display = tk.Text(output_frame, height=18, wrap=tk.WORD, state='disabled', 
                                           font=('Consolas', 10), background='#212529', foreground='#20C997', relief=tk.FLAT)
        self.output_text_display.pack(fill=constants.BOTH, expand=True, padx=5, pady=5)

    def _populate_right_panel(self):
        """Creates the Model Info and OOP Explanation panels (Right side)."""
        
        # 1. Model Information Display (Dynamically updated)
        self.model_info_frame = ExplanationFrame(self.right_panel, "Selected Model Information & Status", "", height=5, style='secondary.TLabelframe')
        self.model_info_frame.pack(fill=constants.X, pady=10)
        self._update_model_info_display() # Display initial info on startup
        
        # 2. OOP Explanation Display (Static HD requirement content)
        oop_explanation_text = """
        • MULTIPLE INHERITANCE: Achieved by 'ExplanationFrame' inheriting from both 'ttk.Frame' (GUI container) and 'ExplanationMixin' (text utilities).
        
        • ENCAPSULATION: Enforced in 'BaseModelManager' where model details are protected (_model_name) and only accessible via the public 'get_public_model_info()' method.
        
        • POLYMORPHISM/METHOD OVERRIDING: The base class defines 'run_model()'. This method is overridden with unique logic in both 'TextGenerator' and 'ImageClassifier', allowing a single button click to execute different code paths.
        
        • MULTIPLE DECORATORS: The custom '@time_and_log_activity' decorator is used to wrap and time core functions in the model classes.
        
        • INHERITANCE: Both specific model classes reuse shared setup logic (like 'initialize_hf_pipeline') from the parent 'BaseModelManager'.
        """
        ExplanationFrame(self.right_panel, "OOP Concepts Explanation (HD Requirement)", oop_explanation_text, style='primary.TLabelframe').pack(fill=constants.BOTH, expand=True, pady=10)

    # --- Interaction and Logic Methods ---

    def _handle_model_switch(self, event):
        """
        Dedicated handler for the Combobox selection event.
        Reads the value directly from the widget to ensure state synchronization.
        """
        # Read the selection directly from the Combobox widget (event.widget)
        # and explicitly set the variable.
        selected_value = event.widget.get() 
        self.model_selection_var.set(selected_value) 
        
        # Process UI updates
        self._update_model_info_display()
        self._update_input_prompt()


    def _update_model_info_display(self):
        """
        Fetches the latest information from the currently selected model 
        (using the public getter) and refreshes the display panel.
        """
        # Select the correct model instance
        model = self.text_model if "Model 1" in self.model_selection_var.get() else self.image_model
            
        # Call the Encapsulated getter method
        info = model.get_public_model_info()
        
        # Format the information for clear display
        info_text = (
            f"• Model Name: {info.get('Model Name', 'N/A')}\n"
            f"• Category: {info.get('Category', 'N/A')}\n"
            f"• Purpose: {info.get('Purpose', 'N/A')}\n"
            f"• Status: {info.get('Status', 'Initialising...')}" 
        )
        
        self.model_info_frame.update_content(info_text)

    def _update_input_prompt(self):
        """Updates the input field with the appropriate prompt for the selected model."""
        self.input_entry.delete(0, tk.END)
        if "Model 1" in self.model_selection_var.get():
            self.input_entry.insert(0, "Enter text prompt here...")
        else:
            self.input_entry.insert(0, "Enter or Browse Image File Path...")


    def _handle_browse_file(self):
        """Opens a file dialog, only available when the Image Classifier is selected."""
        
        # This condition now correctly relies on the value set immediately in _handle_model_switch
        if "Model 2" in self.model_selection_var.get():
            filepath = filedialog.askopenfilename(
                title="Select Image File (JPG/PNG)",
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
            )
            if filepath:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, filepath)
        else:
            # When the button is clicked in the wrong mode, show a warning.
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, "ERROR: Switch to 'Model 2: Image Classifier' first!")


    def _execute_selected_model(self):
        """
        Executes the correct model's 'run_model' method based on the current selection.
        """
        input_data = self.input_entry.get()
        
        # Clear output and show loading status
        self.output_text_display.config(state='normal')
        self.output_text_display.delete(1.0, tk.END)
        self.output_text_display.insert(tk.END, "STATUS: Running AI model... Please wait. (Check terminal for execution time)\n")
        self.update() 

        try:
            if "Model 1" in self.model_selection_var.get():
                if not input_data.strip() or input_data == "Enter text prompt here...":
                     final_result = "Input Error: Text prompt cannot be empty."
                else:
                    final_result = self.text_model.run_model(input_data)
            else:
                # The input check must match the prompt set in _update_input_prompt
                if not input_data.strip() or input_data == "Enter or Browse Image File Path...":
                    final_result = "Input Error: Must provide an image file path."
                else:
                    final_result = self.image_model.run_model(input_data)
            
            self.output_text_display.insert(tk.END, f"\n--- MODEL RESULT ---\n{final_result}")

        except Exception as e:
            self.output_text_display.insert(tk.END, f"\nCRITICAL APPLICATION ERROR: {e}")
            
        # Ensure the output area remains read-only
        self.output_text_display.config(state='disabled')