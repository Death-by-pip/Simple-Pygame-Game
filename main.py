import pygame
# from pygamevideo import Video

enable_display_window = True

display_size = 6
block_size = 50
tick = 20

pygame.init()
clock = pygame.time.Clock()
if enable_display_window:
    window = pygame.display.set_mode((display_size*block_size, display_size*block_size))
    window_rect = pygame.Rect(0,0,display_size*block_size, display_size*block_size)
    screen = pygame.Surface((display_size*block_size, display_size*block_size), pygame.SRCALPHA)
else:
    screen = pygame.display.set_mode((display_size*block_size, display_size*block_size))
# pygame.display.toggle_fullscreen()

blocks = {
    "#": (0,0,0,255),
    "|": (70,30,5,255),
    "/": (70,30,5,255),
    ":": (35,15,2,255),
    "@": (35,15,2,255),
    " ": (150,200,255,255),
    "$": (150,200,255,255),
    ">": (150,200,255,255),
    "<": (150,200,255,255),
    "V": (150,200,255,255),
    "^": (150,200,255,255),
    "&": (150,70,10,255),
    "~": (80,80,80,255),
}

# class Solid(pygame.sprite.Sprite):
#     def __init__(self, x, y, ):
#         super().__init__()
#         self.image = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
#         pygame.draw.circle(self.image, (255, 0, 0, 128), (size, size), size)
#         self.rect = self.image.get_rect(center = (x,y))

class Player(pygame.sprite.Sprite):
    def __init__(self, relative_size=0.75):
        super().__init__()
        self.size = relative_size*block_size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (160, 210, 80, 250), pygame.rect.Rect(0,0,self.size,self.size))
        self.rect = self.image.get_rect(center = (0,0))
        self.deltax = 0
        self.deltay = 0
        self.x = 0
        self.y = 0
        self.dead = False

    # def redefine_player(self,x,y):
    #     self.image = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
    #     pygame.draw.rect(self.image, (160, 210, 80, 250), pygame.rect.Rect(0,0,self.size*2,self.size*2))
    #     self.rect = self.image.get_rect(center = (0,0))

    def move(self, map_, moves, xspeed=4, jumpspeed=-10, acceleration=1, maxspeed=10):  # moves = [left, right, up]
        # keys = pygame.key.get_pressed()
        # print("")
        multiplier = block_size/tick
        self.deltax = 0
        jump = False
        if moves[1]:
            self.deltax += xspeed*multiplier
        if moves[0]:
            self.deltax -= xspeed*multiplier
        if moves[2]:
            jump = True
        self.y+=1
        if "#" in self.get_collided(map_):
            if jump:
                self.deltay = jumpspeed*multiplier
            else:
                self.deltay = 0
        else:
            self.deltay += acceleration*multiplier
        self.y-=1
        if self.deltay>maxspeed*multiplier:
            self.deltay = maxspeed*multiplier
        elif self.deltay < -maxspeed*multiplier:
            self.deltay = -maxspeed*multiplier
        deltax = round(self.deltax)
        deltay = round(self.deltay)
        while (deltax!=0 or deltay!=0):
            if deltax<0:
                self.x -= 1
            elif deltax>0:
                self.x += 1
            if "#" in self.get_collided(map_):
                if deltax<0:
                    self.x += 1
                elif deltax>0:
                    self.x -= 1
                deltax = 0
            elif deltax<0:
                deltax += 1
            elif deltax>0:
                deltax -= 1

            if deltay<0:
                self.y -= 1
            elif deltay>0:
                self.y += 1
            if "#" in self.get_collided(map_):
                if deltay<0:
                    self.y += 1
                elif deltay>0:
                    self.y -= 1
                deltay = 0
            elif deltay<0:
                deltay += 1
            elif deltay>0:
                deltay -= 1
        self.update()
        # if enable_display_window:
        #     window_rect.center = (self.x,self.y)
        #     window.blit(screen,(0,0),window_rect)

    def get_collided(self, map_):
        self.rect.center = (self.x, self.y)
        collided = []
        y = [(self.rect.top)//block_size, self.rect.centery//block_size, (self.rect.bottom-1)//block_size]
        x = [(self.rect.left)//block_size, self.rect.centerx//block_size, (self.rect.right-1)//block_size]
        # lvl = [i for i in map_]
        # lvl[y[1]] = lvl[y[1]][:x[1]]+"$"+lvl[y[1]][x[1]+1:]
        # print("\n".join(lvl))
        # print(x, y)
        if x[2]==x[1]:
            x.pop(2)
            # print("left")
            # collide = "left"
        if x[0]==x[1]:
            x.pop(0)
            # print("right")
        #     collide = "right"
        # if len(x)==1:
        #     collide = ""
        if y[2]==y[1]:
            y.pop(2)
            # print("up")
            # collide2 = "up"
        if y[0]==y[1]:
            y.pop(0)
            # print("down")
        #     collide2 = "down"
        # if len(y)==1:
        #     collide2 = ""
        # print(x, y)
        global playing
        if y[-1]>len(map_):
            print("Player has died.")
            # global playing
            self.dead = True
            return ["X"]
        for x_ in x:
            for y_ in y:
                try:
                    collided.append(map_[y_][x_])
                except:
                    collided.append("X")
        if "@" in collided:
            global advance
            advance = True
        if ">" in collided:
            global win
            # global playing
            playing = False
            win = True
        print(collided)
        return collided

    def update(self):
        self.rect.center = (self.x, self.y)
        # print(self.x, self.y)
        if enable_display_window:
            window.fill((0,0,0,255))
            # print(self.x, self.y)
            window_rect.center = (self.x, self.y)
            # print(window_rect.center)
            # # print(window_rect.centerx)
            # print(window_rect.width/2)
            # print(screen.get_width())
            height = 0
            width = 0
            if self.x < window_rect.width//2:
                # print("left")
                width = window_rect.width//2 - window_rect.centerx
                window_rect.centerx = window_rect.width/2
            elif (self.x+window_rect.width//2)>screen.get_width():
                # print("right")
                width = window_rect.width//2 - window_rect.centerx
                window_rect.centerx = screen.get_width()-window_rect.width/2
            if self.y < window_rect.height//2:
                # print("up")
                height = window_rect.height//2 - window_rect.centery
                window_rect.centery = window_rect.height/2
            elif (self.y+window_rect.height//2)>screen.get_height():
                # print("down")
                height = window_rect.height//2 - window_rect.centery + block_size
                window_rect.centery = screen.get_height()-window_rect.height/2
            # print(window_rect.center)
            window.blit(screen.subsurface(window_rect).copy(), (0, 0))
            window.blit(self.image, (window_rect.width//2-width-self.size//2, window_rect.height//2-height-self.size//2))

def clamp(value, min, max):
    if value<min:
        return min
    elif value>max:
        return max
    else:
        return value

# def playcutscene(title: str, extension="mp4"):
#     cutscene = Video("cutscenes/"+title+"."+extension)
#     cutscene.play()

#     while cutscene.remaining_time>0:
#         clock.tick(0)
#         cutscene.draw_to(screen, (0,0))
#         pygame.display.flip()

def load_level(stage, sleep=False):
    with open("levels/"+stage+".txt", "r") as f:
        lvl = ("".join(f.readlines()).split("\n"))
    lvl1 = lvl[:lvl.index("zzz")]
    lvl2 = lvl[lvl.index("zzz")+1:]
    if sleep:
        lvl = [(lvl1[i].replace("$"," ").replace("@",":").replace(">"," ").replace("[","").replace("]","")+lvl2[i]).replace("[","").replace("]","") for i in range(len(lvl1))]
    else:
        lvl = [row.replace("[","").replace("]","") for row in lvl1]
    for n, row in enumerate(lvl):
        if "$" in row:
            player.y = n*block_size
            player.x = row.find("$")*block_size
            break
    
    global screen
    if enable_display_window:
        screen = pygame.Surface((len(lvl[0])*block_size, len(lvl)*block_size))
    else:
        screen = pygame.display.set_mode((len(lvl[0])*block_size, len(lvl)*block_size))
    screen.fill(blocks[" "])
    for y, row in enumerate(lvl):
        for x, tile in enumerate(row):
            if tile in ["/","\\"]:
                n = [row[x+1], lvl[y+1][x], row[x-1], lvl[y-1][x]]
                n_map = {
                    "|": 3,
                    "/": 2,
                    "\\": 2,
                    "#": 1
                }
                n = [n_map[i] if i in n_map.keys() else 0 for i in n]
                if tile=="/":
                    if (n[0]+n[1]) >= (n[2]+n[3]):
                        pygame.draw.polygon(screen, blocks["/"], (((x+1)*block_size,(y)*block_size), ((x)*block_size,(y+1)*block_size), ((x+1)*block_size,(y+1)*block_size)))
                    else:
                        pygame.draw.polygon(screen, blocks["/"], (((x+1)*block_size,(y)*block_size), ((x)*block_size,(y+1)*block_size), ((x)*block_size,(y)*block_size)))
                elif tile=="\\":
                    if (n[2]+n[1]) >= (n[0]+n[3]):
                        pygame.draw.polygon(screen, blocks["/"], (((x)*block_size,(y)*block_size), ((x)*block_size,(y+1)*block_size), ((x+1)*block_size,(y+1)*block_size)))
                    else:
                        pygame.draw.polygon(screen, blocks["/"], (((x+1)*block_size,(y)*block_size), ((x)*block_size,(y)*block_size), ((x+1)*block_size,(y+1)*block_size)))
            else:
                pygame.draw.rect(screen, blocks[tile], pygame.rect.Rect(x*block_size,y*block_size,block_size,block_size))
    if enable_display_window:
        window_rect.center = (player.x+block_size, player.y-block_size)
        window.blit(screen, (0,0), window_rect)
    print("\n".join(lvl))
    return lvl

stages = ["intro"]
player = Player()
advance = False

# while True:
win = False
loaded_stage = load_level(stages[0])
playing = True
moves = [False, False, False]
current = (stages[0], False)
while playing:
    if advance:
        current = (stages[0], True)
        loaded_stage = load_level(stages[0], True)
        advance = False
    if player.dead:
        player.dead = False
        loaded_stage = load_level(current[0], current[1])
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_ESCAPE]:
        # pygame.quit()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # pygame.quit()
            playing = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                # pygame.quit()
                playing = False
            elif event.key==pygame.K_LEFT:
                moves[0] = True
            elif event.key==pygame.K_RIGHT:
                moves[1] = True
            elif event.key==pygame.K_UP:
                moves[2] = True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                moves[0] = False
            elif event.key==pygame.K_RIGHT:
                moves[1] = False
            elif event.key==pygame.K_UP:
                moves[2] = False

    player.move(loaded_stage, moves)

    # offsetx = (player.x%block_size)-block_size/2
    # offsety = (player.y%block_size)-block_size/2
    # x_ = player.x//block_size
    # y_ = player.y//block_size
    # grid = []
    # for y1 in range(display_size+1):
    #     y = y_+y1-display_size//2
    #     row = []
    #     for x1 in range(display_size+1):
    #         x = x_+x1-display_size//2
    #         try:
    #             i = loaded_stage[y][x]
    #         except:
    #             i = "#"
    #         if i in ["/","\\"]:
    #             n = [loaded_stage[y][x+1],loaded_stage[y+1][x],loaded_stage[y][x-1],loaded_stage[y-1][x]]
    #             n_map = {
    #                 "|": 3,
    #                 "/": 2,
    #                 "\\": 2,
    #                 "#": 1
    #             }
    #             if i=="/":
    #                 if (n_map[n[0]]+n_map[n[1]]) >= (n_map[n[2]]+n_map[n[3]]):
    #                     i = "/}"
    #                 else:
    #                     i = "{/"
    #             elif i=="\\":
    #                 if (n_map[n[2]]+n_map[n[1]]) >= (n_map[n[0]]+n_map[n[3]]):
    #                     i = "{\\"
    #                 else:
    #                     i = "\\}"
    #         # if i==".\\":
    #         #     pygame.draw
    #         row.append(i)
    #     grid.append(row)

    # print("coloring screen")
    # screen.fill(blocks[" "])
    # for y in range(display_size+1):
    #     for x in range(display_size+1):
    #         i = grid[y][x]
    #         if i=="./":
    #             pygame.draw.polygon(screen, blocks["/"], [((x1-offsetx)*block_size, (y1-offsety)*block_size) for x1, y1 in [(x-.5,y-.5), (x-.5,y+.5), (x+.5,y-.5)]])
    #         elif i=="/.":
    #             pygame.draw.polygon(screen, blocks["/"], [((x1-offsetx)*block_size, (y1-offsety)*block_size) for x1, y1 in [(x+.5,y-.5), (x-.5,y+.5), (x+.5,y+.5)]])
    #         elif i==".\\":
    #             pygame.draw.polygon(screen, blocks["/"], [((x1-offsetx)*block_size, (y1-offsety)*block_size) for x1, y1 in [(x-.5,y-.5), (x-.5,y+.5), (x+.5,y+.5)]])
    #         elif i=="\\.":
    #             pygame.draw.polygon(screen, blocks["/"], [((x1-offsetx)*block_size, (y1-offsety)*block_size) for x1, y1 in [(x-.5,y-.5), (x+.5,y-.5), (x+.5,y+.5)]])
    #         else:
    #             pygame.draw.rect(screen, blocks["/"], pygame.rect.Rect((x-.5-offsetx)*block_size, (y-.5-offsety)*block_size, block_size, block_size))
    
    # window.blit(player.image, (0,0))
    pygame.display.flip()

    clock.tick(tick)
if win:
    window.fill((0,0,0,255))
    pygame.font.init()
    font = pygame.font.SysFont('Courier New', 30)
    text_surface = font.render('YOU WIN', False, (0, 255, 0, 255))
    window.blit(text_surface, (window_rect.width//2, window_rect.height//2))
    pygame.display.flip()
    while not playing:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                # pygame.quit()
                playing = True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    # pygame.quit()
                    playing = True
pygame.quit()
