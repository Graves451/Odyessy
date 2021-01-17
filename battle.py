import pygame
import sys

Map_width = 800
Map_length = 520

Grid_size = 40

Grid_width = int(Map_width/Grid_size)
Grid_length = int(Map_length/Grid_size)

blocks = {
    "G":{"name":"grass","passable":True,"color":(126, 200, 80)},
    "W":{"name":"water","passable":False,"color":(0, 159, 225)},
    "M":{"name":"mountain","passable":False,"color":(151,145,144)},
    "F":{"name":"fort","passable":True,"color":(149,148,139)}
}

motion = {
    "up":(0,-1),
    "down":(0,1),
    "left":(-1,0),
    "right":(1,0)
}

map = []

enemies = {}
allies = {}

class BattleMap:
    def __init__(self,surface,screen,battlenum):
        self.screen = screen
        self.surface = surface
        clock = pygame.time.Clock()
        with open("game_data/"+str(battlenum)+"battle.txt","r") as file:
            for y in range(Grid_length):
                map.append([])
                array = file.readline().split(" ")
                for x in range(len(array)):
                    block_name = array[x]
                    block_name = block_name.replace("\n", "")
                    map[y].append(blocks[block_name])
            enemyspawn = file.readline().split(" ")
            alliedspawn = [int(x) for x in file.readline().split(" ")]


        file.close()

        drawGrid(surface)

        user_cursor = Cursor()

        while True:
            output = user_cursor.handle_keys()
            clock.tick(100)
            drawGrid(surface)
            user_cursor.draw(surface)
            screen.blit(surface, (0,0))
            pygame.display.update()

    def generate_enemies(self,level):
        #stats [name,health,attack,defense,movement]
        enemyTroop = ["generic infantry",(7,7),2,4,3]


class Cursor:
    def __init__(self):
        self.position = (6,6)
        self.color = (255,255,0)

    def handle_keys(self):
        for user_input in pygame.event.get():
            if user_input.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if user_input.type == pygame.KEYDOWN:
                if user_input.key == pygame.K_UP:
                    self.move(motion["up"])
                elif user_input.key == pygame.K_DOWN:
                    self.move(motion["down"])
                elif user_input.key == pygame.K_LEFT:
                    self.move(motion["left"])
                elif user_input.key == pygame.K_RIGHT:
                    self.move(motion["right"])
                #goes in when the user pressed x
                elif user_input.key == 120:
                    a = 0

    def move(self,direction):
        moved_position = (self.position[0]+direction[0],self.position[1]+direction[1])
        print(moved_position)
        if 0 <= moved_position[0] < Grid_width and 0 <= moved_position[1] < Grid_length:
            if map[moved_position[1]][moved_position[0]]["passable"]:
                self.position = moved_position

    def draw(self,surface):
        s = pygame.Surface((Grid_size,Grid_size))
        s.set_alpha(128)
        s.fill(self.color)
        surface.blit(s, (self.position[0]*Grid_size, self.position[1]*Grid_size))


def drawGrid(surface):
    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            rr = pygame.Rect((x*Grid_size, y*Grid_size), (Grid_size,Grid_size))
            pygame.draw.rect(surface, map[y][x]["color"], rr)