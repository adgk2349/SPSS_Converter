import os
import sys
import platform
import webbrowser
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

        # --- Manual TkinterDnD Loading for macOS ---
        try:
            import tkinterdnd2
            dnd_base_path = os.path.dirname(tkinterdnd2.__file__)
            
            is_arm = platform.processor() == "arm" or "arm" in platform.machine().lower()
            arch_folder = "osx-arm64" if is_arm else "osx-x64"
            
            tkdnd_path = os.path.join(dnd_base_path, 'tkdnd', arch_folder)
            
            if not os.path.exists(tkdnd_path):
                tkdnd_path = os.path.join(dnd_base_path, 'tkdnd')

            self.tk.call('lappend', 'auto_path', tkdnd_path)
            self.tk.call('package', 'require', 'tkdnd')
        except Exception:
            try:
                self.tk.call('package', 'require', 'tkdnd')
            except:
                pass

        # Window Setup
        self.title("SPSS Converter")
        self.geometry("500x540")
        self.configure(fg_color="#1A1A1A")
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
            text="v1.2.9", 
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
            corner_radius=14,
            command=self.quit
        )
        self.exit_button.pack(side="right")

        # Drop Zone
        self.drop_container = ctk.CTkFrame(
            self,
            fg_color="#121212",
            corner_radius=20,
            border_color="#2A2A2A",
            border_width=1
        )
        self.drop_container.pack(fill="both", expand=True, padx=35, pady=0)

        try:
            self.drop_container.drop_target_register(DND_FILES)
            self.drop_container.dnd_bind('<<Drop>>', self.handle_drop)
        except Exception:
            pass

        # Drop Zone Content - Emojis removed
        self.instruction_label = ctk.CTkLabel(
            self.drop_container, 
            text="파일을 이곳으로 끌어다 놓으세요\nDrag and drop files here", 
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#666666"
        )
        self.instruction_label.place(relx=0.5, rely=0.5, anchor="center")

        # Footer Actions
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=35, pady=(25, 20))

        self.select_button = ctk.CTkButton(
            self.footer_frame, 
            text="직접 선택 (Select File)", 
            height=42,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#0A84FF",
            hover_color="#0066CC",
            corner_radius=21,
            command=self.browse_file
        )
        self.select_button.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.about_btn = ctk.CTkButton(
            self.footer_frame,
            text="Info",
            width=60,
            height=42,
            fg_color="#2A2A2A",
            hover_color="#333333",
            corner_radius=21,
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
        # Custom "About" Window for clickable link
        about_window = ctk.CTkToplevel(self)
        about_window.title("About")
        about_window.geometry("380x280")
        about_window.resizable(False, False)
        about_window.configure(fg_color="#1A1A1A")
        about_window.after(100, lambda: about_window.focus()) # Ensure focus

        content_frame = ctk.CTkFrame(about_window, fg_color="transparent")
        content_frame.pack(pady=30, padx=30, fill="both", expand=True)

        ctk.CTkLabel(
            content_frame, 
            text="SPSS Converter", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            content_frame, 
            text="Version 1.2.9", 
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            content_frame, 
            text="Premium SPSS to CSV conversion tool.\nDeveloped for macOS & Windows.", 
            font=ctk.CTkFont(size=13),
            text_color="#BBBBBB",
            justify="center"
        ).pack(pady=(0, 20))

        # Clickable Link
        link_label = ctk.CTkLabel(
            content_frame, 
            text="github.com/adgk2349/SPSS_Converter", 
            font=ctk.CTkFont(size=13, underline=True),
            text_color="#0A84FF",
            cursor="hand2"
        )
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/adgk2349/SPSS_Converter"))

        # Close Button
        ctk.CTkButton(
            content_frame,
            text="Close",
            width=100,
            fg_color="#2A2A2A",
            hover_color="#333333",
            corner_radius=15,
            command=about_window.destroy
        ).pack(pady=(30, 0))

if __name__ == "__main__":
    app = SPSSConverterApp()
    app.mainloop()
