from tkinter import Tk, Button, filedialog
from PIL import Image
import pytesseract

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        text = pytesseract.image_to_string(Image.open(file_path))
        print(text)

root = Tk()
root.title("OCR Application")

select_button = Button(root, text="Select Image", command=select_file)
select_button.pack(pady=20)

root.mainloop()
