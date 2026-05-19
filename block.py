import tkinter as tk
import random
import time

WIDTH = 800
HEIGHT = 960
pl_x = WIDTH/2#プレイヤー初期位置
pl_y = HEIGHT-300
cm_x = pl_x
cm_y = 300
cl_x = 0#クリックしたｘ軸
BLOCK_x = 10
BLOCK_y = 4
SIZE = 80 #岩の大きさ
BLOCK = [[0 for i in range(BLOCK_x)] for i in range(BLOCK_y)]#ブロックのあるなしを管理
BLOCK_type = [[0 for i in range(BLOCK_x)] for i in range(BLOCK_y)]
magic = []
mp = 5
mp_max = 5
cm_magic = []
enemy_timer = 0
homing_magic = []
split_magic = []
laser = []
scene = "ホーム画面"
magic_vy = 10
cmmg_x = cm_x
cmmg_y = cm_y+10
key = ""
timer = 0
score = 0
stage = 1

def move(e):#マウスを動かすと魔法使いが動く
    global pl_x
    pl_x = int(0.8*pl_x+0.2*e.x)
    if pl_x<0:pl_x=0
    if pl_x>800:pl_x=800

def click(e):#クリックすると魔法弾を発射する
    global magic,mp
    if mp > 0:
        magic.append([pl_x,pl_y-10])
        mp -= 1

def pkey(e):
    global key
    key = e.keysym

def effect(cx, cy):
    for i in range(10):
        cvs.create_oval(cx,cy,cx+SIZE,cy+SIZE,fill="red")
        cvs.update()
        time.sleep(0.01)
        cvs.create_oval(cx,cy,cx+SIZE,cy+SIZE,fill="yellow")
        cvs.update()
        time.sleep(0.01)

def set_BLOCK():#岩を生成する関数
    global BLOCK_x,BLOCK_y
    for y in range(BLOCK_y):
        for x in range(BLOCK_x):
            BLOCK[y][x] = random.randint(0,1)
            if BLOCK[y][x] == 1:
                Z = random.randint(0,100)
                if Z<=20:
                    BLOCK_type[y][x] = 2
                else:
                    BLOCK_type[y][x] = 1
            
def draw_BLOCK():#岩を描く関数
    global BLOCK_y,BLOCK_x
    for y in range(BLOCK_y):
        for x in range(BLOCK_x):
            if BLOCK[y][x] == 1:
                X = x*SIZE + SIZE/2
                Y = y*SIZE + SIZE/2 + 50
                if BLOCK_type[y][x] == 1:
                    cvs.create_image(X,Y,image=red)
                if BLOCK_type[y][x] == 2:
                    cvs.create_image(X,Y,image=blue)

def text(x,y,txt,siz,col):
    fnt = ("Times New Roman",siz)
    cvs.create_text(x+1, y+1, text=txt, font=fnt, fill="black")
    cvs.create_text(x, y, text=txt, font=fnt, fill=col)        
            
def main():
    global magic,BLOCK_x,BLOCK_y,magic_vy,SIZE,WIDTH,HEIGHT
    global scene,key,timer,score,stage
    global cm_x,cm_y,cmmg_x,cmmg_y,cm_magic,mp,mp_max
    global enemy_timer, homing_magic, split_magic, laser
    cvs.delete("all")
    cvs.create_image(WIDTH/2,HEIGHT/2,image=bg)
    cvs.create_image(pl_x, pl_y, image=mahou, anchor="s")
    player_hit_x = pl_x
    player_hit_y = pl_y - 40
    cvs.create_oval(
        player_hit_x-5,
        player_hit_y-5,
        player_hit_x+5,
        player_hit_y+5,
        fill="white"
        )
    text(200,30,"TIME"+str(timer),40,"red")
    text(500,30,"STAGE"+str(stage),40,"red")
    if scene == "ホーム画面":
        text(360,380,"魔法使いの冒険",60,"red")
        text(360,480,"[S]を押してスタート",40,"yellow")
        if key=="s":
            timer = 1000
            scene = "ゲーム説明"
            key=""
    if scene == "ゲーム説明":
        cvs.create_rectangle(80,80,WIDTH-80,HEIGHT-80,fill="black", stipple="gray50")
        text(400,200,"ゲームの遊び方",40,"white")
        text(400,400,"あなたは魔法の材料を集めに洞窟に来た魔法使い\n"+
             "魔法弾を打って魔法石を集めよう！\n"+
             "赤い石は一回、青い石は二回攻撃すれば壊れるよ\n"+
             "石を壊すとタイマーが増えるよ\n"+
             "魔法はクリックで使えるよ\n"+
             "魔法を使うとmpが減り、時間で回復するよ\n"
             "洞窟には魔物がいて、攻撃をしかけてくるよ\n"+
             "攻撃にあたるとタイマーが減るから注意してね\n"+
             "タイマーが０になるとゲームオーバー\nそれまでに石を集め切ろう！\n"+
             "[S]を押してスタート",20,"white")
        if key=="s":
            scene = "ゲーム"
    if scene == "ゲーム":
        draw_BLOCK()
        if stage == 2:
            cvs.create_image(cm_x, cm_y, image=monster, anchor="s")#敵の初期位置
            if pl_x>cm_x:cm_x += 5
            if pl_x<cm_x:cm_x -= 5
            if abs(pl_x-cm_x) <= 10 and timer % 5 == 0:
                cm_magic.append([cm_x, cm_y+10])
            for cmmg in cm_magic[:]:
                cmmg[1] += 10
                cvs.create_oval(cmmg[0]-10, cmmg[1]-10, cmmg[0]+10, cmmg[1]+10, fill="red")
                if cmmg[1] > HEIGHT:
                    cm_magic.remove(cmmg)
                if abs(cmmg[0] - pl_x) < 20 and abs(cmmg[1] - pl_y) < 20:
                    effect(player_hit_x-SIZE/2, player_hit_y-SIZE/2)
                    timer -= 500
        if stage == 3:
             cvs.create_image(cm_x,cm_y,image=dragon,anchor="s")
             if pl_x>cm_x:cm_x += 8
             if pl_x<cm_x:cm_x -= 8
             enemy_timer += 1
             if enemy_timer % 60 == 0:
                 attack = random.randint(1,3)
                 if attack == 1:#レーザー弾
                     dx = pl_x -cm_x
                     dy = pl_y -cm_y
                     dist = (dx**2 + dy**2)**0.5
                     vx = dx / dist * 12
                     vy = dy / dist * 12
                     laser.append([cm_x, cm_y, vx, vy])
                 if attack == 2:#３way弾
                     split_magic.append([cm_x, cm_y, -5])
                     split_magic.append([cm_x, cm_y, 0])
                     split_magic.append([cm_x, cm_y, 5])
                 if attack == 3:#ホーミング弾
                     homing_magic.append([cm_x, cm_y])
             for ls in laser[:]:
                 ls[0] += ls[2]
                 ls[1] += ls[3]
                 cvs.create_line(ls[0],ls[1],ls[0] - ls[2]*5,ls[1] - ls[3]*5, fill="cyan", width=8)
                 if abs(ls[0]-player_hit_x) < 20 and abs(ls[1]-player_hit_y) < 20:
                     effect(player_hit_x-SIZE/2, player_hit_y-SIZE/2)
                     timer -= 500
                     laser.remove(ls)
                 if ls[1] > HEIGHT or ls[0] < 0 or ls[0] > WIDTH:
                     laser.remove(ls)
             for sp in split_magic[:]:
                 sp[0] += sp[2]
                 sp[1] += 8
                 cvs.create_oval(sp[0]-10, sp[1]-10, sp[0]+10, sp[1]+10, fill="orange")
                 if abs(sp[0]-player_hit_x) < 20 and abs(sp[1]-player_hit_y) < 20:
                     effect(player_hit_x-SIZE/2, player_hit_y-SIZE/2)
                     timer -= 500
                     split_magic.remove(sp)
                 if sp[1] > HEIGHT:
                     split_magic.remove(sp)
             for hm in homing_magic[:]:
                 if pl_x>hm[0]:hm[0] += 4
                 if pl_x<hm[0]:hm[0] -= 4
                 if pl_y>hm[1]:hm[1] += 4
                 if pl_y<hm[1]:hm[1] -= 4
                 cvs.create_oval(hm[0]-12, hm[1]-12, hm[0]+12, hm[1]+12, fill="purple")
                 if abs(hm[0]-player_hit_x) < 20 and abs(hm[1]-player_hit_y) < 20:
                     effect(player_hit_x-SIZE/2, player_hit_y-SIZE/2)
                     timer -= 500
                     homing_magic.remove(hm)
                 if hm[1] > pl_y-5:
                     homing_magic.remove(hm)
        for mg in magic[:]:
            mg[1] -= magic_vy
            cvs.create_oval(mg[0]-10, mg[1]-10, mg[0]+10, mg[1]+10, fill="yellow")
            ax = int(mg[0]//SIZE)
            ay = int((mg[1]-50)//SIZE)
            if 0 <= ax <BLOCK_x and 0 <= ay <BLOCK_y:
                if BLOCK[ay][ax]==1:
                    effect(ax*SIZE,ay*SIZE+50)
                    if BLOCK_type[ay][ax]==1:
                        BLOCK[ay][ax]=0
                    if BLOCK_type[ay][ax]==2:
                        BLOCK_type[ay][ax]=1
                    timer += 100
                    magic.remove(mg)
            if mg[1] < 0:
                magic.remove(mg)
        for i in range(mp):
            cvs.create_oval(pl_x+50 + i*25, pl_y -80, pl_x+70+i*25, pl_y-60, fill="cyan")
        if all(BLOCK[y][x] == 0 for y in range(BLOCK_y) for x in range(BLOCK_x)):
            if stage<3:
                stage += 1
                scene = "ゲーム"
                set_BLOCK()
            else:
                scene = "クリア"
        if timer <= 0:
            if not all(BLOCK[y][x] == 0 for y in range(BLOCK_y) for x in range(BLOCK_x)):
                scene = "ゲームオーバー"
        timer -= 1
        if timer % 30 == 0:
            if mp < mp_max:
                mp += 1
    if scene == "クリア":
        text(360,380,"ゲームクリア",60,"red")
        text(360,480,"[R]を押してリスタート",40,"yellow")
        if key=="r":
            scene = "ゲーム"
            key=""
            set_BLOCK()
    if scene == "ゲームオーバー":
        text(360,380,"ゲームオーバー",60,"red")
        text(360,480,"[R]を押してリスタート",40,"yellow")
        if key=="r":
            scene = "ゲーム"
            key=""
            timer = 1000
            stage = 1
    root.after(30,main)

root = tk.Tk()
root.title("魔法使いの冒険")
root.resizable(False, False)
root.bind("<Motion>",move)
root.bind("<Button>",click)
root.bind("<Key>", pkey)
cvs = tk.Canvas(width=WIDTH, height=HEIGHT)
cvs.pack()
bg = tk.PhotoImage(file="image/bg.png")
mahou = tk.PhotoImage(file = "image/majo.png")
monster = tk.PhotoImage(file = "image/monster.png")
dragon = tk.PhotoImage(file = "image/dragon.png")
red = tk.PhotoImage(file = "image/red.png")
blue = tk.PhotoImage(file = "image/blue.png")
set_BLOCK()
main()
root.mainloop()
                    
            
        
        
    
