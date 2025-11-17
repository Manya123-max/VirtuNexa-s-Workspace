# News Scraper & Recommender

A Python-based desktop application developed during my internship at Virtunexa that aggregates news headlines from multiple sources and allows users to filter by category.

## 📋 Project Overview

This project was created as part of my Python internship at Virtunexa. It demonstrates web scraping, GUI development, and database management skills by building a comprehensive news aggregation tool.

## ✨ Features

- **Multi-Source News Aggregation**: Fetches headlines from 6+ major news sources
  - BBC
  - CNN
  - TechCrunch
  - ESPN
  - Reuters
  - The Guardian
  
- **Custom Source Support**: Add any news website URL for scraping

- **Category Filtering**: Browse news by topic
  - General
  - Sports
  - Business
  - Technology
  - Entertainment
  - Health
  - Science
  - Politics

- **User-Friendly GUI**: Clean, intuitive interface built with Tkinter

- **History Tracking**: SQLite database stores user browsing history

- **Operation Logging**: Automatic logging of all scraping operations

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter**: GUI framework
- **Requests**: HTTP library for web scraping
- **LXML**: HTML parsing
- **SQLite3**: Database for preferences and history
- **DateTime**: Timestamp management

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/news-scraper-recommender.git
cd news-scraper-recommender
```

2. **Install required dependencies**
```bash
pip install requests lxml
```

Note: Tkinter comes pre-installed with Python

3. **Run the application**
```bash
python main.py
```

## 💻 Usage

1. **Launch the application**
   - Run the script to open the GUI

2. **Select news sources**
   - Check boxes for desired news outlets
   - Or enter a custom news source URL

3. **Choose a category**
   - Select from the dropdown menu

4. **Fetch news**
   - Click "Fetch News" button
   - View aggregated headlines in a new window

## 📁 Project Structure

```
news-scraper-recommender/
│
├── main.py                      # Main application file
├── news_preferences.db          # SQLite database (auto-generated)
├── news_scraper_logs.txt        # Operation logs (auto-generated)
└── README.md                    # Project documentation
```

## 🗄️ Database Schema

### Preferences Table
```sql
CREATE TABLE preferences (
    id INTEGER PRIMARY KEY,
    user TEXT,
    category TEXT
)
```

### History Table
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    source TEXT,
    category TEXT
)
```

## 🔍 How It Works

1. **Web Scraping**: Uses XPath expressions to extract headlines from HTML elements (h1, h2, h3, links)
2. **URL Mapping**: Automatically appends category-specific paths to base URLs
3. **Data Filtering**: Removes duplicates and short strings to ensure quality headlines
4. **Storage**: Saves user interaction history in SQLite database
5. **Logging**: Records all operations with timestamps for debugging

## 🚀 Future Enhancements

- [ ] Add article summaries using NLP
- [ ] Implement user authentication
- [ ] Create personalized recommendations based on reading history
- [ ] Add export functionality (CSV, PDF)
- [ ] Include sentiment analysis of headlines
- [ ] Mobile-responsive web version

## ⚠️ Limitations

- Scraping effectiveness depends on website structure
- Some sites may block automated requests
- Requires internet connection
- Web scraping may break if source websites update their HTML structure

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author
**Manya Vishwakarma**
