# Speechi PRO

**Speechi PRO** is a real-time speech-to-text translation application built with **Python**, **CustomTkinter**, and **Machine Learning** technologies.  
It listens to your speech, translates it instantly into another language, and speaks the translation out loud — all through a clean and simple interface!

---

## Features

- 🎙️ **Speech Recognition**: Converts your voice into text quickly and accurately.
- 🌍 **Instant Translation**: Supports multiple languages like Turkish, English, German, French, Japanese, Korean, Chinese, Russian, and Danish.
- 🔈 **Text-to-Speech**: Reads the translated text aloud using natural-sounding voices.
- 🖥️ **Modern GUI**: Designed with a sleek and user-friendly interface using **CustomTkinter**.
- 🔄 **Automatic & Manual Modes**:
  - **Automatic Mode**: Speechi PRO asks you which languages you want to use and then starts translating automatically.
  - **Manual Mode**: You select the source and destination languages manually and click a button to start listening.
- 📝 **Conversation History**: View all your conversations — both the original and translated texts.

---

## Supported Languages

- Turkish
- English
- German
- French
- Korean
- Japanese
- Chinese
- Russian
- Danish

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/SpeechiPro.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python speechi_pro.py
```

---

## Requirements

- Python 3.8 or higher
- Modules:
  - `speechrecognition`
  - `googletrans`
  - `gTTS`
  - `playsound`
  - `customtkinter`
  - `pyaudio` (required for microphone input)

You can install them all easily with:

```bash
pip install SpeechRecognition googletrans==4.0.0-rc1 gTTS playsound==1.2.2 customtkinter pyaudio
```

> **Note**: On some systems, you might need additional setup for `PyAudio`.  
> For Windows:  
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

---

## Screenshots
![image](https://github.com/user-attachments/assets/3452d7d7-762e-45e1-9c98-d65a791b0583)


## Usage

- **Automatic Mode**:  
  - The app will ask you which languages you want to use by voice.  
  - Example: Say "Turkish Japanese" to set source and target languages.
  - It will automatically start listening and translating.

- **Manual Mode**:  
  - Select source and target languages manually from the dropdowns.
  - Click "Start Listening" to begin the translation process.

---

## License

This project is licensed under the MIT License — feel free to use and modify it!

---

## Credits

- Built using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Translation powered by [Google Translate API](https://pypi.org/project/googletrans/)
- Speech Recognition powered by [Google Speech Recognition](https://pypi.org/project/SpeechRecognition/)

