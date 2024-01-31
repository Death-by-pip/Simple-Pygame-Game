import pygame
from pygamevideo import Video

class Solid(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        super().__init__()
        self.image = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0, 128), (size, size), size)
        self.rect = self.image.get_rect(center = (x,y))

# class Player(pygame.sprite.Sprite):

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
    with open(stage+".txt", "r") as f:
        f

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800))
pygame.display.toggle_fullscreen()

display_radius = 3

stages = ["start"]

while True:
