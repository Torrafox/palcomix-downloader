# Palcomix Free Comic Downloader

A simple Python script to **automatically download full-sized comic pages** from [Palcomix](https://www.palcomix.com/freecomics.html).

### FREE COMICS ONLY!

## 📥 Features
- Extracts **all comic pages** from the given URL.
- Downloads **full-sized images**, not thumbnails.
- Saves files in `~/Downloads/COMIC_NAME` with **proper naming** (decoded from URL).
- Bypasses site restrictions using **headers and referer spoofing**.

## 🔧 Requirements
- Python 3.x

## 📦 Installation

For **Linux/macOS**:
```bash
git clone https://github.com/Torrafox/palcomix-downloader.git && cd palcomix-downloader && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

For **Windows**:
```bash
git clone https://github.com/Torrafox/palcomix-downloader.git && cd palcomix-downloader && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

## 🚀 Usage
1. Run the script:
   ```bash
   python main.py
   ```
2. Enter the **landing page URL** of a Palcomix comic (e.g. `https://palcomix.com/digilove/index.html`).
3. The script will automatically find and download all pages.

## 📂 Output
- Comics are saved in:
  ```
  ~/Downloads/COMIC_NAME
  ```
- Example:
  ```
  ~/Downloads/Digital Love/
  ├── 01 Digital Love.jpg
  ├── 02 Digital Love.png
  ├── ...
  ```

## ⚠ Disclaimer
This script is for **personal use only**. Respect the original creators and their work.
