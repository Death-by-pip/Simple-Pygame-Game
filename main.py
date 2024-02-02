import pygame
from pygamevideo import Video

display_size = 6
block_size = 50

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((display_size*block_size, display_size*block_size))
pygame.display.toggle_fullscreen()

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

    def move(self, map, tick, xspeed=2*block_size, jumpspeed=150, acceleration=-90):
        keys = pygame.key.get_pressed()
        self.deltax = 0
        if keys[pygame.K_RIGHT]:
            self.deltax += xspeed
        if keys[pygame.K_LEFT]:
            self.deltax -= xspeed
        if keys[pygame.K_UP]:
            jump = True
        collision = {}
        y = [(self.y-self.size)//block_size, (self.y+self.size)//block_size]
        x = [(self.x-self.size)//block_size, (self.x+self.size)//block_size]
        if x[1]==x[0]:
            x.pop(0)
        if y[1]==y[0]:
            y.pop(0)
        if y[-1]>len(map):
            print("Player has died.")
            return
        if "#" in map[y[-1]][x]:
            self.deltay = 

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
        lvl = ("".join(f.readlines()).replace("\\\\","\\").split("\n"))
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
    return lvl

stages = ["start"]
player = Player()

# while True:
load_level("intro")
pygame.quit()