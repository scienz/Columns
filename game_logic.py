# Xinchen Zhang
# 25702388

'''
Algorithm (maybe) completely fixed on 13 March, 2018
'''

# Constants used to determine the game state

START= -1
FALL= 0
LAND= 1
FREEZE= 2
MATCH= 3
OVER= 4

class Game:
    def __init__(self):
        self.game_state= START
        self.field= []

        self._faller_index= [-3, -2, -1]
        self._faller_column= -1
        self._faller= []

        self.jewelIndex= set()
        self.matchIndex= set()
        self._further_match_list= []

    def initialize_field(self, row: int, column: int)->[[], [], ...]:
        # The general function used to create a two-dimensional list
        # filled with empty spaces for further usage

        self._get_row(row)
        self._get_column(column)

        for i in range(row):
            list_in_a_row= []

            for j in range(column):
                list_in_a_row.append(' ')

            self.field.append(list_in_a_row)

        self._row_filled= len(self.field)

        return self.field

    def gravitate(self)-> [[], [], ...]:
        # The function that let jewels drop when they matched or
        # when the user input says 'CONTENTS'

        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if self.field[i][j]== ' ':

                    for n in range(i):
                        self.field[i-n][j]= self.field[i-n-1][j]
                        self.field[i-n-1][j]= ' '

        self._grav_remaining_jewels()

        return self.field

    def generate_field(self, column: int):
        faller= self._faller
        self.jewelIndex= set()

        for n in range(len(self._faller_index)):
            _row_to_fall= self._faller_index[n]

            if _row_to_fall>= 0:
                _jewel= faller[n]
                
                self.jewelIndex.add((_row_to_fall, column))

                self.field[_row_to_fall][column]= _jewel

        # Eraser
        if self._faller_index[0]> 0:
            for n in range(self._faller_index[0]):
                self.field[n][column]= ' '
                

    def start(self)-> None:
        self._posi_pairs= self._check_position()

    def fall(self, column: int)-> None:
        # Deal with the index of the faller
        self.game_state= FALL
        self._faller_column= column

        self._get_row_filled()

        for n in range(len(self._faller_index)):
            if((self._faller_index[2]+ 1)< self._row_filled):
                
                self._faller_index[n]+= 1


    def land(self)-> None:
        if self._isLand():    
            self.game_state= LAND
   
        # Leave for the user interface to judge the match
        
    def freeze(self)-> None:          
        if self.match(self.field)== False:
            if self.game_over(False):
                self.game_state= OVER
                
            else:            
                self.game_state= FREEZE
                
                self._faller_index= [-3, -2, -1]
                self._row_filled= len(self.field)
                
                self._posi_pairs= self._check_position()


    def match(self, field)-> bool:
        # Judge whether a match occurs
        _isMatch= self._isMatch()

        if _isMatch:
            self.game_state= MATCH

        return _isMatch

        # else:
        #   whether it should freeze or not should be left for the
        #   user interface to decide

    def disappear(self)-> 'field':
        # The disappearance of the matched jewels
        for indexPair in self.matchIndex:
            _row= indexPair[0]
            _column= indexPair[1]

            self.field[_row][_column]= ' '
            self.matchIndex= set()


    def rotate(self, column: int)-> None:
        # Rotate the faller
        _last_jewel_index= len(self._faller)- 1
        _original_faller= self._faller
        
        _rotated_faller= [_original_faller[_last_jewel_index]]     
        _rotated_faller.append(_original_faller[0])
        _rotated_faller.append(_original_faller[1])

        self._faller= _rotated_faller

        self.generate_field(column)

    
    def move_to_left(self, column, faller)-> bool:
        _moved= False
        
        if self._check_if_can_move(column, 'LEFT'):
            self._faller_column= column   
            self.generate_field(column)

            self._clean('LEFT')

            _moved= True
 
            self.game_state= FALL
            self.land()          
            
        return _moved

        
    def move_to_right(self, column, faller)-> bool:
        _moved= False
        
        if self._check_if_can_move(column, 'RIGHT'):
            self._faller_column= column
            self.generate_field(column)

            self._clean('RIGHT')

            _moved= True
     
            self.game_state= FALL
            self.land()

        return _moved

    def get_faller(self, faller: []):
        self._faller= faller
    
    def game_over(self, force_quit: bool)-> bool:
        _isOver= False
        
        if force_quit:
            self.game_state= OVER

        else:
            if self._check_game_over():
                _isOver= True
                
                return _isOver

    '''
    The following are private functions
    '''

    def _isLand(self)-> bool:
        # See whether the faller has landed or not
        self._get_row_filled()
       
        if (self._faller_index[2]+1)== self._row_filled:
            return True
        else:
            return False

    def _isMatch(self)-> bool:
        # See whether the faller gets a match or matches
        _isMatch= False

        _isRowMatch= self.__isRowMatch(self.field)
        _isColumnMatch= self.__isColumnMatch(self.field)
        _isDiagonalMatch= self.__isDiagonalMatch(self.field)

        if (_isRowMatch or _isColumnMatch or _isDiagonalMatch):
            _isMatch= True

        return _isMatch

    def _get_row(self, row: int)-> None:
        # Get the row number for the field
        # Row number should be no less than 4

        if row>= 4:
            self._row= row

        else:
            raise RowNumberError

    def _get_column(self, column: int)-> None:
        # Get the column number for the field
        # Column number should be no less than 3

        if column>= 3:
            self._column= column

        else:
            raise ColumnNumberError

    # God damn bugs!!!
    # My project4 score is lowered because of you three stupid functions!!!!
    
    def __isRowMatch(self, field)-> bool:
        _isMatch= False

        for i in range(len(field)):
            for j in range(len(field[i])):
                if (j+1)!= len(field[i]) and (j-1)>= 0:
                    if field[i][j]== field[i][j+1] and field[i][j]== field[i][j-1]:
                        if field[i][j]!= ' ':
                            self.matchIndex.add((i, j-1))
                            self.matchIndex.add((i, j))
                            self.matchIndex.add((i, j+1))

                            self._check_row_further_matches(field, i, j+1)

                            if self._further_match_list!= []:
                                for column in self._further_match_list:
                                    self.matchIndex.add((i, column))

                                self._further_match_list= []

                            _isMatch= True
                            break

        return _isMatch

    def __isColumnMatch(self, field)-> bool:
        _isMatch= False

        for j in range(len(field[0])):
            for i in range(len(field)):
                if (i+ 1)!= len(field) and (i-1)>= 0:
                    if field[i][j]== field[i+1][j] and field[i][j]== field[i-1][j]:
                        if field[i][j]!= ' ':           
                            self.matchIndex.add((i-1, j))
                            self.matchIndex.add((i, j))
                            self.matchIndex.add((i+1, j))

                            self._check_column_further_matches(field, i+1, j)
                    
                            if self._further_match_list!= []:
                                for row in self._further_match_list:
                                    self.matchIndex.add((row, j))

                                self._further_match_list= []
              
                            _isMatch= True
                            break

        return _isMatch

    def __isDiagonalMatch(self, field)-> bool:
        _isMatch= False

        for i in range(len(field)):

            for j in range(len(field[i])):
                if (i-1)>= 0 and (i+1)< len(field) and (j-1)>= 0 and (j+1)< len(field[0]):

                    if ((field[i][j]== field[i-1][j-1] and field[i][j]== field[i+1][j+1]) or
                    (field[i][j]== field[i-1][j+1] and field[i][j]== field[i+1][j-1])):

                        if field[i][j]!= ' ':

                            if (field[i][j]== field[i-1][j-1] and field[i][j]== field[i+1][j+1]):
                                self.matchIndex.add((i, j))
                                self.matchIndex.add((i-1, j-1))
                                self.matchIndex.add((i+1, j+1))

                                self._check_diag_further_matches(field, i+1, j+1)

                                if self._further_match_list!= []:
                                    for pairs in self._further_match_list:
                                            self.matchIndex.add((pairs[0], pairs[1]))

                                self._further_match_list= []

                            if (field[i][j]== field[i-1][j+1] and field[i][j]== field[i+1][j-1]):
                                self.matchIndex.add((i,j))
                                self.matchIndex.add((i-1, j+1))
                                self.matchIndex.add((i+1, j-1))

                                self._check_diag_further_matches(field, i+1, j-1)

                                if self._further_match_list!= []:
                                    for pairs in self._further_match_list:
                                            self.matchIndex.add((pairs[0], pairs[1]))

                                self._further_match_list= []

                            
                            

                            _isMatch= True
                            break

        return _isMatch

    def _check_row_further_matches(self, field, _row: int, _last_matching_column: int)-> None:
        if ((len(field[0])- 1)- _last_matching_column)> 0:
            if field[_row][_last_matching_column]== field[_row][_last_matching_column+ 1]:
                self._further_match_list.append(_last_matching_column+ 1)
                
                self._check_row_further_matches(field, _row, _last_matching_column+ 1)

            else:         
                return

        else:
            return
                              

    def _check_column_further_matches(self, field, _last_matching_row: int, _column: int)-> None:
        if ((len(field)- 1)- _last_matching_row)> 0:
            if field[_last_matching_row][_column]== field[_last_matching_row+ 1][_column]:
                self._further_match_list.append(_last_matching_row+ 1)
                
                self._check_column_further_matches(field, _last_matching_row+ 1, _column)

            else:            
                return

        else:
            return
        

    def _check_diag_further_matches(self, field, _last_matching_row: int,
                                    _last_matching_column: int)-> []:

        if ((len(field[0])- 1)- _last_matching_column)> 0 and ((len(field)- 1)- _last_matching_row)> 0:
            if field[_last_matching_row][_last_matching_column]==\
               field[_last_matching_row+ 1][_last_matching_column+ 1]:
                self._further_match_list.append((_last_matching_row+ 1, _last_matching_column+ 1))

                self._check_column_further_matches(field, _last_matching_row+ 1,
                                                   _last_matching_column+ 1)

            else:
                return

        else:
            return
        


    def _check_position(self)-> list:
        # Go through self.field and see wether a certain
        # place is filled with a jewel(jewels) for landing
        # and moving purposes.
        #
        # Returns a list of row and column pairs.
        #
        # row: the highest position of the jewel
        # column: in which column does this jewel lies
        _pair_list= []

        for j in range(len(self.field[0])):
            for i in range(len(self.field)):
                if self.field[i][j]!= ' ':
                    _pair_list.append((i, j))
                    break

        return _pair_list
    
        
    def _get_row_filled(self)-> None:
        self._row_filled= len(self.field)
        
        for pairs in self._posi_pairs:
            _row, _column= pairs

            if _column== self._faller_column:
                self._row_filled= _row
                

    def _check_remains(self)-> bool:
        # check whether there are some remaining jewels
        # i.e., some jewels are displayed and some are not
        _wasDisplayed= False
        _notDisplayed= False

        for index in self._faller_index:
            if index<= -1:
                _notDisplayed= True

            elif index>= 0:
                _wasDisplayed= True

        if ((_wasDisplayed== True) and (_notDisplayed== True)):
            # Then the match must have been trigger by the faller
            return True
        else:
            return False

    def _check_none(self)-> bool:
        # Check whether all faller jewels are not displayed
        _notDisplayed= True

        for index in self._faller_index:
            if index> -1:
                _notDisplayed= False

        return _notDisplayed

    
    def _grav_remaining_jewels(self)-> None:
        # Since this function is called by self.gravitate(),
        # the game state can be assumed to be MATCH
        self._posi_pairs= self._check_position()
        self._get_row_filled()
        _substract= 0
        
        if self._check_remains() and self._faller!= []:
            
            for n in range(len(self._faller_index)):
                _row_to_fall= self._faller_index[n]

                if _row_to_fall< -1:
                    _substract+= 1
                    
                    self.field[self._row_filled- _substract][self._faller_column]=\
                        self._faller[1-n]
                    
        self._posi_pairs= self._check_position()

    def _clean(self, direction: str)-> None:
        # Clean up the mess left when moving a faller to left or right
        
        for indexPair in self.jewelIndex:
            _row_to_clean, _column= indexPair

            if direction== 'LEFT':
                _column_to_clean= _column+ 1
                
            else:
                _column_to_clean= _column- 1

            self.field[_row_to_clean][_column_to_clean]= ' '
            

    def _check_if_can_move(self, column, direction: str)-> bool:
        _can_move= False
       
        if direction== 'LEFT':
            _column_delta= -1

        else:
            _column_delta= 1

        if column>= 0 and column<= len(self.field[0])-1:
            if self._posi_pairs== []:
                _can_move= True

            else:
                _next_posi= (
                    self._faller_index[2], self._faller_column+ _column_delta)
                                    
                for posiPairs in self._posi_pairs:
                    
                    if _next_posi!= posiPairs:
                        if _next_posi[1]== posiPairs[1]:
                            
                            if posiPairs[0]> _next_posi[0]:       
                                _can_move= True

                            else:
                                _can_move= False
                                break

                        else:       
                            _can_move= True

                    else:
                        _can_move= False
                        break

        if _can_move:
            self._faller_column= column

        return _can_move

    def _check_game_over(self):        
        if self._check_remains() or self._check_none():
            return True
        else:
            return False
        

'''
The following classes are exceptions designed for this game
'''

class RowNumberError(Exception):
    # Raise when the number of rows is illegal
    pass

class ColumnNumberError(Exception):
    # Raise when the number of columns is illegal
    pass
