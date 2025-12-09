import pyautogui
import time 

time.sleep(5)  # Wait for 5 seconds to switch to the target application
x, y = pyautogui.position()
print(f"Current mouse position: ({x}, {y})")