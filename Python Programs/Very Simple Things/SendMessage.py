import pyautogui
import time

time.sleep(5)

for i in range(10):
    pyautogui.write('Hey, Wassup!!')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.write('Sent this from python 😃')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
