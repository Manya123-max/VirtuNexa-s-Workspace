Goal

To create a Python script that scrapes the latest news headlines from a website and displays them in a user-friendly graphical user interface (GUI). The application allows users to input a news website URL, fetch unique headlines, and display them in an organized format. It also logs operations and maintains a history of activities.

Features:-
1. News Scraping
Fetches the latest news headlines from the provided URL using Python’s requests library and lxml for HTML parsing.
Supports dynamic XPath patterns to extract headlines from multiple website structures.
Filters and displays unique news headlines only, avoiding repetition.
Handles exceptions gracefully to manage invalid URLs or server errors.

2. User Interface
Built using the tkinter library for a simple, interactive GUI.
Provides input fields for entering a URL and buttons for fetching news, displaying history, and closing the application.
Displays fetched news headlines in a scrollable text box.

4. Operation Logs
Logs every URL request and its outcome to a text file (news_scraper_logs.txt) for tracking and debugging purposes.
Includes a feature to display operation history directly in the GUI.
