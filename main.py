import pygame
from pygamevideo import Video

display_size = 6
block_size = 50
tick = 1

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((display_size*block_size, display_size*block_size))
screen = pygame.Surface((display_size*block_size, display_size*block_size), pygame.SRCALPHA)
pygame.display.toggle_fullscreen()

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
        self.image = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (160, 210, 80, 250), pygame.rect.Rect(0,0,self.size*2,self.size*2))
        self.rect = self.image.get_rect(center = (0,0))
        self.deltax = 0
        self.deltay = 0
        self.x = 0
        self.y = 0

    # def redefine_player(self,x,y):
    #     self.image = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
    #     pygame.draw.rect(self.image, (160, 210, 80, 250), pygame.rect.Rect(0,0,self.size*2,self.size*2))
    #     self.rect = self.image.get_rect(center = (0,0))

    def move(self, map_, xspeed=2, jumpspeed=3, acceleration=-1.8, maxspeed=5):
        keys = pygame.key.get_pressed()
        multiplier = block_size/tick
        self.deltax = 0
        jump = False
        if keys[pygame.K_RIGHT]:
            self.deltax += xspeed*multiplier
        if keys[pygame.K_LEFT]:
            self.deltax -= xspeed*multiplier
        if keys[pygame.K_UP]:
            jump = True
        self.y-=1
        if "#" in self.get_collided(map_):
            if jump:
                self.deltay = jumpspeed*multiplier
            else:
                self.deltay = 0
        else:
            self.deltay += acceleration*multiplier
        self.y+=1
        if self.deltay>maxspeed*block_size:
            self.deltay = maxspeed*block_size
        elif self.deltay < -maxspeed*block_size:
            self.deltay = -maxspeed*block_size
        deltax = self.deltax
        deltay = self.deltay
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
            if deltax<0:
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
            if deltay<0:
                deltay += 1
            elif deltay>0:
                deltay -= 1
        screen.blit(window,(self.x,self.y))

    def get_collided(self, map_):
        collided = []
        y = [(self.y-self.size-1)//block_size, self.y//block_size, (self.y+self.size)//block_size]
        x = [(self.x-self.size-1)//block_size, self.x//block_size, (self.x+self.size)//block_size]
        if x[2]==x[1]:
            x.pop(2)
            # collide = "left"
        if x[0]==x[1]:
            x.pop(0)
        #     collide = "right"
        # if len(x)==1:
        #     collide = ""
        if y[2]==y[1]:
            y.pop(2)
            # collide2 = "up"
        if y[0]==y[1]:
            y.pop(0)
        #     collide2 = "down"
        # if len(y)==1:
        #     collide2 = ""
        if y[-1]>len(map_):
            print("Player has died.")
            return ["X"]
        for x_ in x:
            for y_ in y:
                try:
                    collided.append(map_[y_][x_])
                except:
                    collided.append("#")
        return collided

    def update(self):
        screen.blit(self.image, self.rect.topleft)

def clamp(value, min, max):
    if value<min:
        return min
    elif value>max:
        return max
    else:
        return value

def playcutscene(title: str, extension="mp4"):
    cutscene = Video("cutscenes/"+title+"."+extension)
    cutscene.play()

    while cutscene.remaining_time>0:
        clock.tick(0)
        cutscene.draw_to(screen, (0,0))
        pygame.display.flip()

def load_level(stage, sleep=False):
    with open("levels/"+stage+".txt", "r") as f:
        lvl = ("".join(f.readlines()).split("\n"))
    lvl1 = lvl[:lvl.index("zzz")]
    lvl2 = lvl[lvl.index("zzz")+1:]
    if sleep:
        lvl = [(lvl1[i].replace("$"," ").replace("@",":").replace(">"," ")+lvl2[i]).replace("[","").replace("]","") for i in range(len(lvl1))]
    else:
        lvl = [row.replace("[","").replace("]","") for row in lvl1]
    for n, row in enumerate(lvl):
        if "$" in row:
            player.y = n*block_size
            player.x = row.find("$")*block_size
            break

    screen = pygame.Surface((len(lvl[0])*block_size, len(lvl)*block_size))
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
    screen.blit(window, (player.x, player.y))
    return lvl

stages = ["intro"]
player = Player()

# while True:
loaded_stage = load_level(stages[0])
playing = True
while playing:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    player.move(loaded_stage)

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
    
    window.blit(player.image, (0,0))
    pygame.display.flip()

    clock.tick(tick)
pygame.quit()
