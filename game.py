import pygame
import sys
import random
import time
folders = {
    'audio': 'assets\\audio\\',
    'fonts': 'assets\\fonts\\',
    'img': 'assets\\img\\',
    'save': 'assets\\save\\',
}
pygame.init() #初始化pygame module
screen = pygame.display.set_mode((1280, 720)) # 建立 window 視窗畫布，大小為 1280x720
clock = pygame.time.Clock() #時間控制模組 用來管理時間以及遊戲幀數
pygame.display.set_caption("Dino Game") #設定遊戲介面的標題
game_font = pygame.font.Font(folders["fonts"]+"PressStart2P-Regular.ttf", 24) #文字模組，用來顯示文字，可用來顯示儀表板資料
score_file = folders["save"]+"high_score.txt" #紀錄最高成績


#雲
class Cloud(pygame.sprite.Sprite): #繼承pygame.sprite.Sprite對象
    name = "Cloud"
    def __init__(self, image, x_pos, y_pos): #設定物件本身(self)屬性(x_pos/y_pos)為座標
        super().__init__()
        self.image = image #初始化圖片
        self.x_pos = x_pos #初始化X座標
        self.y_pos = y_pos #初始化Y座標
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #呼叫圖片並重新設置XY座標

    def update(self): #雲的移動
        self.rect.x -= 1 #計算雲的新座標


#恐龍
class Dino(pygame.sprite.Sprite):
    name = "Dino"
    normal_height = 0
    ducking_height = 0
    rising_height = 0
    def __init__(self, x_pos, y_pos): #設定恐龍的座標
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load(folders["img"]+"Dino1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load(folders["img"]+"Dino2.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(folders["img"]+"DinoDucking1.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(folders["img"]+"DinoDucking2.png"), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.normal_height = y_pos
        self.ducking_height = y_pos + 20
        self.rising_height = y_pos - 260
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 30
        self.gravity = 4.5
        self.ducking = False
        self.jump_delay = 5
        self.jump_count = 0
        self.rising = False

    def jump(self): #恐龍跳躍時會換成跳躍動作，跳到一定高度會落下
        jump_sfx.play()
        if self.rect.centery >= self.normal_height:
            self.rising = True
        #     for i in range(self.jump_delay):
        #         self.rect.centery -= self.velocity
                
        #     while self.rect.centery - self.velocity > 40:
        #         self.rect.centery -= 1
    
    def rise(self):
        if self.rising and self.rect.centery >= self.rising_height:
            self.rect.centery -= self.velocity
            return True
        elif self.rising and not self.rect.centery < self.rising_height:
            self.rising = False
            return False
        else:
            self.rising = False
            return False

    def duck(self):
        self.ducking = True
        self.rect.centery = 380 #當恐龍蹲下時，改變座標以及顯示圖案

    def unduck(self):
        self.ducking = False
        self.rect.centery = self.normal_height #當沒有跳的時候，回到原本的高度

    def apply_gravity(self): #當恐龍不在地面時 就會因重力落下
        if self.rect.centery <= self.normal_height:
            self.rect.centery += self.gravity

    def update(self): 
        self.animate()
        self.apply_gravity()

    def animate(self): #讓恐龍能夠看起來像是在跑
        self.current_image += 0.05

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)%2]
        else:
            self.image = self.running_sprites[int(self.current_image)%2]


#仙人掌
class Cactus(pygame.sprite.Sprite): #繼承pygame.sprite.Sprite對象
    name = "Cactus"
    def __init__(self, x_pos, y_pos):  #設定物件本身(self)屬性(x_pos/y_pos)為座標
        super().__init__()  #使用父類的初始化方法來初始化子類
        self.x_pos = x_pos #初始化X座標
        self.y_pos = y_pos #初始化Y座標
        self.sprites = [] #負責對sprite做以下指令
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(folders["img"]+f"cactus{i}.png"), (80, 80)) #匯入仙人掌圖片並給予座標
            self.sprites.append(current_sprite) #呼叫sprite並附加上當前的sprite
        self.image = random.choice(self.sprites) #匯入圖片
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #顯示圖片並展現座標

    def update(self): #重新定義
        self.x_pos -= game_speed #降低遊戲前進速度
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #顯示圖片並展現座標


#金幣
class Coin(pygame.sprite.Sprite): #繼承pygame.sprite.Sprite對象
    name = "Coin"
    def __init__(self, x_pos, y_pos):  #設定物件本身(self)屬性(x_pos/y_pos)為座標
        super().__init__()  #使用父類的初始化方法來初始化子類
        self.x_pos = x_pos #初始化X座標
        self.y_pos = y_pos #初始化Y座標
        self.sprites = [] #負責對sprite做以下指令
        current_sprite = pygame.transform.scale(
                pygame.image.load(folders["img"]+"coin50.png"), (80, 80)) #匯入仙人掌圖片並給予座標
        self.sprites.append(current_sprite) #呼叫sprite並附加上當前的sprite
        self.image = random.choice(self.sprites) #匯入圖片
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #顯示圖片並展現座標

    def update(self): #重新定義
        self.x_pos -= game_speed #降低遊戲前進速度
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #顯示圖片並展現座標

    def die(self):
        self.kill()



#翼龍
class Ptero(pygame.sprite.Sprite): #繼承pygame.sprite.Sprite對象
    name = "Ptero"
    def __init__(self): #初始化物件
        super().__init__() #使用父類的初始化方法來初始化子類
        self.x_pos = 1300 #定義X座標
        self.y_pos = random.choice([285, 295, 350]) #隨機選取Y座標
        self.sprites = [] #負責對sprite做以下指令
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load(folders["img"]+"Ptero1.png"), (70, 52))) #呼叫圖片1並展現其XY座標
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load(folders["img"]+"Ptero2.png"), (70, 52))) #呼叫圖片2並展現其XY座標
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #顯示圖片並展現座標

    def update(self): #重新定義
        self.animate() #呼叫動畫
        self.x_pos -= game_speed #降低遊戲前進速度
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #顯示圖片並展現座標

    def animate(self): #定義動畫並執行下列指令
        self.current_image += 0.025 #當前圖片加值0.025
        self.image = self.sprites[int(self.current_image)%2] #呼叫當前圖片數值


# Variables
game_speed = 5 #設定遊戲速度
jump_count = 10 #設定跳躍的圖片
player_score = 0 #設定遊戲速度
game_over = False #設定遊戲結束
obstacle_timer = 0 #設定障礙物時間
obstacle_spawn = False #設定障礙物產生
obstacle_cooldown = 1000 #設定障礙物cooldown
game_start = False #設定遊戲開始
start_time = 0 #設定遊戲開始時間
play_time = 0 #設定遊玩時間
show_best = False #設定最佳戰績



#讀取地面圖片並將其起始位置設定在畫面最左邊，中心點在畫面底部中央
ground = pygame.image.load(folders["img"]+"ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))
#讀取雲朵圖片
cloud = pygame.image.load(folders["img"]+"cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))


#設定Groups方便分組管理
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()


#設定主角恐龍的起始位置
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)


#加入死亡、得分、跳躍音效
death_sfx = pygame.mixer.Sound(folders["audio"]+"assets_sfx_lose.mp3")
points_sfx = pygame.mixer.Sound(folders["audio"]+"assets_sfx_100points.mp3")
jump_sfx = pygame.mixer.Sound(folders["audio"]+"assets_sfx_jump.mp3")
getCoin_sfx = pygame.mixer.Sound(folders["audio"]+"assets_sfx_getCoin.mp3")


#建立CLOUD_EVENT，每3000毫秒觸發一次來生成雲朵（.USEREVENT是一個常量，用於創建自定義事件）
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)


#遊戲開始
def start_game():
    global game_start, start_time, high_score
    game_start = True
    start_time = time.time()
    #讀取最高紀錄  
    try:
        with open(score_file, "r") as file:
            high_score = int(float(file.read()))
    except FileNotFoundError:
        high_score = 0


#遊戲結束
def end_game():
    global player_score, game_speed, high_score
    #顯示Game Over
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    screen.blit(game_over_text, game_over_rect)
    #顯示分數
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(score_text, score_rect)
    #判斷是否為最高成績，並寫進file裡
    if player_score > high_score:
        global show_best
        high_score = player_score
        with open(score_file, "w") as file:
            file.write(str(int(high_score)))
        show_best = True
    if show_best:
        best_text = game_font.render("*BEST*", True, "red")
        best_rect = best_text.get_rect(center=(score_rect.centerx + 215, 340))
        screen.blit(best_text, best_rect)
    #顯示遊玩時間
    play_time_minutes = play_time // 60
    play_time_seconds = play_time % 60
    play_time_text = game_font.render(f"Time: {play_time_minutes:02d}:{play_time_seconds:02d}", True, "black")
    play_time_rect = play_time_text.get_rect(center=(640, 380))
    screen.blit(play_time_text, play_time_rect)
    #恢復原始速度，清空雲朵和障礙物
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()
    bonus_group.empty()


#主迴圈
while True:
    #獲取按鍵狀態，按下時恐龍蹲，否則不蹲
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    elif dinosaur.ducking:
        dinosaur.unduck()
    #事件處理
    for event in pygame.event.get():
        #關閉遊戲視窗
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #如果是CLOUD_EVENT就隨機生成雲朵（圖像，x，隨機從50~300生成y），並將其加進group
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        #當玩家按下某個鍵時
        if event.type == pygame.KEYDOWN:
            if not game_start:
                start_game()
            #如果是空白鍵或上，恐龍跳
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                #如果遊戲已經結束，玩家按任意鍵遊戲就會重新開始
                if game_over:
                    game_over = False
                    show_best = False
                    game_speed = 5
                    player_score = 0
                    start_time = time.time()
                else:
                    dinosaur.jump()
    #每一幀都用白色畫面刷新
    screen.fill("white")



    #遊戲還沒開始時呈現的畫面
    if not game_start:
        screen.blit(dinosaur.image, dinosaur.rect)
        screen.blit(ground, (ground_x, 360))
        game_start_text = game_font.render("Press any key to start", True, "black")
        game_start_rect = game_start_text.get_rect(center=(750, 300))
        screen.blit(game_start_text, game_start_rect)
        pygame.display.update()
        continue


    #碰撞檢測（第一個參數是sprite，第二個是sprite所在的組，第三個是碰撞之後是否刪除sprite）
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True #有發生碰撞為True，則game over
        death_sfx.play() #播放死亡音效

    if pygame.sprite.spritecollide(dino_group.sprite, bonus_group, True):
        getCoin_sfx.play()
        player_score += 20


    if game_over:
        end_game() #game over遊戲結束


    if not game_over:
        game_speed += 0.0025 #加快遊戲速度
        current_time = time.time()
        play_time = int(current_time - start_time)

        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play() #播放得分音效

        #獲取以毫秒爲單位的時間，並設定障礙物產生
        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        #產生障礙物
        if obstacle_spawn:
            obstacle_random = random.randint(1, 58)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1280, 340)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(10, 15):
                new_obstacle = Coin(1280, 340)
                bonus_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1 #遊戲分數增加
        player_score_surface = game_font.render(str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10)) #視窗變數.blit(背景變數, 繪製位置)

        dinosaur.rise()
        cloud_group.update()#更新雲
        cloud_group.draw(screen)#把雲畫到螢幕上


        ptero_group.update()#更新翼龍
        ptero_group.draw(screen)#把翼龍畫到螢幕上


        dino_group.update()#更新恐龍
        dino_group.draw(screen)#把恐龍畫到螢幕上


        obstacle_group.update()#更新障礙物
        obstacle_group.draw(screen)#把障礙物畫到螢幕上

        bonus_group.update()#更新障礙物
        bonus_group.draw(screen)#把障礙物畫到螢幕上


        ground_x -= game_speed #移動背景

        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))

        if ground_x <= -1280:
            ground_x = 0 #背景重新回到畫面最左邊
        
        #於遊玩畫面中顯示最高分的歷史紀錄
        high_score_text = game_font.render(f"HI: {int(high_score)}", True, "black")
        high_score_rect = high_score_text.get_rect(center=(1015, 22))
        screen.blit(high_score_text, high_score_rect)


    clock.tick(120)
    pygame.display.update()