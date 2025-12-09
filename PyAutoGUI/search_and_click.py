"""
search_and_click.py

Requires:
    pip install pyautogui opencv-python pillow

What it does:
    1. Opens your default browser to google.com
    2. Focuses the address bar, types "south africa vs india score" and presses Enter
    3. Waits for results to load
    4. Tries to click the first result using an image match (recommended)
    5. If the image isn't found, optionally clicks a fallback coordinate

Important safety:
    - Move your mouse to any corner of the screen to abort (PyAutoGUI failsafe).
    - Run this with your screen unlocked and browser visible.
"""

import webbrowser
import time
import os
import sys

import pyautogui

# === User-configurable options ===
QUERY = "south africa vs india score"
USE_IMAGE_MATCH = True           # set to False to force coordinate click
IMAGE_FILENAME = "first_result.png"  # screenshot of the first link area (see guide)
IMAGE_CONFIDENCE = 0.8          # 0.6-0.95 depending on match quality; needs opencv
FALLBACK_CLICK = True
# If using fallback coordinate, set these to the pixel location of the first result on your screen:
FALLBACK_X = 500
FALLBACK_Y = 400

# Timings (tweak to match your machine/network speed)
OPEN_BROWSER_WAIT = 2.0
SEARCH_RESULTS_WAIT = 3.5
POST_CLICK_WAIT = 2.0

# PyAutoGUI safety + default pause between actions
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25

def open_browser_and_search(query):
    print("Opening browser...")
    webbrowser.open("https://www.google.com")
    time.sleep(OPEN_BROWSER_WAIT)

    # Focus address bar and type query
    print("Focusing address bar and typing query...")
    # Works on Windows & Linux/Chrome/Firefox: Ctrl+L. On macOS use command+L.
    if sys.platform == "darwin":
        pyautogui.hotkey('command', 'l')
    else:
        pyautogui.hotkey('ctrl', 'l')

    time.sleep(0.2)
    pyautogui.typewrite(query, interval=0.05)
    pyautogui.press('enter')

def click_first_result_by_image(image_path, confidence=0.8, timeout=8):
    """Try to locate image on screen and click its center."""
    print(f"Looking for image '{image_path}' (confidence={confidence}) ...")
    start = time.time()
    while time.time() - start < timeout:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            print(f"Found image at {location}, clicking...")
            pyautogui.moveTo(location.x, location.y, duration=0.3)
            pyautogui.click()
            return True
        time.sleep(0.5)
    print("Image not found within timeout.")
    return False

def click_first_result_by_coord(x, y):
    print(f"Clicking fallback coordinates: ({x}, {y})")
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click()

def main():
    try:
        open_browser_and_search(QUERY)
        print("Waiting for search results to load...")
        time.sleep(SEARCH_RESULTS_WAIT)

        clicked = False

        if USE_IMAGE_MATCH and os.path.exists(IMAGE_FILENAME):
            clicked = click_first_result_by_image(IMAGE_FILENAME, confidence=IMAGE_CONFIDENCE, timeout=10)

        if not clicked and FALLBACK_CLICK:
            # If image failed or not supplied, click fallback coordinates
            click_first_result_by_coord(FALLBACK_X, FALLBACK_Y)
            clicked = True

        if clicked:
            time.sleep(POST_CLICK_WAIT)
            print("Done. First link should have been clicked.")
        else:
            print("Didn't click anything. Provide a good screenshot or adjust fallback coordinates.")

    except pyautogui.FailSafeException:
        print("Aborted by moving mouse to screen corner (failsafe).")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
