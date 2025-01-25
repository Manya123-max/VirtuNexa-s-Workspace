import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from googletrans import Translator
import speech_recognition as sr
import sqlite3
import csv

# Database setup
def setup_database():
    connection = sqlite3.connect("translation_history.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS History (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            source_language TEXT,
            destination_language TEXT,
            translated_text TEXT
        )
    """)
    connection.commit()
    connection.close()

# Function to save history to the database
def save_to_history(input_text, source_language, destination_language, translated_text):
    connection = sqlite3.connect("translation_history.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO History (input_text, source_language, destination_language, translated_text)
        VALUES (?, ?, ?, ?)
    """, (input_text, source_language, destination_language, translated_text))
    connection.commit()
    connection.close()

# Function to view history
def view_history():
    connection = sqlite3.connect("translation_history.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM History")
    records = cursor.fetchall()
    connection.close()

    # Display history in a new window
    history_window = tk.Toplevel(app)
    history_window.title("Translation History")
    history_window.geometry("600x400")

    # Table headers
    tk.Label(history_window, text="ID", width=5, borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
    tk.Label(history_window, text="Input Text", width=20, borderwidth=1, relief="solid").grid(row=0, column=1, sticky="nsew")
    tk.Label(history_window, text="Source Language", width=15, borderwidth=1, relief="solid").grid(row=0, column=2, sticky="nsew")
    tk.Label(history_window, text="Destination Language", width=15, borderwidth=1, relief="solid").grid(row=0, column=3, sticky="nsew")
    tk.Label(history_window, text="Translated Text", width=20, borderwidth=1, relief="solid").grid(row=0, column=4, sticky="nsew")

    # Display records
    for i, record in enumerate(records, start=1):
        tk.Label(history_window, text=record[0], borderwidth=1, relief="solid").grid(row=i, column=0, sticky="nsew")
        tk.Label(history_window, text=record[1], borderwidth=1, relief="solid").grid(row=i, column=1, sticky="nsew")
        tk.Label(history_window, text=record[2], borderwidth=1, relief="solid").grid(row=i, column=2, sticky="nsew")
        tk.Label(history_window, text=record[3], borderwidth=1, relief="solid").grid(row=i, column=3, sticky="nsew")
        tk.Label(history_window, text=record[4], borderwidth=1, relief="solid").grid(row=i, column=4, sticky="nsew")

# Function to download history as a file
def download_history():
    connection = sqlite3.connect("translation_history.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM History")
    records = cursor.fetchall()
    connection.close()

    if not records:
        messagebox.showinfo("Info", "No history available to download.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")],
        title="Save History As"
    )
    if file_path:
        if file_path.endswith(".csv"):
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Input Text", "Source Language", "Destination Language", "Translated Text"])
                writer.writerows(records)
            messagebox.showinfo("Success", "History saved as CSV file successfully.")
        else:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("ID\tInput Text\tSource Language\tDestination Language\tTranslated Text\n")
                for record in records:
                    file.write("\t".join(map(str, record)) + "\n")
            messagebox.showinfo("Success", "History saved as text file successfully.")

# Function to handle speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Listening", "Please speak now...")
            audio = recognizer.listen(source, timeout=5)  # Wait for 5 seconds of speech
            text = recognizer.recognize_google(audio)  # Recognize speech using Google Web Speech API
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Failed to connect to the speech recognition service.")
        except Exception as e:
            messagebox.showerror("Error", f"Speech to text failed: {e}")

# Function to translate text
def translate_text():
    translator = Translator()
    try:
        source_text = input_text.get(1.0, tk.END).strip()
        if not source_text:
            raise ValueError("Input text cannot be empty.")

        src_language = source_lang.get()
        dest_language = dest_lang.get()

        if not src_language or not dest_language:
            raise ValueError("Please select both source and destination languages.")

        # Perform translation
        translation = translator.translate(source_text, src=src_language, dest=dest_language)
        translated_text = translation.text

        # Display the translated text in the output box
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, translated_text)

        # Save to history
        save_to_history(source_text, src_language, dest_language, translated_text)
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")

# Initialize the GUI application
app = tk.Tk()
app.title("Multilingual Translator with Speech to Text")
app.geometry("800x600")

# Setup the database
setup_database()

# Source text input label and box
tk.Label(app, text="Input Text:").grid(row=0, column=0, padx=10, pady=10)
input_text = tk.Text(app, height=5, width=70)
input_text.grid(row=0, column=1, padx=10, pady=10)

# Source and destination language selection
tk.Label(app, text="Source Language:").grid(row=1, column=0, padx=10, pady=5)
source_lang = ttk.Combobox(app, width=25)
source_lang['values'] = ["auto", "en", "es", "fr", "de", "zh-cn", "hi", "ar", "ru", "ja"]  # Add more language codes as needed
source_lang.set("auto")  # Default: Auto-detect language
source_lang.grid(row=1, column=1, sticky="w", padx=10, pady=5)

tk.Label(app, text="Destination Language:").grid(row=2, column=0, padx=10, pady=5)
dest_lang = ttk.Combobox(app, width=25)
dest_lang['values'] = ["en", "es", "fr", "de", "zh-cn", "hi", "ar", "ru", "ja"]  # Add more language codes as needed
dest_lang.set("en")  # Default: English
dest_lang.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Output text label and box
tk.Label(app, text="Translated Text:").grid(row=3, column=0, padx=10, pady=10)
output_text = tk.Text(app, height=5, width=70)
output_text.grid(row=3, column=1, padx=10, pady=10)

# Buttons for translating, speech to text, viewing history, and downloading history
translate_button = tk.Button(app, text="Translate", command=translate_text)
translate_button.grid(row=4, column=1, sticky="w", padx=10, pady=10)

speech_button = tk.Button(app, text="Speech to Text", command=speech_to_text)
speech_button.grid(row=4, column=0, sticky="e", padx=10, pady=10)

history_button = tk.Button(app, text="View History", command=view_history)
history_button.grid(row=5, column=0, sticky="e", padx=10, pady=10)

download_button = tk.Button(app, text="Download History", command=download_history)
download_button.grid(row=5, column=1, sticky="w", padx=10, pady=10)

# Main event loop
app.mainloop()
