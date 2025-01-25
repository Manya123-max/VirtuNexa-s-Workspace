# Multilingual Translator with Speech-to-Text

This is a Python-based multilingual translator that allows users to input text, translate it between languages, and save the translation history. It also supports speech-to-text functionality for easy text input. The application is built using **Tkinter**, **Googletrans**, and **SpeechRecognition** libraries.

---

## 🚀 Features

- Translate text between multiple languages.
- Automatically detect the source language or choose manually.
- Speech-to-text functionality for input via a microphone.
- Save translation history to a local SQLite database.
- View translation history in a GUI table.
- Download the translation history as a `.txt` or `.csv` file.

---

## 🛠️ Requirements

Make sure you have the following installed:

- Python 3.x
- pip (Python package manager)

Install the required Python libraries by running the following command:

```bash
pip install googletrans==4.0.0-rc1 SpeechRecognition tk
```

---

## 📂 Project Structure

```
|-- translation_app.py      # Main Python script
|-- translation_history.db  # SQLite database (created automatically)
|-- README.md               # This file
```

---

## 🔧 How to Run the Application

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/multilingual-translator.git
   cd multilingual-translator
   ```

2. Run the script:

   ```bash
   python translation_app.py
   ```

3. Use the GUI to translate text, use speech-to-text, view translation history, and download the history.

---

## 🎨 GUI Overview

- **Input Text Box**: Enter the text you want to translate.
- **Source Language Selector**: Choose the source language or set it to `auto` for automatic detection.
- **Destination Language Selector**: Choose the language to which you want to translate.
- **Translated Text Box**: Displays the translated text.
- **Buttons**:
  - `Translate`: Perform the translation.
  - `Speech to Text`: Use your microphone to input text via speech.
  - `View History`: Open a new window to see all previous translations.
  - `Download History`: Save the translation history as a `.txt` or `.csv` file.

---

## 🗂️ Supported Languages

The app supports a wide range of languages such as:

- English (`en`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Chinese Simplified (`zh-cn`)
- Hindi (`hi`)
- Arabic (`ar`)
- Russian (`ru`)
- Japanese (`ja`)

You can customize this list by editing the `source_lang` and `dest_lang` values in the script.

---

## 📥 Saving and Viewing History

- Every translation is saved in database (`translation_history.txt`).
- You can view and download the saved history using the provided buttons in the GUI.

---

## 📝 Known Issues

- **SpeechRecognition** may require an active internet connection for accurate recognition.
- **Googletrans** relies on the Google Translate API, and temporary API changes might occasionally disrupt the translation service.

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests to improve the project. Suggestions and bug reports are welcome!

---

## 📧 Contact

If you have any questions or suggestions, feel free to contact me at **manyadhiman19nov2000@gmail.com**.


