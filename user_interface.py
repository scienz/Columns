# Xinchen Zhang
# 25702388

from pathlib import Path
import pygame
import game_logic
import random


'''
"Please, fix your game algorithm first before dealing with these fancy stuff."
"Will do." (No)
'''

'''
Constants
'''

RED= pygame.Color(255, 109, 109)
GREEN= pygame.Color(48, 255, 114)
BLUE= pygame.Color(72, 140, 249)
PINK= pygame.Color(255, 114, 196)
YELLOW= pygame.Color(240, 242, 123)
CYAN= pygame.Color(132, 255, 230)
PURPLE= pygame.Color(179, 158, 255)

WHITE= pygame.Color(255, 255, 255)
DARK= pygame.Color(0, 0, 0)
GREY= pygame.Color(222, 227, 234)

FONT= 'comicsansms'

DEFAULT_WINDOW_WIDTH= 570
DEFAULT_WINDOW_HEIGHT= 730

'''
The main class for the game
'''

class GameInterface:
    def __init__(self):
        self.game= game_logic.Game()
        
        self.scale= ToScale()
        self.picture= Picture()
        
        self._running= True
        self._game_begin= False
        self._pause= False

        self._score= 0
        self._column= -1

        
    def run(self)-> None:
        # Main function of running the game
        pygame.init()

        try:
            clock= pygame.time.Clock()
            self._display_surface((570, 730))
            self.color_amount= 255
            self.delay= 0
            self._switch= False
            self._delay_switch= False

            pygame.display.set_caption('Columns- Xinchen Zhang')
            self._launch_game()
             
            while self._running:
                clock.tick(90)
                
                self._draw()       
                self._handle_events()
                
        finally:       
            pygame.quit()

    '''
    The function used to control all the drawings
    in self.surface
    '''

    def _draw(self)-> None:
        if self._game_begin== False:
            self.surface.fill(WHITE)
            self._display_init_ui()

        else:
            if self._delay(0.03):
                self.surface.fill(WHITE)

                self._run_game()               
                self._draw_infoBoard()
                self._draw_frames()                   
                #self._DEBUG()
                if self.game.game_state== game_logic.OVER:
                    self._draw_game_over()
            
        pygame.display.flip()
        

    '''
    Functions used to handle events
    '''
        
    def _handle_events(self)-> None:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                self._stop_game()

            elif event.type== pygame.VIDEORESIZE:
                self._display_surface(event.size)

            elif event.type== pygame.MOUSEBUTTONDOWN:
                self._mouse_button_down(event.pos)

            elif event.type== pygame.KEYDOWN:
                self._key_down()
                self._start_game()
                

    def _mouse_button_down(self, pos: (int, int))-> None:
        pass
    

    def _key_down(self)-> None:
        if self._game_begin== True and self.game.game_state!= game_logic.OVER\
           and self._column!= -1:
            key= pygame.key.get_pressed()

            if self.game.game_state!= game_logic.FREEZE:
                if key[pygame.K_LEFT]:
                    if self.game.game_state!= game_logic.MATCH:
                        if self.game.move_to_left(self._column-1, self._faller):
                            self._column-= 1
                            self.surface.fill(WHITE)
                            
                            self._redraw_everything()

                if key[pygame.K_RIGHT]:
                    if self.game.game_state!= game_logic.MATCH:
                        if self.game.move_to_right(self._column+1, self._faller):
                            self._column+= 1
                            self.surface.fill(WHITE)

                            self._redraw_everything()
                      
                if key[pygame.K_SPACE] or key[pygame.K_DOWN]:
                    if self.game.game_state!= game_logic.MATCH:
                        self.game.rotate(self._column)
                        
                        self._redraw_everything()

            if key[pygame.K_F1]:
                self._pause_game()
                

    '''
    Functions used to control any other displays aside from
    the main game part
    '''
                
                
    def _display_surface(self, size: (int, int))-> None:
        self.surface= pygame.display.set_mode(size, pygame.RESIZABLE)
  
    def _display_init_ui(self)-> None:
        # Display title picture, name picture and the initial caption
        self._display_game_pic()
        self._display_name_pic()
        self._draw_init_caption()
        
    
    def _display_game_pic(self)-> None:
        # Display the picture "COLUMNS"
        try:
            title_pic= pygame.image.load((str(Path.cwd())+ '\\columns.png'))

        except:
            title_pic= pygame.image.load('C:\\Program Files\\Columns by Cyan\\columns.png')

        
        title_pic_width= title_pic.get_width()

        left= self.scale.scale_x(title_pic_width,
                                 self.surface.get_width(), 2)
        top= self.scale.frac_to_pixel(
            self.picture.get_title_pic_height(), self.surface.get_height())
        
        self.surface.blit(title_pic, (left, top))


    def _display_name_pic(self)-> None:
        # Display the picture "name"
        try:
            name_pic= pygame.image.load((str(Path.cwd())+ '\\name.png'))

        except:
            name_pic= pygame.image.load('C:\\Program Files\\Columns by Cyan\\name.png')
        
        name_pic_width= name_pic.get_width()

        _height_left= self.surface.get_height()*\
                      (1- self.picture.get_title_pic_height())

        left= self.scale.scale_x(name_pic_width,
                                 self.surface.get_width(), 2)
        top= self.scale.frac_to_pixel(
            self.picture.get_name_pic_height(),_height_left)
        
        self.surface.blit(name_pic, (left, top))
        
        
    def _draw_init_caption(self)-> None:
        init_text= 'Press any key to start'
        color_amount= self._tick()
        
        font= pygame.font.SysFont(FONT, 35)
        caption= font.render(init_text, True, pygame.Color(
            color_amount, color_amount, color_amount))

        font_width, font_height= font.size(init_text)

        left= self.scale.scale_x(font_width, self.surface.get_width(), 2)
        top= self.surface.get_height()- font_height

        self.surface.blit(caption, (left, top))

    def _tick(self)-> int:        
        # return the delta value for color change
        if self._switch== False:
            self.color_amount-= 5

            if self.color_amount== 0:
                self._switch= True

        else:          
            self.color_amount+= 5

            if self.color_amount== 255:      
                self._switch= False

        return self.color_amount

    def _delay(self, time: float)-> bool:
        # And later I found out there is a method in pygame called
        # pygame.time.delay()
        # Too late :(
        if self._delay_switch== False:
            self.delay+= time

            if int(self.delay)== 1:
                self._delay_switch= True

        else:
            self.delay=0
            self._delay_switch= False

        return self._delay_switch
    

    '''
    Functions used to deal with the game state
    (start or end the game, start or end the
    whole program)
    '''
    

    def _stop_game(self)-> None:
        self._running= False
        
    def _start_game(self)-> None:
        if self._game_begin== False:
            self._game_begin= True
            self.surface.fill(pygame.Color(255, 255, 255))
            self._switch= False
            self.color_amount= 255

    def _pause_game(self)-> None:
        if self._pause== True:
            self._pause= False

        else:
            self._pause= True
            

    '''
    Functions used to draw the main part of the game
    (generate faller, display matching effect and so on)
    '''

    def _launch_game(self)-> None:
        # Initialize the field in game_logic
        self.game.initialize_field(13, 6)
        self.game.start()

        self._faller_created= False
        
    def _run_game(self)-> None:
        if self._pause== False:
            if self.game.game_state!= game_logic.START:
                if self._faller_created== False:
                    self._randomize_faller()
                    self._faller_created= True
            
            if self.game.game_state== game_logic.START:
                self._randomize_faller()
                self._get_faller()
                self._generate_faller()

            elif self.game.game_state== game_logic.FREEZE:
                self._faller_created= False
                self._get_faller()
                self._generate_faller()

            elif self.game.game_state== game_logic.FALL:
                self._fall(self._column)
                self.game.land()

            elif self.game.game_state== game_logic.LAND:
                self._score+= 10
            
                self.game.freeze()

            elif self.game.game_state== game_logic.MATCH:
                for n in range(len(self.game.matchIndex)):
                    self._score+= 10
                
                self.game.disappear()
                self.game.gravitate()
                self.game.freeze()

            self._draw_field()

        else:
            self._draw_field()
                    
    def _generate_faller(self)-> None:
        self.game.get_faller(self._faller)
        self._fall(self._column)

        self.game.land()

    def _randomize_faller(self)-> None:
        jewels= ['R', 'G', 'B', 'Y', 'PI', 'C', 'PU']
        faller= []
        
        column= round(random.random()* 4.5)

        for n in range(3):
            _random_jewel_index= round(random.random()* 6)
            faller.append(jewels[_random_jewel_index])

        self._next_faller= faller
        self._next_column= column

    def _get_faller(self)-> None:
        self._faller= self._next_faller
        self._column= self._next_column

    def _fall(self, column: int):
        self.game.fall(column)
        self.game.generate_field(column)

    def _draw_field(self)-> None:      
        field= self.game.field
        data= []
      
        for i in range(len(field)):          
            for j in range(len(field[i])):
                if field[i][j]== 'R':
                    data.append((i, j, 'R'))

                elif field[i][j]== 'G':
                    data.append((i, j, 'G'))

                elif field[i][j]== 'B':
                    data.append((i, j, 'B'))

                elif field[i][j]== 'Y':
                    data.append((i, j, 'Y'))

                elif field[i][j]== 'C':
                    data.append((i, j, 'C'))

                elif field[i][j]== 'PI':
                    data.append((i, j, 'PI'))

                elif field[i][j]== 'PU':
                    data.append((i, j, 'PU'))

                if data!= []:
                    _row= data[0][0]
                    _column= data[0][1]
                    _color= data[0][2]
                    
                    if self.game.game_state== game_logic.MATCH:
                        if (_row, _column) in self.game.matchIndex:
                            self._draw_match_effect(_row, _column, _color)
                            
                        else:
                            self._draw_commonly(_row, _column, _color)                    

                    else:
                        self._draw_commonly(_row, _column, _color)
                        
                    data= []
           

    def _determine_pos(self, row_in_field: int, column_in_field: int)-> [()]:
        '''
        /\
        ||
        \/
        '''

        jewel_radius= round(self.surface.get_height()/ 26)
        jewel_diam= jewel_radius* 2

        _infoBoard_width= self.scale.frac_to_pixel(
            self.picture.get_infoBoard_width(), self.surface.get_width())

        jewel_width= (self.surface.get_width()- _infoBoard_width)/ 6
        half_width= jewel_width/ 2

        _left= _infoBoard_width+ jewel_width* column_in_field
        _top= jewel_diam* row_in_field

        _top_vertice= (_left+ half_width, _top)
        _left_top_vertice= (_left, _top+ jewel_diam/ 4)
        _left_bott_vertice= (_left, _top+ (jewel_diam/ 4)* 3)
        _right_top_vertice= (_left+ jewel_width, _top+ jewel_diam/ 4)
        _right_bott_vertice= (_left+ jewel_width, _top+ (jewel_diam/ 4)* 3)
        _bott_vertice= (_left+ half_width, _top+ jewel_diam)

        point_list= [_top_vertice, _left_top_vertice, _left_bott_vertice,
                     _bott_vertice, _right_bott_vertice, _right_top_vertice]

        return point_list
        

        '''
        left= round(self.scale.frac_to_pixel(
            self.picture.get_infoBoard_width(), self.surface.get_width())+\
            (jewel_radius+ (jewel_diam* column_in_field)))

        top= round(jewel_diam* (row_in_field)+ jewel_radius)

        return left, top, jewel_radius
        '''
    

    def _draw_jewel(self, point_list: [], color)-> None:
        if type(color)== str:
            _color= self._parse_color(color)

        else:
            _color= color
      
        pygame.draw.polygon(self.surface, _color, point_list)
        

    def _draw_match_effect(self, _row: int, _column: int, _color: str)-> None:        
        point_list= self._determine_pos(
            _row, _column)
        
        self._draw_jewel(point_list, 'D')

        if self._delay(0.05):
            self._draw_jewel(point_list, _color)

    def _draw_commonly(self, _row: int, _column: int, color: str)-> None:
        point_list= self._determine_pos(
            _row, _column)
        self._draw_jewel(point_list, color)
        

    def _redraw_everything(self)-> None:
        self._draw_field()
        self._draw_infoBoard()
        self._draw_frames()

    def _parse_color(self, color: str)-> pygame.Color:
        if color== 'R':
            _color= RED

        elif color== 'G':
            _color= GREEN

        elif color== 'B':
            _color= BLUE

        elif color== 'Y':
            _color= YELLOW

        elif color== 'PI':
            _color= PINK

        elif color== 'C':
            _color= CYAN

        elif color== 'PU':
            _color= PURPLE

        elif color== 'W':
            _color= WHITE

        elif color== 'D':
            _color= DARK

        return _color
      

    '''
    Functions that draw the info board
    '''

    def _draw_infoBoard(self)-> None:
        left, font_height, number_height, number_left= self._display_score()
        bott_top= self._display_next_faller(left, font_height, number_height, number_left)
        self._display_desc(left, bott_top)

    def _display_score(self):
        font_width, font_height, left, top= self._display_score_caption()
        number_height, number_left= self._display_score_number(font_width, font_height, left, top)

        return left, font_height, number_height, number_left

    def _display_score_caption(self):
        text= 'SOCRE'
        
        _font, _caption= self._generate_font(
            FONT, 20, text, True, DARK)   

        font_width, font_height= _font.size(text)

        left= self.scale.frac_to_pixel(
            self.picture.get_score_caption_left(), self.surface.get_width())
        top= self.scale.frac_to_pixel(
            self.picture.get_score_caption_top(), self.surface.get_height())

        self.surface.blit(_caption, (left, top))

        return font_width, font_height, left, top
        

    def _display_score_number(self, font_width: float, font_height: float, left:float, top:float):       
        score= str(self._score)

        _font, _caption= self._generate_font(
            FONT, 20, score, True, DARK)
        
        _width, _height= _font.size(score)

        _left= self.scale.frac_to_pixel(
            self.picture.get_score_number_scale(), left+ font_width)
        _top= top+ font_height

        self.surface.blit(_caption, (_left, _top))

        return _height, _left

    def _display_next_faller(self, left, font_height, number_height, number_left):
        caption_width, caption_top= self._display_next_faller_caption(left, font_height, number_height)
        bott_top= self._display_next_faller_graph(
            caption_width, number_left, caption_top)

        return bott_top

    def _display_next_faller_caption(self, left, font_height, number_height):        
        text= 'NEXT'
        _font, _caption= self._generate_font(
            FONT, 20, text, True, DARK)

        _width, _height= _font.size(text)

        _left= left
        _top= font_height+ number_height+ self.picture.get_space_distance()

        self.surface.blit(_caption, (_left, _top))

        return _height, _top

    def _display_next_faller_graph(self, caption_height, number_left, caption_top):
        n= 0
        
        for _color in self._next_faller:          
            jewel_radius= round(self.surface.get_height()/ 26)
            jewel_diam= jewel_radius* 2

            _distance= n* jewel_diam
            n+= 1
            
            _infoBoard_width= self.scale.frac_to_pixel(
                self.picture.get_infoBoard_width(), self.surface.get_width())

            jewel_width= (self.surface.get_width()- _infoBoard_width)/ 6
            half_width= jewel_width/ 2

            _left= number_left+ half_width
            _top= caption_top+ caption_height

            _top_vertice= (_left, _top+ _distance)
            _left_top_vertice= (_left- half_width, _top+ jewel_diam/ 4+ _distance)
            _left_bott_vertice= (_left- half_width, _top+ (jewel_diam/ 4)* 3+ _distance)
            _right_top_vertice= (_left+ half_width, _top+ jewel_diam/ 4+ _distance)
            _right_bott_vertice= (_left+ half_width, _top+ (jewel_diam/ 4)* 3+ _distance)
            _bott_vertice= (_left, _top+ jewel_diam+ _distance)

            point_list= [_left_top_vertice, _top_vertice, _right_top_vertice, _right_bott_vertice, _bott_vertice, _left_bott_vertice]

            self._draw_jewel(point_list, _color)

        return _bott_vertice[1]

    def _display_desc(self, left, bott_top):
        arrow_height= self._display_ARROW(left, bott_top)
        space_height= self._display_SPACE(left, arrow_height, bott_top)
        self._display_F1(left, arrow_height, space_height, bott_top)

    def _display_ARROW(self, left, bott_top):
        # left_... refers to properities of the left arrow. Same story as right_...
        left_text= '<- MOVE LEFT'
        right_text= '-> MOVE RIGHT'

        left_top= bott_top+ self.picture.get_space_distance()

        left_font, left_caption= self._generate_font(
            FONT, 17, left_text, True, DARK)

        self.surface.blit(
            left_caption, (left, left_top))

        left_width, left_height= left_font.size(left_text)

        right_font, right_caption= self._generate_font(
            FONT, 17, right_text, True, DARK)

        self.surface.blit(
            right_caption, (left, left_top+ left_height))

        arrow_height= left_height

        return arrow_height

    def _display_SPACE(self, left, arrow_height, bott_top):
        text= '|__| ROTATE'
        
        _font, _caption= self._generate_font(
            FONT, 17, text, True, DARK)

        _left= left
        _top= arrow_height* 2+ bott_top+\
              self.picture.get_space_distance()

        self.surface.blit(_caption, (_left, _top))
        
        space_width, space_height= _font.size(text)

        return space_height

    def _display_F1(self, left, arrow_height, space_height, bott_top):
        text= 'F1 PAUSE'

        _font, _caption= self._generate_font(
            FONT, 17, text, True, DARK)

        _left= left
        _top= arrow_height* 2+ bott_top+\
              self.picture.get_space_distance()+\
              space_height

        self.surface.blit(_caption, (_left, _top))

   
    '''
    Functions that draw the frames
    '''

    def _draw_frames(self)-> None:
        self._draw_grid(GREY)
        infoBoard_width, infoBoard_height= self._draw_infoBoard_frame()
        self._draw_gameField_frame(infoBoard_width, infoBoard_height)

        if self.game.game_state== game_logic.LAND:
            self._draw_land_effect()

    def _draw_infoBoard_frame(self)-> ('width', 'height'):
        width= self.scale.frac_to_pixel(
            self.picture.get_infoBoard_width(), self.surface.get_width())

        height= self.scale.frac_to_pixel(
            self.picture.get_infoBoard_height(), self.surface.get_height())
        
        infoBoard_frame= pygame.Rect(0, 0, width, height)
       
        pygame.draw.rect(self.surface, DARK, infoBoard_frame, 1)

        return width, height
        
    def _draw_gameField_frame(self, infoBoard_width, infoBoard_height)-> None:
        width= self.surface.get_width()- infoBoard_width
        height= infoBoard_height

        gameField_frame= pygame.Rect(infoBoard_width, 0, width, height)

        pygame.draw.rect(self.surface, DARK, gameField_frame, 1)

    def _draw_grid(self, color: pygame.Color)-> None:
        for i in range(len(self.game.field)):
            for j in range(len(self.game.field[i])):
                _point_list= self._determine_pos(i, j)
                pygame.draw.polygon(self.surface, color, _point_list, 1)

    def _draw_land_effect(self):
        for _row in self.game._faller_index:
            _point_list= self._determine_pos(_row, self._column)
            pygame.draw.polygon(self.surface, DARK, _point_list, 1)
                

    '''
    Functions that draw game over prompt
    '''

    def _draw_game_over(self):
        text= 'GAME OVER'
        
        font= pygame.font.SysFont(FONT, 35, True)
        caption= font.render(text, True, DARK)

        font_width, font_height= font.size(text)

        _infoBoard_width= self.scale.frac_to_pixel(
            self.picture.get_infoBoard_width(),
            self.surface.get_width())

        _distance= (self.surface.get_width()- _infoBoard_width- font_width)/ 2
            
        left= _infoBoard_width+ _distance
        top= self.surface.get_height()/ 2- font_height/ 2

        self.surface.blit(caption, (left, top))

    '''
    Functions that deal with fonts
    '''

    def _generate_font(self, font: pygame.font, size: int, text: str, ifBold: bool, color: pygame.Color)-> (pygame.font, pygame.Surface):
        _shrink= self._font_shrink()
        
        _font= pygame.font.SysFont(font, size- _shrink, ifBold)
        _caption= _font.render(text, True, color)

        return _font, _caption       
                       

    def _font_shrink(self)-> int:
        _shrink= round(
            self.picture.get_font_shrink_rate()*\
            (DEFAULT_WINDOW_WIDTH- self.surface.get_width()))

        return _shrink

    '''
    DEBUG
    '''
        

    def _DEBUG(self):
        for i in range(len(self.game.field)):
            print()
            for j in range(len(self.game.field[i])):
                print(self.game.field[i][j], end='')

        print('Game state: {}'.format(self.game.game_state))
        


'''
The class used to deal with scale transformation
'''

class ToScale:
    def scale_x(self, x: int, whose_scale: int, ratio: float)-> float:
        return (whose_scale- x)/ ratio

    def frac_to_pixel(self, frac: float, pixel: int)-> int:
        return frac* pixel

    
'''
The class used to keep track of the appropriate scales
'''

class Picture:
    # The class used to adjust the scale of pictures
    
    def get_title_pic_height(self)-> float:
        return 0.3

    def get_name_pic_height(self)-> float:
        return 0.7
    
    def get_infoBoard_width(self)-> float:
        return 0.3

    def get_infoBoard_height(self)-> float:
        return 1.0

    def get_score_caption_left(self)-> float:
        return 0.005

    def get_score_caption_top(self)-> float:
        return 0.05

    def get_score_number_scale(self)-> float:
        return 0.7

    def get_space_distance(self)-> int:
        return 100

    def get_infoBoard_inBetween_distance(self)-> int:
        return 30

    def get_font_shrink_rate(self)-> float:
        return 0.02


        

if __name__== '__main__':
    GameInterface().run()
