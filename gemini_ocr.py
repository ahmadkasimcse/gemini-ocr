import os
from dotenv import load_dotenv 
import google.generativeai as genai
from PIL import Image
import pyperclip
import keyboard
import tkinter as tk
from mss import mss
import pyautogui


# --- Configuration ---
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY") 

# Add a check to ensure the API key was loaded
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")


# --- Main Functions ---

def capture_screen_region():
    """
    Creates a transparent overlay to let the user select a screen region.
    Returns the file path of the captured screenshot.
    """
    print("Waiting for screen region selection...")

    # Create a transparent, borderless window
    root = tk.Tk()
    root.attributes("-alpha", 0.3) # Transparency
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
        root.destroy() # Close the selection window

        # Ensure coordinates are top-left and bottom-right
        left = min(start_x, end_x)
        top = min(start_y, end_y)
        right = max(start_x, end_x)
        bottom = max(start_y, end_y)
        
        # Define the monitor region to capture
        monitor = {'top': top, 'left': left, 'width': right - left, 'height': bottom - top}

        # Capture the screen using mss
        with mss() as sct:
            sct_img = sct.grab(monitor)
            # Convert to a PIL Image and save
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(screenshot_path)
            
        print(f"Screenshot saved to {screenshot_path}")

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()
    return screenshot_path if os.path.exists(screenshot_path) else None

def get_text_from_image(image_path):
    """
    Sends the image to the Gemini API and returns the extracted text.
    """
    try:
        genai.configure(api_key=API_KEY)
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = "Extract the text precisely as it appears in this image. Do not add any extra commentary, explanation, or formatting."
        
        print("Sending image to Gemini for OCR...")
        # Use a 'with' block to ensure the image file is closed automatically
        # This is the fix for any permission errors.
        with Image.open(image_path) as img:
            response = model.generate_content([prompt, img])
        
        # Clean up the response text
        return response.text.strip()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Clean up the temporary screenshot file
        # This will work because the 'with' block has closed the file.
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Cleaned up {image_path}")

def main_ocr_process():
    """
    The main workflow: capture, process, and copy to clipboard.
    """
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

# --- Hotkey Setup ---
if __name__ == "__main__":
    # You can change the hotkey here. Let's use Ctrl+Shift+X to avoid conflicts.
    hotkey = 'ctrl+shift+x'
    
    print(f"Gemini OCR script is running. Press '{hotkey}' to capture screen text.")
    keyboard.add_hotkey(hotkey, main_ocr_process)
    
    # Keep the script running to listen for the hotkey
    keyboard.wait()