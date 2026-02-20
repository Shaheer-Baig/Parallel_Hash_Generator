"""
Modern GUI for Parallel File Hash Generator
Beautiful bluish theme with gradient effects and professional styling
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import hashlib
import threading
from datetime import datetime
import sys

class ModernButton(tk.Canvas):
    """Custom styled button with gradient and hover effects"""
    def __init__(self, parent, text, command, bg_color="#4A90E2", hover_color="#357ABD", **kwargs):
        super().__init__(parent, height=40, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        
        self.draw_button(bg_color)
        self.bind("<Enter>", lambda e: self.draw_button(self.hover_color))
        self.bind("<Leave>", lambda e: self.draw_button(self.bg_color))
        self.bind("<Button-1>", lambda e: self.command())
        
    def draw_button(self, color):
        self.delete("all")
        width = self.winfo_reqwidth() or 150
        height = 40
        self.create_rectangle(0, 0, width, height, fill=color, outline="", tags="bg")
        self.create_text(width//2, height//2, text=self.text, fill="white", 
                        font=("Segoe UI", 10, "bold"), tags="text")

class HashGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parallel File Hash Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Color scheme - Modern Blue theme
        self.colors = {
            'primary': '#1E3A8A',      # Deep blue
            'secondary': '#3B82F6',    # Bright blue
            'accent': '#60A5FA',       # Light blue
            'success': '#10B981',      # Green
            'danger': '#EF4444',       # Red
            'bg_dark': '#0F172A',      # Very dark blue
            'bg_light': '#F1F5F9',     # Light gray-blue
            'bg_card': '#FFFFFF',      # White
            'text_dark': '#1E293B',    # Dark text
            'text_light': '#64748B',   # Light text
            'border': '#E2E8F0'        # Border color
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg_light'])
        
        # Variables
        self.directory_path = tk.StringVar()
        self.hash_algorithm = tk.StringVar(value="sha256")
        self.is_running = False
        self.total_files = 0
        self.processed_files = 0
        self.current_output_path = None  # Store current result file path
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure frame
        style.configure('Card.TFrame', background=self.colors['bg_card'], 
                       relief='flat', borderwidth=0)
        
        # Configure labels
        style.configure('Title.TLabel', background=self.colors['bg_card'],
                       foreground=self.colors['primary'], font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['bg_card'],
                       foreground=self.colors['text_light'], font=('Segoe UI', 11))
        style.configure('Header.TLabel', background=self.colors['bg_card'],
                       foreground=self.colors['text_dark'], font=('Segoe UI', 11, 'bold'))
        style.configure('Status.TLabel', background=self.colors['bg_card'],
                       foreground=self.colors['secondary'], font=('Segoe UI', 10))
        
        # Configure entry
        style.configure('Modern.TEntry', fieldbackground='white', 
                       borderwidth=2, relief='solid')
        
        # Configure radiobuttons
        style.configure('Modern.TRadiobutton', background=self.colors['bg_card'],
                       foreground=self.colors['text_dark'], font=('Segoe UI', 10))
        
        # Configure progress bar
        style.configure('Modern.Horizontal.TProgressbar', 
                       background=self.colors['secondary'],
                       troughcolor=self.colors['border'],
                       borderwidth=0, thickness=30)
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header card
        header_card = tk.Frame(main_frame, bg=self.colors['bg_card'], relief='flat', bd=0)
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        # Add shadow effect
        shadow = tk.Frame(main_frame, bg='#CBD5E1', height=2)
        shadow.place(in_=header_card, relx=0, rely=1, relwidth=1)
        
        header_inner = tk.Frame(header_card, bg=self.colors['bg_card'])
        header_inner.pack(fill=tk.X, padx=30, pady=25)
        
        # Icon and title
        title_frame = tk.Frame(header_inner, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X)
        
        icon_label = tk.Label(title_frame, text="🔐", font=('Segoe UI', 32), 
                             bg=self.colors['bg_card'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        text_frame = tk.Frame(title_frame, bg=self.colors['bg_card'])
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title = ttk.Label(text_frame, text="Hash Generator", style='Title.TLabel')
        title.pack(anchor=tk.W)
        
        subtitle = ttk.Label(text_frame, text="Parallel File Integrity Monitoring System", 
                            style='Subtitle.TLabel')
        subtitle.pack(anchor=tk.W)
        
        # Content card
        content_card = tk.Frame(main_frame, bg=self.colors['bg_card'], relief='flat')
        content_card.pack(fill=tk.BOTH, expand=True)
        
        content_inner = tk.Frame(content_card, bg=self.colors['bg_card'])
        content_inner.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Directory selection section
        dir_frame = tk.Frame(content_inner, bg=self.colors['bg_card'])
        dir_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(dir_frame, text="📁 Directory", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        dir_input_frame = tk.Frame(dir_frame, bg=self.colors['bg_card'])
        dir_input_frame.pack(fill=tk.X)
        
        self.dir_entry = tk.Entry(dir_input_frame, textvariable=self.directory_path,
                                  font=('Segoe UI', 10), relief='solid', bd=2,
                                  highlightthickness=0, bg='white',
                                  fg=self.colors['text_dark'])
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        
        browse_btn = ModernButton(dir_input_frame, "Browse...", self.browse_directory,
                                 bg_color=self.colors['secondary'], 
                                 hover_color=self.colors['primary'], width=120)
        browse_btn.pack(side=tk.LEFT)
        
        # Algorithm selection
        algo_frame = tk.Frame(content_inner, bg=self.colors['bg_card'])
        algo_frame.pack(fill=tk.X, pady=(0, 25))
        
        ttk.Label(algo_frame, text="🔐 Hash Algorithm", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        radio_frame = tk.Frame(algo_frame, bg=self.colors['bg_card'])
        radio_frame.pack(anchor=tk.W)
        
        sha256_radio = ttk.Radiobutton(radio_frame, text="SHA-256 (Recommended)", 
                                      variable=self.hash_algorithm, value="sha256",
                                      style='Modern.TRadiobutton')
        sha256_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        md5_radio = ttk.Radiobutton(radio_frame, text="MD5 (Legacy)", 
                                   variable=self.hash_algorithm, value="md5",
                                   style='Modern.TRadiobutton')
        md5_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        both_radio = ttk.Radiobutton(radio_frame, text="Both (MD5 + SHA-256)", 
                                    variable=self.hash_algorithm, value="both",
                                    style='Modern.TRadiobutton')
        both_radio.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(content_inner, bg=self.colors['bg_card'])
        button_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.start_btn = ModernButton(button_frame, "▶  Start Hashing", self.start_hashing,
                                      bg_color=self.colors['success'], 
                                      hover_color='#059669', width=180)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ModernButton(button_frame, "⏹  Stop", self.stop_hashing,
                                     bg_color=self.colors['danger'], 
                                     hover_color='#DC2626', width=120)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.stop_btn.config(state=tk.DISABLED)
        
        results_btn = ModernButton(button_frame, "📄  View Results", self.open_results,
                                  bg_color=self.colors['accent'], 
                                  hover_color=self.colors['secondary'], width=150)
        results_btn.pack(side=tk.LEFT)
        
        # Progress section
        progress_section = tk.Frame(content_inner, bg=self.colors['bg_card'])
        progress_section.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(progress_section, text="📊 Progress", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_section, variable=self.progress_var, 
                                           maximum=100, mode='determinate',
                                           style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(progress_section, text="Ready to process files", 
                                     style='Status.TLabel')
        self.status_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Output console
        console_frame = tk.Frame(progress_section, bg=self.colors['border'], bd=2)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(console_frame, height=12, wrap=tk.WORD,
                                                     font=('Consolas', 9), bg='#1E293B',
                                                     fg='#E2E8F0', relief='flat',
                                                     borderwidth=0, padx=10, pady=10)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Add welcome message
        self.log_message("🎯 Welcome to Hash Generator", color='#60A5FA')
        self.log_message("📌 Select a directory and click 'Start Hashing'", color='#94A3B8')
        
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
        footer_frame.pack(pady=(15, 0))
        
        footer_text = tk.Label(footer_frame, 
                              text="Parallel & Distributed Computing Project", 
                              font=('Segoe UI', 9), bg=self.colors['bg_light'],
                              fg=self.colors['text_light'])
        footer_text.pack()
        
        developer_text = tk.Label(footer_frame, 
                                 text="Developed by Code_of_Duty", 
                                 font=('Segoe UI', 9, 'bold'), bg=self.colors['bg_light'],
                                 fg=self.colors['primary'])
        developer_text.pack()
        
        
    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select Directory to Hash")
        if directory:
            self.directory_path.set(directory)
            self.log_message(f"📁 Selected: {directory}", color='#10B981')
    
    def log_message(self, message, color='#E2E8F0'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.tag_config(color, foreground=color)
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n", color)
        self.output_text.see(tk.END)
    
    def start_hashing(self):
        directory = self.directory_path.get()
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory first!")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist!")
            return
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.is_running = True
        
        # Clear output
        self.output_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        # Start processing
        thread = threading.Thread(target=self.hash_files, daemon=True)
        thread.start()
    
    def stop_hashing(self):
        self.is_running = False
        self.log_message("⏹ Stopping process...", color='#EF4444')
        self.status_label.config(text="Process stopped by user")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def hash_files(self):
        directory = self.directory_path.get()
        algorithm = self.hash_algorithm.get()
        
        self.log_message(f"🔍 Scanning directory...", color='#60A5FA')
        self.status_label.config(text="Collecting files...")
        
        # Collect files
        files = []
        try:
            for root, dirs, filenames in os.walk(directory):
                if not self.is_running:
                    return
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    files.append(filepath)
        except Exception as e:
            self.log_message(f"❌ Error: {e}", color='#EF4444')
            self.stop_hashing()
            return
        
        self.total_files = len(files)
        self.processed_files = 0
        
        if self.total_files == 0:
            self.log_message("ℹ️  No files found", color='#F59E0B')
            self.stop_hashing()
            return
        
        self.log_message(f"✓ Found {self.total_files} files", color='#10B981')
        algo_display = "MD5 + SHA-256" if algorithm == "both" else algorithm.upper()
        self.log_message(f"🔐 Algorithm: {algo_display}", color='#60A5FA')
        self.log_message(f"⚙️  Processing...", color='#8B5CF6')
        
        # Create results directory
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Get folder name from selected directory
        folder_name = os.path.basename(os.path.normpath(directory))
        
        # Create output filename using folder name
        output_filename = f"{folder_name}_{algorithm}.txt"
        output_path = os.path.join(results_dir, output_filename)
        self.current_output_path = output_path  # Store for later use
        
        try:
            with open(output_path, 'w') as f:
                f.write(f"File Hash Results ({algo_display})\n")
                f.write(f"Directory: {directory}\n")
                f.write(f"Total Files: {self.total_files}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
        except Exception as e:
            self.log_message(f"❌ Error creating output: {e}", color='#EF4444')
            self.stop_hashing()
            return
        
        # Process files
        start_time = datetime.now()
        
        for filepath in files:
            if not self.is_running:
                self.log_message("⏹ Stopped", color='#EF4444')
                break
            
            try:
                if algorithm == "both":
                    # Calculate both MD5 and SHA-256
                    md5_obj = hashlib.md5()
                    sha256_obj = hashlib.sha256()
                    
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(4096):
                            md5_obj.update(chunk)
                            sha256_obj.update(chunk)
                    
                    md5_hash = md5_obj.hexdigest()
                    sha256_hash = sha256_obj.hexdigest()
                    
                    with open(output_path, 'a') as f:
                        f.write(f"File: {filepath}\n")
                        f.write(f"  MD5:    {md5_hash}\n")
                        f.write(f"  SHA256: {sha256_hash}\n\n")
                else:
                    # Calculate single hash
                    hash_obj = hashlib.new(algorithm)
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(4096):
                            hash_obj.update(chunk)
                    hash_value = hash_obj.hexdigest()
                    
                    with open(output_path, 'a') as f:
                        f.write(f"{hash_value}  {filepath}\n")
                
                self.processed_files += 1
                progress = (self.processed_files / self.total_files) * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"Processing: {self.processed_files}/{self.total_files} files ({progress:.1f}%)")
                
                if self.processed_files % 10 == 0 or self.processed_files == self.total_files:
                    self.log_message(f"✓ Processed {self.processed_files}/{self.total_files} files", 
                                   color='#10B981')
                
            except Exception as e:
                self.log_message(f"⚠️  Error: {os.path.basename(filepath)}", color='#F59E0B')
        
        # Complete
        duration = (datetime.now() - start_time).total_seconds()
        
        if self.is_running:
            self.log_message("━" * 50, color='#475569')
            self.log_message(f"✅ Completed successfully!", color='#10B981')
            self.log_message(f"📊 Files: {self.processed_files}/{self.total_files}", color='#60A5FA')
            self.log_message(f"⏱️  Time: {duration:.2f}s", color='#60A5FA')
            self.log_message(f"💾 Saved: results/{output_filename}", color='#8B5CF6')
            self.status_label.config(text=f"✓ Completed: {self.processed_files} files in {duration:.1f}s")
            
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"✅ Hashing completed!\n\n📊 Processed: {self.processed_files} files\n⏱️ Time: {duration:.2f}s\n💾 Saved: results/{output_filename}"))
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.is_running = False
    
    def open_results(self):
        # Use the current output path if available
        if self.current_output_path and os.path.exists(self.current_output_path):
            output_path = self.current_output_path
        else:
            # Fallback: try to find the most recent result file
            results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
            if not os.path.exists(results_dir):
                messagebox.showwarning("No Results", "No results folder found. Please run a hash operation first.")
                return
            
            # Get all result files and find the most recent
            result_files = [f for f in os.listdir(results_dir) if f.endswith('.txt')]
            if not result_files:
                messagebox.showwarning("No Results", "No result files found. Please run a hash operation first.")
                return
            
            # Get the most recently modified file
            result_files_with_time = [(f, os.path.getmtime(os.path.join(results_dir, f))) for f in result_files]
            most_recent = max(result_files_with_time, key=lambda x: x[1])[0]
            output_path = os.path.join(results_dir, most_recent)
        
        # Open the file
        if sys.platform == 'win32':
            os.startfile(output_path)
        elif sys.platform == 'darwin':
            os.system(f'open "{output_path}"')
        else:
            os.system(f'xdg-open "{output_path}"')

def main():
    root = tk.Tk()
    app = HashGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
