import pygame
import sys
import math
from pygame.locals import *

# ==== INICIALIZĀCIJA ====
pygame.init()

# Loga izmēri
LOG_WIDTH = 800
LOG_HEIGHT = 600

# Krāsas
BALTA = (255, 255, 255)
MELNA = (0, 0, 0)
ZAĻA = (0, 255, 0)
SARKANA = (255, 0, 0)
ZILA = (0, 0, 255)
PELĒKA = (200, 200, 200)
GAIŠI_ZILA = (173, 216, 230)

# Fonti
lielais_fonts = pygame.font.Font(None, 36)
mazais_fonts = pygame.font.Font(None, 24)

# Izveidojam logu
logs = pygame.display.set_mode((LOG_WIDTH, LOG_HEIGHT))
pygame.display.set_caption("MaxLiga Spēle")

# ==== SPĒLES KLASE ====
class Spele:
    def __init__(self, sakuma_skaitlis):
        self.pašreizējais_skaitlis = sakuma_skaitlis
        self.kopējie_punkti = 0
        self.banka = 0
        self.spēle_beigusies = False
        self.uzvaretajs = None

    def veikt_gajienu(self, reizinatajs):
        if self.spēle_beigusies:
            return False

        self.pašreizējais_skaitlis *= reizinatajs
        
        if self.pašreizējais_skaitlis % 2 == 0:
            self.kopējie_punkti += 1
        else:
            self.kopējie_punkti -= 1

        if self.pašreizējais_skaitlis % 10 == 0 or self.pašreizējais_skaitlis % 10 == 5:
            self.banka += 1

        if self.pašreizējais_skaitlis >= 3000:
            self.spēle_beigusies = True
            self.noskaidrot_uzvaretaju()
        
        return True

    def noskaidrot_uzvaretaju(self):
        if self.kopējie_punkti % 2 == 0:
            self.kopējie_punkti -= self.banka
        else:
            self.kopējie_punkti += self.banka

        self.uzvaretajs = "Spēlētājs 1" if self.kopējie_punkti % 2 == 0 else "Spēlētājs 2 (dators)"

def heiristiska_funkcija(speles_stavoklis):
    vertejums = 0
    vertejums += speles_stavoklis.kopējie_punkti * 2
    vertejums += speles_stavoklis.banka * 1.5
    
    if speles_stavoklis.pašreizējais_skaitlis >= 2000:
        sods = (speles_stavoklis.pašreizējais_skaitlis - 2000) / 1000
        vertejums -= 15 * sods
    
    if speles_stavoklis.pašreizējais_skaitlis % 2 == 0:
        vertejums += 1.5
    
    last_digit = speles_stavoklis.pašreizējais_skaitlis % 10
    if last_digit == 0 or last_digit == 5:
        vertejums -= 0.8
    
    return vertejums

def minimaksa_algoritms(speles_stavoklis, dziļums, maksimizetajs):
    if dziļums == 0 or speles_stavoklis.spēle_beigusies:
        return heiristiska_funkcija(speles_stavoklis)

    if maksimizetajs:
        max_eval = -math.inf
        for reizinatajs in [3, 4, 5]:
            jauns_stavoklis = Spele(speles_stavoklis.pašreizējais_skaitlis)
            jauns_stavoklis.kopējie_punkti = speles_stavoklis.kopējie_punkti
            jauns_stavoklis.banka = speles_stavoklis.banka
            jauns_stavoklis.veikt_gajienu(reizinatajs)
            eval = minimaksa_algoritms(jauns_stavoklis, dziļums - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for reizinatajs in [3, 4, 5]:
            jauns_stavoklis = Spele(speles_stavoklis.pašreizējais_skaitlis)
            jauns_stavoklis.kopējie_punkti = speles_stavoklis.kopējie_punkti
            jauns_stavoklis.banka = speles_stavoklis.banka
            jauns_stavoklis.veikt_gajienu(reizinatajs)
            eval = minimaksa_algoritms(jauns_stavoklis, dziļums - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def alfabeta_algoritms(speles_stavoklis, dziļums, alfa, beta, maksimizetajs):
    if dziļums == 0 or speles_stavoklis.spēle_beigusies:
        return heiristiska_funkcija(speles_stavoklis)

    if maksimizetajs:
        value = -math.inf
        for reizinatajs in [3, 4, 5]:
            jauns_stavoklis = Spele(speles_stavoklis.pašreizējais_skaitlis)
            jauns_stavoklis.kopējie_punkti = speles_stavoklis.kopējie_punkti
            jauns_stavoklis.banka = speles_stavoklis.banka
            jauns_stavoklis.veikt_gajienu(reizinatajs)
            value = max(value, alfabeta_algoritms(jauns_stavoklis, dziļums - 1, alfa, beta, False))
            alfa = max(alfa, value)
            if alfa >= beta:
                break
        return value
    else:
        value = math.inf
        for reizinatajs in [3, 4, 5]:
            jauns_stavoklis = Spele(speles_stavoklis.pašreizējais_skaitlis)
            jauns_stavoklis.kopējie_punkti = speles_stavoklis.kopējie_punkti
            jauns_stavoklis.banka = speles_stavoklis.banka
            jauns_stavoklis.veikt_gajienu(reizinatajs)
            value = min(value, alfabeta_algoritms(jauns_stavoklis, dziļums - 1, alfa, beta, True))
            beta = min(beta, value)
            if alfa >= beta:
                break
        return value

def datora_gajiens(speles_stavoklis, algoritms, dziļums=3):
    labakais_reizinatajs = 3
    
    if algoritms == "minimaks":
        labakais_vertejums = -math.inf
        for reizinatajs in [3, 4, 5]:
            jauns_stavoklis = Spele(speles_stavoklis.pašreizējais_skaitlis)
            jauns_stavoklis.kopējie_punkti = speles_stavoklis.kopējie_punkti
            jauns_stavoklis.banka = speles_stavoklis.banka
            jauns_stavoklis.veikt_gajienu(reizinatajs)
            vertejums = minimaksa_algoritms(jauns_stavoklis, dziļums, False)
            if vertejums > labakais_vertejums:
                labakais_vertejums = vertejums
                labakais_reizinatajs = reizinatajs
    else:
        labakais_vertejums = -math.inf
        for reizinatajs in [3, 4, 5]:
            jauns_stavoklis = Spele(speles_stavoklis.pašreizējais_skaitlis)
            jauns_stavoklis.kopējie_punkti = speles_stavoklis.kopējie_punkti
            jauns_stavoklis.banka = speles_stavoklis.banka
            jauns_stavoklis.veikt_gajienu(reizinatajs)
            vertejums = alfabeta_algoritms(jauns_stavoklis, dziļums, -math.inf, math.inf, False)
            if vertejums > labakais_vertejums:
                labakais_vertejums = vertejums
                labakais_reizinatajs = reizinatajs
    
    return labakais_reizinatajs

def zimet_pogu(teksts, x, y, platums, augstums, krāsa, parvietojuma_krāsa=None, teksta_krāsa=MELNA):
    pele_pozicija = pygame.mouse.get_pos()
    pogas_taisnstūris = pygame.Rect(x, y, platums, augstums)
    
    if parvietojuma_krāsa and pogas_taisnstūris.collidepoint(pele_pozicija):
        pygame.draw.rect(logs, parvietojuma_krāsa, pogas_taisnstūris)
    else:
        pygame.draw.rect(logs, krāsa, pogas_taisnstūris)
    
    pygame.draw.rect(logs, MELNA, pogas_taisnstūris, 2)
    teksta_virsma = lielais_fonts.render(teksts, True, teksta_krāsa)
    teksta_taisnstūris = teksta_virsma.get_rect(center=pogas_taisnstūris.center)
    logs.blit(teksta_virsma, teksta_taisnstūris)
    
    return pogas_taisnstūris

def zimet_tekstu(teksts, x, y, krāsa=MELNA, fonts=lielais_fonts):
    teksta_virsma = fonts.render(teksts, True, krāsa)
    logs.blit(teksta_virsma, (x, y))
    return teksta_virsma.get_rect(topleft=(x, y))

def galvenais():
    pulkstenis = pygame.time.Clock()
    spele = None
    sakuma_skaitlis = 0
    ievade_aktiva = True
    ievades_teksts = ""
    speletaja_gajiens = True
    pašreizējais_algoritms = "minimaks"
    dziļums = 3
    zinojums = ""
    zinojuma_laiks = 0
    
    while True:
        logs.fill(BALTA)
        
        for notikums in pygame.event.get():
            if notikums.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if notikums.type == KEYDOWN and ievade_aktiva:
                if notikums.key == K_RETURN:
                    if ievades_teksts.strip():
                        try:
                            sakuma_skaitlis = int(ievades_teksts)
                            if 20 <= sakuma_skaitlis <= 30:
                                spele = Spele(sakuma_skaitlis)
                                ievade_aktiva = False
                                zinojums = f"Spēle sākta ar skaitli {sakuma_skaitlis}"
                                zinojuma_laiks = 180
                            else:
                                zinojums = "Skaitlim jābūt no 20 līdz 30!"
                                zinojuma_laiks = 180
                        except ValueError:
                            zinojums = "Ievadiet derīgu skaitli!"
                            zinojuma_laiks = 180
                elif notikums.key == K_BACKSPACE:
                    ievades_teksts = ievades_teksts[:-1]
                elif notikums.unicode.isdigit():
                    ievades_teksts += notikums.unicode
                    
            if notikums.type == MOUSEBUTTONDOWN and not ievade_aktiva and spele:
                pele_pozicija = pygame.mouse.get_pos()
                
                # Algoritma pogas
                minimaks_poga = pygame.Rect(50, 150, 150, 40)
                alfabeta_poga = pygame.Rect(220, 150, 150, 40)
                
                if minimaks_poga.collidepoint(pele_pozicija):
                    pašreizējais_algoritms = "minimaks"
                    zinojums = "Izvēlēts algoritms: Minimaks"
                    zinojuma_laiks = 180
                elif alfabeta_poga.collidepoint(pele_pozicija):
                    pašreizējais_algoritms = "alfabeta"
                    zinojums = "Izvēlēts algoritms: Alfa-beta"
                    zinojuma_laiks = 180
                
                # Gājiena pogas
                if speletaja_gajiens:
                    poga3 = pygame.Rect(50, 250, 100, 50)
                    poga4 = pygame.Rect(170, 250, 100, 50)
                    poga5 = pygame.Rect(290, 250, 100, 50)
                    
                    if poga3.collidepoint(pele_pozicija):
                        if spele.veikt_gajienu(3):
                            speletaja_gajiens = False
                            zinojums = "Izvēlēts reizinātājs: 3"
                            zinojuma_laiks = 60
                    elif poga4.collidepoint(pele_pozicija):
                        if spele.veikt_gajienu(4):
                            speletaja_gajiens = False
                            zinojums = "Izvēlēts reizinātājs: 4"
                            zinojuma_laiks = 60
                    elif poga5.collidepoint(pele_pozicija):
                        if spele.veikt_gajienu(5):
                            speletaja_gajiens = False
                            zinojums = "Izvēlēts reizinātājs: 5"
                            zinojuma_laiks = 60
        
        if ievade_aktiva:
            zimet_tekstu("Ievadiet sākuma skaitli (20-30):", 50, 50, MELNA)
            zimet_tekstu(ievades_teksts, 50, 90, MELNA)
            zimet_pogu("Sākt spēli", 50, 130, 200, 50, ZAĻA, GAIŠI_ZILA)
            
            if zinojuma_laiks > 0:
                zimet_tekstu(zinojums, 50, 200, SARKANA)
                zinojuma_laiks -= 1
        else:
            # Informācijas panelis
            zimet_tekstu(f"Skaitlis: {spele.pašreizējais_skaitlis}", 50, 50, ZILA)
            zimet_tekstu(f"Punkti: {spele.kopējie_punkti}", 50, 90, ZILA)
            zimet_tekstu(f"Banka: {spele.banka}", 50, 130, ZILA)
            
            # Algoritmu izvēle
            zimet_pogu("MINIMAKS", 50, 150, 150, 40, 
                      GAIŠI_ZILA if pašreizējais_algoritms == "minimaks" else PELĒKA,
                      GAIŠI_ZILA)
            zimet_pogu("ALFA-BETA", 220, 150, 150, 40,
                      GAIŠI_ZILA if pašreizējais_algoritms == "alfabeta" else PELĒKA,
                      GAIŠI_ZILA)
            
            # Gājiena izvēle
            if speletaja_gajiens:
                zimet_tekstu("Izvēlieties reizinātāju:", 50, 210, MELNA)
                zimet_pogu("3", 50, 250, 100, 50, PELĒKA, GAIŠI_ZILA)
                zimet_pogu("4", 170, 250, 100, 50, PELĒKA, GAIŠI_ZILA)
                zimet_pogu("5", 290, 250, 100, 50, PELĒKA, GAIŠI_ZILA)
            else:
                zimet_tekstu("Dators veic gājienu...", 50, 250, MELNA)
                # Datora gājiens
                reizinatajs = datora_gajiens(spele, pašreizējais_algoritms, dziļums)
                spele.veikt_gajienu(reizinatajs)
                speletaja_gajiens = True
                zinojums = f"Dators izvēlējās reizinātāju: {reizinatajs}"
                zinojuma_laiks = 60

            if spele.spēle_beigusies:
                zimet_tekstu(f"Uzvarētājs: {spele.uzvaretajs}", 50, 320, SARKANA)
                zimet_tekstu("Spēle beigusies!", 50, 360, SARKANA)

        pygame.display.update()
        pulkstenis.tick(30)

if __name__ == "__main__":
    galvenais()