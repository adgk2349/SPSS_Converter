import os
import sys
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SPSSConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Robust TkinterDnD loading for macOS/Windows with CustomTkinter
        try:
            # First try the standard way
            self.tk.call('package', 'require', 'tkdnd')
        except Exception:
            # If it fails, try to find it in site-packages
            try:
                import tkinterdnd2
                path = os.path.dirname(tkinterdnd2.__file__)
                tkdnd_path = os.path.join(path, 'tkdnd')
                self.tk.call('lappend', 'auto_path', tkdnd_path)
                self.tk.call('package', 'require', 'tkdnd')
            except Exception as e:
                print(f"Warning: TkinterDnD could not be loaded: {e}")

        # Window Setup
        self.title("SPSS Converter")
        self.geometry("500x530")
        self.configure(fg_color="#1A1A1A")  # Use fg_color for consistent macOS background
        self.attributes("-alpha", 0.98)
        self.resizable(False, False)

        # Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=35, pady=(35, 15))

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="SPSS Converter", 
            font=ctk.CTkFont(family="Inter", size=26, weight="bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(side="left")

        self.version_label = ctk.CTkLabel(
            self.header_frame, 
            text="v1.2.7", 
            font=ctk.CTkFont(family="Inter", size=13),
            text_color="#555555"
        )
        self.version_label.pack(side="left", padx=12, pady=(8, 0))

        self.exit_button = ctk.CTkButton(
            self.header_frame, 
            text="✕", 
            width=28, 
            height=28,
            fg_color="#2A2A2A",
            hover_color="#CC3333",
            corner_radius=14, # Fully rounded
            command=self.quit
        )
        self.exit_button.pack(side="right")

        # Drop Zone (Central unified area)
        self.drop_container = ctk.CTkFrame(
            self,
            fg_color="#121212",
            corner_radius=20, # Distinct rounded corners
            border_color="#333333",
            border_width=1
        )
        self.drop_container.pack(fill="both", expand=True, padx=35, pady=0)

        # Register Drag & Drop (Only if tkdnd is loaded)
        try:
            self.drop_container.drop_target_register(DND_FILES)
            self.drop_container.dnd_bind('<<Drop>>', self.handle_drop)
        except Exception:
            pass

        # Drop Zone Content
        self.icon_label = ctk.CTkLabel(
            self.drop_container, 
            text="📥", 
            font=ctk.CTkFont(size=60)
        )
        self.icon_label.place(relx=0.5, rely=0.42, anchor="center")

        self.instruction_label = ctk.CTkLabel(
            self.drop_container, 
            text="파일을 이곳으로 끌어다 놓으세요\nDrag and drop files here", 
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#666666"
        )
        self.instruction_label.place(relx=0.5, rely=0.62, anchor="center")

        # Footer Actions
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=35, pady=(25, 20))

        self.select_button = ctk.CTkButton(
            self.footer_frame, 
            text="⊕ 직접 선택 (Select File)", 
            height=42,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#0A84FF",
            hover_color="#0066CC",
            corner_radius=21, # Pill shaped (matches Exit button)
            command=self.browse_file
        )
        self.select_button.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.about_btn = ctk.CTkButton(
            self.footer_frame,
            text="ⓘ",
            width=42,
            height=42,
            fg_color="#2A2A2A",
            hover_color="#333333",
            corner_radius=21, # Circular (matches Exit button)
            command=self.show_about
        )
        self.about_btn.pack(side="right")

        # Status Overlay
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready for conversion",
            font=ctk.CTkFont(size=12),
            text_color="#333333"
        )
        self.status_label.pack(pady=(0, 15))

    def handle_drop(self, event):
        data = event.data
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]
        self.process_conversion(data)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select SPSS File",
            filetypes=[("SPSS Files", "*.sav"), ("All Files", "*.*")]
        )
        if file_path:
            self.process_conversion(file_path)

    def process_conversion(self, file_path):
        base_path, extension = os.path.splitext(file_path)
        
        if extension.lower() != '.sav':
            self.update_status("Invalid file format. Use .sav", "#FF453A")
            messagebox.showerror("Error", "Please select a valid .sav file.")
            return

        try:
            self.update_status("Converting... ⏳", "#FF9F0A")
            self.update_idletasks()

            df = pd.read_spss(file_path)
            csv_file_path = f"{base_path}.csv"
            df.to_csv(csv_file_path, index=False)
            
            self.update_status(f"Done: {os.path.basename(csv_file_path)}", "#32D74B")
            messagebox.showinfo("Success", f"File saved as:\n{os.path.basename(csv_file_path)}")
            
        except ImportError:
            self.update_status("Dependency missing!", "#FF453A")
            messagebox.showerror("Error", "The 'pyreadstat' library is required.")
        except Exception as e:
            self.update_status("Error occurred", "#FF453A")
            messagebox.showerror("Error", f"Failed to convert:\n{str(e)}")

    def update_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

    def show_about(self):
        about_text = (
            "SPSS Converter\n"
            "Version 1.2.7\n\n"
            "Premium SPSS to CSV conversion tool.\n\n"
            "GitHub: adgk2349/SPSS_Converter"
        )
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    app = SPSSConverterApp()
    app.mainloop()
