import pygame
import time
import sys
from googletrans import Translator


language = 'en'
translator = Translator()


# if the bot is within range of player
#       for every object
#               if the object is in range
#                       let players x and y be P.x and P.y, bots is B.x and B.y, objs is O.x and O.y
#                       Math: d =
#                               |(P.x - B.x)*(B.y - O.y) - (P.x - O.x)*(B.y - P.y)|
#                               -----------------------------------------------------
#                                                distance b/w player and bot
#           if d < r (which we'll have to play with to find a good value)
#                  theres an intersection and u lose
# no intersection, move twoards the player
#

#make the window and name
window = pygame.display.set_mode((1600, 1000), pygame.RESIZABLE)
pygame.display.set_caption('Loading...')

class Mob(object):
        """docstring for Mob"""
        def __init__(self, image_name, x, y, name):
                super(Mob, self).__init__()
                self.image = pygame.image.load(image_name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = x
                self.y = y
                self.name = name

        def move(self):
                # print(CheckDistance((hero.x, hero.y), (self.x, self.y)))
                dist_to_player = CheckDistance((hero.x, hero.y), (self.x, self.y))
                if dist_to_player < 1000 and dist_to_player > 20: #TODO: play w this
                        for obs in obstacles:
                                if CheckDistance((obs.x, obs.y), (self.x, self.y)) < 1000:
#                                       if parity x diff between obs and self is not parity of x diff between self and player
#
                                        parity_x_o_s = obs.x > self.x
                                        parity_x_h_s = hero.x > self.x
                                        parity_y_o_s = obs.y > self.y
                                        parity_y_h_s = hero.y > self.y
                                        parity_check_good = (parity_x_o_s == parity_x_h_s) and (parity_y_o_s == parity_y_h_s)
#
#
#
                                        if parity_check_good and CheckDistance((hero.x, hero.y), (self.x, self.y)) > CheckDistance((obs.x, obs.y), (self.x, self.y)):
                                                d = abs((hero.x - self.x)*(self.y - obs.y) - (self.x - obs.x)*(hero.y - self.y)) / CheckDistance((hero.x, hero.y), (self.x, self.y))
                                                if d < 25:
                                                        # print("collision detected", obs.image_name)
                                                        pygame.draw.line(window, (255,0,0), (self.x, self.y), (obs.x, obs.y), 2)
                                                        return False
                        total = abs(hero.x - self.x) + abs(hero.y - self.y)
                        self.x += (hero.x - self.x) / total
                        self.y += (hero.y - self.y) / total


class Npc(object):
        """docstring for Npc"""
        def __init__(self, image_name, x, y, message_1, message_2, name):
                super(Npc, self).__init__()
                self.image = pygame.image.load(image_name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = x
                self.y = y
                self.message_1 = message_1
                self.message_2 = message_2
                self.message_3 = "Quest not yet completed."
                self.name = name

        def complete_quest(self):
                self.message_3 = "Quest completed!"

LEVEL_UP_MESSAGE = translator.translate("Level up!", dest=language).text
FOUND_NOTHING_MESSAGE = translator.translate("You found nothing.", dest=language).text
class Obstacle(object):
        """docstring for Obstacle"""
        def __init__(self, image_name, x, y, onpickup_item=None):
                super(Obstacle, self).__init__()
                self.image = pygame.image.load(image_name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = x
                self.y = y
                self.onpickup_item = onpickup_item
                self.image_name = image_name
                if onpickup_item != None:
                        self.message = "You found a " + onpickup_item.name + "."
                else:
                        self.message = FOUND_NOTHING_MESSAGE


        def interact(self):
                item_to_give = self.onpickup_item
                self.onpickup_item = None
                self.message = FOUND_NOTHING_MESSAGE
                return item_to_give


class Player(object):
        """docstring for Player"""
        def __init__(self):
                super(Player, self).__init__()
                self.image = pygame.image.load('player.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = 775
                self.y = 475
                self.vel = 1
                self.xp = 0
                self.health = 100
                self.mana = 100
                self.level = 1
                self.health_text = 'Health: ' + str(self.health) + '/100'
                self.mana_text = 'Mana: ' + str(self.mana) + '/100'
                self.xp_text = 'XP: ' + str(self.xp) + '/' + str(100 + ((self.level-1) * 25))

        def add_xp(self, amount):
                amount_to_next_level = 100 + ((self.level-1) * 25)
                self.xp += amount
                self.xp_text = str(self.xp) + '/' + str(100 + ((self.level-1) * 25)) +' XP'
                if self.xp >= amount_to_next_level:
                        self.level += 1
                        self.add_xp(amount - amount_to_next_level)
                        pinMessage(LEVEL_UP_MESSAGE)

        def change_health(self, amount):
                self.health += amount
                if self.health < 0:
                        print("TODO: YOU DIED")


class Item(object):
        def __init__(this, image, name):
                super(Item, this).__init__()
                this.name = name
                this.image = pygame.image.load(image).convert_alpha()
                this.image = pygame.transform.scale(this.image, (64, 64))

class Quest(object):
        def __init__(self, goal, hint_image, target_npc, target_item):
                super(Quest, self).__init__()
                self.completed = False
                self.active = False
                self.goal = goal
                self.hint_image = pygame.image.load(hint_image).convert_alpha()
                self.hint_image = pygame.transform.scale(self.hint_image, (64, 64))
                self.time_spent = 0
                self.target_item = target_item
                self.target_npc = target_npc


# from player import Player
# from obstacle import Obstacle
# from npc import Npc

#globals
global FPSSecondStartTime
global FrameCount
global questList
global FPSCount
global pin_time
global message_text
global itemList
global invPositions
global inventoryList
global isSaved
global isLoaded
global hero
hero = Player()
mob = Mob('water_bucket.png', 700, 700, 'Buckethead')
pygame.init()
pygame.font.init()


#FONTS

font_inv = pygame.font.SysFont('georgia', 50)
font_inv_small = pygame.font.SysFont('georgia', 15)
font_message = pygame.font.SysFont('georgia', 35)
debugFont = pygame.font.SysFont('arial', 12)
font_questbox = pygame.font.SysFont('georgia', 20)

#print(pygame.font.get_fonts()) #print all fonts

#Blit positions for inventory
invPositions = [(10, 38),  (35.25, 38),  (61.5, 38),  (87.75, 38),
                                (10, 64),  (35.25, 64),  (61.5, 64),  (87.75, 64),
                                (10, 90),  (35.25, 90),  (61.5, 90),  (87.75, 90),
                                (10, 116), (35.25, 116), (61.5, 116), (87.75, 116),
                                (10, 142), (35.25, 142), (61.5, 142), (86.75, 142),
                                (10, 168), (35.25, 168), (61.5, 168), (86.75, 168)]
invPositionsScaled = []
for coord in invPositions:
        invPositionsScaled.append((coord[0] * 4, coord[1] * 4))
invPositions = invPositionsScaled




#List of NPCs
npcs = [
        Npc('npc_1.png', 400, 550, 'I would like some water, please.', '', 'Ethan'),
        Npc('npc_1.png', 600, 550, 'Give me a scroll', '', 'Devin')
        ]




#list of all items
itemList = []
item_debugX = Item('debugX.png', 'Poggers')
item_key = Item('key.png', 'Key')
item_scroll = Item('scroll.png', 'Scroll')
item_water_bucket = Item('water_bucket.png', 'Water Bucket')
itemList = [item_debugX, item_key, item_scroll, item_water_bucket]
inventoryList = [item_water_bucket, item_scroll, item_debugX]
#\/  stop deleting this  \/
#for x in range(0, 10):
        #inventoryList.append(item_debugX)

#array of all the non-player obstacles and static stuff on the screen
obstacles = [
        Obstacle('chest.png', 200, 300, onpickup_item=item_scroll),
        Obstacle('chest.png', 700, 900, onpickup_item=item_scroll),
        Obstacle('chest.png', 1200, 300, onpickup_item=item_scroll),
        Obstacle('tree_1.png', 900, 700),
        Obstacle('tree_1.png', 100, 900),
        Obstacle('tree_1.png', 1000, 300),
        Obstacle('fence_1.png', 1050, 300),
        Obstacle('fence_1.png', 1000, 350)
        ]

#list of all quests the player has to do
questList = [
        Quest('Give water to the West goblin', 'water_bucket.png', npcs[0], item_water_bucket),
        Quest('Give a scroll to the East goblin', 'scroll.png', npcs[1], item_scroll)
        ]
#General Images
inventory_hover = pygame.image.load('inv_hover.png').convert_alpha()
inventory_hover = pygame.transform.scale(inventory_hover, (80, 80))
pauseBG = pygame.image.load('pausebackground.png').convert_alpha()
def FindItemByName(itemName):
        global itemList
        for item in itemList:
                if item.name == itemName:
                        return item
        return 'item does not exist'
def PauseMenu_Save():
        global inventoryList
        global isSaved
        isSaved = True
        saveFile = open('SaveGame.save', 'w')
        for item in inventoryList:
                saveFile.write(str(item.name) + '\n')
        saveFile.close()
def PauseMenu_Load():
        global inventoryList
        global isLoaded
        isLoaded = True
        saveFile = open('SaveGame.save')
        saveLines = saveFile.readlines()
        saveFile.close()
        for line in saveLines:
                saveLines[saveLines.index(line)] = line.replace('\n', '')
        inventoryList = []
        for line in saveLines:
                inventoryList.append(FindItemByName(line))
def PauseMenu_ChangeLanguage():
        print('Change Language')
def DONOTHING():
        print('pog')
menubox = pygame.image.load('menubox.png').convert_alpha()
menubox = pygame.transform.scale(menubox, (700, 170))
menubox_hover = pygame.image.load('menubox_hover.png').convert_alpha()
menubox_hover = pygame.transform.scale(menubox_hover, (700, 170))
pause = pygame.image.load('pause.png').convert_alpha()
pause = pygame.transform.scale(pause, (496, 168))
pauseMenuBoxes = [['Save', PauseMenu_Save], ['Load', PauseMenu_Load], ['Change Language', PauseMenu_ChangeLanguage]]
#Status Bar Stuff
statusbar = pygame.image.load('statusbar.png').convert_alpha()
statusbar = pygame.transform.scale(statusbar, (318, 42))
healthpixel = pygame.image.load('statusbar_healthpixel.png').convert_alpha()
healthpixel = pygame.transform.scale(healthpixel, (3, 24))
manapixel = pygame.image.load('statusbar_manapixel.png').convert_alpha()
manapixel = pygame.transform.scale(manapixel, (3, 24))
xppixel = pygame.image.load('statusbar_xppixel.png').convert_alpha()
xppixel = pygame.transform.scale(xppixel, (3, 24))
# questList.append(Quest('Find a key from the king', 'key.png', npcs[0], item_water_bucket))
# questList.append(Quest('Get the scroll from a knight', 'scroll.png', npcs[0], item_water_bucket))

current_quest = 0
questList[0].active = True

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (63, 73, 204)
YELLOW = (255, 242, 0)
BROWN = (172, 113, 79)

#Language Stuff
# translator = Translator(to_lang="es")
# print(translator.translate("Hello I want water please"))
inventory_word = 'Inventory'
def convert_language_setup():
        global inventory_word
        # translation = translator.translate("Der Himmel ist blau und ich mag Bananen", dest='es')
        # print(translation.text)
        # #output: 'The sky is blue and I like bananas'
        inventory_word = translator.translate('Inventory', dest=language).text
        for guy in npcs:
                guy.message_1 = translator.translate(guy.message_1, dest=language).text
                guy.message_2 = translator.translate(guy.message_2, dest=language).text
                guy.message_3 = translator.translate(guy.message_3, dest=language).text
        for quest in questList:
                quest.goal = translator.translate(quest.goal, dest=language).text
        for obj in obstacles:
                obj.message = translator.translate(obj.message, dest=language).text

        hero.health_text = translator.translate(hero.health_text, dest=language).text
        hero.mana_text = translator.translate(hero.mana_text, dest=language).text
        hero.xp_text = translator.translate(hero.xp_text, dest=language).text

def updateMobs():
        mob.move()
        drawMobs()

def drawMobs():
        window.blit(mob.image, (int(mob.x), int(mob.y)))

def drawPlayer():
        window.blit(hero.image, (hero.x, hero.y))

def drawObstacles():
        for obs in obstacles:
                window.blit(obs.image, (obs.x, obs.y))

def drawNpcs():
        for guy in npcs:
                window.blit(guy.image, (guy.x, guy.y))

def drawInventory():
        global invPositions
        global inventoryList
        global inventory_word
        if inventory_open:
                inventoryImage = pygame.image.load('Inventory.png').convert_alpha()
                inventoryStartPixel = (window.get_width() - inventoryImage.get_width() * 4 + 13, int(window.get_height() / 2 - (inventoryImage.get_height() / 2) * 4))
                inventoryImage = pygame.transform.scale(inventoryImage, (464, 800))
                window.blit(inventoryImage, inventoryStartPixel)
                text = font_inv.render(inventory_word, True, (139, 69, 19))
                window.blit(text,(inventoryStartPixel[0] + int(inventoryImage.get_width() / 2) - int(text.get_width() / 2), inventoryStartPixel[1] + 65))
                for loops, item in enumerate(inventoryList):
                        if MousePosition[0] > invPositions[loops][0] + inventoryStartPixel[0] and MousePosition[0] < invPositions[loops][0] + inventoryStartPixel[0] + 80 and MousePosition[1] > invPositions[loops][1] + inventoryStartPixel[1] and MousePosition[1] < invPositions[loops][1] + inventoryStartPixel[1] + 80:
                                window.blit(inventory_hover, (int(invPositions[loops][0] + inventoryStartPixel[0]), int(invPositions[loops][1] + inventoryStartPixel[1])))
                        itemTitle = font_inv_small.render((inventoryList[loops].name), True, BLACK)
                        window.blit(itemTitle, (int(invPositions[loops][0] + inventoryStartPixel[0] - (itemTitle.get_width() / 2)) + 40, invPositions[loops][1] + inventoryStartPixel[1] + 85))
                        window.blit(inventoryList[loops].image, (int(invPositions[loops][0] + inventoryStartPixel[0] + 8), int(invPositions[loops][1] + inventoryStartPixel[1] + 8)))
                        if loops == 23:
                                break

def checkInteraction():
        global interactable
        interactable = False
        for guy in npcs:
                if (abs(hero.x - guy.x) < 40 and (hero.y - guy.y < 35) and (hero.y - guy.y > 0)) or (abs(hero.x - guy.x) < 40 and (guy.y - hero.y < 50) and (guy.y - hero.y > 0)) or (hero.x - guy.x < 50 and hero.x - guy.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0))) or guy.x - hero.x < 50 and guy.x - hero.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                        interactable = True
                        # try to give the npc an item
                        for thing in inventoryList:
                                if len(questList) > 0 and thing.name == questList[current_quest].target_item.name and guy.name == questList[current_quest].target_npc.name:
                                        guy.complete_quest()
                                        inventoryList.remove(thing)
                                        hero.add_xp(75)
                                        # auto-switch to next quest
                                        questList.remove(questList[current_quest])
                                        break
                        break
                        #drawMessage()
        for obj in obstacles:
                if CheckDistance((hero.x, hero.y), (obj.x, obj.y)) < 100:
                        item_got = obj.onpickup_item
                        if item_got != None:
                                pinMessage(obj.message)
                                inventoryList.append(item_got)
                                print("GOT", item_got.name)
                                obj.interact()

pin_time = 0
message_text = ""
start_time = 0

def pinMessage(message):
        global message_text
        global pin_time

        message_text = message
        pin_time = 4

def drawPinnedMessage():
        if message_text != "":
                textbox_image = pygame.image.load('textbox.png').convert_alpha()
                textbox_image = pygame.transform.scale(textbox_image, (1200, 300))
                window.blit(textbox_image, (int(window.get_width() / 2 - textbox_image.get_width() / 2), window.get_height() - textbox_image.get_height()))
                text = font_message.render(message_text, True, (139, 69, 19))
                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2 + 50), window.get_height() - textbox_image.get_height()))

def drawMessage():
        if interactable:
                for guy in npcs:
                        if (abs(hero.x - guy.x) < 40 and (hero.y - guy.y < 35) and (hero.y - guy.y > 0)) or (abs(hero.x - guy.x) < 40 and (guy.y - hero.y < 50) and (guy.y - hero.y > 0)) or (hero.x - guy.x < 50 and hero.x - guy.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0))) or guy.x - hero.x < 50 and guy.x - hero.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                                #print(guy.message)
                                textbox_image = pygame.image.load('textbox.png').convert_alpha()
                                textbox_image = pygame.transform.scale(textbox_image, (1200, 300))
                                window.blit(textbox_image, (int(window.get_width() / 2 - textbox_image.get_width() / 2), window.get_height() - textbox_image.get_height()))
                                text = font_message.render(guy.name, True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height()))
                                text = font_message.render(guy.message_1, True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height() + 50))
                                text = font_message.render(guy.message_2, True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height() + 85))
                                text = font_message.render(guy.message_3, True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height() + 120))

def drawQuest():
        textbox_image = pygame.image.load('questbox.png').convert_alpha()
        textbox_image = pygame.transform.scale(textbox_image, (492, 104))
        quest_icon = pygame.image.load('icon_quest.png').convert_alpha()
        quest_icon = pygame.transform.scale(quest_icon, (64, 64))
        window.blit(textbox_image, (0, 0))
        if len(questList) > 0:
                text = font_questbox.render(questList[current_quest].goal, True, BLACK)
                window.blit(text, (20, (int(textbox_image.get_height() / 2 - (text.get_height() / 2)))))
                text = font_questbox.render(questList[current_quest].goal, True, YELLOW)
                window.blit(text, (22, (int(textbox_image.get_height() / 2 - (text.get_height() / 2)))))
                if questList[current_quest].time_spent > 3:
                        window.blit(questList[current_quest].target_item.image, (402, 20))
                else:
                        window.blit(quest_icon, (402, 20))

def drawStatsUI():
        global hero
        for pixel in range(hero.health):
                window.blit(healthpixel, (window.get_width() - statusbar.get_width() - 10 + 9 + (pixel * 3), 10 + 12))
        for pixel in range(hero.mana):
                window.blit(manapixel, (window.get_width() - statusbar.get_width() - 10 + 9 + (pixel * 3), 20 + statusbar.get_height() + 12))
        for pixel in range(hero.xp):
                window.blit(xppixel, (window.get_width() - statusbar.get_width() - 10 + 9 + (pixel * 3), 30 + (statusbar.get_height() * 2) + 12))
        window.blit(statusbar, (window.get_width() - statusbar.get_width() - 10, 10))
        window.blit(statusbar, (window.get_width() - statusbar.get_width() - 10, 20 + statusbar.get_height()))
        window.blit(statusbar, (window.get_width() - statusbar.get_width() - 10, 30 + (statusbar.get_height() * 2)))
        healthText = font_inv_small.render(hero.health_text, True, WHITE)
        manaText = font_inv_small.render(hero.mana_text, True, WHITE)
        xpText = font_inv_small.render(hero.xp_text, True, WHITE)
        window.blit(healthText, (int(window.get_width() - statusbar.get_width() - 10 + statusbar.get_width() / 2 - healthText.get_width() / 2), int(10 + statusbar.get_height() / 2 - healthText.get_height() / 2)))
        window.blit(manaText, (int(window.get_width() - statusbar.get_width() - 10 + statusbar.get_width() / 2 - manaText.get_width() / 2), int(20 + statusbar.get_height() + statusbar.get_height() / 2 - healthText.get_height() / 2)))
        window.blit(xpText, (int(window.get_width() - statusbar.get_width() - 10 + statusbar.get_width() / 2 - xpText.get_width() / 2), int(30 + (statusbar.get_height() * 2 + statusbar.get_height() / 2 - healthText.get_height() / 2))))

def drawDebug():
        global FPSSecondStartTime
        global FrameCount
        global questList
        global pin_time
        global message_text
        global FPSCount
        if time.time() < FPSSecondStartTime + 1:
                FrameCount += 1
        else:
                if len(questList) > 0:
                        questList[current_quest].time_spent += 1
                if pin_time > 0:
                        pin_time-=1
                else:
                        message_text = ""
                #print(questList[current_quest].time_spent)
                FPSSecondStartTime = time.time()
                FPSCount = debugFont.render('FPS: ' + str(FrameCount), True, WHITE)
                FrameCount = 0
        window.blit(mouseLoc, (window.get_width() - 80, window.get_height() - mouseLoc.get_height()))
        window.blit(FPSCount, (window.get_width() - 80, window.get_height() - (mouseLoc.get_height() * 2)))

def move(direction):
        collision = False
        if direction == 'up':
                for obs in obstacles:
                        if abs(hero.x - obs.x) < 40 and (hero.y - obs.y < 35) and (hero.y - obs.y > 0):
                                collision = True
                for guy in npcs:
                        if abs(hero.x - guy.x) < 40 and (hero.y - guy.y < 35) and (hero.y - guy.y > 0):
                                collision = True
                # if abs(hero.x - mob.x) < 40 and (hero.y - mob.y < 35) and (hero.y - mob.y > 0):
                #       collision = True
                if not collision:
                        for obs in obstacles:
                                obs.y += hero.vel
                        for guy in npcs:
                                guy.y += hero.vel
                        mob.y += hero.vel
        if direction == 'down':
                for obs in obstacles:
                        if abs(hero.x - obs.x) < 40 and (obs.y - hero.y < 50) and (obs.y - hero.y > 0):
                                collision = True
                for guy in npcs:
                        if abs(hero.x - guy.x) < 40 and (guy.y - hero.y < 50) and (guy.y - hero.y > 0):
                                collision = True
                # if abs(hero.x - mob.x) < 40 and (mob.y - hero.y < 50) and (mob.y - hero.y > 0):
                #       collision = True
                if not collision:
                        for obs in obstacles:
                                obs.y -= hero.vel
                        for guy in npcs:
                                guy.y -= hero.vel
                        mob.y -= hero.vel
        if direction == 'left':
                for obs in obstacles:
                        if hero.x - obs.x < 50 and hero.x - obs.x > 0 and (((hero.y - obs.y < 25) and (hero.y - obs.y > 0)) or (obs.y - hero.y < 45) and (obs.y - hero.y > 0)):
                                collision = True
                for guy in npcs:
                        if hero.x - guy.x < 50 and hero.x - guy.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                                collision = True
                # if hero.x - mob.x < 50 and hero.x - mob.x > 0 and (((hero.y - mob.y < 25) and (hero.y - mob.y > 0)) or (mob.y - hero.y < 45) and (mob.y - hero.y > 0)):
                #       collision = True
                if not collision:
                        for obs in obstacles:
                                obs.x += hero.vel
                        for guy in npcs:
                                guy.x += hero.vel
                        mob.x += hero.vel
        if direction == 'right':
                for obs in obstacles:
                        if obs.x - hero.x < 50 and obs.x - hero.x > 0 and (((hero.y - obs.y < 25) and (hero.y - obs.y > 0)) or (obs.y - hero.y < 45) and (obs.y - hero.y > 0)):
                                collision = True
                for guy in npcs:
                        if guy.x - hero.x < 50 and guy.x - hero.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                                collision = True
                # if mob.x - hero.x < 50 and mob.x - hero.x > 0 and (((hero.y - mob.y < 25) and (hero.y - mob.y > 0)) or (mob.y - hero.y < 45) and (mob.y - hero.y > 0)):
                #       collision = True
                if not collision:
                        for obs in obstacles:
                                obs.x -= hero.vel
                        for guy in npcs:
                                guy.x -= hero.vel
                        mob.x -= hero.vel

def CheckDistance(pos1, pos2):
        distance = ((pos1[0] - pos2[0])**2 + (pos2[1] - pos1[1])**2)**0.5
        return distance

inventory_open = False
interactable = False


#update all time delays
def updateDelays():
        if len(questList) > 0:
                questList[current_quest].time_spent


convert_language_setup()
e_held = False
return_held = False

#FPS Counter initiation
FPSSecondStartTime = time.time()
FPSCount = debugFont.render('', True, WHITE)
FrameCount = 0
pygame.display.set_caption('NAME OF GAME')

FRAMEENDED = False
BEGINPAUSE = False
escapeHeld = False
#The main loop where the game runs
run = True
while run:
        ## DEBUG:
        MousePosition = pygame.mouse.get_pos()
        mouseLoc = debugFont.render('(' + str(MousePosition[0]) + ',' + str(MousePosition[1]) + ')', True, WHITE)


        pygame.time.delay(0)

        #special events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                elif event.type == pygame.VIDEORESIZE:
                        window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        #Keep track of quest Stuff



        #Key input
        keys = pygame.key.get_pressed()

        #Pause
        if keys[pygame.K_ESCAPE] and escapeHeld == False:
                BEGINPAUSE = True
        if BEGINPAUSE == True and FRAMEENDED == True:
                escapeHeld = True
                pauseBG = pygame.transform.scale(pauseBG, (window.get_width(), window.get_height()))
                window.blit(pauseBG, (0, 0))
                dimensions = (window.get_width(), window.get_height())
                boxSelected = 0
                keyHeld = False
                enterHeld = False
                isSaved = False
                isLoaded = False
                while True:
                        #Handle window resizing
                        if (window.get_width(), window.get_height()) != dimensions:
                                dimensions = (window.get_width(), window.get_height())
                                pauseBG = pygame.transform.scale(pauseBG, dimensions)
                                window.blit(pauseBG, (0, 0))
                        #Get and handle keys
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_ESCAPE] and escapeHeld == False:
                                escapeHeld = True
                                BEGINPAUSE = False
                                FRAMEENDED = False
                                break
                        if keys[pygame.K_ESCAPE] == False:
                                escapeHeld = False
                        #Move menu up/down
                        if keys[pygame.K_w] and keyHeld == False:
                                if boxSelected == 0:
                                        boxSelected = 2
                                else:
                                        boxSelected = boxSelected - 1
                        elif keys[pygame.K_s] == True and keyHeld == False:
                                if boxSelected == 2:
                                        boxSelected = 0
                                else:
                                        boxSelected = boxSelected + 1
                        if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
                                keyHeld = False
                        else:
                                keyHeld = True
                        #Click menu button
                        if keys[pygame.K_RETURN] and enterHeld == False:
                                pauseMenuBoxes[boxSelected][1]()
                                enterHeld = True
                        if keys[pygame.K_RETURN] == False:
                                enterHeld = False
                        #Blit 'pause' and boxes, text
                        window.blit(pause, (int(window.get_width() / 2 - pause.get_width() / 2), 50))
                                #'Save!'/'Load!' text
                        if isSaved == True:
                                savedText = font_inv.render('Saved!', True, BLACK)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 30), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2)))
                                savedText = font_inv.render('Saved!', True, YELLOW)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 32), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2)))
                        if isLoaded == True:
                                savedText = font_inv.render('Loaded!', True, BLACK)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 30), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2 + menubox.get_height() + 50)))
                                savedText = font_inv.render('Loaded!', True, YELLOW)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 32), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2 + menubox.get_height() + 50)))
                        for box in pauseMenuBoxes:
                                window.blit(menubox, (int(window.get_width() / 2 - menubox.get_width() / 2), 260 + (menubox.get_height() + 50) * pauseMenuBoxes.index(box)))
                                boxText = font_inv.render(box[0], True, BROWN)
                                window.blit(boxText, (int(window.get_width() / 2 - boxText.get_width() / 2), 260 + (menubox.get_height() + 50) * pauseMenuBoxes.index(box) + 58))
                                if boxSelected == pauseMenuBoxes.index(box):
                                        window.blit(menubox_hover, (int(window.get_width() / 2 - menubox.get_width() / 2), 260 + (menubox.get_height() + 50) * pauseMenuBoxes.index(box)))
                        #Event loop
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit(0)
                                elif event.type == pygame.VIDEORESIZE:
                                        window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                        pygame.display.flip()
        escapeHeld = keys[pygame.K_ESCAPE]

        #directional input
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not inventory_open:
                move('up')
                interactable = False
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not inventory_open:
                move('down')
                interactable = False
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not inventory_open:
                move('left')
                interactable = False
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not inventory_open:
                move('right')
                interactable = False
        if keys[pygame.K_RETURN] and not inventory_open and not interactable and not return_held:
                return_held = True
                checkInteraction()
        if keys[pygame.K_RETURN] and not inventory_open and not return_held:
                interactable = False

        return_held = keys[pygame.K_RETURN]

        #inventory input
        if keys[pygame.K_e] and not e_held:
                inventory_open = not inventory_open
        e_held = keys[pygame.K_e]

        #draw in all the stuff
        window.fill((0,0,0)) #fill background, deletes old positions of stuff

        #If goint to pause next frame, don't draw UI elements
        if BEGINPAUSE == False:
                drawStatsUI()
                drawQuest()
                drawDebug()
        else:
                FRAMEENDED = True

        drawObstacles()
        drawNpcs()
        updateMobs()
        drawPlayer()
        drawInventory()
        drawMessage()
        drawPinnedMessage()
        updateDelays()

        pygame.display.update()
pygame.quit()
sys.exit(0)





#class Item(object):
