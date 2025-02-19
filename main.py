import pygame

pygame.init()

SKÄRMENS_BREDD = 800
SKÄRMENS_HÖJD = 600

skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

pygame.display.set_caption("Space Shooter")

spelet_körs = True

while (spelet_körs == True):
    skärm.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False

# Skriv din kod här för att skapa spelet! Följ dessa steg:
'''
Steg 1 - Skapa en skärm och rita ett skepp
Steg 2 - Lägga till en scrollande stjärnbakgrund
Steg 3 - Sätt jetmotorer på rymdskeppet
Steg 4 - Gör så rymdskeppet kan skjuta
Steg 5 - Slumpa fram Asteroider 
Steg 6 - Detektera kollisioner mellan rymdskeppet och asteroiden
Steg 7 - Skapa explosionseffekten (samt lär dig partikeleffekter)
Steg 8 - Gör så att rymdskeppet kan explodera i kollision med asteroiden
Steg 9 - Gör så att rymdskeppet kan skjuta ner asteroider
Steg 10 - Lägg till musik och ljudeffekter
'''