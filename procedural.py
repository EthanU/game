import numpy as np
import pygame

class Obstacle(object):
        """docstring for Obstacle"""
        def __init__(self, image_name, x, y, onpickup_item=None, collidable=True):
                super(Obstacle, self).__init__()
                self.image = pygame.image.load(image_name).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.x = x
                self.y = y
                self.onpickup_item = onpickup_item
                self.image_name = image_name
                self.collidable  = collidable
                if onpickup_item != None:
                        self.message = "You found a " + onpickup_item.name + "."
                else:
                        self.message = 'You found nothing.'


        def interact(self):
                item_to_give = self.onpickup_item
                self.onpickup_item = None
                # self.message = translate('You found nothing.')
                return item_to_give



class Chunk(object):
    """docstring for Chunk."""

    def __init__(self, x, y):
        super(Chunk, self).__init__()
        # np.random.seed(str(x) + "---" + str(y))

        sin_vals = (np.sin(x / 6000 + 10) + 0.1*np.sin(x / 2500) + np.sin(y / 900 + 2468) + 0.07*np.sin(y / 2500)) / 2.17 # between -1 and 1

        np.random.seed(abs(x * y) % 100000000 )

        self.x = x
        self.y = y


        #VARIATIONS

        self.rgb = (128 + 100*sin_vals, 0,0)
        self.vege = sin_vals
        if self.vege > .5:
            self.rgb = (0, 255, 0)
        elif self.vege > -0.5:
            self.rgb = (210, 180, 140)
        else:
            self.rgb = (192, 192, 192)

        obstacle_frequency = self.vege + 1

        self.obs_list = []

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
                elif (bridge_X_sin_y > 0 and abs(bridge_X_sin_x) < 0.05) or (bridge_Y_sin_x > 0 and abs(bridge_Y_sin_y) < 0.05):
                    self.obs_list.append(Obstacle('dirt.png', xx, yy, collidable=False))

                    #branch out
                    chance = np.random.randint(0, 10)
                    direction = np.random.randint(0,4) #up down left right
                    distance = np.random.randint(5,14)
                    if chance < 1:
                        if direction == 0:
                            for num in range(0, distance):
                                valid = True
                                for obs in self.obs_list:
                                    if obs.x == xx + 50*num and obs.y == yy:
                                        valid = False
                                if valid:
                                    self.obs_list.append(Obstacle('dirt.png', xx + 50*num, yy, collidable=False))
                        if direction == 1:
                            for num in range(0, distance):
                                valid = True
                                for obs in self.obs_list:
                                    if obs.x == xx - 50*num and obs.y == yy:
                                        valid = False
                                if valid:
                                    self.obs_list.append(Obstacle('dirt.png', xx - 50*num, yy, collidable=False))
                        if direction == 2:
                            for num in range(0, distance):
                                valid = True
                                for obs in self.obs_list:
                                    if obs.x == xx and obs.y == yy + 50*num:
                                        valid = False
                                if valid:
                                    self.obs_list.append(Obstacle('dirt.png', xx, yy + 50*num, collidable=False))
                        if direction == 3:
                            for num in range(0, distance):
                                valid = True
                                for obs in self.obs_list:
                                    if obs.x == xx and obs.y == yy - 50*num:
                                        valid = False
                                if valid:
                                    self.obs_list.append(Obstacle('dirt.png', xx, yy - 50*num, collidable=False))



        #Trees, fences, etc
        for i in range(0, np.random.randint(25,int(obstacle_frequency * 50) + 50)):
            x = np.random.randint(0, 39)*50+self.x
            y = np.random.randint(0, 39)*50+self.y
            valid = True
            for obs in self.obs_list:
                if obs.x == x and obs.y == y:
                    valid = False
            if valid:
                rando = np.random.uniform(0, self.vege+1)
                if rando > .65:
                    self.obs_list.append(Obstacle('tree_1.png', x, y, collidable=False))
                else:
                    self.obs_list.append(Obstacle('fence_1.png', x, y, collidable=False))





    def draw(self, window, offset):
        pygame.draw.rect(window, self.rgb, (self.x+offset[0], self.y+offset[1], 2000, 2000))
        for obs in self.obs_list:
                window.blit(obs.image, (obs.x+offset[0], obs.y+offset[1]))


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
            print('getting new chunks')
            self.chunks_list[1] = self.chunks_list[0]
            self.chunks_list[0] = [
                    Chunk(self.chunks_list[1][0].x, self.chunks_list[1][0].y - 2000),
                    Chunk(self.chunks_list[1][1].x, self.chunks_list[1][1].y - 2000)
            ]
        #MOVE CHUNKS DOWN
        if offset[1] > self.chunks_list[1][0].y + 0.4*2000 - 475:
            print('getting new chunks')
            self.chunks_list[0] = self.chunks_list[1]
            self.chunks_list[1] = [
                    Chunk(self.chunks_list[0][0].x, self.chunks_list[0][0].y + 2000),
                    Chunk(self.chunks_list[0][1].x, self.chunks_list[0][1].y + 2000)
            ]
        #MOVE CHUNKS LEFT
        if offset[0] < self.chunks_list[0][0].x + 0.4*2000 - 775:
            print('getting new chunks')
            self.chunks_list[0][1] = self.chunks_list[0][0]
            self.chunks_list[1][1] = self.chunks_list[1][0]

            self.chunks_list[0][0] = Chunk(self.chunks_list[0][0].x - 2000, self.chunks_list[0][0].y)
            self.chunks_list[1][0] = Chunk(self.chunks_list[1][0].x - 2000, self.chunks_list[1][0].y)

        #MOVE CHUNKS RIGHT
        if offset[0] > self.chunks_list[0][1].x + 0.4*2000 - 775:
            print('getting new chunks')
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
