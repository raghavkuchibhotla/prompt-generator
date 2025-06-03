import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
from datetime import datetime

class PromptGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Prompt Generator")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Set color scheme
        self.colors = {
            "primary": "#2E1A47",  # Dark purple
            "secondary": "#6B46C1",  # Medium purple
            "accent": "#8A63D2",  # Light purple
            "text": "#FFFFFF",  # White
            "background": "#F5F5F7"  # Light gray
        }
        
        # Configure the root window
        self.root.configure(bg=self.colors["primary"])
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors["primary"], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create prompt generator card
        self.create_prompt_card()
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W,
                             bg=self.colors["primary"], fg=self.colors["text"])
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize saved prompts
        self.saved_prompts = {}
        self.load_saved_prompts()
    
    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.main_frame, bg=self.colors["primary"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo and title
        logo_label = tk.Label(header_frame, text="AI Prompt Generator", 
                             font=("Helvetica", 24, "bold"), 
                             bg=self.colors["primary"], fg=self.colors["text"])
        logo_label.pack(side=tk.LEFT)
        
        # Description
        description = "Create engaging prompts for AI models to generate better content"
        desc_label = tk.Label(header_frame, text=description, 
                             font=("Helvetica", 12), 
                             bg=self.colors["primary"], fg=self.colors["text"])
        desc_label.pack(side=tk.LEFT, padx=20)
    
    def create_prompt_card(self):
        """Create the main prompt generator card"""
        # Card frame with white background and rounded corners
        card_frame = tk.Frame(self.main_frame, bg="white", padx=20, pady=20,
                             highlightbackground=self.colors["accent"], 
                             highlightthickness=1)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Logo at the top of the card
        logo_frame = tk.Frame(card_frame, bg="white")
        logo_frame.pack(fill=tk.X, pady=(0, 20))
        
        logo_label = tk.Label(logo_frame, text="✨", font=("Helvetica", 24),
                             bg="white", fg=self.colors["secondary"])
        logo_label.pack()
        
        # Prompt input
        input_frame = tk.Frame(card_frame, bg="white")
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        prompt_label = tk.Label(input_frame, text="Purpose of the prompt", 
                               font=("Helvetica", 12), bg="white")
        prompt_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.prompt_text = scrolledtext.ScrolledText(input_frame, height=10, 
                                                   font=("Helvetica", 12),
                                                   wrap=tk.WORD)
        self.prompt_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(card_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Generate button
        generate_style = ttk.Style()
        generate_style.configure("Generate.TButton", 
                                font=("Helvetica", 12, "bold"),
                                background=self.colors["secondary"])
        
        generate_btn = ttk.Button(button_frame, text="GENERATE", 
                                 command=self.generate_prompt,
                                 style="Generate.TButton")
        generate_btn.pack(side=tk.TOP)
        
        # Usage counter
        usage_label = tk.Label(button_frame, text="0/20 Uses Today", 
                              font=("Helvetica", 10), bg="white", fg="gray")
        usage_label.pack(side=tk.TOP, pady=(5, 0))
        
        # Terms and conditions
        terms_frame = tk.Frame(button_frame, bg="white")
        terms_frame.pack(side=tk.TOP, pady=(5, 0))
        
        terms_label = tk.Label(terms_frame, text="By continuing you agree to our ", 
                              font=("Helvetica", 10), bg="white", fg="gray")
        terms_label.pack(side=tk.LEFT)
        
        terms_link = tk.Label(terms_frame, text="Terms and conditions", 
                             font=("Helvetica", 10), bg="white", 
                             fg=self.colors["secondary"], cursor="hand2")
        terms_link.pack(side=tk.LEFT)
        terms_link.bind("<Button-1>", self.show_terms)
        
        # Output frame (initially hidden)
        self.output_frame = tk.Frame(card_frame, bg="white")
        
        output_label = tk.Label(self.output_frame, text="Generated Prompt", 
                               font=("Helvetica", 12, "bold"), bg="white")
        output_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=10, 
                                                   font=("Helvetica", 12),
                                                   wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Copy button
        copy_btn = ttk.Button(self.output_frame, text="Copy to Clipboard", 
                             command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.RIGHT, pady=(10, 0))
        
        # Save button
        save_btn = ttk.Button(self.output_frame, text="Save Prompt", 
                             command=self.save_prompt)
        save_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=(10, 0))
    
    def generate_prompt(self):
        """Generate a prompt based on user input"""
        purpose = self.prompt_text.get("1.0", tk.END).strip()
        
        if not purpose:
            messagebox.showwarning("Input Required", "Please enter the purpose of your prompt.")
            return
        
        # Simple prompt generation logic
        generated_prompt = f"""# AI Content Generation Prompt

## Purpose
{purpose}

## Instructions
- Create content that is engaging and original
- Ensure the tone is professional yet conversational
- Include relevant examples and details
- Structure the content in a clear, logical manner

## Format
Please provide the output in well-formatted markdown with appropriate headings, bullet points, and paragraphs.

## Additional Requirements
- Length: Approximately 500-800 words
- Include a compelling introduction and conclusion
- Avoid generic or repetitive phrasing
- Cite sources if referencing specific data or research
"""
        
        # Show the output frame
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display the generated prompt
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, generated_prompt)
        
        self.status_var.set("Prompt generated successfully")
    
    def copy_to_clipboard(self):
        """Copy the generated prompt to clipboard"""
        prompt = self.output_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.root.update()  # Required to finalize clipboard changes
        self.status_var.set("Prompt copied to clipboard")
    
    def save_prompt(self):
        """Save the current prompt"""
        prompt = self.output_text.get("1.0", tk.END).strip()
        purpose = self.prompt_text.get("1.0", tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Save Prompt", "No prompt generated. Please generate a prompt first.")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt_info = {
            "purpose": purpose,
            "prompt": prompt,
            "timestamp": timestamp
        }
        
        self.saved_prompts[timestamp] = prompt_info
        self.save_prompts_to_file()
        self.status_var.set(f"Prompt saved successfully")
        messagebox.showinfo("Prompt Saved", "Your prompt has been saved successfully.")
    
    def load_saved_prompts(self):
        """Load saved prompts from a file"""
        try:
            with open("saved_prompts.json", "r") as file:
                self.saved_prompts = json.load(file)
        except FileNotFoundError:
            self.saved_prompts = {}
    
    def save_prompts_to_file(self):
        """Save the saved prompts to a file"""
        with open("saved_prompts.json", "w") as file:
            json.dump(self.saved_prompts, file, indent=4)
    
    def show_terms(self, event):
        """Show terms and conditions"""
        messagebox.showinfo("Terms and Conditions", 
                          "By using this AI Prompt Generator, you agree to our terms of service. "
                          "Generated prompts are for personal or commercial use. "
                          "We do not store or use your prompts for training our models.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PromptGenerator(root)
    root.mainloop()
