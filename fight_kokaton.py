import math
import os
import pygame as pg
import random
import sys
import time
# import random
# import sys
# import time
# import pygame as pg
# import os
# import math

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
NUM_OF_BOMBS = 10
COLORS = {"red": (255, 0, 0),
          "blue": (0, 0, 255),
          "green": (0, 255, 0),
          "yellow": (0, 255, 255),
          "orange": (255, 0, 255),
          "pink": (255, 192, 203),
          "purple": (128, 0, 128),
          "teal": (0, 128, 128),
          "lime": (0, 255, 0),
          "golden":  (218, 165, 32)}


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとん，または，爆弾SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        img0 = pg.transform.rotozoom(pg.image.load(f"ex03/fig/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
        self.imgs = {  # 0度から反時計回りに定義
            (+5, 0): img,  # 右
            (+5, -5): pg.transform.rotozoom(img, 45, 1.0),  # 右上
            (0, -5): pg.transform.rotozoom(img, 90, 1.0),  # 上
            (-5, -5): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
            (-5, 0): img0,  # 左
            (-5, +5): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
            (0, +5): pg.transform.rotozoom(img, -90, 1.0),  # 下
            (+5, +5): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        # self.img = pg.transform.flip(  # 左右反転
        #     pg.transform.rotozoom(  # 2倍に拡大
        #         pg.image.load(f"ex03/fig/{num}.png"), 
        #         0, 
        #         2.0), 
        #     True, 
        #     False
        # )
        self.img = img
        self.rct = img.get_rect()
        self.rct.center = xy
        self.dire = (5, 0)

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        screen.blit(img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """

        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if sum_mv != [0, 0]:
            self.img = self.imgs[tuple(sum_mv)]
            self.dire = tuple(sum_mv)
        screen.blit(self.img, self.rct)


class Beam:
    """
    ビームのクラス
    """
    def __init__(self, kk):
        self.img = pg.image.load(f"{MAIN_DIR}/fig/beam.png")
        self.rct = self.img.get_rect()
        kk_x, kk_y = kk.rct.center
        x, y = kk.dire
        self.rct.center = (kk_x+10*x, kk_y+10*y)
        theta = math.atan2(-y, x)
        self.img = pg.transform.rotozoom(self.img, math.degrees(theta), 1.0)
        self.vx = x
        self.vy = y

    def update(self, screen: pg.Surface):
        """
        ビームを速度ベクトルself.vx,vy に基づいて移動させる
        引数 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)

class Guided:
    def __init__(self, kk, bombs):
        self.img = pg.image.load(f"{MAIN_DIR}/fig/beam.png")
        self.rct = self.img.get_rect()
        kk_x, kk_y = kk.rct.center
        x, y = kk.dire
        self.rct.center = (kk_x+10*x, kk_y+10*y)
        theta = math.atan2(-y, x)
        self.img = pg.transform.rotozoom(self.img, math.degrees(theta), 1.0)
        self.vx = 
        self.vy = 
        rect_ydis = rect1.center[1] - rect2.center[1]
        rect_xdis = rect1.center[0] - rect2.center[0]
        r = rect_xdis**2 + rect_ydis**2
        r = r**0.5
        dx = rect_xdis/r
        dy = rect_ydis/r
        

class Bomb:
    """
    爆弾に関するクラス
    """
    def __init__(self, bird:Bird):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        x = (random.random()-0.5) * 2
        y = 1 - x**2
        clrname = random.choice(list(COLORS.keys()))
        color = COLORS[clrname]
        del COLORS[clrname]
        rad = random.randint(10, 80)
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)
        # リスキル対策
        while self.rct.colliderect(bird.rct):
            self.rct.center = random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)
        self.vx = 7 * x
        self.vy = 7 * y

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)

class Explosion:
    """
    爆発エフェクトのクラス
    """
    def __init__(self, bomb_rct):
        img = pg.image.load(f"{MAIN_DIR}/fig/explosion.gif")
        self.rct = img.get_rect()
        self.imgs = [img,
                    pg.transform.flip(img, True, False),
                    pg.transform.flip(img, True, True),
                    pg.transform.flip(img, False, True)]
        self.rct.center = bomb_rct.center
        self.life = 10

    def update(self, screen: pg.Surface):
        """
        self.lifeに基づいて爆弾のイメージを変化させる
        self.lifeを1減らす
        """
        img = self.imgs[self.life%4]
        screen.blit(img, self.rct)
        self.life -= 1


class Score:
    """
    スコアの表示に関するクラス
    """
    def __init__(self):
        """
        self.score(スコア)の初期値:0
        文字色を青で設定
        """
        self.score = 0
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.text = self.font.render(f"スコア:{self.score}", 0, (0, 0, 255))
        self.rct = self.text.get_rect()
        self.rct.center = (100, 850)

    def hit(self):
        pass

    def update(self, screen: pg.Surface):
        self.text = self.font.render(f"スコア:{self.score}", 0, (0, 0, 255))
        screen.blit(self.text, self.rct)

def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")
    bird = Bird(3, (900, 400))
    score = Score()
    bombs = list()
    explosions = list()
    bombs = [(Bomb(bird)) for _ in range(NUM_OF_BOMBS)]
    beams = list()
    guideds = list()
    cool_time = 0
    fps = 50

    clock = pg.time.Clock()
    tmr = 0
    while True:
        key_lst = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return      

        if key_lst[pg.K_SPACE] and cool_time < 0:
            beams.append(Beam(bird))
            cool_time = 10

        if key_lst[pg.K_LCTRL]:
            guideds.append(Guided(bird, bombs))

        if key_lst[pg.K_ESCAPE]: fps = 0 if fps != 0 else 50
        
        screen.blit(bg_img, [0, 0]) 
        
        if bombs == []:
            bird.change_img(6, screen)
            pg.display.update()
            time.sleep(2)
            return

        for bn, bomb in enumerate(bombs):
            if bomb is not None:
                if bird.rct.colliderect(bomb.rct):
                    # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                    bird.change_img(8, screen)
                    pg.display.update()
                    time.sleep(1)
                    return
                
                for beamn, beam in enumerate(beams):
                    if beam is not None and bomb.rct.colliderect(beam.rct):
                            explosions.append(Explosion(bomb.rct))
                            score.score += 1
                            beams[beamn] = None
                            bombs[bn] = None

        beams = [_ for _ in beams if _ is not None]
        bombs = [_ for _ in bombs if _ is not None]
        explosions = [_ for _ in explosions if _.life > 0]

        score.update(screen)
        bird.update(key_lst, screen)
        for bomb in bombs:
            bomb.update(screen)
        for beam in beams:
           beam.update(screen)
           if check_bound(beam.rct) != (True, True):
               beams.remove(beam)
        for explosion in explosions:
            explosion.update(screen)
        pg.display.update()
        tmr += 1
        cool_time -= 1
        clock.tick(fps)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()