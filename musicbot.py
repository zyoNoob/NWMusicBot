# from cv2 import cv2
import cv2
import mss
import numpy as np
import os
import time
from pynput import mouse, keyboard
import operator
import sys
import threading
from pynput.keyboard import Key, Listener, KeyCode

def setInstruments():
    path = sys.path[0]
    print("Type the tier for your music instrument; choose from [green/legendary]; and then press enter.")
    instrument_tier = input()
    if instrument_tier=='':
        instrument_tier='legendary'
    img_path = os.path.join(path, f"img\\{instrument_tier}")
    return img_path

global img_path
img_path = setInstruments()

def setDuration():
    print("Type the duration of your music in seconds and press enter.")
    song_duration = input()
    song_duration = int(song_duration)+8
    return song_duration

global song_duration
song_duration = setDuration()

def compImage(imgSource, imgTarget, charName):
    resultTry = cv2.matchTemplate(imgSource, imgTarget, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(resultTry)
    # print(imgSource.shape, imgTarget.shape, minVal, maxVal, minLoc, maxLoc)
    w, h, c = imgTarget.shape
#     cv2.rectangle(imgSource, maxLoc, (maxLoc[0] + w , maxLoc[1] + h), (0,0,255), 2)
#     cv2.imwrite(os.path.join('results/',f'res_{charName}.png'), imgSource)
    return maxVal

def Screen_Shot(left=600, top=775, width=55, height=150):
    stc = mss.mss()
    scr = stc.grab({
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })

    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    return img

def click_Note(targetList, counter):
    charList = ['w','a','s','d','space','biclick']
    score = {}
    img = Screen_Shot()
#     cv2.imwrite(os.path.join('output/',f'img_{counter}.png'), img)
    for idx, imgTarget in enumerate(targetList):
        imgSource = img.copy()
        score[charList[idx]] = compImage(imgSource, imgTarget, charList[idx])
    maxChar = [key for key, value in score.items() if value == max(score.values())][0]
    if (score[maxChar]>0.85):
#         print(maxChar, score)
#         cv2.imwrite(os.path.join('results/',f'res_{maxChar}_{score[maxChar]}.png'), img)
        if maxChar in ['w','a','s','d']:
            keyboardC.press(maxChar)
            time.sleep(0.01)
            keyboardC.release(maxChar)
            return True
        elif maxChar=='space':
            time.sleep(0.03)
            keyboardC.press(keyboard.Key.space)
            time.sleep(0.01)
            keyboardC.release(keyboard.Key.space)
            return True
        else:
            time.sleep(0.03)
            mouseC.press(mouse.Button.left)
            mouseC.press(mouse.Button.right)
            time.sleep(0.01)
            mouseC.release(mouse.Button.left)
            mouseC.release(mouse.Button.right)
            return True
        # return True
    else:
        return False

def performance():
    print("NWMusicBot is now active.\n")
    counter = 0
    while keep_playing:
        click_Note(img_list, counter)
        counter += 1
    return 0

def loop_executor():
    print(f"NWMusicBot looping with duration of {song_duration+3}")
    while keep_playing:
        for i in range(song_duration):
            if keep_playing==False:
                break
            else:
                time.sleep(1)
        if keep_playing==True:
            keyboardC.press('e')
            time.sleep(2)
            keyboardC.release('e')
        if keep_playing==True:
            keyboardC.press('e')
            time.sleep(0.5)
            keyboardC.release('e')
    return 0

def statusCheck(key):
    global keep_playing
    if key == KeyCode.from_char('1'):
        keep_playing=False
        return False

def loadImageList():
    img_list = []
    img_list.append(cv2.imread(os.path.join(img_path, 'W.jpg'), cv2.IMREAD_UNCHANGED))
    img_list.append(cv2.imread(os.path.join(img_path, 'A.jpg'), cv2.IMREAD_UNCHANGED))
    img_list.append(cv2.imread(os.path.join(img_path, 'S.jpg'), cv2.IMREAD_UNCHANGED))
    img_list.append(cv2.imread(os.path.join(img_path, 'D.jpg'), cv2.IMREAD_UNCHANGED))
    img_list.append(cv2.imread(os.path.join(img_path, 'Space.jpg'), cv2.IMREAD_UNCHANGED))
    img_list.append(cv2.imread(os.path.join(img_path, 'BiClick.jpg'), cv2.IMREAD_UNCHANGED))
    return img_list

global img_list
img_list = loadImageList()

mouseC = mouse.Controller()
keyboardC = keyboard.Controller()
stc = mss.mss()
os.makedirs('results', exist_ok=True)
os.makedirs('output', exist_ok=True)

def main():
    global keep_playing, song_duration
    keep_playing = True

    t_music = threading.Thread(target=performance)
    t_loop = threading.Thread(target=loop_executor)

    t_music.start()
    t_loop.start()

    # Collect all event until released
    with Listener(on_press = statusCheck) as listener:
        listener.join()

    if keep_playing==False:
        print(f"Music bot service will stop within {song_duration+3} seconds.")
        _ = t_music.join()
        _ = t_loop.join()
        print(f"Restart Service? [y/n]")
        restart_status = input()
        if restart_status=='y':
            song_duration = setDuration()
            main()
        else:
            exit()

main()