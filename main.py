#HIT137_A3_S2 : Group No : 24
#Author: Jagdeep Singh: Setting up the application entry point.
# Purpose: Main entry point for the application.

from gui_app import AIApplicationWindow

# Standard check to ensure the code only runs when directly executed
if __name__ == "__main__":
    # Create the main window instance, which handles model initialization
    app = AIApplicationWindow()
    
    # Start the Tkinter event loop to display the GUI and handle all interactions
    app.mainloop()