import os
import threading
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import pyperclip
import keyboard
import tkinter as tk
from mss import mss
from pystray import MenuItem as item
import pystray

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

# --- OCR and Capture Functions (No changes here) ---

def capture_screen_region():
    # This function remains the same as before
    print("Waiting for screen region selection...")
    root = tk.Tk()
    root.attributes("-alpha", 0.3)
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.wait_visibility(root)
    canvas = tk.Canvas(root, cursor="cross", bg="grey")
    canvas.pack(fill="both", expand=True)
    start_x, start_y = 0, 0
    rect = None
    screenshot_path = "temp_screenshot.png"
    
    def on_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_drag(event):
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_release(event):
        end_x, end_y = event.x, event.y
        root.destroy()
        left, top = min(start_x, end_x), min(start_y, end_y)
        right, bottom = max(start_x, end_x), max(start_y, end_y)
        monitor = {'top': top, 'left': left, 'width': right - left, 'height': bottom - top}
        with mss() as sct:
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.mainloop()
    return screenshot_path if os.path.exists(screenshot_path) else None

def get_text_from_image(image_path):
    # This function also remains the same
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = "Extract the text precisely as it appears in this image. Do not add any extra commentary, explanation, or formatting."
        print("Sending image to Gemini for OCR...")
        with Image.open(image_path) as img:
            response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Cleaned up {image_path}")

def main_ocr_process():
    # This function also remains the same
    screenshot_file = capture_screen_region()
    if screenshot_file:
        extracted_text = get_text_from_image(screenshot_file)
        if extracted_text:
            pyperclip.copy(extracted_text)
            print("\n--- OCR Result ---")
            print(extracted_text)
            print("--------------------\nText copied to clipboard! ✅")
        else:
            print("Could not extract text or an error occurred.")

# --- NEW: System Tray and Threading Logic ---

def start_keyboard_listener():
    """Sets up and runs the keyboard listener."""
    keyboard.add_hotkey('ctrl+shift+x', main_ocr_process)
    keyboard.wait()

def exit_action(icon, item):
    """Function to stop the listeners and exit the app."""
    print("Exiting application...")
    keyboard.unhook_all() # Disable the hotkey
    icon.stop() # Stop the tray icon
    os._exit(0) # Force exit the script

def main():
    """Main function to set up threading and the system tray icon."""
    # Run the keyboard listener in a separate thread so it doesn't block the tray icon
    listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    listener_thread.start()
    
    # Create the system tray icon
    image = Image.open("icon.png")
    menu = (item('Exit', exit_action),)
    icon = pystray.Icon("GeminiOCR", image, "Gemini OCR", menu)
    
    print("Gemini OCR script is running in the background. Press 'ctrl+shift+x' to capture.")
    icon.run()

if __name__ == "__main__":
    main()