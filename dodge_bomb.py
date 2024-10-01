import os
import sys
import pygame as pg
import random

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
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img= pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct=bb_img.get_rect()
    bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

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
        bb_rct.move_ip(vx,vy)
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        #print(tmr)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
