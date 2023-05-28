from asyncio import Event
import pygame as pg
import sys
import time


WIDTH = 800
HEIGHT = 600


class Bird(pg.sprite.Sprite):
    """
    操作キャラクター(こうかとん)に関するクラス
    """
    def __init__(self,num: int,x: int):
        super().__init__()
        self.mode = 0 
        self.jump = 0 # ジャンプフラグ(0: ジャンプしない, 1: ジャンプ中)
        self.cnt = 0 # ジャンプのカウンター
        self.img = pg.image.load(f"ex05/fig/{num}.png")
        self.rect = self.img.get_rect()
        self.rect.centerx = x # こうかとんのx座標
        self.rect.centery = 450 # こうかとんのy座標

    def update(self,screen: pg.Surface):
        """
        こうかとんのジャンプの処理
        """
        if self.mode == 0:
            screen.blit(self.img,self.rect)
        if self.mode == 1:
            screen.blit(pg.transform.flip(self.img,True,False),self.rect)
        if self.jump == 1: # ジャンプ中
            self.rect.centery -= 5 # 上昇
            if self.rect.centery <= 300:
                self.cnt += 1
                self.rect.centery += 5  # 上昇
                if self.cnt >= 10:  # 滞空時間   
                    self.jump = 0  # ジャンプ終了
                    self.cnt = 0 
        if self.jump == 0 and self.rect.centery < 450:
            self.rect.centery += 5
        

class Background:
    """
    背景の処理
    """
    def __init__(self,screen:pg.Surface):
        self.x=0
        self.bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
        self.bg_img_fl = pg.transform.flip(self.bg_img,True,False)
        screen.blit(self.bg_img_fl,[-800,0])
    def update(self,screen:pg.Surface):
        """
        移動に応じたupdateを行う
        """
        self.x%=3200
        screen.blit(self.bg_img,[800-self.x,0])
        screen.blit(self.bg_img_fl,[2400-self.x,0])
        screen.blit(self.bg_img_fl,[-800-self.x,0])


class Enemy(pg.sprite.Sprite):
    """
    敵に関する処理
    """
    def __init__(self, screen: pg.Surface, e_x: int, bg: Background):
        super().__init__()
        self.e_x=e_x
        self.ene_img = pg.transform.rotozoom(pg.image.load("ex05/fig/monster11.png"),0,0.2)
        self.rect= self.ene_img.get_rect()
        self.rect.centerx = self.e_x - bg.x
        self.rect.centery = 450
        screen.blit(self.ene_img,self.rect)

    def update(self, screen: pg.Surface):
        self.rect.centerx -= 5
        screen.blit(self.ene_img,self.rect)


class Goal(pg.sprite.Sprite):
    """
    ゴールに関する処理
    """
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.g_img = pg.transform.rotozoom(pg.image.load("ex05/fig/torinosu_egg.png"),0,0.2)
        self.rect = self.g_img.get_rect()
        self.rect.centerx = 3200
        self.rect.centery = 450
        screen.blit(self.g_img,self.rect)

    def update(self, screen: pg.Surface,bg: Background):
        self.rect.centerx = 3200 - bg.x
        screen.blit(self.g_img,self.rect)


class TitleScreen:
    """
    # タイトル画面の背景色やテキストの処理
    """
    def __init__(self,screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_color = (175,238,238)  # 背景色
        self.text_color = (0,128,0) # テキストの色
        self.title_font = pg.font.Font(None, 100) # メインタイトルの設定
        self.subtitle_font = pg.font.Font(None, 50) # サブタイトルの設定
        self.title_text = self.title_font.render("Super Kokaton", True, self.text_color) 
        self.subtitle_text = self.subtitle_font.render("Press Space to Start", True, self.text_color) 

    def show(self,screen):
        screen.fill(self.background_color)
        screen.blit(self.title_text, (160,200)) # メインタイトルの描画
        screen.blit(self.subtitle_text, (250,300)) # サブタイトルの描画


def main():
    pg.display.set_caption("Super_Kokaton")
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    bird = Bird(2, 200)
    bg = Background(screen)
    enes = pg.sprite.Group()
    gls = pg.sprite.Group()
    for i in range(3):
        enes.add(Enemy(screen, i * 400 + 800, bg))
    gl = Goal(screen)
    gls.add(gl)
    tmr = 0
    clock = pg.time.Clock()
    game_state = 0
    title_screen = TitleScreen(WIDTH,HEIGHT)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if game_state == 0:
                title_screen.show(screen)
                pg.display.update()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game_state = 1
        if game_state == 1:
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                bird.mode = 0
                bg.x += 10
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                bird.mode = 1
                bg.x -= 10
            if bg.x <= 0:
                bg.x = 0
            if bird.rect.centerx >= gl.rect.centerx:
                bg.x = 3000
            if bird.rect.centery == 450 and event.type == pg.KEYDOWN and event.key == pg.K_UP:
                bird.jump = 1
        
            for ene in pg.sprite.spritecollide(bird, enes, True):
                font1 = pg.font.SysFont(None, 80)
                text1 = font1.render("GAME OVER",True,(0,0,0))  
                screen.blit(text1, (240,200)) # テキストを描画
                pg.display.update() # 描画処理を実行
                time.sleep(1)
                return
            
            for goal in pg.sprite.spritecollide(bird,gls,False):
                font1 = pg.font.SysFont(None, 80)
                text1 = font1.render("GAME CLEAR",True,(255,215,0))  
                screen.blit(text1, (220,200)) # テキストを描画
                pg.display.update() # 描画処理を実行
                time.sleep(1)
                return

            tmr += 1
            x = tmr%3200

            bg.update(screen)
            bird.update(screen)
            enes.update(screen)
            gls.update(screen,bg)
            pg.display.update()
            clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
