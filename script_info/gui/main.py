import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from ..core import get_system_info


class SystemInfoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Info - System Information")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Create main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(
            main_frame,
            text="System Information Collector",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Collect button
        self.collect_button = tk.Button(
            button_frame,
            text="Collect System Info",
            command=self.collect_info,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        self.collect_button.pack(side=tk.LEFT)

        # Refresh button
        self.refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            command=self.collect_info,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        self.refresh_button.pack(side=tk.LEFT, padx=(10, 0))

        # Clear button
        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_info,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        self.clear_button.pack(side=tk.RIGHT)

        # Copy All button
        self.copy_button = tk.Button(
            button_frame,
            text="Copy All",
            command=self.copy_all_info,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            state=tk.DISABLED
        )
        self.copy_button.pack(side=tk.RIGHT, padx=(0, 10))

        # Download PDF button
        self.pdf_button = tk.Button(
            button_frame,
            text="Download PDF",
            command=self.download_pdf,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            state=tk.DISABLED
        )
        self.pdf_button.pack(side=tk.RIGHT)

        # Scrolled text area for displaying information
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            padx=5,
            pady=5
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to collect system information",
            fg="#666666",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(5, 0))

        # Initially disable refresh and clear buttons
        self.refresh_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        self.copy_button.config(state=tk.DISABLED)
        self.pdf_button.config(state=tk.DISABLED)

    def download_pdf(self):
        """Generate and download system information as PDF."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.units import inch
            from reportlab.lib.colors import blue, black, green
            import datetime

            # Get save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save System Information as PDF",
                initialfile=f"system_info_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )

            if not file_path:
                return

            self.status_label.config(text="Generating PDF...", fg="#FF9800")
            self.root.update()

            # Get current information
            info = {}
            text_content = self.text_area.get(1.0, tk.END).strip()
            if text_content:
                # Parse the text content back to dict format
                lines = text_content.split('\n')
                current_section = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith('===') or not line:
                        continue
                    elif ':' in line and not line.startswith('  '):
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
                    elif line.startswith('  ') and current_section:
                        # Continuation of previous value
                        info[current_section] += ' ' + line.strip()

            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center
                textColor=blue
            )

            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=20,
                textColor=blue
            )

            key_style = ParagraphStyle(
                'KeyStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor=green,
                fontName='Helvetica-Bold'
            )

            value_style = ParagraphStyle(
                'ValueStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor=black
            )

            # Build PDF content
            content = []

            # Title
            content.append(Paragraph("System Information Report", title_style))
            content.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            content.append(Spacer(1, 20))

            # Group information by categories
            categories = {
                'System': ['OS', 'Hostname', 'Current User', 'Uptime', 'System Age', 'System Status', 'Is Virtual Machine'],
                'Hardware': ['CPU', 'Memory', 'GPU', 'Battery', 'BIOS'],
                'Storage': ['Disk', 'Partition'],
                'Network': ['IP Address', 'Network', 'WiFi', 'DNS', 'Open Ports'],
                'Security': ['Windows Defender', 'Firewall', 'UAC', 'Windows Updates'],
                'Software': ['Python', 'Development Tools', 'Installed Programs', 'Browser History'],
                'Environment': ['Environment Variables', 'Locale', 'Timezone']
            }

            for category_name, keywords in categories.items():
                category_content = []
                for key, value in info.items():
                    if any(keyword.lower() in key.lower() for keyword in keywords):
                        category_content.append((key, value))

                if category_content:
                    content.append(Paragraph(category_name, header_style))
                    for key, value in category_content:
                        content.append(Paragraph(f"{key}:", key_style))
                        content.append(Paragraph(str(value), value_style))
                        content.append(Spacer(1, 5))
                    content.append(Spacer(1, 15))

            # Generate PDF
            doc.build(content)

            self.status_label.config(text=f"PDF saved to: {file_path}", fg="#4CAF50")
            messagebox.showinfo("Success", f"PDF report saved successfully!\n\nLocation: {file_path}")

        except ImportError:
            messagebox.showerror("Error", "PDF generation library not available.\nPlease install reportlab: pip install reportlab")
            self.status_label.config(text="PDF library not available", fg="#f44336")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF:\n{str(e)}")
            self.status_label.config(text="PDF generation failed", fg="#f44336")

    def copy_all_info(self):
        """Copy all displayed information to clipboard."""
        try:
            text_content = self.text_area.get(1.0, tk.END).strip()
            if text_content:
                self.root.clipboard_clear()
                self.root.clipboard_append(text_content)
                self.status_label.config(text="Information copied to clipboard", fg="#4CAF50")
            else:
                self.status_label.config(text="No information to copy", fg="#FF9800")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard:\n{str(e)}")
            self.status_label.config(text="Error copying to clipboard", fg="#f44336")

    def collect_info(self):
        """Collect and display system information."""
        try:
            self.status_label.config(text="Collecting system information...", fg="#FF9800")
            self.root.update()

            # Get system information
            info = get_system_info()

            # Clear previous content
            self.text_area.delete(1.0, tk.END)

            # Insert header
            self.text_area.insert(tk.END, "System Information\n", "header")
            self.text_area.insert(tk.END, "=" * 50 + "\n\n", "header")

            # Insert information
            for key, value in info.items():
                self.text_area.insert(tk.END, f"{key}: ", "key")
                self.text_area.insert(tk.END, f"{value}\n", "value")

            # Configure tags for styling
            self.text_area.tag_config("header", font=("Consolas", 12, "bold"), foreground="#1976D2")
            self.text_area.tag_config("key", font=("Consolas", 10, "bold"), foreground="#388E3C")
            self.text_area.tag_config("value", font=("Consolas", 10), foreground="#000000")

            # Update status
            self.status_label.config(text="System information collected successfully", fg="#4CAF50")

            # Enable buttons
            self.refresh_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.copy_button.config(state=tk.NORMAL)
            self.pdf_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to collect system information:\n{str(e)}")
            self.status_label.config(text="Error collecting information", fg="#f44336")

    def clear_info(self):
        """Clear the displayed information."""
        self.text_area.delete(1.0, tk.END)
        self.status_label.config(text="Information cleared", fg="#666666")
        self.refresh_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        self.copy_button.config(state=tk.DISABLED)
        self.pdf_button.config(state=tk.DISABLED)


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = SystemInfoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()