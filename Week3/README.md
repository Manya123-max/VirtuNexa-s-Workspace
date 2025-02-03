# Virtual Assistant in Python

## Overview
This is a simple Virtual Assistant built using Python and Tkinter. It can respond to basic user queries, fetch weather updates, and set reminders.

## Features
- **Basic Chatbot**: Responds to common queries.
- **Weather Information**: Fetches weather updates using the WeatherStack API.
- **Reminder System**: Allows users to set timed reminders.
- **Database & CSV Logging**: Saves query history in SQLite and CSV files.

## Requirements
Make sure you have the following dependencies installed:

```sh
pip install requests
```

## How to Run
1. Clone the repository or download the script.
2. Open a terminal and navigate to the project folder.
3. Run the script using:
   ```sh
   python virtual_assistant.py
   ```

## File Structure
- `virtual_assistant.py` - Main script that runs the assistant.
- `assistant_history.db` - SQLite database storing conversation history.
- `assistant_history.csv` - CSV file logging chat history.

## Usage
1. Open the application.
2. Type a query (e.g., "Hello", "Tell me a joke", "Weather in London").
3. Set reminders by clicking the "Set Reminder" button.
4. Fetch weather by clicking the "Weather" button.

## API Key Setup
This project uses WeatherStack API for weather data. Replace the `api_key` in the `open_weather_window()` function with your API key.

## Contributions
Feel free to contribute by submitting issues and pull requests.

## Future Enhancements
1. Voice Command Support: Integrate speech recognition to interact via voice commands.
2. AI-Powered Responses: Use NLP to generate intelligent responses.
3. Task Scheduler: Extend reminder functionality to schedule tasks with notifications.
4. Multi-Language Support: Enable responses in multiple languages.
5. Weather API Optimization: Implement caching to reduce API requests.
