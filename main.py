import tkinter as tk  # it is used for creating GUI elements 
from tkinter import scrolledtext, messagebox  # it is used for displaying text with a scrollbar
from transformers import pipeline  # it will load pretrained model like summarization
import threading  # it will run the task in background

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")    # it will load the model

def summarize_text():
    input_text = input_box.get("1.0", tk.END).strip()  # input text displayed here
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text to summarize.")  # it gives warning if input is empty
        return

    summarize_button.config(state=tk.DISABLED)   # it will disable the summarize button to avoid multiple clicks on summarize button
    summary_box.delete("1.0", tk.END)  # it clears the previous summary
    summary_box.insert(tk.END, "Summarizing... Please wait.")  # it will show loading message

    # this function will handle the summarization task
    def process():
        try:
            summary = summarizer(input_text, max_length=150, min_length=30, do_sample=False)    # it will run the model
            summary_text = summary[0]['summary_text']           # it display result
            summary_box.delete("1.0", tk.END)  
            summary_box.insert(tk.END, summary_text)  # it display the summary
        except Exception as e:
           
            messagebox.showerror("Error", str(e))   # it will show the error if any occured
        finally:
            summarize_button.config(state=tk.NORMAL)  # it will Re-enable the button after processing

    
    threading.Thread(target=process).start()

root = tk.Tk()
root.title("Text Summarization Tool")  # it displays the title
root.geometry("800x600")  # it represents size
root.resizable(False, False)  # Prevent resizing

tk.Label(root, text="Enter text to summarize:", font=("Helvetica", 12)).pack(pady=5)   # it display input text

input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=15, font=("Helvetica", 10))   # it display scrollbar
input_box.pack(pady=10)

summarize_button = tk.Button(root, text="Summarize", command=summarize_text, font=("Helvetica", 12), bg="#4CAF50", fg="white")  # it displays summarization button
summarize_button.pack(pady=10)

tk.Label(root, text="Summary:", font=("Helvetica", 12)).pack(pady=5)

summary_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, font=("Helvetica", 10))   # Scrollable output text box for displaying summary
summary_box.pack(pady=10)

root.mainloop()
