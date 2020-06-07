import pygame, sys
from pygame.locals import *

# Set up pygame.
pygame.init()

# Set up the window.
windowsSurface = pygame.display.set_mode((500,400), 0, 32)
pygame.display.set_caption('Hello world!')

# Set up the colours.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the fonts
basicFont = pygame.font.SysFont(None, 48)

# Set up the text.
text = basicFont.render('Hello world!', True, WHITE, BLUE)
textRect = text.get_rect()
textRect.centerx = windowsSurface.get_rect().centerx
textRect.centery = windowsSurface.get_rect().centery

# Draw the white background onto the surface.
windowsSurface.fill(WHITE)

# Draw a green polygon onto the surface.
pygame.draw.polygon(windowsSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

# Draw some blue lines onto the surface.
pygame.draw.line(windowsSurface, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(windowsSurface, BLUE, (120, 60), (60, 120))
pygame.draw.line(windowsSurface, BLUE, (60, 120), (120, 120), 4)

# Draw a blue circle onto the surface.
pygame.draw.circle(windowsSurface, BLUE, (300, 50), 20, 0)

# Draw a red ellipse onto the surface.
pygame.draw.ellipse(windowsSurface, RED, (300, 250, 40, 80), 1)

# Draw the text's background rectangle onto the surface.
pygame.draw.rect(windowsSurface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

# Get a pixel array of the surface.
pixArray = pygame.PixelArray(windowsSurface)
pixArray[480][380] = BLACK
del pixArray

# Draw the text onto the surface.
windowsSurface.blit(text, textRect)

# Draw the window onto the screen.
pygame.display.update()

# Run the game loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
