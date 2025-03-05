# *** IMPORTERA ALLA MODULER OCH STARTA PYGAME ***
# Importerar pygame
import pygame

# Importerar random för att kunna skapa slumptal
import random

# Initiera pygame
pygame.init()

# Initiera Pygame Mixer
pygame.mixer.init()

# Ladda och spela bakgrundsmusiken (ange filnamnet)
pygame.mixer.music.load("assets/music/Mesmerizing Galaxy Loop.mp3") # Ersätt med rätt sökväg
pygame.mixer.music.set_volume(0.5) # Justera volym (0.0 - 1.0)
pygame.mixer.music.play(-1) # Spela loopen (-1 betyder oändlig loop)

# Ladda ljudeffekter
sound_liten_explosion = pygame.mixer.Sound("assets/sounds/scfi_explosion.wav") # Explosion-ljud
sound_stor_explosion = pygame.mixer.Sound("assets/sounds/huge_explosion.wav") # Explosion-ljud

# Justera volym om det behövs
sound_liten_explosion.set_volume(0.7)
sound_stor_explosion.set_volume(0.9)

# *** KONFIGURERA FÖNSTRET ***
# Skärmstorlek
SKÄRMENS_BREDD = 800
SKÄRMENS_HÖJD = 600

# Skapar en skärm med angiven bredd och höjd
skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

# Sätter en fönstertitel på spelet
pygame.display.set_caption("Space Shooter")

# *** LADDAR IN ALLA SPRITES ***
# Laddar i en ny sprite för rymdskeppet
original_bild = pygame.image.load("assets/sprites/SpaceShip.png")
# Laddar in en ny sprite för jetstrålen till rymdskeppet
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")
# Laddar i en ny sprite till ett skott till rymdskeppet
sprite_skott = pygame.image.load("assets/sprites/bullet.png")
# Laddar in en ny sprite till en liten ateroid
sprite_asteroid_liten = pygame.image.load("assets/sprites/small-A.png")

# *** LADDAR IN ALLA BAKGRUNDSBILDER ***
# Laddar en stjärnbakgrund
background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/Stars-A.png")

# Skalar om rymdskeppet till halva storleken
# Den nya spriten länkas till sprite_spelare
# OBS // är operatorn för heltalsdivision
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

# Sätt spelarens startposition
spelare_x = SKÄRMENS_BREDD // 2 - 60
spelare_y = SKÄRMENS_HÖJD - 110
spelarens_hastighet = 1

# Sätt jetstrålens starposition
jetstråle_x = spelare_x + 13
jetstråle_y = spelare_y + 46

# *** BAKGRUNDSRÖRELSE ***
# Bakgrunds Y-position (börjar från toppen av skärmen)
bakgrund_y = 0

# Skapar en tom lista att fylla för alla skotten som spelaren avfyrar
skott_lista = [] # Lista för att hålla reda på alla skott

asteroid_liten_lista = []

# Lista för alla explosioner (varje explosion är en lista med partiklar)
explosioner = []

# Variabler för att kunna skapa en kort fördröjning som hindrar spelaren från att skjuta för ofta
skott_räknare = 0 # Håller koll på tiden mellan skott

# Variabel för att skapa en fördröjning för hur ofta en asteroid får skapas
asteroid_liten_räknare = 0

# Färger som används till explosionseffekten
SVART = (0, 0, 0)
FÄRG_LISTA = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]  # Röd, orange, gul

# Denna klass hanterar allt som rör spelarens rymdskepp
class RymdSkepp:
    def __init__(self):
        """Alla instansvariabler för rymdskeppet"""
        self.spelare_x = SKÄRMENS_BREDD // 2 - 60 # Rymdskeppets startposition x-led
        self.spelare_y = SKÄRMENS_HÖJD - 110 # Rymdskeppets startposition y-led
        self.sprite_spelare = sprite_spelare # Spelarens sprite/bild

        self.jetstråle_x = spelare_x + 13 # Jetstrålens startposition x-led
        self.jetstråle_y = spelare_y + 46 # Jetstrålens startposition y-led
        self.sprite_jetstråle = sprite_jetstråle # Jetstrålens sprite/bild

        self.spelarens_hastighet = 1 # Rymdskeppets hastighet

        self.exploderat = False # När spelet börjar har INTE rymdskeppet exploderat

        # Skapar en rektangel för rymdskeppet baserat på dess position och storlek
        self.kollision_rektangel = pygame.Rect(self.spelare_x, self.spelare_y, self.sprite_spelare.get_width(), self.sprite_spelare.get_height())
    
    def flytta(self, riktning):
        """Flyttar spelaren i en viss riktning."""
        if not self.exploderat: # Om rymdskeppet har exploderat, gör ingeting
            if riktning == "vänster":
                self.spelare_x = self.spelare_x - self.spelarens_hastighet
                self.jetstråle_x = self.jetstråle_x - self.spelarens_hastighet
            elif riktning == "höger":
                self.spelare_x = self.spelare_x + self.spelarens_hastighet
                self.jetstråle_x = self.jetstråle_x + self.spelarens_hastighet
            elif riktning == "upp":
                self.spelare_y = self.spelare_y - self.spelarens_hastighet
                self.jetstråle_y = self.jetstråle_y - self.spelarens_hastighet
            elif riktning == "ner":
                self.spelare_y = self.spelare_y + self.spelarens_hastighet
                self.jetstråle_y = self.jetstråle_y + self.spelarens_hastighet
            
            # Flytta med kollisionsrektangeln till där rymdskeppet är
            self.kollision_rektangel.topleft = (self.spelare_x, self.spelare_y)
    
    def rita(self, skärm):
        """Ritar spelaren på skärmen."""
        if not self.exploderat: # Om rymdskeppet har exploderat, rita inte det längre
            skärm.blit(self.sprite_spelare, (self.spelare_x, self.spelare_y))
            skärm.blit(self.sprite_jetstråle, (self.jetstråle_x, self.jetstråle_y))

            # Rita kollisionsrektangeln (färgen kan justeras)
            pygame.draw.rect(skärm, (0, 0, 255), self.kollision_rektangel, 2) # Blå rektangel med trjocklek 2
        else:
            # Ta bort kollisionsrektangeln när rymdskeppet är förstört
            self.kollision_rektangel = pygame.Rect(0, 0, 0, 0)

# Denna klass hanterar liten asteroid.
class AsteroidLiten:
    # Sätter alla instansvariabler för asteroiden
    def __init__(self, asteroid_liten_x, asteroid_liten_y):
        self.x = asteroid_liten_x # Asteroidens position i x-led
        self.y = asteroid_liten_y # Asteroidens position i y-led
        self.hastighet = 1 # Asteroidens rörelsehastighet
        self.bild = sprite_asteroid_liten # Använd sprite-bilden
        self.kollisions_rektangel_asteroid = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())
        
    # Metod som flyttar asteroiden neråt
    def flytta(self):
        self.y = self.y + self.hastighet # Flytta asteroiden neråt
        self.kollisions_rektangel_asteroid.topleft = (self.x, self.y) # Uppdatera rektangelns position

    # Metod som ritar asteroiden på skärmen
    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y)) # Rita asteroiden på skärmen

    # Rita kollisionsrektangeln (färgen kan justeras)
        #pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel_asteroid, 2) # Röd rektangel med tjocklek 2
    
    # Metod som undersöker om asteroiden har kolliderat med rymdskeppet
    def kollidera(self, rymdskepp):
        if not spelare.exploderat: # Kontrollera kollision endast om skeppet inte är förstört
            if (self.kollisions_rektangel_asteroid.colliderect(rymdskepp)):
                print("Kollision upptäckt med rymdskeppet!")
                sound_stor_explosion.play()
                spelare.exploderat = True
                explosion = [Partikel(jetstråle_x, jetstråle_y) for _ in range(100)] # Skapa 100 partiklar
                explosioner.append(explosion)
    
    def kollidera_med_skott(self, skott_lista):
        """Kontrollerar om en asteroid har kolliderat med ett skott"""
        for skott in skott_lista:
            if self.kollisions_rektangel_asteroid.colliderect(pygame.Rect(skott.x, skott.y, skott.bild.get_width(), skott.bild.get_height())):
                print("Asteroiden träffades av skottet!")
                sound_liten_explosion.play()
                skott_lista.remove(skott) # Ta bort skottet
                explosion = [Partikel(self.x + self.bild.get_width() // 2, self.y + self.bild.get_height() // 2) for _ in range(100)]
                explosioner.append(explosion) # Skapa explosionseffekten
                return True # Returnera True om kollision har skett
        return False

# Klass för en enskild partikel
class Partikel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.livstid = random.randint(20, 50)  # Hur länge partikeln lever
        self.hastighet_x = random.uniform(-2, 2)  # Slumpmässig rörelse i x-led
        self.hastighet_y = random.uniform(-2, 2)  # Slumpmässig rörelse i y-led
        self.radius = random.randint(3, 6)  # Storlek på partikeln
        self.färg = random.choice(FÄRG_LISTA)  # Slumpmässig färg

    def uppdatera(self):
        self.x += self.hastighet_x  # Flytta partikeln i x-led
        self.y += self.hastighet_y  # Flytta partikeln i y-led
        self.livstid -= 1  # Minska livslängden

    def rita(self, skärm):
        if self.livstid > 0:
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius)
    
spelare = RymdSkepp()

paus = 0

# *** SPELET STARTAR HÄR ***
# Spelloop
spelet_körs = True
while (spelet_körs == True):
    # *** RITA BAKGRUNDSBILDEN ***
    # Skapa en mörk bakgrundsbild
    skärm.blit(background_mörkblå, (0,0))

    # Rita stjärnorna i bakgrunden
    skärm.blit(background_stjärnor, (0, bakgrund_y)) # Lägg till stjärnbilden från hörnet (0, 0)

    # Rita en andra bakgrundsbild utanför skärmen för att skapa illusionen av kontinuerlig rörelse
    skärm.blit(background_stjärnor, (0, bakgrund_y - SKÄRMENS_HÖJD)) # Andra bilden som ligger ovanpå den första

    # Uppdatera både bakgrundsbildernas position
    bakgrund_y = bakgrund_y + 2 # Rör bakgrunden neråt (justera denna för att få önskad hastighet)

    # Om bakgrunden har rört sig för långt (längden på skärmen) så sätt tillbaka till toppen
    if bakgrund_y >= SKÄRMENS_HÖJD:
        bakgrund_y = 0

    # *** SAMTLIGA KLASSER I SPELET ***
    # # Denna klass hanterar det vanliga skottet som skeppet kan skjuta
    class Skott:
        # Sätter alla instansvariabler som hör till skottet
        def __init__(self, x, y):
            self.x = x # Skottets position i x-led
            self.y = y # Skottets position i y-led
            self.hastighet = 5 # Skottets rörelsehastighet
            self.bild = sprite_skott # Använd sprite-bilden
            
        # Metod som flyttar skottet uppåt
        def flytta(self):
            self.y = self.y - self.hastighet # Flytta skottet uppåt
                
        #Metod som ritar skottet på skärmen
        def rita(self, skärm):
            skärm.blit(self.bild, (self.x, self.y)) # Rita skottet på skärmen

    # *** LITEN ASTEROID ***
    # Om tillräckligt lång tid passerat
    if (asteroid_liten_räknare >= 60):
        # Skapar en ny instans av asteroiden
        asteroid_liten_lista.append(AsteroidLiten(random.randint(0, SKÄRMENS_BREDD), -50))
        # Återställ räknaren
        asteroid_liten_räknare = 0

    # Uppdaterar asteroid_litens räknare för att se när nästa asteroid ska skapas i spelet
    asteroid_liten_räknare = asteroid_liten_räknare + 1

    # Skapa en rektangel för rymdskeppet baserat på dess position och storlek
    kollisions_rektangel_spelare = pygame.Rect(spelare_x, spelare_y, sprite_spelare.get_width(), sprite_spelare.get_height())

    # Rita kollisionsrektangeln (färger kan justeras)
    #pygame.draw.rect(skärm, (0, 0, 255), kollisions_rektangel_spelare, 2) # Blå rektangel med tjocklek 2

    # Loopar igenom asteroidlistan baklänges och flyttar varje instans av asteroiderna och ritar dem på skärmen
    for asteroid_liten in reversed(asteroid_liten_lista): # Iterera baklänges genom listan
        asteroid_liten.flytta()
        asteroid_liten.kollidera(kollisions_rektangel_spelare)
        asteroid_liten.rita(skärm)

        # Ta bort asteroider som hamnat utanför skärmen
        if asteroid_liten.y > 600:
            asteroid_liten_lista.remove(asteroid_liten)

    # Om asteroiden kolliderar med ett skot
        if asteroid_liten.kollidera_med_skott(skott_lista):
            asteroid_liten_lista.remove(asteroid_liten) # Ta bort asteroiden från listan

    # Om spelarens skepp exploderat läggs en kort paus in här innan spelet avslutas
    if (spelare.exploderat == True):
        paus = paus + 1
        if (paus >= 120):
            exit()

    # Hantera tangenttryckningar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x = spelare_x - spelarens_hastighet
        jetstråle_x = jetstråle_x - spelarens_hastighet
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x = spelare_x + spelarens_hastighet
        jetstråle_x = jetstråle_x + spelarens_hastighet
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y = spelare_y - spelarens_hastighet
        jetstråle_y = jetstråle_y - spelarens_hastighet
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_width() + 26:
        spelare_y = spelare_y + spelarens_hastighet
        jetstråle_y = jetstråle_y + spelarens_hastighet
    # Om spelaren trycker på X skjut en kula
    if keys[pygame.K_x]:
        # Om tilräckligt lång tid har gått frå spelaren skjuta igen
        if (skott_räknare > 30):
            # Uppdaterar skottlistan med en ny instans (kopia av skottet) på den position där det avfyrades
            skott_lista.append(Skott(spelare_x + 20, spelare_y))
            
            # Nollställer räknaren
            skott_räknare = 0
            
    for skott in reversed(skott_lista): # Iterera baklängen genom listan
        skott.flytta()
        skott.rita(skärm)

        # Ta bort skott som hamnat utanför skärmen
        if skott.y < -50:
            skott_lista.remove(skott)

    # Rita spelare
    # blit är en metod i Pygame som används för att rita (eller kopiera) en bild (eller yta) till en annan yta
    skärm.blit(sprite_spelare, (spelare_x, spelare_y))

    # Rita Jetstråle
    skärm.blit(sprite_jetstråle, (jetstråle_x, jetstråle_y))

    # Uppdatera och rita explosionerna
    for explosion in explosioner:
        for partikel in explosion:
            partikel.uppdatera()
            partikel.rita(skärm)

    # Ta bort döda partiklar (de som har en livslängd på 0)
    explosioner = [[p for p in explosion if p.livstid > 0] for explosion in explosioner]
    explosioner = [e for e in explosioner if len(e) > 0]  # Ta bort tomma explosioner

    # Uppdaterar grafiken på skärmen så att spelaren ser vart alla spelfigurer flyttat någonstans
    pygame.display.update()

    # Den här koden kollar hela tiden om användaren försöker stänga spelet
    # genom att klicka på fönstrets stängknapp.
    for event in pygame.event.get():
        # Om användaren klickar på fönstrets stängningsknapp avslutas loopen
        if event.type == pygame.QUIT:
            spelet_körs = False
    
    # Ökar skott räknaren
    skott_räknare = skott_räknare + 1

# Avslutar spelet
pygame.quit()

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
# Google Presentationer: 139