import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
from ..core import get_system_info
from ..reporting import PDFReporter
import datetime

class SystemInfoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Info - System Information")
        self.root.geometry("700x600")
        
        # Data store
        self.current_info = {}

        # Styles
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        # Main Layout
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="System Information Collector",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 10))

        # Controls
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.collect_button = tk.Button(button_frame, text="Collect Info", command=self.start_collection, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), padx=15)
        self.collect_button.pack(side=tk.LEFT)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.start_collection, bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"), padx=15, state=tk.DISABLED)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_info, bg="#f44336", fg="white", font=("Segoe UI", 10, "bold"), padx=15, state=tk.DISABLED)
        self.clear_button.pack(side=tk.RIGHT)

        self.pdf_button = tk.Button(button_frame, text="Export PDF", command=self.download_pdf, bg="#9C27B0", fg="white", font=("Segoe UI", 10, "bold"), padx=15, state=tk.DISABLED)
        self.pdf_button.pack(side=tk.RIGHT, padx=5)

        # Text Area
        self.text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Consolas", 10), padx=5, pady=5)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Status Bar
        self.status_label = tk.Label(main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0))

        # Tags
        self.text_area.tag_config("header", font=("Consolas", 12, "bold"), foreground="#1976D2")
        self.text_area.tag_config("key", font=("Consolas", 10, "bold"), foreground="#388E3C")
        self.text_area.tag_config("value", font=("Consolas", 10), foreground="#000000")

    def log(self, message, color="black"):
        self.status_label.config(text=message, fg=color)

    def set_buttons_state(self, state):
        self.collect_button.config(state=state)
        self.refresh_button.config(state=state)
        # Clear/PDF usually stay enabled if we have data, but during collection maybe disable everything?
        # Let's disable collect/refresh during collection
        if state == tk.NORMAL:
             self.collect_button.config(state=tk.NORMAL)
             self.refresh_button.config(state=tk.NORMAL if self.current_info else tk.DISABLED)
             self.clear_button.config(state=tk.NORMAL if self.current_info else tk.DISABLED)
             self.pdf_button.config(state=tk.NORMAL if self.current_info else tk.DISABLED)
        else:
             self.collect_button.config(state=tk.DISABLED)
             self.refresh_button.config(state=tk.DISABLED)
             self.clear_button.config(state=tk.DISABLED)
             self.pdf_button.config(state=tk.DISABLED)


    def start_collection(self):
        self.set_buttons_state(tk.DISABLED)
        self.log("Collecting system information... Please wait.", "blue")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Loading...\n")
        
        # Run in thread
        thread = threading.Thread(target=self.collect_bg)
        thread.daemon = True
        thread.start()

    def collect_bg(self):
        try:
            info = get_system_info()
            # Schedule UI update on main thread
            self.root.after(0, self.collection_complete, info)
        except Exception as e:
            self.root.after(0, self.collection_error, str(e))

    def collection_complete(self, info):
        self.current_info = info
        self.text_area.delete(1.0, tk.END)
        
        self.text_area.insert(tk.END, "System Information Report\n", "header")
        self.text_area.insert(tk.END, "=" * 30 + "\n\n", "header")

        for key, value in info.items():
            if isinstance(value, dict):
                 self.text_area.insert(tk.END, f"{key}:\n", "key")
                 for k, v in value.items():
                     self.text_area.insert(tk.END, f"  {k}: ", "key")
                     self.text_area.insert(tk.END, f"{v}\n", "value")
            else:
                self.text_area.insert(tk.END, f"{key}: ", "key")
                self.text_area.insert(tk.END, f"{value}\n", "value")

        self.log(f"Collection complete. Found {len(info)} items.", "green")
        self.set_buttons_state(tk.NORMAL)

    def collection_error(self, error_msg):
        self.log(f"Error: {error_msg}", "red")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Error Occurred:\n{error_msg}")
        self.set_buttons_state(tk.NORMAL)
        messagebox.showerror("Error", f"Failed to collect info:\n{error_msg}")

    def clear_info(self):
        self.current_info = {}
        self.text_area.delete(1.0, tk.END)
        self.log("Cleared.", "black")
        self.set_buttons_state(tk.NORMAL)

    def download_pdf(self):
        if not self.current_info:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save PDF Report",
            initialfile=f"system_info_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if file_path:
            self.log(f"Generating PDF: {file_path}...", "blue")
            self.root.update()
            
            reporter = PDFReporter(file_path)
            if reporter.generate(self.current_info):
                self.log("PDF saved successfully.", "green")
                messagebox.showinfo("Success", f"PDF saved to:\n{file_path}")
            else:
                self.log("PDF generation failed.", "red")
                messagebox.showerror("Error", "Failed to generate PDF. Check dependencies (reportlab).")

def main():
    root = tk.Tk()
    app = SystemInfoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()