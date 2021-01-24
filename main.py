import pygame
import time
import sys
import numpy as np
from googletrans import Translator
import json

languages = ['en', 'es', 'ru','fr', 'de', 'ar', 'tr', 'zu']
language_names = ['English', 'Spanish', 'Russian', 'French', 'German', 'Arabic', 'Turkish', 'Zulu']
language = languages[0]
print(languages[0])
#print(translate(languages[0]))

translator = Translator()
print(translator.translate('Hello', dest='es').text)

offset = [775,475]

f = open("translations.json", encoding='utf-8')
all_translated_text = json.load(f)
f.close()
def translate(text):
    key = text + language
    if key not in all_translated_text.keys():
        all_translated_text[key] = translator.translate(text, dest=language).text
        print("unable to translate", key, "defaulting to google, got", all_translated_text[key])
    # if language == "ar":
    #     print(all_translated_text[key])
    return all_translated_text[key]

for lang in language_names:
    lang = translate(lang)





class Tile(object):
    """docstring for Tile."""

    def __init__(self, image, x, y):
        super(Tile, self).__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.x  = x
        self.y  = y


class Obstacle(object):
        """docstring for Obstacle"""
        def __init__(self, image_name, x, y, onpickup_item=None, collidable=True, x_size=50, y_size=50):
                super(Obstacle, self).__init__()

                self.x = x
                self.y = y
                self.x_size = x_size
                self.y_size = y_size

                self.image = pygame.image.load(image_name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.x_size, self.y_size))

                self.collidable  = collidable
                self.onpickup_item = onpickup_item
                self.image_name = image_name
                if onpickup_item != None:
                        self.message = translate("You found a " + onpickup_item.name + ".")
                else:
                        self.message = translate('You found nothing.')


        def interact(self):
                item_to_give = self.onpickup_item
                self.onpickup_item = None
                self.message = translate('You found nothing.')
                return item_to_give






















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
                self.goal = None

                self.last_attacked_time = 0

        def move(self):
                # print(CheckDistance((hero.x, hero.y), (self.x, self.y)))
                dist_to_player = CheckDistance((hero.x, hero.y), (self.x, self.y))
                if dist_to_player < 20 and time.time() - self.last_attacked_time > 1:
                    self.last_attacked_time = time.time()
                    print("ATTACKING")
                    hero.change_health(-10)
                    miscSound1.play()


                if dist_to_player < 1000 and dist_to_player > 20: #TODO: play w this
                        can_update_goal = True
                        for obs in world.get_obstacles():
                                if CheckDistance((obs.x+offset[0], obs.y+offset[1]), (self.x, self.y)) < 1000:
#                                       if parity x diff between obs and self is not parity of x diff between self and player
#
                                        parity_x_o_s = obs.x+offset[0] > self.x
                                        parity_x_h_s = hero.x> self.x
                                        parity_y_o_s = obs.y+offset[1] > self.y
                                        parity_y_h_s = hero.y> self.y
                                        parity_check_good = (parity_x_o_s == parity_x_h_s) and (parity_y_o_s == parity_y_h_s)
#
#
#
                                        if parity_check_good and CheckDistance((hero.x, hero.y), (self.x, self.y)) > CheckDistance((obs.x+offset[0], obs.y+offset[1]), (self.x, self.y)):
                                                d = abs((hero.x - self.x)*(self.y - obs.y-offset[1]) - (self.x - obs.x-offset[0])*(hero.y - self.y)) / CheckDistance((hero.x, hero.y), (self.x, self.y))
                                                if d < 50:
                                                        can_update_goal = False
                        if can_update_goal:
                            self.goal = [hero.x, hero.y]
                if self.goal is not None and CheckDistance(self.goal, (self.x, self.y)) > 1:
                    total = abs(self.goal[0] - self.x) + abs(self.goal[1] - self.y)
                    self.x += 2* (self.goal[0] - self.x) / total
                    self.y += 2* (self.goal[1] - self.y) / total
                else:
                    self.goal = None
                    return False


class Npc(object):
        """docstring for Npc"""
        def __init__(self, image_name, x, y, message_1, message_2, name):
                super(Npc, self).__init__()
                self.image_name = image_name
                self.image = pygame.image.load(image_name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = x
                self.y = y
                self.message_1 = translate(message_1)
                self.message_2 = translate(message_2)
                self.message_3 = translate("Quest not yet completed.")
                self.name = translate(name)

        def complete_quest(self):
                self.message_3 = translate("Quest completed!")


class Player(object):
        """docstring for Player"""
        def __init__(self):
                super(Player, self).__init__()
                self.image = pygame.image.load('player.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = 775
                self.y = 475
                self.vel = 3 ###SET TO 1 FOR REAL GAMEPLAY
                self.xp = 0
                self.health = 100
                self.mana = 100
                self.level = 1

        def add_xp(self, amount):
                amount_to_next_level = 100 + ((self.level-1) * 25)
                self.xp += amount
                self.xp_text = str(self.xp) + '/' + str(100 + ((self.level-1) * 25)) +' XP'
                if self.xp >= amount_to_next_level:
                        self.level += 1
                        self.xp -= amount_to_next_level

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
mobs = []#Mob('goblin.png', 700, 700, 'Buckethead')]
        # Mob('goblin.png', 200, 700, 'Buckethead'),
        # Mob('goblin.png', 700, 300, 'Buckethead'),
        # Mob('goblin.png', 750, 700, 'Buckethead'),
        # Mob('goblin.png', 750, 750, 'Buckethead'),
        # Mob('goblin.png', 850, 700, 'Buckethead'),
        # Mob('goblin.png', 700, 950, 'Buckethead')]
pygame.init()
pygame.font.init()


#FONTS

font_inv_english = pygame.font.SysFont('georgia', 50)
font_inv_small_english = pygame.font.SysFont('georgia', 15)
font_message_english = pygame.font.SysFont('georgia', 35)
debugFont_english = pygame.font.SysFont('arial', 12)
font_questbox_english = pygame.font.SysFont('georgia', 20)

font_inv_arabic = pygame.font.Font('NotoNaskhArabic-Regular.ttf', 50)
font_inv_small_arabic = pygame.font.Font('NotoNaskhArabic-Regular.ttf', 15)
font_message_arabic = pygame.font.Font('NotoNaskhArabic-Regular.ttf', 35)
debugFont_arabic = pygame.font.Font('NotoNaskhArabic-Regular.ttf', 12)
font_questbox_arabic = pygame.font.Font('NotoNaskhArabic-Regular.ttf', 20)

font_inv = font_inv_english
font_inv_small = font_inv_small_english
font_message = font_message_english
debugFont = debugFont_english
font_questbox = font_questbox_english

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
        Npc('npc_1.png', 400, 550, translate('I would like some water, please.'), '', 'Ethan'),
        Npc('npc_1.png', 600, 550, translate('Give me a scroll'), '', 'Devin')
        ]




#list of all items
itemList = []
item_debugX = Item('debugX.png', translate('Poggers'))
item_key = Item('key.png', translate('Key'))
item_scroll = Item('scroll.png', translate('Scroll'))
item_water_bucket = Item('water_bucket.png', translate('Water Bucket'))
item_gold_coin = Item('gold_coin.png', translate('Gold Coin'))
item_gold_bar = Item('gold_bar.png', translate('Gold Bar'))



itemList = [item_debugX, item_key, item_scroll, item_water_bucket, item_gold_coin, item_gold_bar]
inventoryList = [item_water_bucket, item_scroll, item_debugX]
#\/  stop deleting this  \/
#for x in range(0, 10):
        #inventoryList.append(item_debugX)

#array of all the non-player obstacles and static stuff on the screen














class Chunk(object):
    """docstring for Chunk."""

    def __init__(self, x, y):
        super(Chunk, self).__init__()
        # np.random.seed(str(x) + "---" + str(y))

        sin_vals = (np.sin(x / 3000 + 10)  + 0.1*np.sin(x / 1500) + np.sin(y / 2900 + 2468) + 0.07*np.sin(y / 1200)) / 2.17 # between -1 and 1
        sin_vals_2 = (np.sin(x / 2900 + 120) + 0.1*np.sin(x / 1900) + np.sin(y / 2470 + 268) + 0.07*np.sin(y / 532 + 5)) / 2.17 # between -1 and 1

        np.random.seed((abs(x + (3*y+7)) + x + y + int(np.sin(y))*1000) % 2**31 )

        self.x = x
        self.y = y


        #VARIATIONS
        self.biome_type = None

        tree_spawn_limit = (1.5-(sin_vals+1))/2.0 + 0.75

        if sin_vals > 0.66:
            self.biome_type = "forest"
            type_of_tile = 'darkgrass.png'
            # tree_spawn_limit = 0.6
            tree_type = 'tree_1.png'
            path_type = 'dirt.png'
        elif sin_vals > .33:
            self.biome_type = "grasslands"
            type_of_tile = 'grass.png'
            # tree_spawn_limit = 1.3
            tree_type = 'tree_1.png'
            path_type = 'dirt.png'
        elif sin_vals > .0:
            self.biome_type = 'savannah'
            type_of_tile = 'dirt.png'
            # tree_spawn_limit = 1.4
            tree_type = 'bush.png'
            path_type = 'cobblestone.png'
        elif sin_vals > -.33:
            self.biome_type = 'desert'
            type_of_tile = 'sand.png'
            # tree_spawn_limit = 1.4
            tree_type = 'cactus.png'
            path_type = 'cobblestone.png'
        elif sin_vals > -.66:
            self.biome_type = 'mountain'
            type_of_tile = 'mountain.png'
            # tree_spawn_limit = 1.4
            tree_type = 'rock.png'
            path_type = 'cobblestone.png'
        else:
            self.biome_type = "tundra"
            type_of_tile = 'snow.png'
            # tree_spawn_limit = 1.5
            tree_type = 'evergreen.png'
            path_type = 'dirt.png'


        def get_tree_type(xx, yy):
            tree_sin_vals = (np.sin(xx / 3000 + 10)  + 0.1*np.sin(xx / 1500) + np.sin(yy / 2900 + 2468) + 0.07*np.sin(yy / 1200)) / 2.17 # between -1 and 1

            tree_sin_vals += np.random.uniform(-0.1, 0.1)
            if tree_sin_vals > 0.66:
                return 'tree_1.png'
            elif tree_sin_vals > .33:
                return 'tree_1.png'
            elif tree_sin_vals > .0:
                return 'bush.png'
            elif tree_sin_vals > -.33:
                return 'cactus.png'
            elif tree_sin_vals > -.66:
                return 'rock.png'
            return 'evergreen.png'




        self.obs_list = []
        self.npcs_list = [Npc('knight.png', self.x+100, self.y+100, translate('Give me a scroll'), '', 'Ethan'),
                          Npc('enemy_knight.png', self.x+200, self.y+200, translate('Give me a scroll'), '', 'Devin')
        ]

        pot_house_spots = []
        pot_chest_spots = []
        pot_npc_spots = []

        self.tiles_list = [
            [Tile(type_of_tile, xx, yy) for xx in range(self.x, self.x+2000, 200)]
            for yy in range(self.y, self.y+2000, 200)
        ]
        #Roads, rivers, and bridges, etc
        for xx in range(self.x, self.x+2000, 50):
            for yy in range(self.y, self.y+2000, 50):
                river_sin_x = (np.sin(xx / 600) +     2*np.sin(xx / 1000 + 17)  +  4*np.sin(xx / 2300 + 7)    )/7
                river_sin_y = (np.sin(yy / 500 + 5) + 2*np.sin(yy / 1200 + 127) +  4*np.sin(yy / 2100 + 77)   )/7

                bridge_X_sin_x = (np.sin(xx / 300) +     2*np.sin(xx / 500 + 47)  +  4*np.sin(xx / 1200 + 37)    )/7
                bridge_X_sin_y = (np.sin(yy / 600 + 19) + 2*np.sin(yy / 1200 + 17) +  4*np.sin(yy / 1800 + 777)   )/7
                bridge_Y_sin_x = (np.sin(xx / 600 + 139) + 2*np.sin(xx / 1210 + 171) +  4*np.sin(xx / 1700 + 773)   )/7
                bridge_Y_sin_y = (np.sin(yy / 391 + 17) +     2*np.sin(yy / 501 + 437)  +  4*np.sin(yy / 1400 + 37)    )/7


                river_comb = river_sin_x + river_sin_y
                if abs(river_comb) < 0.05:
                    if (bridge_X_sin_y > 0 and abs(bridge_X_sin_x) < 0.05) or (bridge_Y_sin_x > 0 and abs(bridge_Y_sin_y) < 0.05):
                        self.obs_list.append(Obstacle('planks.png', xx, yy, collidable=False))
                    else:
                        self.obs_list.append(Obstacle('water.png', xx, yy, collidable=False))


        #
        #
        #
        #
        #
        #
        # # adding house
        # for spot in pot_house_spots:
        #     # if nothing is within spot[0] - spot[0]+250 and spot[1] - spot[1]+150
        #     # make a house
        #     valid = True
        #     if spot[0] > self.x + 1600 or spot[1] > self.y + 1600:
        #         valid = False
        #     else:
        #         for obj in self.obs_list:
        #             if obj.x >= spot[0] and obj.x < spot[0]+250 and obj.y >= spot[1] and obj.y < spot[1]+150:
        #                 valid = False
        #     if valid:
        #         self.obs_list.append(Obstacle('tree_1.png', spot[0]+100, spot[1]+100, collidable=False, x_size=50, y_size=50))
        #         self.obs_list.append(Obstacle('tree_1.png', spot[0], spot[1]+100, collidable=False, x_size=50, y_size=50))
        #         self.obs_list.append(Obstacle('tree_1.png', spot[0]+200, spot[1]+100, collidable=False, x_size=50, y_size=50))
        #         self.obs_list.append(Obstacle('cabin2.png', spot[0], spot[1], collidable=False, x_size=250, y_size=150))
        #
        # #adding chest or npc
        # for spot in pot_chest_spots:
        #     valid = True
        #     for obj in self.obs_list:
        #         if obj.x == spot[0] and obj.y == spot[1]:
        #             valid = False
        #     if valid:
        #         choice = np.random.choice([0, 1],1,p=[0.5,0.5])[0]
        #         chest_type = np.random.choice(['chest.png', 'barrel.png'],1,p=[0.5,0.5])[0]
        #         npc_type = np.random.choice(['knight.png', 'enemy_knight.png'],1,p=[0.5,0.5])[0]
        #
        #         if choice == 0:
        #             self.obs_list.append(Obstacle(chest_type, spot[0], spot[1], collidable=False, x_size=50, y_size=50, onpickup_item=np.random.choice(itemList,1)[0]))
        #         if choice == 1:
        #             if npc_type == 'knight.png':
        #                 npcs.append(Npc(npc_type, spot[0]+offset[0], spot[1]+offset[1], 'I want some water', '', 'Ethan'))
        #             else:
        #                 npcs.append(Npc(npc_type, spot[0]+offset[0], spot[1]+offset[1], 'Can I have a gold coin, please?', '', 'Ethan'))
        #
        #
        for xx in range(self.x, self.x+2000, 50):
            for yy in range(self.y, self.y+2000, 50):
                forest_sin_x = (np.sin(xx / 100) +     2*np.sin(xx / 200 + 17)  +  4*np.sin(xx / 500 + 7)    )/7
                forest_sin_y = (np.sin(yy / 150 + 5) + 2*np.sin(yy / 158 + 127) +  4*np.sin(yy / 450 + 77)   )/7
                if abs(forest_sin_x + forest_sin_y) > tree_spawn_limit:
                    can_add_tree = True
                    for obj in self.obs_list:
                        if obj.x == xx and obj.y == yy:
                            can_add_tree = False
                    for npc in npcs:
                        if npc.x == xx and npc.y == yy:
                            can_add_tree = False
                    if can_add_tree:
                        self.obs_list.append(Obstacle(get_tree_type(xx,yy), xx, yy, collidable=False))


        def is_clear(top_left, bottom_right):
            clear = top_left[0] >= self.x and top_left[1] >= self.y and bottom_right[0] <= self.x+2000 and bottom_right[1] <= self.y + 2000
            for obj in self.obs_list:
                if  obj.x >= top_left[0] and obj.x < bottom_right[0] and obj.y >= top_left[1] and obj.y < bottom_right[1]:
                    return False
            return clear

        def house_spot_valid(target_spot):
            top_left = [target_spot[0]-50, target_spot[1]-50]
            bottom_right = [target_spot[0]+300, target_spot[1]+200]

            contains_a_road = False
            for obj in self.obs_list:
                if  obj.x >= top_left[0] and obj.x < bottom_right[0] and obj.y >= top_left[1] and obj.y < bottom_right[1] and (obj.image_name == "dirt.png" or obj.image_name == "cobblestone.png" or obj.image_name == "granite.png" ):
                    contains_a_road = True
                    break
            return is_clear([top_left[0]+50, top_left[1]+50], [bottom_right[0]-50, bottom_right[1]-50]) and (contains_a_road or np.random.uniform(0,1) > 0.99)

        def chest_spot_valid(target_spot):
            top_left = [target_spot[0]-50, target_spot[1]-50]
            bottom_right = [target_spot[0]+50, target_spot[1]+50]

            contains_a_road = False
            for obj in self.obs_list:
                if  obj.x >= top_left[0] and obj.x <= bottom_right[0] and obj.y >= top_left[1] and obj.y <= bottom_right[1] and (obj.image_name == "dirt.png" or obj.image_name == "cobblestone.png" or obj.image_name == "granite.png"):
                    contains_a_road = True
                    break
            return is_clear([top_left[0]+50, top_left[1]+50], [bottom_right[0], bottom_right[1]]) and contains_a_road

        def create_road(start, direction, length):
            if length < 5:
                return False
            if direction == 0:# left
                top_left = [start[0]-(length+1)*50, start[1]-50]
                bottom_right = [start[0]-50, start[1]+50]
                if is_clear(top_left, bottom_right):
                    for l in range(1,length+1):
                        self.obs_list.append(Obstacle(path_type, start[0]-l*50, start[1], collidable=False))
                    for i in range(5):
                        random_start = [np.random.choice(range(start[0]-50,start[0] - length*50,-50),1)[0],
                                        start[1]]
                        random_length = np.random.choice(range(length-5, length-2),1)[0]
                        random_dir = np.random.choice([2,3],1)[0]
                        create_road(random_start, random_dir, random_length)
            if direction == 1:# right
                top_left = [start[0]+50, start[1]-50]
                bottom_right = [start[0]+(length+1)*50, start[1]+50]
                if is_clear(top_left, bottom_right):
                    for l in range(1,length+1):
                        self.obs_list.append(Obstacle(path_type, start[0]+l*50, start[1], collidable=False))
                    for i in range(5):
                        random_start = [np.random.choice(range(start[0]+50,start[0] + length*50,50),1)[0],
                                        start[1]]
                        random_length = np.random.choice(range(length-5, length-2),1)[0]
                        random_dir = np.random.choice([2,3],1)[0]
                        create_road(random_start, random_dir, random_length)
            if direction == 2:# up
                top_left = [start[0]-50, start[1]-(length+1)*50]
                bottom_right = [start[0]+50, start[1]-50]
                if is_clear(top_left, bottom_right):
                    for l in range(1,length+1):
                        self.obs_list.append(Obstacle(path_type, start[0], start[1]-l*50, collidable=False))
                    for i in range(5):
                        random_start = [start[0],
                                        np.random.choice(range(start[1]-50,start[1] - length*50,-50),1)[0]]
                        random_length = np.random.choice(range(length-5, length-2),1)[0]
                        random_dir = np.random.choice([0,1],1)[0]
                        create_road(random_start, random_dir, random_length)
            if direction == 3:# down
                top_left = [start[0]-50, start[1]-50]
                bottom_right = [start[0]+50, start[1]+(length+1)*50]
                if is_clear(top_left, bottom_right):
                    for l in range(1,length+1):
                        self.obs_list.append(Obstacle(path_type, start[0], start[1]+l*50, collidable=False))
                    for i in range(5):
                        random_start = [start[0],
                                        np.random.choice(range(start[1]+50,start[1] + length*50,50),1)[0]]
                        random_length = np.random.choice(range(length-5, length-2),1)[0]
                        random_dir = np.random.choice([0,1],1)[0]
                        create_road(random_start, random_dir, random_length)




        create_road([self.x+50*(np.random.randint(40)), self.y+50*(np.random.randint(40))], np.random.randint(4), np.random.randint(20,30))

        #MAKE SOME HOUSES
        for xx in range(self.x, self.x+2000, 50):
            for yy in range(self.y, self.y+2000, 50):

                if house_spot_valid([xx, yy]):
                    chance_of_house = np.random.randint(0,8)
                    if chance_of_house == 0:
                        self.obs_list.append(Obstacle('cabin2.png', xx, yy, collidable=False, x_size=250, y_size=150))
                        for xoff in range(0, 5):
                            for yoff in range(0,3):
                                self.obs_list.append(Obstacle('nothing.png', xx+xoff*(50), yy+yoff*50, collidable=False))

        #MAKE SOME CHESTS
        for xx in range(self.x, self.x+2000, 50):
            for yy in range(self.y, self.y+2000, 50):
                if chest_spot_valid([xx, yy]):
                    chance_of_chest = np.random.randint(0,15)
                    item = np.random.randint(0,len(itemList))
                    if chance_of_chest == 0:
                        self.obs_list.append(Obstacle('chest.png', xx, yy, collidable=False, onpickup_item=itemList[item]))
                    if chance_of_chest == 1:
                        self.obs_list.append(Obstacle('barrel.png', xx, yy, collidable=False, onpickup_item=itemList[item]))

    def draw(self, window, offset):
        # pygame.draw.rect(window, self.rgb, (self.x+offset[0], self.y+offset[1], 2000, 2000))
        for x in range(len(self.tiles_list)):
            for y in range(len(self.tiles_list[0])):
                tile = self.tiles_list[x][y]
                window.blit(tile.image, (tile.x+offset[0], tile.y+offset[1]))
        for obs in self.obs_list:
            window.blit(obs.image, (obs.x+offset[0], obs.y+offset[1]))
        for npc in self.npcs_list:
            window.blit(npc.image, (npc.x+offset[0], npc.y+offset[1]))



class COC(object):
    """docstring for COC."""

    def __init__(self, x, y):
        super(COC, self).__init__()
        self.chunks_list = [
            [ Chunk(-2000,-2000), Chunk(0,-2000)],
            [ Chunk(-2000, 0) , Chunk(0,0)],
        ]

    def draw(self, window, offset):
        self.update(offset)
        self.chunks_list[0][0].draw(window, offset)
        self.chunks_list[0][1].draw(window, offset)
        self.chunks_list[1][0].draw(window, offset)
        self.chunks_list[1][1].draw(window, offset)

    def update(self,offset):
        offset = [offset[0]*-1, offset[1]*-1]
        # if offsets y is > 30% of a chunks height above the center y
        # remove the bottom 2 chunks from chunks_list
        # move the top two chunks to the bottom
        # generate 2 new chunks on the top
        # X vals should not change from the current two chunks, Y values should be math.floor((offset.y-500) / 500)*500

        #MOVE CHUNKS UP
        if offset[1] < self.chunks_list[0][0].y + 0.4*2000 - 475:
            #print('getting new chunks')
            self.chunks_list[1] = self.chunks_list[0]
            self.chunks_list[0] = [
                    Chunk(self.chunks_list[1][0].x, self.chunks_list[1][0].y - 2000),
                    Chunk(self.chunks_list[1][1].x, self.chunks_list[1][1].y - 2000)
            ]
        #MOVE CHUNKS DOWN
        if offset[1] > self.chunks_list[1][0].y + 0.4*2000 - 475:
            #print('getting new chunks')
            self.chunks_list[0] = self.chunks_list[1]
            self.chunks_list[1] = [
                    Chunk(self.chunks_list[0][0].x, self.chunks_list[0][0].y + 2000),
                    Chunk(self.chunks_list[0][1].x, self.chunks_list[0][1].y + 2000)
            ]
        #MOVE CHUNKS LEFT
        if offset[0] < self.chunks_list[0][0].x + 0.4*2000 - 775:
            #print('getting new chunks')
            self.chunks_list[0][1] = self.chunks_list[0][0]
            self.chunks_list[1][1] = self.chunks_list[1][0]

            self.chunks_list[0][0] = Chunk(self.chunks_list[0][0].x - 2000, self.chunks_list[0][0].y)
            self.chunks_list[1][0] = Chunk(self.chunks_list[1][0].x - 2000, self.chunks_list[1][0].y)

        #MOVE CHUNKS RIGHT
        if offset[0] > self.chunks_list[0][1].x + 0.4*2000 - 775:
            #print('getting new chunks')
            self.chunks_list[0][0] = self.chunks_list[0][1]
            self.chunks_list[1][0] = self.chunks_list[1][1]

            self.chunks_list[0][1] = Chunk(self.chunks_list[0][1].x + 2000, self.chunks_list[0][1].y)
            self.chunks_list[1][1] = Chunk(self.chunks_list[1][1].x + 2000, self.chunks_list[1][1].y)



    def get_obstacles(self):
        all_obstacles = []
        for obs in self.chunks_list[0][0].obs_list:
            all_obstacles.append(obs)
        for obs in self.chunks_list[0][1].obs_list:
            all_obstacles.append(obs)
        for obs in self.chunks_list[1][0].obs_list:
            all_obstacles.append(obs)
        for obs in self.chunks_list[1][1].obs_list:
            all_obstacles.append(obs)
        return all_obstacles

    def get_all_npcs(self):
        return self.chunks_list[0][0].npcs_list + self.chunks_list[0][1].npcs_list + self.chunks_list[1][0].npcs_list + self.chunks_list[1][1].npcs_list





world = COC(0,0)

obstacles = [
        Obstacle('chest.png', 200, 300, onpickup_item=item_scroll),
        Obstacle('chest.png', 700, 900, onpickup_item=item_scroll),
        Obstacle('chest.png', 1200, 300, onpickup_item=item_scroll),
        Obstacle('tree_1.png', 900, 700),
        Obstacle('tree_1.png', 100, 900),
        Obstacle('tree_1.png', 1000, 300),
        Obstacle('fence_1.png', 1050, 300),
        Obstacle('fence_1.png', 1000, 350),
        Obstacle('tree_1.png', 1100, 300),
        Obstacle('tree_1.png', 1000, 400),
        Obstacle('tree_1.png', 1150, 300),
        Obstacle('tree_1.png', 1000, 450),

        Obstacle('tree_1.png', 2000, 300),
        Obstacle('tree_1.png', 2050, 300),
        Obstacle('tree_1.png', 2100, 300),
        Obstacle('tree_1.png', 2150, 300),
        Obstacle('tree_1.png', 2150, 350),
        Obstacle('tree_1.png', 2150, 400),
        Obstacle('tree_1.png', 2150, 450)

        ]

#list of all quests the player has to do

quest_tiers = [

    [
    Quest(translate('Give water to the yellow knight.'), 'water_bucket.png', 'knight.png', item_water_bucket),
    Quest(translate('Give a gold coin to the red knight.'), 'gold_coin.png', 'enemy_knight.png', item_gold_coin),
    Quest(translate('Give a key to the yellow knight.'), 'key.png', 'knight.png', item_key),
    Quest(translate('Give a gold bar to the red knight'), 'gold_bar.png', 'knight.png', item_gold_bar)
    ],
    [
    Quest(translate('The yellow knight wants to be rich.'), 'gold_bar.png', 'knight.png', item_gold_bar),
    Quest(translate('Take a scroll to the red knight.'), 'scroll.png', 'enemy_knight.png', item_scroll),
    Quest(translate('Bring yellow knight a shiny key'), 'key.png', 'knight.png', item_key),
    Quest(translate('Red knight needs a gold bar'), 'gold_bar.png', 'knight.png', item_gold_bar)
    ],
    [
    Quest(translate('Yellow knight is rich. Red knight is poor.'), 'gold_coin.png', 'enemy_knight.png', item_gold_coin),
    Quest(translate('Red knight has seen a fire!'), 'water_bucket.png', 'enemy_knight.png', item_water_bucket),
    Quest(translate('The yellow knight cannot get in to his house!'), 'key.png', 'knight.png', item_key),
    Quest(translate('Red knight has been robbed! His gold bar is missing!'), 'gold_bar.png', 'knight.png', item_gold_bar)
    ]

]

questList = [
        Quest(translate('Give water to the yellow knight'), 'water_bucket.png', 'enemy_knight.png', item_water_bucket),
        Quest(translate('Give a gold coin to the red knight'), 'gold_coin.png', 'knight.png', item_gold_coin)
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
        print('change language')
def DONOTHING():
        print('pog')
menubox = pygame.image.load('menubox.png').convert_alpha()
menubox = pygame.transform.scale(menubox, (700, 170))
menubox_hover = pygame.image.load('menubox_hover.png').convert_alpha()
menubox_hover = pygame.transform.scale(menubox_hover, (700, 170))
pause = pygame.image.load('pause.png').convert_alpha()
pause = pygame.transform.scale(pause, (496, 168))
pauseMenuBoxes = [[translate('Save'), PauseMenu_Save], [translate('Load'), PauseMenu_Load], [translate(str(language_names[languages.index(language)])), PauseMenu_ChangeLanguage]]
#Status Bar Stuff
statusbar = pygame.image.load('statusbar.png').convert_alpha()
statusbar = pygame.transform.scale(statusbar, (318, 42))
healthpixel = pygame.image.load('statusbar_healthpixel.png').convert_alpha()
healthpixel = pygame.transform.scale(healthpixel, (3, 24))
manapixel = pygame.image.load('statusbar_manapixel.png').convert_alpha()
manapixel = pygame.transform.scale(manapixel, (3, 24))
xppixel = pygame.image.load('statusbar_xppixel.png').convert_alpha()
xppixel = pygame.transform.scale(xppixel, (3, 24))
leftArrowPressed = pygame.image.load('menuArrow_pressed.png').convert_alpha()
leftArrowPressed = pygame.transform.scale(leftArrowPressed, (100, 100))
leftArrowPressed = pygame.transform.flip(leftArrowPressed, False, False)
leftArrow = pygame.image.load('menuArrow.png').convert_alpha()
leftArrow = pygame.transform.scale(leftArrow, (100, 100))
leftArrow = pygame.transform.flip(leftArrow, False, False)
rightArrowPressed = pygame.image.load('menuArrow_pressed.png').convert_alpha()
rightArrowPressed = pygame.transform.scale(rightArrowPressed, (100, 100))
rightArrowPressed = pygame.transform.flip(rightArrowPressed, True, False)
rightArrow = pygame.image.load('menuArrow.png').convert_alpha()
rightArrow = pygame.transform.scale(rightArrow, (100, 100))
rightArrow = pygame.transform.flip(rightArrow, True, False)

#SOUND
pygame.mixer.init()
deathSound = pygame.mixer.Sound('SFX_Dead.wav')
miscSound1 = pygame.mixer.Sound('SFX_Misc.wav')

#SPRITES
global knight_sprites
global currentSprite
knight_spritesheet = pygame.image.load('knight2.png').convert_alpha()
knight_spritelist = [[0, 0, 20, 20], [-21, 0, 20, 20], [-42, 0, 20, 20], [-63, 0, 20, 20], [0, -21, 20, 20], [-21, -21, 20, 20], [-42, -21, 20, 20], [-63, -21, 20, 20], [0, -42, 20, 20]]
knight_sprites = []
for sprite in knight_spritelist:
    surf = pygame.Surface((sprite[2], sprite[3]), pygame.SRCALPHA)
    surf.blit(knight_spritesheet.convert_alpha(), (sprite[0], sprite[1]))
    knight_sprites.append(surf)
movementInterval = 0.45
movetime = time.time()
still = False
direction = 'down'
lastpressed = None

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






def updateMobs():
        for mob in mobs:
            mob.move()
            if CheckDistance((hero.x, hero.y), (mob.x, mob.y)) > 2000:
                mobs.remove(mob)
                mobs.append(Mob('goblin.png', hero.x + np.random.choice([-1,1],1)[0]*np.random.randint(50,150), hero.y + np.random.choice([-1,1],1)[0]*np.random.randint(50,150), "Buckethead 2"))
        drawMobs()

def drawMobs():
        for mob in mobs:
            window.blit(mob.image, (int(mob.x), int(mob.y)))

def drawPlayer():
        global currentSprite
        global knight_sprites
        currentSprite = knight_sprites[currentSprite]
        tempsurf = pygame.transform.scale(currentSprite, (50, 50))
        if flip == True:
            tempsurf = pygame.transform.flip(tempsurf, True, False)
        window.blit(tempsurf, (hero.x, hero.y))

def drawObstacles():
        for obs in obstacles:
                window.blit(obs.image, (obs.x, obs.y))

def drawNpcs():
        for guy in npcs:
                window.blit(guy.image, (guy.x, guy.y))

def drawInventory():
        global invPositions
        global inventoryList
        if inventory_open:
                inventoryImage = pygame.image.load('Inventory.png').convert_alpha()
                inventoryStartPixel = (window.get_width() - inventoryImage.get_width() * 4 + 13, int(window.get_height() / 2 - (inventoryImage.get_height() / 2) * 4))
                inventoryImage = pygame.transform.scale(inventoryImage, (464, 800))
                window.blit(inventoryImage, inventoryStartPixel)
                text = font_inv.render(translate('Inventory'), True, (139, 69, 19))
                window.blit(text,(inventoryStartPixel[0] + int(inventoryImage.get_width() / 2) - int(text.get_width() / 2), inventoryStartPixel[1] + 65))
                for loops, item in enumerate(inventoryList):
                        if MousePosition[0] > invPositions[loops][0] + inventoryStartPixel[0] and MousePosition[0] < invPositions[loops][0] + inventoryStartPixel[0] + 80 and MousePosition[1] > invPositions[loops][1] + inventoryStartPixel[1] and MousePosition[1] < invPositions[loops][1] + inventoryStartPixel[1] + 80:
                                window.blit(inventory_hover, (int(invPositions[loops][0] + inventoryStartPixel[0]), int(invPositions[loops][1] + inventoryStartPixel[1])))
                        itemTitle = font_inv_small.render((translate(inventoryList[loops].name)), True, BLACK)
                        window.blit(itemTitle, (int(invPositions[loops][0] + inventoryStartPixel[0] - (itemTitle.get_width() / 2)) + 40, invPositions[loops][1] + inventoryStartPixel[1] + 85))
                        window.blit(inventoryList[loops].image, (int(invPositions[loops][0] + inventoryStartPixel[0] + 8), int(invPositions[loops][1] + inventoryStartPixel[1] + 8)))
                        if loops == 23:
                                break

def checkInteraction():
        global interactable
        interactable = False
        for guy in world.get_all_npcs():
                # print(guy.x, guy.y, [hero.x-offset[0], hero.y-offset[1]], CheckDistance([guy.x, guy.y], [hero.x-offset[0], hero.y-offset[1]]))
                if CheckDistance([guy.x, guy.y], [hero.x-offset[0], hero.y-offset[1]]) < 50:
                # if (abs((hero.x-offset[0]) - guy.x) < 40 and ((hero.y-offset[1]) - guy.y < 35) and ((hero.y-offset[1]) - guy.y > 0)) or (abs((hero.x-offset[0]) - guy.x) < 40 and (guy.y - (hero.y-offset[1]) < 50) and (guy.y - (hero.y-offset[1]) > 0)) or ((hero.x-offset[0]) - guy.x < 50 and (hero.x-offset[0]) - guy.x > 0 and ((((hero.y-offset[1]) - guy.y < 25) and ((hero.y-offset[1]) - guy.y > 0)) or (guy.y - (hero.y-offset[1]) < 45) and (guy.y - (hero.y-offset[1]) > 0))) or guy.x - (hero.x-offset[0]) < 50 and guy.x - (hero.x-offset[0]) > 0 and ((((hero.y-offset[1]) - guy.y < 25) and ((hero.y-offset[1]) - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                        interactable = True
                        # try to give the npc an item
                        for thing in inventoryList:
                                if len(questList) > 0 and thing.name == questList[current_quest].target_item.name and guy.image_name == questList[current_quest].target_npc:
                                        guy.complete_quest()
                                        pinMessage(guy.message_3)
                                        inventoryList.remove(thing)
                                        hero.add_xp(75)
                                        # auto-switch to next quest
                                        questList.remove(questList[current_quest])
                                        print(hero.level)
                                        questList.append(quest_tiers[min(2,hero.level-1)][np.random.choice([0,1],1)[0]])

                                        break
                        break
                        #drawMessage()
        for obj in world.get_obstacles():
                if CheckDistance((hero.x - offset[0], hero.y - offset[1]), (obj.x, obj.y)) < 100:
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

        message_text = translate(message)
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
                                text = font_message.render(translate(guy.message_1), True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height() + 50))
                                text = font_message.render(translate(guy.message_2), True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height() + 85))
                                text = font_message.render(translate(guy.message_3), True, (139, 69, 19))
                                window.blit(text, (int(window.get_width() / 2 - textbox_image.get_width() / 2) + 50, window.get_height() - textbox_image.get_height() + 120))

def drawQuest():
        textbox_image = pygame.image.load('questbox.png').convert_alpha()
        textbox_image = pygame.transform.scale(textbox_image, (492, 104))
        quest_icon = pygame.image.load('icon_quest.png').convert_alpha()
        quest_icon = pygame.transform.scale(quest_icon, (64, 64))
        window.blit(textbox_image, (0, 0))
        if len(questList) > 0:
                text = font_questbox.render(translate(questList[current_quest].goal), True, BLACK)
                window.blit(text, (20, (int(textbox_image.get_height() / 2 - (text.get_height() / 2)))))
                text = font_questbox.render(translate(questList[current_quest].goal), True, YELLOW)
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
        healthText = font_inv_small.render(translate('Health: ' + str(hero.health) + ' of 100'), True, WHITE)
        manaText = font_inv_small.render(translate('Mana: ' + str(hero.mana) + ' of 100'), True, WHITE)
        xpText = font_inv_small.render(translate('experiance: ' + str(hero.xp) + ' of ' + str(100 + ((hero.level-1) * 25))), True, WHITE)
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
        global offset
        collision = False
        if direction == 'up':

                for obs in obstacles:
                        if abs(hero.x - obs.x) < 40 and (hero.y - obs.y < 26) and (hero.y - obs.y > 0) and obs.collidable:
                                collision = True
                for obs in world.get_obstacles():
                        if abs(hero.x - offset[0] - obs.x) < 40 and (hero.y - offset[1] - obs.y < 26) and (hero.y - offset[1] - obs.y > 0) and obs.collidable:
                                collision = True
                for guy in npcs:
                        if abs(hero.x - guy.x) < 40 and (hero.y - guy.y < 26) and (hero.y - guy.y > 0):
                                collision = True
                # if abs(hero.x - mob.x) < 40 and (hero.y - mob.y < 35) and (hero.y - mob.y > 0):
                #       collision = True
                if not collision:
                        offset[1] += hero.vel
                        for obs in obstacles:
                                obs.y += hero.vel
                        for guy in npcs:
                                guy.y += hero.vel
                        for mob in mobs:
                            mob.y += hero.vel
                            if mob.goal is not None:
                                mob.goal[1] += hero.vel
        if direction == 'down':
                for obs in obstacles:
                        if abs(hero.x - obs.x) < 40 and (obs.y - hero.y < 50) and (obs.y - hero.y > 0) and obs.collidable:
                                collision = True
                for obs in world.get_obstacles():
                        if abs(hero.x - offset[0] - obs.x) < 40 and (obs.y - hero.y+offset[1] < 50) and (obs.y - hero.y+offset[1] > 0) and obs.collidable:
                                collision = True
                for guy in npcs:
                        if abs(hero.x - guy.x) < 40 and (guy.y - hero.y < 50) and (guy.y - hero.y > 0):
                                collision = True
                # if abs(hero.x - mob.x) < 40 and (mob.y - hero.y < 50) and (mob.y - hero.y > 0):
                #       collision = True
                if not collision:
                        offset[1] -= hero.vel
                        for obs in obstacles:
                                obs.y -= hero.vel
                        for guy in npcs:
                                guy.y -= hero.vel
                        for mob in mobs:
                            mob.y -= hero.vel
                            if mob.goal is not None:
                                mob.goal[1] -= hero.vel
        if direction == 'left':
                for obs in obstacles:
                        if hero.x - obs.x < 50 and hero.x - obs.x > 0 and (((hero.y - obs.y < 25) and (hero.y - obs.y > 0)) or (obs.y - hero.y < 45) and (obs.y - hero.y > 0)) and obs.collidable:
                                collision = True
                for obs in world.get_obstacles():
                        if hero.x - offset[0] - obs.x < 50 and hero.x - offset[0] - obs.x > 0 and (((hero.y - offset[1] - obs.y < 25) and (hero.y - offset[1] - obs.y > 0)) or (obs.y - hero.y + offset[1] < 45) and (obs.y - hero.y + offset[1] > 0)) and obs.collidable:
                                collision = True
                for guy in npcs:
                        if hero.x - guy.x < 50 and hero.x - guy.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                                collision = True
                # if hero.x - mob.x < 50 and hero.x - mob.x > 0 and (((hero.y - mob.y < 25) and (hero.y - mob.y > 0)) or (mob.y - hero.y < 45) and (mob.y - hero.y > 0)):
                #       collision = True
                if not collision:
                        offset[0] += hero.vel
                        for obs in obstacles:
                                obs.x += hero.vel
                        for guy in npcs:
                                guy.x += hero.vel
                        for mob in mobs:
                            mob.x += hero.vel
                            if mob.goal is not None:
                                mob.goal[0] += hero.vel
        if direction == 'right':
                for obs in obstacles:
                        if obs.x - hero.x < 50 and obs.x - hero.x > 0 and (((hero.y - obs.y < 25) and (hero.y - obs.y > 0)) or (obs.y - hero.y < 45) and (obs.y - hero.y > 0)) and obs.collidable:
                                collision = True
                for obs in world.get_obstacles():
                        if obs.x - hero.x + offset[0] < 50 and obs.x - hero.x + offset[0] > 0 and (((hero.y - offset[1] - obs.y < 25) and (hero.y - offset[1] - obs.y > 0)) or (obs.y - hero.y + offset[1] < 45) and (obs.y - hero.y + offset[1] > 0)) and obs.collidable:
                                collision = True
                for guy in npcs:
                        if guy.x - hero.x < 50 and guy.x - hero.x > 0 and (((hero.y - guy.y < 25) and (hero.y - guy.y > 0)) or (guy.y - hero.y < 45) and (guy.y - hero.y > 0)):
                                collision = True
                # if mob.x - hero.x < 50 and mob.x - hero.x > 0 and (((hero.y - mob.y < 25) and (hero.y - mob.y > 0)) or (mob.y - hero.y < 45) and (mob.y - hero.y > 0)):
                #       collision = True
                if not collision:
                        offset[0] -= hero.vel
                        for obs in obstacles:
                                obs.x -= hero.vel
                        for guy in npcs:
                                guy.x -= hero.vel
                        for mob in mobs:
                            mob.x -= hero.vel
                            if mob.goal is not None:
                                mob.goal[0] -= hero.vel

def CheckDistance(pos1, pos2):
        distance = ((pos1[0] - pos2[0])**2 + (pos2[1] - pos1[1])**2)**0.5
        return distance

inventory_open = False
interactable = False


#update all time delays
def updateDelays():
        if len(questList) > 0:
                questList[current_quest].time_spent


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
                miscSound1.play()
                escapeHeld = True
                pauseBG = pygame.transform.scale(pauseBG, (window.get_width(), window.get_height()))
                window.blit(pauseBG, (0, 0))
                dimensions = (window.get_width(), window.get_height())
                boxSelected = 0
                keyHeld = False
                dHeld = False
                enterHeld = False
                isSaved = False
                isLoaded = False
                isLeft = False
                isRight = False
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
                                miscSound1.play()
                                break
                        if keys[pygame.K_ESCAPE] == False:
                                escapeHeld = False
                        #Move menu up/down
                        if not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_d] and not keys[pygame.K_a]:
                                keyHeld = False
                                isLeft = False
                                isRight = False

                        if keys[pygame.K_w] and keyHeld == False:
                                miscSound1.play()
                                keyHeld = True
                                if boxSelected == 0:
                                    boxSelected = 2
                                else:
                                    boxSelected = boxSelected - 1
                        elif keys[pygame.K_s] == True and keyHeld == False:
                                miscSound1.play()
                                keyHeld = True
                                if boxSelected == 2:
                                    boxSelected = 0
                                else:
                                    boxSelected = boxSelected + 1

                        #Click menu button
                        if keys[pygame.K_RETURN] and enterHeld == False:
                                pauseMenuBoxes[boxSelected][1]()
                                enterHeld = True
                        if keys[pygame.K_RETURN] == False:
                                enterHeld = False

                        if keys[pygame.K_d] and keyHeld == False and boxSelected == 2:
                                language = languages[(languages.index(language)+1) % len(languages)]
                                print('Changed language to: ' + language_names[(languages.index(language))])
                                miscSound1.play()
                                keyHeld = True
                                isRight = True

                                if language == "ar":
                                    font_inv = font_inv_arabic
                                    font_inv_small = font_inv_small_arabic
                                    font_message = font_message_arabic
                                    debugFont = debugFont_arabic
                                    font_questbox = font_questbox_arabic
                                else:
                                    font_inv = font_inv_english
                                    font_inv_small = font_inv_small_english
                                    font_message = font_message_english
                                    debugFont = debugFont_english
                                    font_questbox = font_questbox_english

                        if keys[pygame.K_a] and keyHeld == False and boxSelected == 2:
                                language = languages[(languages.index(language)-1) % len(languages)]
                                print('Changed language to: ' + language_names[(languages.index(language))])
                                miscSound1.play()
                                keyHeld = True
                                isLeft = True

                                if language == "ar":
                                    font_inv = font_inv_arabic
                                    font_inv_small = font_inv_small_arabic
                                    font_message = font_message_arabic
                                    debugFont = debugFont_arabic
                                    font_questbox = font_questbox_arabic
                                else:
                                    font_inv = font_inv_english
                                    font_inv_small = font_inv_small_english
                                    font_message = font_message_english
                                    debugFont = debugFont_english
                                    font_questbox = font_questbox_english


                        #Blit 'pause' and boxes, text
                        window.blit(pause, (int(window.get_width() / 2 - pause.get_width() / 2), 50))
                                #'Save!'/'Load!' text


                        window.blit(leftArrow, (int(window.get_width() / 2 - menubox.get_width() / 2 - 100), int(260 + ((menubox.get_height() + 50) * 2) + menubox.get_height() / 2 - leftArrowPressed.get_height() / 2)))
                        window.blit(rightArrow, (int(window.get_width() / 2 + menubox.get_width() / 2), int(260 + ((menubox.get_height() + 50) * 2) + menubox.get_height() / 2 - leftArrowPressed.get_height() / 2)))

                        if isLeft == True:
                            # window.blit(menubox, (int(window.get_width() / 2 - menubox.get_width() / 2), 260 + (menubox.get_height() + 50) * pauseMenuBoxes.index(box)))
                            #
                            window.blit(leftArrowPressed, (int(window.get_width() / 2 - menubox.get_width() / 2 - 100), int(260 + ((menubox.get_height() + 50) * 2) + menubox.get_height() / 2 - leftArrowPressed.get_height() / 2)))
                            pauseMenuBoxes = [[translate('Save'), PauseMenu_Save], [translate('Load'), PauseMenu_Load], [translate(str(language_names[languages.index(language)])), PauseMenu_ChangeLanguage]]
                        if isRight == True:
                            # window.blit(menubox, (int(window.get_width() / 2 - menubox.get_width() / 2), 260 + (menubox.get_height() + 50) * pauseMenuBoxes.index(box)))
                            #
                            window.blit(rightArrowPressed, (int(window.get_width() / 2 + menubox.get_width() / 2), int(260 + ((menubox.get_height() + 50) * 2) + menubox.get_height() / 2 - leftArrowPressed.get_height() / 2)))
                            pauseMenuBoxes = [[translate('Save'), PauseMenu_Save], [translate('Load'), PauseMenu_Load], [translate(str(language_names[languages.index(language)])), PauseMenu_ChangeLanguage]]



                        if isSaved == True:
                                savedText = font_inv.render(translate('Saved!'), True, BLACK)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 30), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2)))
                                savedText = font_inv.render(translate('Saved!'), True, YELLOW)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 32), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2)))
                        if isLoaded == True:
                                savedText = font_inv.render(translate('Loaded!'), True, BLACK)
                                window.blit(savedText, (int(window.get_width() / 2 + menubox.get_width() / 2 + 30), int(260 + menubox.get_height() / 2 - savedText.get_height() / 2 + menubox.get_height() + 50)))
                                savedText = font_inv.render(translate('Loaded!!'), True, YELLOW)
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
        if time.time() > movetime + (movementInterval * 2):
                movetime = time.time()
        flip = False
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not inventory_open:
                direction = 'up'
                if lastpressed != 'up':
                    movetime = time.time()
                lastpressed ='up'
                still = False
                move('up')
                interactable = False
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not inventory_open:
                direction = 'down'
                if lastpressed != 'down':
                    movetime = time.time()
                lastpressed = 'down'
                still = False
                move('down')
                interactable = False
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not inventory_open:
                direction = 'left'
                if lastpressed != 'left':
                    movetime = time.time()
                lastpressed = 'left'
                still = False
                move('left')
                interactable = False
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not inventory_open:
                direction = 'right'
                if lastpressed != 'right':
                    movetime = time.time()
                lastpressed = 'right'
                still = False
                move('right')
                interactable = False
        if keys[pygame.K_RETURN] and not inventory_open and not interactable and not return_held:
                return_held = True
                checkInteraction()
        if keys[pygame.K_RETURN] and not inventory_open and not return_held:
                interactable = False
        #for SPRITES
        if (keys[pygame.K_UP] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_a]) == False:
            still = True
            lastpressed = None
        else:
            still = False
        if still == True:
            if direction == 'up':
                currentSprite = 0
            elif direction == 'right':
                currentSprite = 6
            elif direction == 'down':
                currentSprite = 3
            elif direction == 'left':
                currentSprite = 6
                flip = True
        else:
            if direction == 'up':
                if time.time() > movetime + movementInterval:
                    currentSprite = 1
                else:
                    currentSprite = 2
            elif direction == 'right':
                if time.time() > movetime + movementInterval:
                    currentSprite = 7
                else:
                    currentSprite = 8
            elif direction == 'down':
                if time.time() > movetime + movementInterval:
                    currentSprite = 4
                else:
                    currentSprite = 5
            elif direction == 'left':
                if time.time() > movetime + movementInterval:
                    currentSprite = 7
                    flip = True
                else:
                    currentSprite = 8
                    flip = True
        return_held = keys[pygame.K_RETURN]

        #inventory input
        if keys[pygame.K_e] and not e_held:
                inventory_open = not inventory_open
        e_held = keys[pygame.K_e]

        #draw in all the stuff
        window.fill((0,0,0)) #fill background, deletes old positions of stuff
        world.draw(window, offset)

        drawObstacles()
        drawNpcs()
        updateMobs()
        drawPlayer()
        drawInventory()
        drawMessage()
        drawPinnedMessage()
        updateDelays()

        #If going to pause next frame, don't draw UI elements
        if BEGINPAUSE == False:
                drawStatsUI()
                drawQuest()
                drawDebug()
        else:
                FRAMEENDED = True



        pygame.display.update()

f = open("translations.json", "w", encoding='utf-8')
json.dump(all_translated_text, f, ensure_ascii=False)
f.close()
pygame.quit()
sys.exit(0)





#class Item(object):
