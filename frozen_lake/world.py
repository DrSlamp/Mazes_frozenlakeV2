import pygame
import numpy as np
from . import settings
from .tilemap import TileMap
from . maze_generators import MazeGenerator 
from . maze_generators import DepthFirstMazeGenerator
from . import maze_generators
from . frozen_lake import *


class World:
    def __init__(self, title, state, action, **kwargs):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_character = True
        self.render_walls = True
        self.render_goal = True
        self.tilemap = None
        self.finish_state = None
        self._create_tilemap()

        self._rows = kwargs.get("rows", settings.ROWS)
        self._cols = kwargs.get("cols", settings.COLS)
        maze_generator = kwargs.get(
            "maze_generator_class", maze_generators.DepthFirstMazeGenerator
        )(self._rows, self._cols)
        self.walls = maze_generator.generate()

        
        


    def _create_tilemap(self):
        tile_texture_names = ["ice" for _ in range(settings.NUM_TILES)]
        for _, actions_table in settings.P.items():
            for _, possibilities in actions_table.items():
                for _, state, reward, terminated in possibilities:
                    if terminated:
                        if reward > 0:
                            self.finish_state = state
                        else:
                            tile_texture_names[state] = "hole"

        tile_texture_names[self.finish_state] = "ice"
        self.tilemap = TileMap(tile_texture_names)







    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True
        for tile in self.tilemap.tiles:
            if tile.texture_name == "cracked_hole":
                tile.texture_name = "hole"

    def update(self, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                self.render_goal = False
                settings.SOUNDS['win'].play()
            else:
                self.tilemap.tiles[state].texture_name = "cracked_hole"
                self.render_character = False
                settings.SOUNDS['ice_cracking'].play()
                settings.SOUNDS['water_splash'].play()

        self.state = state
        self.action = action



    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settings.TEXTURES['stool'],
            (self.tilemap.tiles[0].x, self.tilemap.tiles[0].y)
        )

        if self.render_goal:
            self.render_surface.blit(
                settings.TEXTURES['goal'],
                (self.tilemap.tiles[self.finish_state].x,
                 self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES['character'][self.action],
                (self.tilemap.tiles[self.state].x,
                 self.tilemap.tiles[self.state].y)
            )



 # render the top wall
        print("-" * int(self._cols * 2 + 1))
        

        for i in range(self._rows):
            for j in range(self._cols):
                # evaluate if there is a left wall
                current_index = i * self._cols + j
                left_index = i * self._cols + j - 1

               


                has_left_wall = (
                    j == 0
                    or (current_index, left_index) in self.walls
                    or (left_index, current_index) in self.walls
                )

                # render the left wall if exists
                if has_left_wall:
                    # every left cell has a left wall
                    print("|", end="")
                  
               
            

                else:
                    # space if there is no a left wall
                    print(" ", end="")

                # render the cell
                print(" ", end="")

            # render the right wall for the current row
            print("|")

            # render the bottom wall when if exists
            for j in range(self._cols * 2 + 1):
                current_index = i * self._cols + j
                bottom_index = (i + 1) * self._cols + j
                has_bottom_wall = (
                    i == self._rows - 1
                    or j % 2 == 0
                    or (current_index, bottom_index) in self.walls
                    or (bottom_index, current_index) in self.walls
                )
                if has_bottom_wall:
                    print("-", end="")

                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-1].x, -25),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-2].x, -25),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-3].x, -25),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-4].x, -30),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-5].x, -25),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-6].x, -25),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-7].x, -25),       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[settings.NUM_TILES-8].x, -25),       
                )
                


           

            #test purpose
               
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-8].y  ) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-7].y  ) ,       
                )
                
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-6].y  ) ,       
                )

                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-5].y  ) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-4].y  ) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-3].y  ) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-2].y  ) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[-1].y  ) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_v'], (-25,self.tilemap.tiles[0].y  ) ,       
                )
               
                #test purpose
               
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[-1].x, self.tilemap.tiles[settings.NUM_TILES-8].y)
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[-2].x, self.tilemap.tiles[settings.NUM_TILES-8].y) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[-3].x, self.tilemap.tiles[settings.NUM_TILES-8].y) ,       
                )
                self.render_surface.blit(
                settings.TEXTURES['wall_h'], (self.tilemap.tiles[-4].x, self.tilemap.tiles[settings.NUM_TILES-8].y) ,       
                )
                
                
               
          
          
           





               
             
             
               
          
         
            
        else:
                    # space if there is not a bottom wall
            print(" ", end="")

            # finally, end of line
            print("")
            











        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
