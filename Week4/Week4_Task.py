import requests
import lxml.html
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import datetime
import sqlite3


# Function to initialize the preferences database
def init_db():
    conn = sqlite3.connect("news_preferences.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY,
            user TEXT,
            category TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()


# Function to log operations
def log_operation(operation):
    with open("news_scraper_logs.txt", "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {operation}\n")


# Function to store user operation history in the database
def store_history(source, category):
    conn = sqlite3.connect("news_preferences.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (timestamp, source, category) VALUES (?, ?, ?)",
                   (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source, category))
    conn.commit()
    conn.close()


# Function to map category to news URLs
def get_category_url(base_url, category):
    category_map = {
        "Sports": "/sport",
        "Business": "/business",
        "Technology": "/technology",
        "Entertainment": "/entertainment",
        "Health": "/health",
        "Science": "/science",
        "Politics": "/politics"
    }
    return base_url + category_map.get(category, "")


# Function to fetch news headlines from multiple sources based on category
def fetch_news_from_sources(selected_sources, selected_category):
    sources = {
        "BBC": "https://www.bbc.com/news",
        "CNN": "https://edition.cnn.com",
        "TechCrunch": "https://techcrunch.com",
        "ESPN": "https://www.espn.com",
        "Reuters": "https://www.reuters.com",
        "The Guardian": "https://www.theguardian.com"
    }

    all_headlines = {}
    for source in selected_sources:
        base_url = sources.get(source, source)  # Use predefined URL or user-entered custom URL
        category_url = get_category_url(base_url, selected_category)
        all_headlines[source] = fetch_news(category_url)
        store_history(source, selected_category)  # Store the history in the database
    return all_headlines


# Function to fetch news headlines
def fetch_news(url):
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response.raise_for_status()
        tree = lxml.html.fromstring(response.content)
        headlines = tree.xpath(
            "//h1 | //h2 | //h3 | //a[contains(@href, '/news') or contains(@href, '/article')] | //span[contains(@class, 'headline')]")

        extracted_headlines = [headline.text_content().strip() for headline in headlines if
                               headline.text_content().strip()]
        filtered_headlines = list({headline for headline in extracted_headlines if len(headline) > 15})

        return filtered_headlines if filtered_headlines else ["No headlines found."]
    except requests.exceptions.RequestException as e:
        return [f"Error fetching news: {str(e)}"]


# GUI Application
def gui_app():
    root = tk.Tk()
    root.title("News Scraper & Recommender")
    root.geometry("900x600")
    root.configure(bg="#e3f2fd")

    title_label = tk.Label(root, text="News Scraper & Recommender", font=("Arial", 18, "bold"), bg="#2196F3",
                           fg="white", pady=10)
    title_label.pack(fill=tk.X)

    frame = tk.Frame(root, bg="#ffffff", padx=15, pady=15, relief=tk.GROOVE, borderwidth=3)
    frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Select News Sources:", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=0, column=0,
                                                                                                sticky='w', pady=5)

    source_vars = {}
    sources = ["BBC", "CNN", "TechCrunch", "ESPN", "Reuters", "The Guardian"]
    for i, source in enumerate(sources):
        source_vars[source] = tk.BooleanVar()
        tk.Checkbutton(frame, text=source, variable=source_vars[source], bg="#ffffff").grid(row=i + 1, column=0,
                                                                                            sticky='w')

    custom_source_entry = tk.Entry(frame, width=50)
    tk.Label(frame, text="Or Enter Custom News Source URL:", bg="#ffffff").grid(row=7, column=0, pady=5, sticky='w')
    custom_source_entry.grid(row=8, column=0, pady=5)

    tk.Label(frame, text="Select News Category:", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=0, column=1,
                                                                                                 sticky='w', padx=20)
    category_var = tk.StringVar(value="General")
    category_options = ["General", "Sports", "Business", "Technology", "Entertainment", "Health", "Science", "Politics"]
    category_menu = ttk.Combobox(frame, textvariable=category_var, values=category_options, state="readonly")
    category_menu.grid(row=1, column=1, padx=20, pady=5)

    def fetch_and_display_news():
        selected_sources = [source for source, var in source_vars.items() if var.get()]
        if custom_source_entry.get():
            selected_sources.append(custom_source_entry.get())
        selected_category = category_var.get()

        all_news = fetch_news_from_sources(selected_sources, selected_category)
        log_operation("Fetched news headlines from selected sources.")

        news_window = tk.Toplevel(root)
        news_window.title("Fetched News")
        news_window.geometry("700x500")

        text_area = scrolledtext.ScrolledText(news_window, wrap=tk.WORD, font=("Arial", 12))
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for source, headlines in all_news.items():
            text_area.insert(tk.END, f"\n{source}\n{'=' * 50}\n", "header")
            for i, headline in enumerate(headlines, start=1):
                text_area.insert(tk.END, f"{i}. {headline}\n", "content")
            text_area.insert(tk.END, "\n")
        text_area.tag_config("header", font=("Arial", 14, "bold"), foreground="#007BFF")
        text_area.tag_config("content", font=("Arial", 12))

    fetch_button = tk.Button(root, text="Fetch News", command=fetch_and_display_news, bg="#007BFF", fg="white",
                             font=("Arial", 12, "bold"))
    fetch_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    init_db()
    gui_app()

