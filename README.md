# Gemini Screen OCR

A simple Python script that uses Google's Gemini API to perform high-accuracy Optical Character Recognition (OCR) on a selected region of the screen.

## Features

-   Trigger with a global hotkey (`Ctrl+Shift+X`).
-   Select any part of your screen.
-   Uses the powerful `gemini-1.5-flash` model for accurate text extraction.
-   Automatically copies the extracted text to your clipboard.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ahmadkasimcse/gemini-ocr.git
    cd your-repo-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key:**
    -   Create a file named `.env` in the project directory.
    -   Add your Google Gemini API key to it like this:
        ```
        GEMINI_API_KEY="your_api_key_here"
        ```

## Usage

Run the script from your terminal:

```bash
python gemini_ocr.py
```

The script will run in the background. Press `Ctrl+Shift+X` to activate the screen capture, select a region, and the extracted text will be copied to your clipboard.
