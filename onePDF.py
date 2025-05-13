import os
import shutil
import tempfile
import platform
import subprocess
from tkinter import Tk, Listbox, Button, END, filedialog, messagebox, SINGLE, Scrollbar, RIGHT, Y, LEFT, BOTH, Frame
from PIL import Image

# Try to import docx2pdf if available
try:
    from docx2pdf import convert
    DOCX_SUPPORTED = True
except ImportError:
    DOCX_SUPPORTED = False

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

# Constants
A4_WIDTH = 595.28
A4_HEIGHT = 841.89
A4_SIZE = RectangleObject([0, 0, A4_WIDTH, A4_HEIGHT])

SUPPORTED_TYPES = (".pdf", ".docx", ".jpg", ".jpeg", ".png")


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart PDF Merger")
        self.files = []
        self.temp_dir = tempfile.mkdtemp()

        # GUI Layout
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.file_listbox = Listbox(self.frame, width=60, height=15, selectmode=SINGLE)
        self.file_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.frame, command=self.file_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        Button(self.root, text="Add Files", command=self.add_files).pack(pady=5)
        Button(self.root, text="Add Folder", command=self.add_folder).pack(pady=5)

        Button(self.root, text="Move Up", command=self.move_up).pack(pady=2)
        Button(self.root, text="Move Down", command=self.move_down).pack(pady=2)
        Button(self.root, text="Remove Selected", command=self.remove_selected).pack(pady=2)

        Button(self.root, text="Merge to PDF", command=self.merge_files).pack(pady=10)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("Supported Files", "*.pdf *.docx *.jpg *.jpeg *.png")]
        )
        for path in paths:
            if path.lower().endswith(SUPPORTED_TYPES) and path not in self.files:
                self.files.append(path)
                self.file_listbox.insert(END, os.path.basename(path))

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            for root_dir, _, filenames in os.walk(folder):
                for name in filenames:
                    full_path = os.path.join(root_dir, name)
                    if full_path.lower().endswith(SUPPORTED_TYPES) and full_path not in self.files:
                        self.files.append(full_path)
                        self.file_listbox.insert(END, os.path.basename(full_path))

    def move_up(self):
        index = self.file_listbox.curselection()
        if index and index[0] > 0:
            i = index[0]
            self.files[i], self.files[i - 1] = self.files[i - 1], self.files[i]
            self.refresh_listbox(i - 1)

    def move_down(self):
        index = self.file_listbox.curselection()
        if index and index[0] < len(self.files) - 1:
            i = index[0]
            self.files[i], self.files[i + 1] = self.files[i + 1], self.files[i]
            self.refresh_listbox(i + 1)

    def remove_selected(self):
        index = self.file_listbox.curselection()
        if index:
            i = index[0]
            self.files.pop(i)
            self.file_listbox.delete(i)

    def refresh_listbox(self, select_index=None):
        self.file_listbox.delete(0, END)
        for f in self.files:
            self.file_listbox.insert(END, os.path.basename(f))
        if select_index is not None:
            self.file_listbox.select_set(select_index)

    def convert_docx(self, docx_path):
        output_pdf = os.path.join(self.temp_dir, os.path.basename(docx_path).replace(".docx", ".pdf"))
        try:
            if DOCX_SUPPORTED:
                convert(docx_path, output_pdf)
            elif platform.system() == "Linux":
                subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", self.temp_dir])
            return output_pdf if os.path.exists(output_pdf) else None
        except Exception as e:
            print(f"[DOCX ERROR] {e}")
            return None

    def convert_image(self, image_path):
        output_pdf = os.path.join(self.temp_dir, os.path.basename(image_path) + ".pdf")
        try:
            img = Image.open(image_path).convert("RGB")
            img.thumbnail((A4_WIDTH, A4_HEIGHT))
            bg = Image.new("RGB", (int(A4_WIDTH), int(A4_HEIGHT)), "white")
            offset = ((int(A4_WIDTH) - img.width) // 2, (int(A4_HEIGHT) - img.height) // 2)
            bg.paste(img, offset)
            bg.save(output_pdf)
            return output_pdf
        except Exception as e:
            print(f"[IMG ERROR] {e}")
            return None

    def merge_files(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please add files to merge.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not save_path:
            return

        pdfs_to_merge = []

        for f in self.files:
            ext = os.path.splitext(f)[1].lower()
            if ext == ".pdf":
                pdfs_to_merge.append(f)
            elif ext == ".docx":
                converted = self.convert_docx(f)
                if converted:
                    pdfs_to_merge.append(converted)
            elif ext in [".jpg", ".jpeg", ".png"]:
                converted = self.convert_image(f)
                if converted:
                    pdfs_to_merge.append(converted)

        writer = PdfWriter()

        for pdf_path in pdfs_to_merge:
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    page.mediabox = A4_SIZE
                    page.cropbox = A4_SIZE
                    writer.add_page(page)
            except Exception as e:
                print(f"[MERGE ERROR] {pdf_path}: {e}")

        try:
            with open(save_path, "wb") as f_out:
                writer.write(f_out)
            messagebox.showinfo("Success", f"Merged PDF saved successfully to:\n{save_path}")
            print("✅ Merge successful!")
            print("✨ You could add more features like:\n- Password protection\n- Preview final PDF\n- File renaming options")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")
        finally:
            shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == "__main__":
    root = Tk()
    app = PDFMergerApp(root)
    root.mainloop()
