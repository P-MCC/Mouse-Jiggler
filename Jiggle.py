import multiprocessing
import sys
import time
from datetime import datetime
import pyautogui
import keyboard
import random


pyautogui.FAILSAFE = False
width, height= pyautogui.size()


def jiggle(sleepTime):
    
    
    while(True):
        time.sleep(sleepTime)
   
        x = random.randint(-500,500)
        y = random.randint(-500,500)
        print(x,y)
        pyautogui.move(x, y, 1, pyautogui.easeInOutQuad)
        pyautogui.moveTo(width/2,height/2, 0.5, pyautogui.easeInOutQuad)
        print("Mouse movement made at {}".format(datetime.now().time()))
        
        
        
  
def keyChecker(q):
    recorded = keyboard.record(until="esc")
    print(recorded)
    if (recorded != None):
        print("Esc pressed")
        print("KILL JIGGLE!!!")
        q.put("KILL JIGGLE")
    
   
         

def main():
    q = multiprocessing.Queue()
    sleepTime = int(input("Enter the jiggle period in seconds:"))
    
    print("To end the program press esc")
    print("Starting to jiggle in {} seconds!".format(sleepTime))
    
    ProcessJiggle = multiprocessing.Process(target=jiggle, args=(sleepTime,))
    ProcessKeyChecker = multiprocessing.Process(target=keyChecker, args=(q,))
    
    ProcessKeyChecker.daemon = True
    
    ProcessJiggle.start()
    ProcessKeyChecker.start()
    
    while True:
        msg = q.get()
        
        if msg == "KILL JIGGLE":            
            print("Terminating...")
            
            ProcessJiggle.terminate()
            time.sleep(0.1)
            
            if not ProcessJiggle.is_alive():               
                ProcessJiggle.join(timeout=1.0)               
                print("Joined successfully")
                print("Jiggle process terminated!")                                                 
                q.close()
                break  
    
    print("End of jiggling :(")
    sys.exit()


if __name__ == "__main__":
    main()

