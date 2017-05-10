import pygame
import random


AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)


class Moved_card(object):

    moved = False

    moved_card = []
    card_d = ()
    cards = None

    def click_up(self, deck_list):

        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, StartDeck):
                    if item.check_pos() and item.check_card(self.moved_card):
                        item.add_card(self.moved_card)
                        self.moved = False
                        self.moved_card = []
                        if isinstance(self.cards, WastePile):
                            self.cards.show_card()
                        self.cards = None
                        break
            else:
                self.cards.add_card(self.moved_card)
                self.moved = False
                self.moved_card = []
                self.cards = None

    def draw(self, screen, card_dict):

        if self.moved:
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.card_d[0]
            y = pos[1] - self.card_d[1]
            for item in self.moved_card:
                screen.blit(card_dict[item], [x, y])
                y += 32


class Deck(object):


    def __init__(self, x, y):
        self.cards = []
        self.rect = pygame.Rect(x, y, 71, 96)

    def check_pos(self):

        pos = pygame.mouse.get_pos()
        if pos[0] >= self.rect.left and pos[0] <= self.rect.right:
            if pos[1] >= self.rect.top and pos[1] <= self.rect.bottom:
                return True
            else:
                return False
        else:
            return False


class WastePile(Deck):


    def __init__(self, x, y):

        Deck.__init__(self, x, y)
        self.y = y
        self.hidden = []

    def extend_list(self, lst):
        self.hidden.extend(lst)
        self.cards.append(self.hidden.pop())
        if len(self.hidden) > 0:
            for i in range(len(self.hidden)):
                self.rect.top += 32

    def draw_card(self, screen, card_dict):

        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 71, 96], 2)
        i = self.y
        if len(self.cards) > 0:
            for item in self.cards:
                screen.blit(card_dict[item], [self.rect.left, i])
                i += 32

    def add_card(self, card):
        if len(self.cards) > 0 or len(self.hidden) > 0:
            for i in range(len(card)):
                self.rect.top += 32
        else:
            for i in range(len(card)):
                if i > 0:
                    self.rect.top += 32
        self.cards.extend(card)

    def click_down(self, card):

        if len(self.cards) > 0:
            top = self.rect.top
            lst = []
            for i in range(len(self.cards)):
                if self.check_pos():
                    pos = pygame.mouse.get_pos()
                    lst.insert(0, self.cards.pop())
                    card.card_d = (pos[0] - self.rect.left, pos[1] -
                                   self.rect.top)
                    card.moved = True
                    card.cards = self
                    card.moved_card.extend(lst)
                    if len(self.cards) > 0 or len(self.hidden) > 0:
                        self.rect.top -= 32
                    break
                else:
                    lst.insert(0, self.cards.pop())
                    self.rect.top -= 32
            else:
                self.rect.top = top
                self.cards.extend(lst)

    def show_card(self):
        if len(self.cards) == 0 and len(self.hidden) > 0:
            self.cards.append(self.hidden.pop())

    def check_card(self, moved_card):
        card = moved_card[0]
        result = False
        WasteIndicator = '_Waste'

        if WasteIndicator in card:
            result = False
        elif len(self.cards) == 0:
            if "king" or "queen" or "jack" or "10_" or "9_" or "8_" or "7_" or "6_" or "5_" or "4_" or "3_" or "2_" or "ace" in card:
                moved_card[0]+= WasteIndicator
                result = True
        elif len(self.cards) > 0:
            if "king" or "queen" or "jack" or "10_" or "9_" or "8_" or "7_" or "6_" or "5_" or "4_" or "3_" or "2_" or "ace" in card:
                moved_card[0] += WasteIndicator
                result = True
        return result


class StartDeck(Deck):
    def __init__(self, x, y):

        Deck.__init__(self, x, y)
        self.hidden_cards = []
        self.cards_list = []
        self.x = x

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            c = self.cards.pop()
            card.moved_card.append(c)
            self.cards_list.remove(c)
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self
            self.rect.left -= 20
        else:
            pos = pygame.mouse.get_pos()
            flag = False
            if pos[0] >= 30 and pos[0] <= 101:
                if pos[1] >= 30 and pos[1] <= 126:
                    if len(self.hidden_cards) == 0:
                        flag = False
                    else:
                        if len(self.cards) == 0:
                            flag = True
            if flag:
                self.rect.left = self.x
                if len(self.hidden_cards) > 0:
                    self.cards = []
                    c = self.hidden_cards.pop()
                    self.cards_list.insert(0, c)
                    self.cards.append(c)


                else:
                    self.hidden_cards.extend(self.cards_list)
                    self.cards_list = []
                    self.cards = []

                if len(self.cards) > 1:
                    for i in range(len(self.cards)):
                        if i > 0:
                            self.rect.left += 20

    def draw_card(self, screen, card_dict):

        x = self.x
        if len(self.hidden_cards) > 0:
            img = pygame.image.load("H:/Solitaire/CardGame/Deck2.gif").convert()
            screen.blit(img, [30, 30])
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
        else:
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
            pygame.draw.ellipse(screen, OLIVE, [40, 40, 60, 60], 5)

    def add_card(self, card):
        self.cards.extend(card)
        self.cards_list.extend(card)
        self.rect.left += 20


class WinPile1(Deck):

    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:2] == '2_':
                    result = True
            else:
                if '2_' in self.cards[-1]:
                    if card[:2] == '3_':
                        result = True
                elif '3_' in self.cards[-1]:
                    if card[:2] == '4_':
                        result = True
                elif '4_' in self.cards[-1]:
                    if card[:2] == '5_':
                        result = True
                elif '5_' in self.cards[-1]:
                    if card[:2] == '6_':
                        result = True
                elif '6_' in self.cards[-1]:
                    if card[:2] == '7_':
                        result = True
                elif '7_' in self.cards[-1]:
                    if card[:2] == '8_':
                        result = True
                elif '8_' in self.cards[-1]:
                    if card[:2] == '9_':
                        result = True
                elif '9_' in self.cards[-1]:
                    if card[:3] == '10_':
                        result = True
                elif '10_' in self.cards[-1]:
                    if card[:5] == 'jack_':
                        result = True
                elif 'jack_' in self.cards[-1]:
                    if card[:6] == 'queen_':
                        result = True
                elif 'queen_' in self.cards[-1]:
                    if card[:5] == 'king_':
                        result = True
        return result

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    def draw_card(self, screen, card_dict):

        img = pygame.image.load("H:/Solitaire/CardGame/CA.gif").convert()
        screen.blit(img, [330, 30])
        myfont = pygame.font.SysFont("monospace", 12)
        label = myfont.render("A 2 3 4 5", 1, (255, 255, 255))
        screen.blit(label, (330, 130))
        label = myfont.render("6 7 8 9 10", 1, (255, 255, 255))
        screen.blit(label, (330, 150))
        label = myfont.render("J Q K", 1, (255, 255, 255))
        screen.blit(label, (330, 170))


        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])



class WinPile2(Deck):



    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:2] == '4_':
                    result = True
            else:
                if '4_' in self.cards[-1]:
                    if card[:2] == '6_':
                        result = True
                elif '6_' in self.cards[-1]:
                    if card[:2] == '8_':
                        result = True
                elif '8_' in self.cards[-1]:
                    if card[:3] == '10_':
                        result = True
                elif '10_' in self.cards[-1]:
                    if card[:6] == 'queen_':
                        result = True
                elif 'queen_' in self.cards[-1]:
                    if card[:4] == 'ace_':
                        result = True
                elif 'ace_' in self.cards[-1]:
                    if card[:2] == '3_':
                        result = True
                elif '3_' in self.cards[-1]:
                    if card[:2] == '5_':
                        result = True
                elif '5_' in self.cards[-1]:
                    if card[:2] == '7_':
                        result = True
                elif '7_' in self.cards[-1]:
                    if card[:2] == '9_':
                        result = True
                elif '9_' in self.cards[-1]:
                    if card[:5] == 'jack_':
                        result = True
                elif 'jack_' in self.cards[-1]:
                    if card[:5] == 'king_':
                        result = True
        return result

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    def draw_card(self, screen, card_dict):
        """This will draw all the cards on the screen"""
        img = pygame.image.load("H:/Solitaire/CardGame/S2.gif").convert()
        screen.blit(img, [430, 30])
        myfont = pygame.font.SysFont("monospace", 12)
        label = myfont.render("2 4 6 8 10", 1, (255, 255, 255))
        screen.blit(label, (430, 130))
        label = myfont.render("Q A 3 5 7", 1, (255, 255, 255))
        screen.blit(label, (430, 150))
        label = myfont.render("9 J K", 1, (255, 255, 255))
        screen.blit(label, (430, 170))
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])

class WinPile3(Deck):


    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:2] == '6_':
                    result = True
            else:
                if '6_' in self.cards[-1]:
                    if card[:2] == '9_':
                        result = True
                elif '9_' in self.cards[-1]:
                    if card[:6] == 'queen_':
                        result = True
                elif 'queen_' in self.cards[-1]:
                    if card[:2] == '2_':
                        result = True
                elif '2_' in self.cards[-1]:
                    if card[:2] == '5_':
                        result = True
                elif '5_' in self.cards[-1]:
                    if card[:2] == '8_':
                        result = True
                elif '8_' in self.cards[-1]:
                    if card[:5] == 'jack_':
                        result = True
                elif 'jack_' in self.cards[-1]:
                    if card[:4] == 'ace_':
                        result = True
                elif 'ace_' in self.cards[-1]:
                    if card[:2] == '4_':
                        result = True
                elif '4_' in self.cards[-1]:
                    if card[:2] == '7_':
                        result = True
                elif '7_' in self.cards[-1]:
                    if card[:3] == '10_':
                        result = True
                elif '10_' in self.cards[-1]:
                    if card[:5] == 'king_':
                        result = True
        return result

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    def draw_card(self, screen, card_dict):

        img = pygame.image.load("H:/Solitaire/CardGame/H3.gif").convert()
        screen.blit(img, [530, 30])
        myfont = pygame.font.SysFont("monospace", 12)
        label = myfont.render("3 6 9 Q 2", 1, (255, 255, 255))
        screen.blit(label, (530, 130))
        label = myfont.render("5 8 J A 4", 1, (255, 255, 255))
        screen.blit(label, (530, 150))
        label = myfont.render("7 10 K", 1, (255, 255, 255))
        screen.blit(label, (530, 170))
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])

class WinPile4(Deck):
    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:2] == '8_':
                    result = True
            else:
                if '8_' in self.cards[-1]:
                    if card[:6] == 'queen_':
                        result = True
                elif 'queen_' in self.cards[-1]:
                    if card[:2] == '3_':
                        result = True
                elif '3_' in self.cards[-1]:
                    if card[:2] == '7_':
                        result = True
                elif '7_' in self.cards[-1]:
                    if card[:5] == 'jack_':
                        result = True
                elif 'jack_' in self.cards[-1]:
                    if card[:2] == '2_':
                        result = True
                elif '2_' in self.cards[-1]:
                    if card[:2] == '6_':
                        result = True
                elif '6_' in self.cards[-1]:
                    if card[:3] == '10_':
                        result = True
                elif '10_' in self.cards[-1]:
                    if card[:4] == 'ace_':
                        result = True
                elif 'ace_' in self.cards[-1]:
                    if card[:2] == '5_':
                        result = True
                elif '5_' in self.cards[-1]:
                    if card[:2] == '9_':
                        result = True
                elif '9_' in self.cards[-1]:
                    if card[:5] == 'king_':
                        result = True
        return result

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    def draw_card(self, screen, card_dict):

        img = pygame.image.load("H:/Solitaire/CardGame/D4.gif").convert()
        screen.blit(img, [630, 30])
        myfont = pygame.font.SysFont("monospace", 12)
        label = myfont.render("4 8 Q 3 7", 1, (255, 255, 255))
        screen.blit(label, (630, 130))
        label = myfont.render("J 2 6 10 A", 1, (255, 255, 255))
        screen.blit(label, (630, 150))
        label = myfont.render("5 9 K", 1, (255, 255, 255))
        screen.blit(label, (630, 170))
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])

def shuffle_cards():

    r = []
    lst = ["2_clubs", "3_clubs", "4_clubs", "5_clubs", "6_clubs",
           "7_clubs", "8_clubs", "9_clubs", "10_clubs", "jack_clubs", "queen_clubs",
           "king_clubs", "ace_spades", "3_spades", "4_spades",
           "5_spades", "6_spades", "7_spades", "8_spades", "9_spades", "10_spades",
           "jack_spades", "queen_spades", "king_spades", "ace_hearts", "2_hearts",
            "4_hearts", "5_hearts", "6_hearts", "7_hearts", "8_hearts",
           "9_hearts", "10_hearts", "jack_hearts", "queen_hearts", "king_hearts",
           "ace_diamonds", "2_diamonds", "3_diamonds", "5_diamonds",
           "6_diamonds", "7_diamonds", "8_diamonds", "9_diamonds", "10_diamonds",
           "jack_diamonds", "queen_diamonds", "king_diamonds"]

    length = len(lst)
    for i in range(length):
        if len(lst) > 1:
            c = random.choice(lst)
            r.append(c)
            lst.remove(c)
        else:
            c = lst.pop()
            r.append(c)

    return r


def main():
    pygame.init()



    screen = pygame.display.set_mode([725, 580])

    pygame.display.set_caption("Calulation Solitaire")


    done = False


    clock = pygame.time.Clock()

    card_dict = {}
    img = pygame.image.load("H:/Solitaire/CardGame/C2.gif").convert()
    card_dict["2_clubs"] = img
    card_dict["2_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C3.gif").convert()
    card_dict["3_clubs"] = img
    card_dict["3_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C4.gif").convert()
    card_dict["4_clubs"] = img
    card_dict["4_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C5.gif").convert()
    card_dict["5_clubs"] = img
    card_dict["5_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C6.gif").convert()
    card_dict["6_clubs"] = img
    card_dict["6_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C7.gif").convert()
    card_dict["7_clubs"] = img
    card_dict["7_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C8.gif").convert()
    card_dict["8_clubs"] = img
    card_dict["8_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/C9.gif").convert()
    card_dict["9_clubs"] = img
    card_dict["9_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/CT.gif").convert()
    card_dict["10_clubs"] = img
    card_dict["10_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/CJ.gif").convert()
    card_dict["jack_clubs"] = img
    card_dict["jack_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/CQ.gif").convert()
    card_dict["queen_clubs"] = img
    card_dict["queen_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/CK.gif").convert()
    card_dict["king_clubs"] = img
    card_dict["king_clubs_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/SA.gif").convert()
    card_dict["ace_spades"] = img
    card_dict["ace_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S3.gif").convert()
    card_dict["3_spades"] = img
    card_dict["3_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S4.gif").convert()
    card_dict["4_spades"] = img
    card_dict["4_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S5.gif").convert()
    card_dict["5_spades"] = img
    card_dict["5_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S6.gif").convert()
    card_dict["6_spades"] = img
    card_dict["6_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S7.gif").convert()
    card_dict["7_spades"] = img
    card_dict["7_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S8.gif").convert()
    card_dict["8_spades"] = img
    card_dict["8_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/S9.gif").convert()
    card_dict["9_spades"] = img
    card_dict["9_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/ST.gif").convert()
    card_dict["10_spades"] = img
    card_dict["10_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/SJ.gif").convert()
    card_dict["jack_spades"] = img
    card_dict["jack_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/SQ.gif").convert()
    card_dict["queen_spades"] = img
    card_dict["queen_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/SK.gif").convert()
    card_dict["king_spades"] = img
    card_dict["king_spades_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/HA.gif").convert()
    card_dict["ace_hearts"] = img
    card_dict["ace_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H2.gif").convert()
    card_dict["2_hearts"] = img
    card_dict["2_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H4.gif").convert()
    card_dict["4_hearts"] = img
    card_dict["4_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H5.gif").convert()
    card_dict["5_hearts"] = img
    card_dict["5_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H6.gif").convert()
    card_dict["6_hearts"] = img
    card_dict["6_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H7.gif").convert()
    card_dict["7_hearts"] = img
    card_dict["7_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H8.gif").convert()
    card_dict["8_hearts"] = img
    card_dict["8_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/H9.gif").convert()
    card_dict["9_hearts"] = img
    card_dict["9_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/HT.gif").convert()
    card_dict["10_hearts"] = img
    card_dict["10_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/HJ.gif").convert()
    card_dict["jack_hearts"] = img
    card_dict["jack_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/HQ.gif").convert()
    card_dict["queen_hearts"] = img
    card_dict["queen_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/HK.gif").convert()
    card_dict["king_hearts"] = img
    card_dict["king_hearts_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/DA.gif").convert()
    card_dict["ace_diamonds"] = img
    card_dict["ace_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D2.gif").convert()
    card_dict["2_diamonds"] = img
    card_dict["2_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D3.gif").convert()
    card_dict["3_diamonds"] = img
    card_dict["3_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D5.gif").convert()
    card_dict["5_diamonds"] = img
    card_dict["5_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D6.gif").convert()
    card_dict["6_diamonds"] = img
    card_dict["6_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D7.gif").convert()
    card_dict["7_diamonds"] = img
    card_dict["7_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D8.gif").convert()
    card_dict["8_diamonds"] = img
    card_dict["8_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/D9.gif").convert()
    card_dict["9_diamonds"] = img
    card_dict["9_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/DT.gif").convert()
    card_dict["10_diamonds"] = img
    card_dict["10_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/DJ.gif").convert()
    card_dict["jack_diamonds"] = img
    card_dict["jack_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/DQ.gif").convert()
    card_dict["queen_diamonds"] = img
    card_dict["queen_diamonds_Waste"] = img
    img = pygame.image.load("H:/Solitaire/CardGame/DK.gif").convert()
    card_dict["king_diamonds"] = img
    card_dict["king_diamonds_Waste"] = img

    card_list = shuffle_cards()

    deck_list = [StartDeck(130, 30), WastePile(130, 210), WastePile(230, 210), WastePile(330, 210),
                 WastePile(430, 210),  WinPile1(330, 30), WinPile2(430, 30), WinPile3(530, 30),
                 WinPile4(630, 30)]
    m_card = Moved_card()

    deck_list[0].hidden_cards.extend(card_list)
    game_over = False
    font = pygame.font.Font(None, 25)
    text = font.render("Congratulations, You Won!", True, BLACK)

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in deck_list:
                    item.click_down(m_card)

            if event.type == pygame.MOUSEBUTTONUP:
                m_card.click_up(deck_list)


        for item in deck_list:
            if isinstance(item, WinPile1) or isinstance(item, WinPile2) or isinstance(item, WinPile3) or isinstance(item, WinPile4):
                if len(item.cards) != 13:
                    break
        else:
            game_over = True

        screen.fill((GREEN))


        for item in deck_list:
            item.draw_card(screen, card_dict)
        m_card.draw(screen, card_dict)
        if game_over:
            pygame.draw.rect(screen, WHITE, [245, 246, 250, 25])
            screen.blit(text, [250, 250])

        pygame.display.flip()


        clock.tick(20)


    pygame.quit()


if __name__ == '__main__':
    main()
