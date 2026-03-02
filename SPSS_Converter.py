import os
import sys
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SPSSConverterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("SPSS Converter")
        self.geometry("500x550")
        self.configure(bg="#1A1A1A")
        self.resizable(False, False)

        # Main Container
        self.main_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header Section
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(10, 20))

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="SPSS Converter", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(side="left")

        self.version_label = ctk.CTkLabel(
            self.header_frame, 
            text="v1.1.0", 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#888888"
        )
        self.version_label.pack(side="left", padx=10, pady=(8, 0))

        self.exit_button = ctk.CTkButton(
            self.header_frame, 
            text="✕ Exit", 
            width=70, 
            height=32,
            fg_color="#2A2A2A",
            hover_color="#3A3A3A",
            corner_radius=16,
            command=self.quit
        )
        self.exit_button.pack(side="right")

        # Drop Zone Area
        self.drop_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#121212", 
            border_color="#333333", 
            border_width=2,
            corner_radius=25
        )
        self.drop_frame.pack(fill="both", expand=True, pady=10)

        # Drag & Drop functional binding
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)

        # Drop Zone Content
        self.icon_label = ctk.CTkLabel(
            self.drop_frame, 
            text="📄", 
            font=ctk.CTkFont(size=60)
        )
        self.icon_label.place(relx=0.5, rely=0.4, anchor="center")

        self.instruction_label = ctk.CTkLabel(
            self.drop_frame, 
            text="파일을 이곳으로 끌어다 놓으세요\nDrag and drop files here", 
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#BBBBBB"
        )
        self.instruction_label.place(relx=0.5, rely=0.6, anchor="center")

        # Footer Actions
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.footer_frame.pack(fill="x", pady=(20, 10))

        self.select_button = ctk.CTkButton(
            self.footer_frame, 
            text="⊕ 직접 선택 (Select File)", 
            height=40,
            fg_color="#2A2A2A",
            hover_color="#3A3A3A",
            corner_radius=20,
            command=self.browse_file
        )
        self.select_button.pack(side="left")

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready to convert",
            font=ctk.CTkFont(size=12),
            text_color="#555555"
        )
        self.status_label.pack(pady=(10, 0))

        # About Menu (Hidden or as sub-button)
        self.about_btn = ctk.CTkButton(
            self.footer_frame,
            text="ⓘ",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#2A2A2A",
            corner_radius=20,
            command=self.show_about
        )
        self.about_btn.pack(side="right")

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        if files:
            self.process_conversion(files[0])

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
            self.update_status("Invalid file format. Use .sav", "#FF5555")
            messagebox.showerror("Error", "Please select a valid .sav file.")
            return

        try:
            self.update_status("Processing... Please wait.", "#FFA500")
            self.update_idletasks()

            df = pd.read_spss(file_path)
            csv_file_path = f"{base_path}.csv"
            df.to_csv(csv_file_path, index=False)
            
            self.update_status(f"Converted: {os.path.basename(csv_file_path)}", "#55FF55")
            messagebox.showinfo("Success", f"File saved as:\n{os.path.basename(csv_file_path)}")
            
        except ImportError:
            self.update_status("Dependency missing!", "#FF5555")
            messagebox.showerror("Error", "The 'pyreadstat' library is required.")
        except Exception as e:
            self.update_status("An error occurred.", "#FF5555")
            messagebox.showerror("Error", f"Failed to convert:\n{str(e)}")

    def update_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

    def show_about(self):
        about_text = (
            "SPSS Converter\n"
            "Version 1.1.0\n\n"
            "Premium SPSS to CSV conversion tool.\n\n"
            "GitHub: adgk2349/SPSS_Converter"
        )
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    app = SPSSConverterApp()
    app.mainloop()
