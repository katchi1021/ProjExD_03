import random
import sys
import time
import pygame as pg
import os


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
NUM_OF_BOMBS = 10
COLORS = {"red": (230, 0, 0),
          "blue": (0, 0, 230),
          "green": (0, 230, 0),
          "yellow": (0, 230, 230),
          "orange": (230, 0, 230),
          "pink": (230, 130, 130),
          "purple": (230, 230, 50)}


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
        # img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        # img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
        # self.imgs = {  # 0度から反時計回りに定義
        #     (+5, 0): img,  # 右
        #     (+5, -5): pg.transform.rotozoom(img, 45, 1.0),  # 右上
        #     (0, -5): pg.transform.rotozoom(img, 90, 1.0),  # 上
        #     (-5, -5): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
        #     (-5, 0): img0,  # 左
        #     (-5, +5): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
        #     (0, +5): pg.transform.rotozoom(img, -90, 1.0),  # 下
        #     (+5, +5): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        # }
        self.img = pg.transform.flip(  # 左右反転
            pg.transform.rotozoom(  # 2倍に拡大
                pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 
                0, 
                2.0), 
            True, 
            False
        )
        self.rct = self.img.get_rect()
        self.rct.center = xy

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)

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
        screen.blit(self.img, self.rct)


class Beam:
    """
    ビームのクラス
    """
    def __init__(self, kk_rct):
        self.img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/beam.png"), 0, 2.0)
        self.rct = self.img.get_rect()
        kk_x, kk_y = kk_rct.center
        self.rct.center = (kk_x+100, kk_y)
        self.vx = 5
        self.vy = 0

    def update(self, screen: pg.Surface):
        """
        ビームを速度ベクトルself.vx,vy に基づいて移動させる
        引数 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Bomb:
    """
    爆弾に関するクラス
    """
    def __init__(self):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        x = (random.random()-0.5) * 2
        y = 1 - x**2
        color = COLORS[random.choice(list(COLORS.keys()))]
        rad = random.randint(10, 40)
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)
        self.vx = 5 * x
        self.vy = 5 * y

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

class Explosion():
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
        self.life = 5

    def update(self, screen: pg.Surface):
        img = self.imgs[self.life%4]
        screen.blit(img, self.rct)
        
def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")
    bird = Bird(3, (900, 400))
    bombs = list()
    explosions = list()
    for _ in range(NUM_OF_BOMBS):
        bombs.append(Bomb())
    beam = None

    clock = pg.time.Clock()
    tmr = 0
    while True:
        key_lst = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        if key_lst[pg.K_SPACE]: beam = Beam(bird.rct)
        
        screen.blit(bg_img, [0, 0])
        
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                bird.change_img(8, screen)
                pg.display.update()
                time.sleep(1)
                return

            if beam is not None:
                if bomb.rct.colliderect(beam.rct):
                    explosions.append(Explosion(bomb.rct))
                    beam = None
                    bomb = None 

        bird.update(key_lst, screen)
        for bomb in bombs:
            if bomb is not None: bomb.update(screen)
        if beam is not None: beam.update(screen)
        for explosion in explosions:
            if explosion.life != 0: explosion.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()