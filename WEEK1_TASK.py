import requests
import lxml.html
import tkinter as tk
from tkinter import messagebox
import datetime


# Function to fetch news headlines
def fetch_news(url):
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML using lxml
        tree = lxml.html.fromstring(response.content)

        # Generalized XPath patterns to fetch headlines
        headlines = tree.xpath(
            "//h1/text() | "  # Main headlines
            "//h2/text() | "  # Subheadlines
            "//h3/text() | "  # Tertiary headlines
            "//a[contains(@href, '/news') or contains(@href, '/article')]/text() | "  # Links with 'news' or 'article'
            "//div[contains(@class, 'headline')]/text() | "  # Divs with 'headline' in class
            "//span[contains(@class, 'headline')]/text()"  # Spans with 'headline' in class
        )

        # Filter and clean the headlines, ensuring uniqueness
        filtered_headlines = list(
            {headline.strip() for headline in headlines if len(headline.strip()) > 15}
        )

        if not filtered_headlines:
            return ["No headlines found for this URL."]
        return filtered_headlines

    except requests.exceptions.RequestException as e:
        return [f"Error fetching news: {str(e)}"]

# Function to log operations
def log_operation(operation):
    with open("news_scraper_logs.txt", "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {operation}\n")


# Function to read log history
def read_history():
    try:
        with open("news_scraper_logs.txt", "r") as log_file:
            return log_file.readlines()
    except FileNotFoundError:
        return ["No history available."]


# GUI Application
def gui_app():
    def fetch_and_display_news():
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        headlines = fetch_news(url)
        news_text.delete(1.0, tk.END)
        for i, headline in enumerate(headlines, start=1):
            news_text.insert(tk.END, f"{i}. {headline}\n")
        log_operation(f"Fetched news headlines from {url}.")

    def display_history():
        history = read_history()
        news_text.delete(1.0, tk.END)
        news_text.insert(tk.END, "--- Operation History ---\n")
        for line in history:
            news_text.insert(tk.END, line)

    root = tk.Tk()
    root.title("News Scraper")

    tk.Label(root, text="Enter News URL:").pack(pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    fetch_button = tk.Button(root, text="Fetch News", command=fetch_and_display_news, bg="blue", fg="white")
    fetch_button.pack(pady=10)

    history_button = tk.Button(root, text="Show History", command=display_history, bg="green", fg="white")
    history_button.pack(pady=10)

    news_text = tk.Text(root, wrap=tk.WORD, width=60, height=20, bg="lightgrey")
    news_text.pack(pady=10)

    close_button = tk.Button(root, text="Close", command=root.destroy, bg="red", fg="white")
    close_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    gui_app()
