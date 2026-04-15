import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from modules import detect, db


def run_app():

    def upload_image():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )

        if not file_path:
            return

        location = location_entry.get()

        if location.strip() == "":
            messagebox.showwarning("Input Error", "Please enter location")
            return

        detected, img = detect.detect_pothole(file_path)

        if img is not None:
            show_image(img)

        if detected:
            db.insert_data(location, file_path)
            messagebox.showinfo("Result", "✅ Pothole Detected & Saved")
        else:
            messagebox.showinfo("Result", "❌ No Pothole Detected")

    def show_image(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))

        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)

        panel.config(image=img_tk)
        panel.image = img_tk

    def view_records():
        records = db.fetch_data()

        if not records:
            messagebox.showinfo("Records", "No data found")
            return

        text = ""
        for r in records:
            text += f"ID: {r[0]} | Location: {r[1]}\n"

        messagebox.showinfo("Pothole Records", text)

    def clear_fields():
        location_entry.delete(0, tk.END)
        panel.config(image="")
        panel.image = None

    # ---------------- GUI ----------------
    root = tk.Tk()
    root.title("🚧 Road Pothole Tracker System")
    root.geometry("500x550")

    tk.Label(root, text="Pothole Tracker", font=("Arial", 18, "bold")).pack(pady=10)

    tk.Label(root, text="Enter Location:", font=("Arial", 12)).pack()
    location_entry = tk.Entry(root, width=40)
    location_entry.pack(pady=5)

    tk.Button(root, text="Upload Image", command=upload_image, bg="blue", fg="white").pack(pady=10)
    tk.Button(root, text="View Records", command=view_records, bg="green", fg="white").pack(pady=5)
    tk.Button(root, text="Clear", command=clear_fields, bg="red", fg="white").pack(pady=5)

    panel = tk.Label(root)
    panel.pack(pady=20)

    root.mainloop()
