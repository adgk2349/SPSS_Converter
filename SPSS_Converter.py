import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class SPSSConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPSS SAV to CSV Converter")
        self.root.geometry("400x200")
        
        # UI Elements
        self.label_instruction = tk.Label(root, text="Select an SPSS (.sav) file to convert:", pady=20)
        self.label_instruction.pack()

        self.button_convert = tk.Button(root, text="Select & Convert", command=self.convert_to_csv, padx=20, pady=10)
        self.button_convert.pack()

        self.status_label = tk.Label(root, text="", pady=20, fg="blue")
        self.status_label.pack()

    def convert_to_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select SPSS File",
            filetypes=[("SPSS Files", "*.sav"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return

        base_path, extension = os.path.splitext(file_path)
        
        if extension.lower() != '.sav':
            messagebox.showerror("Error", "Please select a valid .sav file.")
            return

        try:
            self.status_label.config(text="Processing... Please wait.", fg="orange")
            self.root.update_idletasks()

            # Read SPSS file
            df = pd.read_spss(file_path)
            
            # Generate CSV path
            csv_file_path = f"{base_path}.csv"
            
            # Save to CSV
            df.to_csv(csv_file_path, index=False)
            
            self.status_label.config(text="Success! File converted.", fg="green")
            messagebox.showinfo("Success", f"File saved as:\n{os.path.basename(csv_file_path)}")
            
        except ImportError:
            self.status_label.config(text="Dependency missing!", fg="red")
            messagebox.showerror("Error", "The 'pyreadstat' library is required. Install it using:\npip install pyreadstat")
        except Exception as e:
            self.status_label.config(text="An error occurred.", fg="red")
            messagebox.showerror("Error", f"Failed to convert:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SPSSConverterApp(root)
    root.mainloop()
