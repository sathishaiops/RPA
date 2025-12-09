import pyautogui
import time


#Mouse Opeerations

pyautogui.click(1037, 50)  # Click at coordinates (100, 200)
time.sleep(3)  # Wait for 1 second
pyautogui.rightClick(150, 250)  # Right-click at coordinates (150, 250)

time.sleep(10)  # Wait for 1 second
x,y = pyautogui.position()
print(f"Current mouse position: ({x}, {y})")

pyautogui.doubleClick(200, 300)  # Double-click at coordinates (200, 300)
time.sleep(3)  # Wait for 1 second


#Keyboard Operations

time.sleep(3)  # Wait for 5 seconds to switch to the target application
pyautogui.click(911,327)  
time.sleep(2)
pyautogui.typewrite('Hello, World!')  # Type 'Hello, World
time.sleep(3)  # Wait for 5 seconds to switch to the target application
while True:
    pyautogui.write("hello")
    pyautogui.press("enter")
time.sleep(1) # Press the 'Enter' key
pyautogui.hotkey('ctrl', 'a')  # Press 'Ctrl+S' to save



#image Recognition



location = pyautogui.locateOnScreen('mac.png', confidence=0.8)
print(location)

time.sleep(5)

#pyautogui.click(pyautogui.center(location))   
print(pyautogui.size())
ss = pyautogui.screenshot()
ss.save('screenshot.png')





