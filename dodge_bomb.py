import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA={pg.K_UP:(0,-5),
       pg.K_DOWN:(0,+5),
       pg.K_LEFT:(-5,0),
       pg.K_RIGHT:(+5,0),
       }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rect: pg.Rect)->tuple[bool,bool]:
    """
    引数：こうかとんまたは爆弾のrect
    戻り値：真理値タプル、横判定結果、縦判定結果
    True：画面内、False：画面外
    """
    yoko,tate=True,True
    if obj_rect.left<0 or WIDTH<obj_rect.right:
        yoko=False
    if obj_rect.top<0 or HEIGHT<obj_rect.bottom:
        tate=False
    return yoko,tate
def sleep_count():
    """
    この関数を呼ぶと呼び出した時点から３秒間その状態を表示する。
    また、pg.display.update()によって直前の動作を更新してから止めている。
    """
    pg.display.update()
    time.sleep(3)

def increase(vx:int,vy:int,r:int,bb_img:pg.Surface)->tuple[int,int,int,pg.Surface]:
    """
    この関数を呼び出すことに変数ｒの値を１ずつプラスにしていき、そのｒを参照にして加速度（vxとvy）と爆弾の大きさ（bb_img）を決定している。
    また、ｒが10の時に上限となるように設定しており、それ以上大きくも速度も増加しなくなっている。最後に加速度を表すものとしてvx,vy、爆弾の大きさを表すものとしてbb_img、次回の関数の使用用にｒをそれぞれ返している。
    """
    if r<11:
        r+=1
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        vx*=r*1.01
        vy*=r*1.01
        return vx,vy,r,bb_img
    elif r==10:
        return vx,vy,r,bb_img

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk8_img=pg.image.load("fig/8.png")
    bb_img= pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    transparent_surface = pg.Surface((WIDTH, HEIGHT))
    transparent_surface.set_alpha(128)
    transparent_surface.fill((0,0,0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    kk8_rct_1=kk8_img.get_rect()
    kk8_rct_1.center=275,325
    kk8_rct_2=kk8_img.get_rect()
    kk8_rct_2.center=675,325
    bb_rct=bb_img.get_rect()
    bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    r=1

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):
            screen.blit(transparent_surface,[0,0])
            screen.blit(txt,[325,300])
            screen.blit(kk8_img,kk8_rct_1)
            screen.blit(kk8_img,kk8_rct_2)
            sleep_count()
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=tpl[0]
                sum_mv[1]+=tpl[1]
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        else:
            kk_rct.move_ip(sum_mv)
        yoko,tate =check_bound(bb_rct)
        if not yoko:
            vx*=-1
        elif not tate:
            vy*=-1
        if tmr%(100*r)==0:
            vx,vy,r,bb_img=increase(vx,vy,r,bb_img)
            print(r)
        bb_rct.move_ip(vx,vy)
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        #print(tmr)
        print(type(bb_img))

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
