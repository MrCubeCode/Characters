import json
import os
import random
import sys
from g4f.client import Client
import requests
import time
import pygame
import win32api
import win32con
import win32gui
import ctypes

if len(sys.argv)==1:
    ctypes.windll.user32.MessageBoxW(0, "The character is not selected for launch", "Error", 0)
    sys.exit(1)

pygame.init()
pygame.mixer.init()
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
print(f"Resolution: {width}x{height}")
window_screen = pygame.display.set_mode((width, height))
hwnd = pygame.display.get_wm_info()["window"]
ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
ex_style |= win32con.WS_EX_TOOLWINDOW
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
win32gui.SetWindowPos(
    hwnd,
    win32con.HWND_TOPMOST,  # Помещаем окно поверх всех окон
    0, 0, 0, 0,
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                       hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(1, 1, 1), 0, win32con.LWA_COLORKEY)
def display_logs(text_log):
    window_screen.fill((1, 1, 1))
    font = pygame.font.SysFont('Comic Sans MS', 50)
    text = font.render(text_log, True, (255,255,255))
    text_rect = text.get_rect(center=(width/2, height/2))
    window_screen.blit(text, text_rect)
    pygame.display.flip()
x=0
y=0
text=""
anim="stand"
text_for_char=""
time_walk=0
in_bin=False
def update():
    global x,y,c_x,c_y,move,time_walk,text,text_for_char,in_bin

    window_screen.fill((1, 1, 1))
    if pygame.mouse.get_pressed()[0] and pygame.Rect(c_x,c_y,150,150).collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
        image = pygame.image.load(f"C:\\characters\\bin.png")

        if pygame.Rect(width/2-100/2,10,100,100).collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            in_bin=True
            image = pygame.transform.scale(image, (150, 150))
            window_screen.blit(image, (width/2-150/2, 10))
        else:
            in_bin = False
            image = pygame.transform.scale(image, (100, 100))
            window_screen.blit(image, (width/2-100/2,10))
        c_x,c_y=pygame.mouse.get_pos()
        c_x -= 150 // 2
        c_y -= 150 // 2
        x = c_x
        y = c_y
        move=False
    elif in_bin:
        c_x,c_y=(-150,-150)
        in_bin=False
        update()
        dialog("AAAAAA!")
        sys.exit(0)

    if move:
        if round(time_walk/10)%2==0:
            anim="walk"
        else:
            anim="walk2"
    else:
        anim="stand"
    image = pygame.image.load(f"C:\\characters\\{anim}.png")
    image = pygame.transform.scale(image,(150,150))
    image = pygame.transform.flip(image,(move and c_x > x),False)
    window_screen.blit(image,(c_x,c_y))
    if c_x!=x or c_y!=y:
        move=True
        time_walk+=1
        if c_x>x:c_x-=1
        if c_x < x: c_x += 1
        if c_y>y:c_y-=1
        if c_y < y: c_y += 1
    else:
        move=False

    font = pygame.font.SysFont('Comic Sans MS', 20)
    window_screen.blit(font.render(text, False, (255, 255, 255)),
                       (0,0))
    pygame.draw.rect(window_screen, (0, 0, 0),
                     pygame.Rect(0,0,width,1))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if pygame.mouse.get_pos()[1]==0:
                if event.key == pygame.K_RETURN:
                    text_for_char=text
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
def sleep(timesleep):
    for i in range(round(timesleep*10)):
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
def dialog(texts):
    global x,y,c_x,c_y,move
    texts = texts.replace("!",".").replace("?",".")
    for text in texts.split("."):
        window_screen.fill((1, 1, 1))
        update()
        scale_x = 420
        scale_y = 180
        pygame.draw.rect(window_screen, (0, 0, 0),
                         pygame.Rect(width / 2 - scale_x // 2, height - scale_y - 10, scale_x, scale_y))
        pygame.draw.rect(window_screen, (255, 255, 255),
                         pygame.Rect(width / 2 - (scale_x - 10) // 2, height - (scale_y - 10) - 10, (scale_x - 10),
                                     (scale_y - 10)), 5)
        image = pygame.image.load(f"C:\\characters\\dialog.png")
        image = pygame.transform.scale(image, (scale_y - 40, scale_y - 40))
        window_screen.blit(image, (round(width // 2 - scale_x // 2 + 20), height - scale_y + 15))
        for i,chunk in enumerate(chunks(text,18)):
            text_in_dialog = ""
            for sim in chunk:
                text_in_dialog+=sim
                #window_screen.fill((1, 1, 1))


                font = pygame.font.SysFont('Comic Sans MS', 20)
                window_screen.blit(font.render(text_in_dialog, False, (255, 255, 255)),(round(width//2-scale_x//2+20)+(scale_y-40)+20,height-scale_y+15+15*i))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                if sim!=" ":
                    pygame.mixer.music.load("C:\\characters\\typing.mp3")
                    pygame.mixer.music.play()
                sleep(0.1)
        sleep(2)
    sleep(5)

character={}
contexts=[]
x=0
y=0
path_to_json=""
move=False

def load_image(url,name):
    data_path = "C:\\characters\\"
    os.makedirs(data_path, exist_ok=True)
    custom_image_path = data_path + name+".png"
    with open(custom_image_path, "wb") as f:
        display_logs(f"Loading {custom_image_path.replace("\\", "/").split("/")[-1]}...")
        print(f"Downloading {custom_image_path}...")
        request = requests.get(url)
        f.write(request.content)


def character_load(path):
    global character,contexts,path_to_json,x,y
    path_to_json=path
    display_logs(f"Loading {path}...")
    with open(path, "r", encoding="utf-8") as f:
        character = json.loads(f.read())
    contexts=character["memory"]
    #contexts.insert(0, {"role":"system","content": "Запомни команду: в предложении в круглых скопках пиши настроение предложения: sad,happy,normal,angry"})
    x=character["x"]
    y=character["y"]
    load_image("https://github.com/MrCubeCode/Characters/blob/main/images/bin.png?raw=true", "bin")
    load_image(character["stand"],"stand")
    load_image(character["dialog"], "dialog")
    load_image(character["walk"],"walk")
    load_image(character["walk2"],"walk2")
    data_path = "C:\\characters\\"
    os.makedirs(data_path, exist_ok=True)
    custom_image_path = data_path + "typing" + ".mp3"
    with open(custom_image_path, "wb") as f:
        display_logs(f"Loading {custom_image_path.replace("\\", "/").split("/")[-1]}...")
        print(f"Downloading {custom_image_path}...")
        request = requests.get("https://github.com/MrCubeCode/Characters/raw/refs/heads/main/sound/typing.mp3")
        f.write(request.content)
def update_json():

    global path_to_json,character,x,y,contexts
    character["x"]=x
    character["y"]=y
    character["memory"]=contexts
    with open(path_to_json,"w",encoding="utf-8") as f:
        f.write(json.dumps(character))
character_load(sys.argv[1])
c_x,c_y=x,y
def brain(text=""):
    global width,height,x,y,contexts,character
    ret={}
    ret["response"]=""
    if len(contexts) > character["memory_len"]:
        contexts.pop(1)
    if text.replace(" ","")!="":
        client = Client()
        contexts.append({"role":"user","content":text})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=contexts,
        )
        ret["response"]=response.choices[0].message.content
    elif random.randint(0,character["volubility"])==1:
        client = Client()
        contexts.append({"role": "user", "content": "System: Спроси пользователя о чём либо или расскажи ему что-то"})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=contexts,
        )
        ret["response"] = response.choices[0].message.content
    else:
        ret["x"] = random.randint(0, width)
        ret["y"] = random.randint(0, height)
        x=ret["x"]
        y=ret["y"]
    ret["x"] = x
    ret["y"] = y
    print(ret)
    update_json()
    return ret

if __name__=="__main__":
    while True:
        update()
        if move==False:
            if 1==random.randint(0,character["activity"]) or text_for_char.replace(" ","")!="":
                brain_response=brain(text_for_char)
                text_for_char=""
                if brain_response["response"]!="":
                    dialog(brain_response["response"])
