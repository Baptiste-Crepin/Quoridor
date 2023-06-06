import pygame
from pygame.locals import *
from choiseBot import NumberBots
from sizeGrid import SizeGrid


class input:
    def __init__(self):
        self.windowXmax = 500
        self.windowYmax = 700
        self.pos1 = (150, 200)
        self.pos2 = (150, 370)
        self.pos3 = (300, 200)
        self.pos4 = (300, 370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue = (138, 201, 244)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font = pygame.font.Font(None, 36)
        self.text = ""

    def createInput(self):
        input = pygame.draw.rect(self.window, self.white, (150, 200, 300, 70))
        text = self.font.render(self.text, True, self.black)
        buttonText = text.get_rect(center=input.center)
        self.window.blit(text, buttonText)

    def mainLoop(self):
        backGround = pygame.image.load('pictures/Foret.jpg')
        self.window.blit(backGround, (0, 0))

        text_surface = self.font.render("How many players?", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

        contour_surface = self.font.render(
            "How many players?", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(
            center=(self.windowXmax // 2, 50))
        contour_rect.move_ip(2, 2)

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        self.createInput()
        self.Event()

    def getChoise(self):
        return self.choise

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.choise = True

            if event.type == pygame.KEYDOWN and len(self.text) < 15:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    return
                keyMap = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f",
                          pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l",
                          pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",
                          pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x",
                          pygame.K_y: "y", pygame.K_z: "z", pygame.K_SPACE: " ", pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2",
                          pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9"}
                self.text += keyMap[event.key]
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = input()

    while not board.getChoise():
        board.mainLoop()
        pygame.display.update()

    pygame.quit()
