import os
import tkinter as tk
from tkinter import messagebox, Toplevel
import requests
import sqlite3
import threading
import time
import csv

# Database setup
def setup_database():
    try:
        conn = sqlite3.connect("assistant_history.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                query TEXT, 
                response TEXT
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error setting up database: {e}")

# Save query to history (Database + CSV)
def save_to_history(query, response):
    try:
        # Save to database
        conn = sqlite3.connect("assistant_history.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (query, response) VALUES (?, ?)", (query, response))
        conn.commit()
        conn.close()

        # Save to CSV file
        file_exists = os.path.isfile("assistant_history.csv")
        with open("assistant_history.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Query", "Response"])  # Write header if file does not exist
            writer.writerow([query, response])
    except Exception as e:
        print(f"Error saving history: {e}")

# Fetch weather information
def open_weather_window():
    def get_weather():
        city = weather_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        api_key = "a75f0f089364eb8b408d7b24d52d4535"  # Replace with your WeatherStack API key
        url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
        try:
            response = requests.get(url)
            data = response.json()

            if "current" in data:
                weather = f"Weather in {city}: {data['current']['weather_descriptions'][0]}, {data['current']['temperature']}°C"
            else:
                weather = f"Error: {data.get('error', {}).get('info', 'City not found.')}"
        except requests.exceptions.RequestException as e:
            weather = f"Error fetching weather data: {str(e)}"

        text_area.insert(tk.END, f"You: Weather in {city}\nAssistant: {weather}\n\n")
        save_to_history(f"Weather query: {city}", weather)
        weather_window.destroy()

    weather_window = Toplevel(root)
    weather_window.title("Weather Info")
    weather_window.geometry("300x150")
    tk.Label(weather_window, text="Enter City Name:").pack()
    weather_entry = tk.Entry(weather_window)
    weather_entry.pack()
    tk.Button(weather_window, text="Get Weather", command=get_weather).pack()

# Set reminders
def open_reminder_window():
    def set_reminder():
        reminder_text = reminder_entry.get().strip()
        try:
            delay = int(reminder_time_entry.get().strip())

            def reminder_thread():
                time.sleep(delay * 60)
                messagebox.showinfo("Reminder", f"Reminder: {reminder_text}")

            threading.Thread(target=reminder_thread, daemon=True).start()
            save_to_history(f"Set Reminder: {reminder_text}", f"Reminder set for {delay} minutes.")
            text_area.insert(tk.END, f"You: {reminder_text}\nAssistant: Reminder set for {delay} minutes.\n\n")
            reminder_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid reminder format. Enter time in minutes.")

    reminder_window = Toplevel(root)
    reminder_window.title("Set Reminder")
    reminder_window.geometry("300x150")
    tk.Label(reminder_window, text="Enter Reminder:").pack()
    reminder_entry = tk.Entry(reminder_window)
    reminder_entry.pack()
    tk.Label(reminder_window, text="Time in Minutes:").pack()
    reminder_time_entry = tk.Entry(reminder_window)
    reminder_time_entry.pack()
    tk.Button(reminder_window, text="Set Reminder", command=set_reminder).pack()

def process_input():
    query = entry.get().strip().lower()  # Convert input to lowercase
    if not query:
        return

    responses = {
        "hello": "Hello! How can I assist you?",
        "who are you": "I am your virtual assistant!",
        "what is your name": "I am a simple assistant built with Python!",
        "bye": "Goodbye! Have a great day!",
        "how are you": "I'm just a virtual assistant, but I'm here to help you!",
        "what can you do": "I can fetch weather info, set reminders, and answer basic questions.",
        "tell me a joke": "Why don’t skeletons fight each other? Because they don’t have the guts!",
        "who created you": "I was created by a Python developer to assist users like you!",
        "what is python": "Python is a high-level programming language known for its simplicity and readability."
    }

    # Get response or default message
    response = responses.get(query, "I'm not sure how to respond to that, but I'm here to help!")

    # Display conversation in the UI
    text_area.insert(tk.END, f"You: {query}\nAssistant: {response}\n\n")

    # Save the conversation history
    save_to_history(query, response)

    # Clear input field
    entry.delete(0, tk.END)

# UI setup
root = tk.Tk()
root.title("Virtual Assistant")
root.geometry("400x500")

title_label = tk.Label(root, text="Virtual Assistant", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

text_area = tk.Text(root, height=15, width=45)
text_area.pack(pady=5)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

ask_button = tk.Button(button_frame, text="Ask", command=process_input)
ask_button.grid(row=0, column=0, padx=5)

weather_button = tk.Button(button_frame, text="Weather", command=open_weather_window)
weather_button.grid(row=0, column=1, padx=5)

reminder_button = tk.Button(button_frame, text="Set Reminder", command=open_reminder_window)
reminder_button.grid(row=0, column=2, padx=5)

setup_database()
root.mainloop()
