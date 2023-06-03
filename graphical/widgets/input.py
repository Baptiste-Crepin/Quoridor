import pygame


class Input:
    def __init__(self, window: pygame.Surface, rect: pygame.Rect, color: pygame.Color, sizeText: int = 15):
        self.window = window
        self.rect = rect
        self.color = color
        self.sizeText = sizeText
        self.blue = (138, 201, 244)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font = pygame.font.Font(None, 36)
        self.text = ""

    def createInput(self):
        input = pygame.draw.rect(
            self.window, self.color, self.rect, border_radius=10)
        text = self.font.render(self.text, True, self.black)
        buttonText = text.get_rect(center=input.center)
        self.window.blit(text, buttonText)

    def Event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return
            if len(self.text) >= self.sizeText:
                return
            keyMap = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f",
                      pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l",
                      pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",
                      pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x",
                      pygame.K_y: "y", pygame.K_z: "z", pygame.K_SPACE: " ", pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2",
                      pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9"}
            letter = keyMap.get(event.key)
            if letter:
                self.text += letter
