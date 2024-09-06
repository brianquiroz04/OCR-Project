import re
from tkinter import Tk, Button, Label, Text, Entry, filedialog, Scrollbar, END, messagebox, StringVar
from tkinter.font import Font
from PIL import Image
import pytesseract

# Define the correct answers for the homework
correct_answers = {
    1: "A",
    2: "B",
    3: "F",
    4: "G",
    5: "R",
    6: "C",
    7: "A",
    8: "B",
    9: "C",
    10: "A"
}

def select_file():
    """Function to open a file dialog to select an image file and perform OCR."""
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            # Perform OCR on the selected image
            text = pytesseract.image_to_string(Image.open(file_path))
            text_area.delete(1.0, END)  # Clear previous text
            text_area.insert(END, text)  # Display extracted text in the text area
            check_answers(text)  # Check answers after displaying text
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}") # Exception handling in case something like the wrong file type was submitted

def save_text():
    """Function to save the extracted text to a file."""
    text = text_area.get(1.0, END)
    if text.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text)
                messagebox.showinfo("Success", "Text saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")
    else:
        messagebox.showwarning("Warning", "There is no text to save!")

def search_text():
    """Function to search for a specific word in the text area."""
    text_area.tag_remove("highlight", 1.0, END) 
    search_word = search_var.get().strip()

    if search_word:
        start_pos = 1.0
        while True:
            start_pos = text_area.search(search_word, start_pos, stopindex=END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_word)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos

        # Configure the highlight tag with a background color
        text_area.tag_config("highlight", background="yellow", foreground="black")

def check_answers(text):
    """Function to check the student's answers against the correct answers."""
    feedback_area.delete(1.0, END)

    # Find all questions and answers using regex
    pattern = r"(\d+):\s*([A-Z])"  # Adjusted pattern to match uppercase answers. d=numbers, s=spaces, *=ignore count
    matches = re.findall(pattern, text, re.IGNORECASE)

    # Store results in feedback area and count score
    results = []
    correct = 0
    incorrect = 0
    total = 0
    for question, student_answer in matches:
        question_num = int(question)
        correct_answer = correct_answers.get(question_num)
        total += 1

        if correct_answer:
            if student_answer.upper() == correct_answer:
                results.append(f"Question {question_num}: Correct! (Your answer: {student_answer})")
                correct += 1
            else:
                results.append(f"Question {question_num}: Incorrect. (Your answer: {student_answer}, Correct answer: {correct_answer})")
        else:
            results.append(f"Question {question_num}: No correct answer defined.")

    # Display results in feedback area
    feedback_area.insert(END, "\n".join(results) + "\nOverall Score: " + str(correct) + "/" + str(total))

# Create the main window
root = Tk()
root.title("OCR Homework Checker")
root.geometry("600x600") 
root.configure(bg="#f0f0f0")  #  background color

# this font will be applied everywhere
custom_font = Font(family="Arial", size=10)

# Label above button
label = Label(root, text="Select an image file to extract text using OCR and check answers:", bg="#f0f0f0", font=custom_font)
label.pack(pady=(20, 10))

# Add a button to select an image file
select_button = Button(root, text="Select Image", command=select_file, font=custom_font, bg="#4CAF50", fg="white", padx=10, pady=5)
select_button.pack(pady=10)

# Add a text area to display the extracted text
text_area = Text(root, wrap="word", font=custom_font)
text_area.pack(padx=10, pady=10, fill="both", expand=True)

# Add a scrollbar to the text area
scrollbar = Scrollbar(text_area)
scrollbar.pack(side="right", fill="y")
text_area.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_area.yview)

# Add a search entry field and button
search_var = StringVar()
search_entry = Entry(root, textvariable=search_var, font=custom_font)
search_entry.pack(pady=(10, 0))

search_button = Button(root, text="Search", command=search_text, font=custom_font, bg="#4CAF50", fg="white", padx=10, pady=5)
search_button.pack(pady=10)

# Add a button to save the extracted text
save_button = Button(root, text="Save Text", command=save_text, font=custom_font, bg="#4CAF50", fg="white", padx=10, pady=5)
save_button.pack(pady=(10, 20))

# Add a text area to display feedback on answers
feedback_area = Text(root, wrap="word", font=custom_font, height=10)
feedback_area.pack(padx=10, pady=(0, 10), fill="both", expand=True)

root.mainloop()
