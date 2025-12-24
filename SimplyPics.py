###################################
#CoolGuy158-Git Copyright 2025 MIT#
#SimplyPics                       #
###################################
import customtkinter
from datetime import datetime
import PIL
from PIL import Image, ImageTk
import sys
from tkinter import messagebox
import os
from pathlib import Path
import platform
def get_file_properties(file_path):
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return None
    stats = os.stat(file_path)
    properties = {
        "size_bytes": stats.st_size,
        "size_kb": round(stats.st_size / 1024, 2),
        "created": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "accessed": datetime.fromtimestamp(stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
    }
    return properties
def gallery_path():
    gallery = Path.home() / "Pictures"
    return gallery if gallery.exists() else Path.home()

gallery_folder = gallery_path()
# GUI
def init_gui():
    root = customtkinter.CTk()
    root.title("Simply Pics")
    root.geometry("1440x700")
    current_image_path = [None]
    top_margin = 5
    left_margin = 5
    right_margin = 1200
    frame_width = 1440 - left_margin - right_margin
    frame_height = 700 - top_margin - 5
    scroll_frame = customtkinter.CTkScrollableFrame(root, width=frame_width, height=frame_height)
    scroll_frame.pack(padx=left_margin, pady=top_margin, fill='y', side='left')
    image_frame = customtkinter.CTkFrame(root, width=1000, height=500)
    image_frame.pack(fill="y", pady=(0, 20))
    props_frame = customtkinter.CTkFrame(root, width=1000, height=150)
    props_frame.pack(fill='x', pady=(0, 10))
    rename_entry = customtkinter.CTkEntry(props_frame, placeholder_text="Enter new name with extension")
    rename_entry.pack(padx=10, pady=(10, 5), fill="x")
    def rename_current_image():
        if not current_image_path[0]:
            return
        new_name = rename_entry.get()
        if not new_name:
            return
        allowed_exts = (".png", ".jpg", ".jpeg", ".ico")
        if not new_name.lower().endswith(tuple(ext.lower() for ext in allowed_exts)):
            messagebox.showerror("Invalid Name", f"File must end with {allowed_exts}")
            return
        dir_path = os.path.dirname(current_image_path[0])
        new_path = os.path.join(dir_path, new_name)
        if os.path.exists(new_path):
            messagebox.showerror("File Exists", "A file with this name already exists!")
            return
        os.rename(current_image_path[0], new_path)
        current_image_path[0] = new_path
        rename_entry.delete(0, "end")
        load_file_buttons()
        open_image(new_path)
    rename_btn = customtkinter.CTkButton(props_frame, text="Rename", command=rename_current_image)
    rename_btn.pack(padx=10, pady=(0, 10))
    def open_image(file_path):
        try:
            img = PIL.Image.open(file_path)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return
        current_image_path[0] = file_path
        frame_width = image_frame.winfo_width()
        orig_width, orig_height = img.size
        scale_w = frame_width / orig_width
        scale_h = frame_height / orig_height
        scale = min(scale_w, scale_h, 1)
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        for widget in image_frame.winfo_children():
            widget.destroy()
        label = customtkinter.CTkLabel(image_frame, image=tk_img, text="", corner_radius=5)
        label.image = tk_img
        label.place(relx=0.5, rely=0.5, anchor="center")
        for widget in props_frame.winfo_children():
            if widget not in (rename_entry, rename_btn):
                widget.destroy()
        props = get_file_properties(file_path)
        if props:
            for key, value in props.items():
                prop_label = customtkinter.CTkLabel(props_frame, text=f"{key}: {value}", anchor="w")
                prop_label.pack(fill="x", padx=10, pady=(0, 3))
    allowed_exts = (".png", ".jpg", ".jpeg", ".ico")
    def get_all_images(folder):
        images = []
        for f in folder.rglob("*"):
            if f.is_file() and f.suffix.lower() in allowed_exts:
                images.append(f)
        return sorted(images, key=lambda f: f.stat().st_mtime, reverse=True)
    def load_file_buttons():
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        all_images = get_all_images(gallery_folder)
        if not all_images:
            label = customtkinter.CTkLabel(scroll_frame, text="No images found in Pictures")
            label.pack(pady=20)
            return
        for f in all_images:
            display_name = f.name[:20] + "..." if len(f.name) > 20 else f.name
            full_path = str(f)
            btn = customtkinter.CTkButton(scroll_frame, text=display_name, command=lambda f=full_path: open_image(f),
                                          width=200)
            btn.pack(pady=10, padx=10)
    load_file_buttons()
    return root
# logs
STARTUP_STATUS = {
    "imports": False,
    "gui_init": False,
    "mainloop": False
}
try:
    STARTUP_STATUS["imports"] = True
    print("Imports successful:", STARTUP_STATUS["imports"])
    sys.stdout.flush()
    root = init_gui()
    STARTUP_STATUS["gui_init"] = True
    print("GUI initialized:", STARTUP_STATUS["gui_init"])
    sys.stdout.flush()
    print("Startup checks passed:", STARTUP_STATUS)
    sys.stdout.flush()
    STARTUP_STATUS["mainloop"] = True
    root.mainloop()
except Exception as e:
    print("Startup failed!")
    sys.stdout.flush()
    print("Status:", STARTUP_STATUS)
    sys.stdout.flush()
    print("Error:", e)
    sys.stdout.flush()



