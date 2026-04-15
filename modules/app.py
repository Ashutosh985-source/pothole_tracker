import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from modules.db import Database
from modules.detector import PotholeDetector


class PotholeApp:

    def __init__(self):
        self.db = Database()
        self.detector = PotholeDetector()

        self.root = tk.Tk()
        self.root.title("🚧 Road Pothole Tracker")
        self.root.geometry("500x550")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Pothole Tracker System",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Enter Location").pack()

        self.location_entry = tk.Entry(self.root, width=40)
        self.location_entry.pack(pady=5)

        tk.Button(self.root, text="Upload Image",
                  command=self.upload_image,
                  bg="blue", fg="white").pack(pady=10)

        tk.Button(self.root, text="View Records",
                  command=self.view_records,
                  bg="green", fg="white").pack(pady=5)

        tk.Button(self.root, text="Clear",
                  command=self.clear,
                  bg="red", fg="white").pack(pady=5)

        self.panel = tk.Label(self.root)
        self.panel.pack(pady=20)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.png *.jpeg")]
        )

        if not file_path:
            return

        location = self.location_entry.get()

        if location.strip() == "":
            messagebox.showwarning("Error", "Enter location")
            return

        detected, img = self.detector.detect(file_path)

        if img is not None:
            self.show_image(img)

        if detected:
            self.db.insert(location, file_path)
            messagebox.showinfo("Result", "✅ Pothole Detected & Saved")
        else:
            messagebox.showinfo("Result", "❌ No Pothole Detected")

    def show_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))

        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)

        self.panel.config(image=img_tk)
        self.panel.image = img_tk

    def view_records(self):
        data = self.db.fetch_all()

        if not data:
            messagebox.showinfo("Records", "No data found")
            return

        text = ""
        for row in data:
            text += f"ID: {row[0]} | Location: {row[1]}\n"

        messagebox.showinfo("Pothole Records", text)

    def clear(self):
        self.location_entry.delete(0, tk.END)
        self.panel.config(image="")
        self.panel.image = None

    def run(self):
        self.root.mainloop()
