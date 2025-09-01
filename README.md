# Gemini Screen OCR 🚀

A lightweight, background utility for Windows that uses Google's Gemini API to perform high-accuracy Optical Character Recognition (OCR) on any selected region of your screen.

The script runs silently in the system tray, is triggered by a global hotkey, and automatically copies the extracted text to your clipboard.



## Features

* **High-Accuracy OCR**: Leverages the `gemini-1.5-flash` model for superior text recognition.
* **System Tray Integration**: Runs silently in the background with an icon in the system tray.
* **Global Hotkey**: Use `Ctrl+Shift+X` from any application to start a screen capture (can be changed!).
* **Silent & Windowless**: No command prompt window is visible during operation.
* **Auto-Start Support**: Can be configured to launch automatically when you log into Windows.
* **Safe Exit**: Easily close the application from the system tray menu.

## Installation & Setup

Follow these steps to get the application running on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/ahmadkasimcse/gemini-ocr.git
cd your-repo-name
```

### 2. Install Dependencies
Make sure you have Python 3 installed. Then, run the following command in the project directory to install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
* Create a file named `.env` in the project directory.
* Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/).
* Add your key to the `.env` file like this:
    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

### 4. Add an Icon
* You may provide an icon for the system tray, however, there is a default one.
* Create or download a small, square `.png` image (e.g., 64x64 pixels).
* Save it in the project directory with the exact name **`icon.png`**.

## Usage

For the best experience, it is recommended to run the script as a windowless application that starts with Windows.

### Recommended: Auto-Start on Windows Login
1.  **Open the Startup Folder**: Press `Win + R` to open the Run dialog, type `shell:startup`, and press Enter.
2.  **Create a Shortcut**: Right-click on your `gemini_ocr.pyw` file and select "Create shortcut".
3.  **Move the Shortcut**: Drag the newly created shortcut into the Startup folder.

The application will now start automatically and silently every time you log in.

### Manual Start
You can run the script manually for testing by running **`pythonw gemini_ocr.pyw`**.

## How to Use
1.  Press the global hotkey **`Ctrl+Shift+X`**.
2.  Your screen will dim. Click and drag to select the area with the text you want to copy.
3.  Release the mouse button.
4.  After a moment, the extracted text will be automatically copied to your clipboard.

## Exiting the Application
To close the program, find its icon in your system tray, right-click it, and select **"Exit"**.
