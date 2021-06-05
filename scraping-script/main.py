# This is a sample Python script.
import pyautogui
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
NONE = pyautogui.press('tab')
none = NONE
PYAUTOGUI_PRESS = none

def start():
    #start up script and refresh page
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.keyUp('alt')
    pyautogui.press('f5')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
def refresh():
    #Refresh page and jump to address input box
    pyautogui.press('f5')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
def search_input(street):
    # Use a breakpoint in the code line below to debug your script.
    res = []
    res[:] = street
    for i in range(len(res)):
        if(res[i].isspace() == False):
            pyautogui.press(res[i])
        else:
            pyautogui.press('space')
        # pyautogui.press('6')
        # pyautogui.press('1')
        # pyautogui.press('3')
        # pyautogui.press('9')
        # pyautogui.press('space')
        # pyautogui.press('Q')
    time.sleep(1)
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('2')
    pyautogui.press('2')
    pyautogui.press('enter')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    start()
    time.sleep( 1)
    search_input('11 Cole Dr    ')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
