import pyautogui
import time

product_id = input('Enter the desired product ID: ')
num_items_list = input('Enter number of items for List')

#Open sql developer from taskbar
#pyautogui.moveTo(858, 1184, duration=0.5)
#pyautogui.click()

#open 'Open file' window
#pyautogui.moveTo(43, 59, duration=0.5)
#pyautogui.click()

#select script file
#pyautogui.moveTo(835, 518, duration=0.5)
#pyautogui.click()

#open script file
#pyautogui.moveTo(1109, 787, duration=0.5)
#pyautogui.click()

#move to product filter line
pyautogui.moveTo(663, 279, duration=0.5)
pyautogui.click()
time.sleep(2)

#highlight product filter row
pyautogui.hotkey('shiftleft', 'home')
time.sleep(2)

#enter new product id
pyautogui.write("AND ipi.productid = '" + product_id + "'")

#query DB
pyautogui.hotkey('ctrl', 'enter')

time.sleep(5)

#move to column
pyautogui.moveTo(469, 825, duration=0.5)
pyautogui.click()

#right click
pyautogui.click(button='right')

#click export option
pyautogui.moveTo(480, 938, duration=0.5)
pyautogui.click()

pyautogui.moveTo(912, 461, duration=0.5)
pyautogui.click()

pyautogui.moveTo(972, 559, duration=0.5)

pyautogui.mouseDown()
pyautogui.moveTo(970, 509, duration=0.5)
pyautogui.mouseUp()

pyautogui.moveTo(938, 481, duration=0.5)
pyautogui.click()

pyautogui.moveTo(961, 589, duration=0.5)
pyautogui.click()

pyautogui.hotkey('ctrl', 'a')
pyautogui.write(r"C:\Users\chorn\OneDrive - MarketAxess Corporation\Documents\KAUAI\AutomateProducts\export.csv")

pyautogui.moveTo(775, 722, duration=0.5)
pyautogui.click()

pyautogui.moveTo(1074, 845, duration=0.5)
pyautogui.click()

pyautogui.moveTo(1026, 634, duration=0.5)
pyautogui.click()

pyautogui.moveTo(1158, 845, duration=0.5)
pyautogui.click()
