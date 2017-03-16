'''		typing_game.py
               by Justin Dowell
   =============================

   classes:
      Action_Board_Class
      Action_Class
      Word_Class

   other methods:
      Set_Font_Size
      main     -     -     -     sample game 1  doesn't use action stuff
      main_two -     -     -     sample game 2  uses action stuff
'''


# imports
#--------------------------------------------
from __future__ import print_function

import copy, pygame, random, string, sys
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

'''   Here's where you can alter colors easily
         colors - string value of the color:( red, green, blue )
         then as easy as changing string value for bg_color, matched_color, unmatched_color, and action_color
'''
# some shared initial values
#--------------------------------------------
pygame.init()		# initialize pygame
# format of colors = { 'color_name': ( R, G, B ) }
colors = { 'black': ( 0, 0, 0 ), 'blue': ( 0, 0, 200 ), 'green': ( 0, 200, 0 ), 'gray': ( 30, 30, 30 ), 'orange': ( 255, 165, 0 ), 'red': ( 200, 0, 0 ), 'white': ( 255, 255, 255 ), 'yellow': ( 255, 255, 0 ) }
word_coords = [ 50, 50 ]
bg_color = colors.get( 'black' )
matched_color = colors.get( 'blue' )
unmatched_color = colors.get( 'green' )
action_color = colors.get( 'orange' )
reward_points_multiplier = 25
reward_timer_multiplier = 1
reward_points = 0
reward_timer = 0
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# some font functionality
#--------------------------------------------
font_size_dict = { 25:[ 15, 26 ], 30:[ 18, 31 ], 38:[ 23, 39 ], 42:[ 25, 43] }
font = pygame.font.Font( './FreeMonoBold.ttf', 42 )         # initialize font
font_width = font_size_dict[ 42 ][ 0 ]
font_height = font_size_dict[ 42 ][ 1 ]
def Set_Font_Size( size ):
   global font
   global font_width
   global font_height
   if size in font_size_dict.keys():
      print( "changing font size")
      font = pygame.font.Font( './FreeMonoBold.ttf', size )         # initialize font
      font_width = font_size_dict[ size ][ 0 ]
      font_height = font_size_dict[ size ][ 1 ]
   else:
      pass

# load in dictionaries
''' note all_words is a property of interface.py
   rewards, timer, score within my test game refernces this, if you need ideas '''
#--------------------------------------------
f = open( 'dictionary.txt', 'r' )
r = f.read()
all_words = string.split( r, sep='\n' )
random.shuffle( all_words )
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Action_Board_Class
#---------------------
#  Action_Board_Class( action_string_list )
#     due to font size, action_string_list is expected to have fewer than 7 items
#  Draw_Surface() is used privately
#  update( letter ) letter in string format ( key pressed by player )
#     returns None until a word is completed
#     returns name of action when word is completed as string
#--------------------------------------------
class Action_Board_Class:
   # Action_Board_Class __init__()
   #-----------------------------------------
   def __init__( self, action_string_list ):
      self.bg_surface_size = ( 800, 200 )
      self.bg_surface_obj = pygame.Surface( self.bg_surface_size )
      self.bg_surface_obj = self.bg_surface_obj.convert()
      self.action_string_list = []
      self.actions_dict = {}
      # set font size based on number of actions for comfortable fit
      # note, all font size in game testing below will be affected, but not outside of module
      if len( action_string_list ) <= 4:
         Set_Font_Size( 42 )
      elif len( action_string_list ) == 5:
         Set_Font_Size( 38 )
      elif len( action_string_list ) == 6:
         Set_Font_Size( 30 )
      elif len( action_string_list ) == 7:
         Set_Font_Size( 25 )
      else:
         return None    # too many actions
      # create action objects for each action in list
      for action in action_string_list:
         self.actions_dict[ action ] = Action_Class( action )
      self.action_string_list = list( self.actions_dict.keys() )
      self.Draw_Surface()
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   # Action_Board_Class Draw_Surface()
   #-----------------------------------------
   def Draw_Surface( self ):
      self.bg_surface_obj.fill( bg_color )
      i = 1
      for action_object in self.actions_dict.values():
         temp_rect_obj = action_object.bg_surface_obj.get_rect()
         temp_rect_obj.left = 100
         temp_rect_obj.top = i
         i += temp_rect_obj.height
         self.bg_surface_obj.blit( action_object.bg_surface_obj, temp_rect_obj )
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   # Action_Board_Class update()
   #-----------------------------------------
   def update( self, letter ):
      result_string = None
      for action_string in self.action_string_list:
         result = self.actions_dict[ action_string ].update( letter )
         self.Draw_Surface()
         if result == False:
            result_string = action_string
      if len( self.action_string_list ) == 0:
         self.action_string_list = list( self.actions_dict.keys() )
      return result_string
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Action_Class
#--------------------------------------------
class Action_Class:
   # Action_Class __init__()
   #-----------------------------------------
   def __init__( self, action_string ):
      self.word_incomplete = True
      # create action_id surface with appended ':'
      self.action_string = action_string
      self.action_word_value = string.upper( action_string ) + ": "
      self.action_word_surface = font.render( self.action_word_value, 1, action_color, bg_color )
      self.action_word_rect = self.action_word_surface.get_rect()
      # generate initial game_word
      self.New_Game_Word()
      self.Draw_Surface()
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   # Action_Class Draw_Surface()
   #-----------------------------------------
   def Draw_Surface( self ):
      self.bg_surface_size = ( self.action_word_rect.width + self.game_word_rect.width, font_height )
      self.bg_surface_obj = pygame.Surface( self.bg_surface_size )
      self.bg_surface_obj = self.bg_surface_obj.convert()
      self.bg_surface_obj.fill( bg_color )
      self.bg_surface_obj.blit( self.action_word_surface, self.action_word_rect )
      self.bg_surface_obj.blit( self.game_word_obj.bg_surface_obj, self.game_word_rect )
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   # Action_Class New_Game_Word()
   #-----------------------------------------
   def New_Game_Word( self ):
      self.game_word_obj = Word_Class( all_words.pop() )
      self.game_word_rect = self.game_word_obj.bg_surface_obj.get_rect()
      self.game_word_rect.left = self.action_word_rect.width
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   # Action_Class Update()
   #-----------------------------------------
   def update( self, letter ):
      result = self.game_word_obj.update( letter )
      self.Draw_Surface()
      if result == False:
         self.New_Game_Word()
         self.Draw_Surface()
      return result
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Word_Class
#--------------------------------------------
class Word_Class:
   # Word_Class __init__()
   #-----------------------------------------
   def __init__ ( self, word_string ):
      self.bg_surface_size = ( len(word_string) * font_width, font_height )
      self.bg_surface_obj = pygame.Surface( self.bg_surface_size )
      self.bg_surface_obj = self.bg_surface_obj.convert()
      self.bg_surface_obj.fill( bg_color )
      self.match_index = 0
      self.string_value = string.upper( word_string )
      self.letter_surface_list = []
      # generate list of letter surface objects for ease of modifying
      for letter in self.string_value:
         self.letter_surface_list.append( font.render( letter, 1, unmatched_color, bg_color ) )
      self.temp_rect_obj = self.letter_surface_list[ 0 ].get_rect()
      # place letter surface objects onto bg_surface_obj
      for i in xrange( len( self.string_value ) ):
         self.temp_rect_obj.left = ( i * font_width )
         self.bg_surface_obj.blit( self.letter_surface_list[ i ], self.temp_rect_obj )
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   # Word_Class update()
   #	returns false if complete, else true
   #-----------------------------------------
   def update( self, letter ):
      # if typed_letter matches word_letter at index
      if string.upper( letter ) == self.string_value[ self.match_index ]:
         self.letter_surface_list[ self.match_index ] = font.render( string.upper( letter ), 1, matched_color, bg_color )
         self.temp_rect_obj.left = ( self.match_index * font_width )
         self.bg_surface_obj.blit( self.letter_surface_list[ self.match_index ], self.temp_rect_obj )
         self.match_index = ( self.match_index + 1 )
      else:
         for i in xrange( 0, self.match_index ):
            self.letter_surface_list[ i ] = font.render( self.string_value[ i ] , 1, unmatched_color, bg_color )
            self.temp_rect_obj.left = ( i * font_width )
            self.bg_surface_obj.blit( self.letter_surface_list[ i ], self.temp_rect_obj )
         self.match_index = 0
      # check for word completion, return result
      if self.match_index == len( self.string_value ):
         return False
      else:
         return True
   #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# main()
#				simple typing game without-use-of( Action_Class, Action_Board_Class )
#--------------------------------------------
def main():
   # some initial values
   screen_size = ( 800, 600 ) 		# ( width, height )
   playing_game = True
   time_remains = True
   word_incomplete = True
   start = True
   game_over = False

   # initilize pygame screen
   screen = pygame.display.set_mode( screen_size )
   pygame.display.set_caption( "main() game testing" )

   background = pygame.Surface( screen.get_size() )
   background = background.convert()

   while playing_game:
      if not time_remains:			# game over, display score and choice of replay
         # TODO redesign to pull initialization out of loop
         game_over_message1 = "Congratulations!"
         game_over_message2 = "You scored " + str( score ) + " points."
         game_over_message3 = "Play again?"
         game_over_message_surface1 = font.render( game_over_message1, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         game_over_message_rect1 = game_over_message_surface1.get_rect()
         game_over_message_rect1.centerx = background.get_rect().centerx
         game_over_message_rect1.top = 149
         game_over_message_surface2 = font.render( game_over_message2, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         game_over_message_rect2 = game_over_message_surface2.get_rect()
         game_over_message_rect2.centerx = background.get_rect().centerx
         game_over_message_rect2.top = 224
         game_over_message_surface3 = font.render( game_over_message3, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         game_over_message_rect3 = game_over_message_surface3.get_rect()
         game_over_message_rect3.centerx = background.get_rect().centerx
         game_over_message_rect3.top = 299
         background.fill( colors.get( 'black' ) )
         background.blit( game_over_message_surface1, game_over_message_rect1 )
         background.blit( game_over_message_surface2, game_over_message_rect2 )
         background.blit( game_over_message_surface3, game_over_message_rect3 )
         screen.blit( background, ( 0, 0 ) )
         pygame.display.flip()
         while game_over:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  sys.exit()
               if event.type == pygame.KEYDOWN:
                  if pygame.key.name( event.key ) == 'n':
                     sys.exit()
                  if pygame.key.name( event.key ) == 'y':
                     start = True
                     time_remains = True
                     word_incomplete = True
                     game_over = False

      if start:				# some starting values
         score = 0
         seconds = 30
         timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
         timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
         timer_rect = timer_surface.get_rect()
         timer_rect.centerx = background.get_rect().centerx
         timer_rect.top = 35
         score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
         start = False

      # TODO create timer class to combine time operations
      if not word_incomplete:		# completed word, distribute rewards and update game
         score = score + reward_points
         score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         seconds = seconds + reward_timer
         timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
         timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
         word_incomplete = True

      # TODO make this into function
      # refresh background
      background.fill( colors.get( 'black' ) )
      background.blit( score_surface, ( 35, 35 ) )
      background.blit( timer_surface, timer_rect )
      screen.blit( background, ( 0, 0 ) )
      pygame.display.flip()

      if len( all_words ) == 0:			# if all_words is empty, exit game [349464]
         print( "Out of words!" )
         sys.exit()
      else:										# keep going, all_words is fine
      # rewards, timer, and score -------
         reward_points = reward_points_multiplier * len( all_words[ -1 ] )
         reward_timer = reward_timer_multiplier * len( all_words[ -1 ] )
      # randomly place word
         game_word = Word_Class( all_words.pop() )
         temp_rect_obj = game_word.bg_surface_obj.get_rect()
         temp_rect_obj.left = random.randint( 100, (750 - temp_rect_obj.width) )
         temp_rect_obj.top = random.randint( 200, 500 )
      # animation -+-+-+-
         background.blit( game_word.bg_surface_obj, temp_rect_obj )
         screen.blit( background, ( 0, 0 ) )
         pygame.display.flip()
         # while player is typing
         while word_incomplete and time_remains:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  sys.exit()
               if event.type == pygame.KEYDOWN:
                  # clear background
                  background.fill( colors.get( 'black' ) )
                  screen.blit( background, ( 0, 0 ) )
                  pygame.display.flip()
                  # check typed letter against word
                  word_incomplete = game_word.update( string.upper( pygame.key.name( event.key ) ) )
                  # update word visually
                  background.blit( score_surface, ( 35, 35 ) )
                  background.blit( timer_surface, timer_rect )
                  background.blit( game_word.bg_surface_obj, temp_rect_obj )
                  screen.blit( background, ( 0, 0 ) )
                  pygame.display.flip()
               if event.type == pygame.USEREVENT + 1:
                  seconds = seconds - 1
                  if seconds > 0:
                     background.fill( colors.get( 'black' ) )
                     screen.blit( background, ( 0, 0 ) )
                     pygame.display.flip()
                     timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
                     timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
                     pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
                     background.blit( timer_surface, timer_rect )
                     background.blit( score_surface, ( 35, 35 ) )
                     background.blit( game_word.bg_surface_obj, temp_rect_obj )
                     screen.blit( background, ( 0, 0 ) )
                     pygame.display.flip()
                  else:
                     time_remains = False
                     game_over = True
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


# This is a sample game using the new classes and new look.
#--------------------------------------------
def main_two():
   # dict of actions
   game_actions = {
      'jump': "Player jumps over something unknown!",
      'crawl': "Player crawls under danger!",
      'high five': "Player high fives the air!",
      'tongue': "The player talks, but no one is listening.",
      'expload': "The player exploads in an imploading manner.",
      'taco': "Where'd you get a taco?",
      'cheese': "Save this for the taco."
      }

   # some initial game values
   playing_game = True
   time_remains = True
   word_incomplete = True
   start = True
   game_over = False

   # initilize game screen
   screen_size = ( 800, 600 )    # ( width, height ) - game screen size
   screen = pygame.display.set_mode( screen_size )
   pygame.display.set_caption( "main_two() interface board testing" )

   # game background
   background = pygame.Surface( screen.get_size() )
   background = background.convert()

   # running game
   while playing_game:

      # if time runs out, game over and display score and choice of replay
      if not time_remains:
         game_over_message1 = "Congratulations!"
         game_over_message_surface1 = font.render( game_over_message1, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         game_over_message_rect1 = game_over_message_surface1.get_rect()
         game_over_message_rect1.centerx = background.get_rect().centerx
         game_over_message_rect1.top = 149
         game_over_message2 = "You scored " + str( score ) + " points."
         game_over_message_surface2 = font.render( game_over_message2, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         game_over_message_rect2 = game_over_message_surface2.get_rect()
         game_over_message_rect2.centerx = background.get_rect().centerx
         game_over_message_rect2.top = 224
         game_over_message3 = "Play again?"
         game_over_message_surface3 = font.render( game_over_message3, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         game_over_message_rect3 = game_over_message_surface3.get_rect()
         game_over_message_rect3.centerx = background.get_rect().centerx
         game_over_message_rect3.top = 299
         background.fill( colors.get( 'black' ) )
         background.blit( game_over_message_surface1, game_over_message_rect1 )
         background.blit( game_over_message_surface2, game_over_message_rect2 )
         background.blit( game_over_message_surface3, game_over_message_rect3 )
         screen.blit( background, ( 0, 0 ) )
         pygame.display.flip()
         while game_over:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  sys.exit()
               if event.type == pygame.KEYDOWN:
                  if pygame.key.name( event.key ) == 'n':
                     sys.exit()
                  if pygame.key.name( event.key ) == 'y':
                     start = True
                     time_remains = True
                     word_incomplete = True
                     game_over = False

      # first game loop iteration initialization
      if start:
         # score
         score = 0      # starting score
         score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         # timer
         seconds = 300   # starting timer in seconds
         timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
         timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
         timer_rect = timer_surface.get_rect()
         timer_rect.centerx = background.get_rect().centerx
         timer_rect.top = 35
         pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
         start = False
         # initialize interface_board
         action_object = Action_Board_Class( list( game_actions.keys() ) )
         temp_rect_obj = action_object.bg_surface_obj.get_rect()
         temp_rect_obj.top = 400

      # completed word, distribute rewards and update game
      if not word_incomplete:
         score = score + reward_points
         score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
         seconds = seconds + reward_timer
         timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
         timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
         word_incomplete = True
         print( game_actions[ result_string ] )

      # refresh game background
      background.fill( colors.get( 'black' ) )
      background.blit( score_surface, ( 35, 35 ) )
      background.blit( timer_surface, timer_rect )
      screen.blit( background, ( 0, 0 ) )
      pygame.display.flip()

      # if all_words is empty, exit game -+- word_count[349464] so unlikely
      if len( all_words ) == 0:
         print( "Out of words!" )
         sys.exit()
      # keep going, all_words is not empty
      else:
      # rewards, timer, and score
         reward_points = reward_points_multiplier * len( all_words[ -1 ] )
         reward_timer = reward_timer_multiplier * len( all_words[ -1 ] )
      # animation -+-+-+-
         background.blit( action_object.bg_surface_obj, temp_rect_obj )
         screen.blit( background, ( 0, 0 ) )
         pygame.display.flip()
         # while player is typing
         while word_incomplete and time_remains:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  sys.exit()
               if event.type == pygame.KEYDOWN:
                  # clear background
                  background.fill( colors.get( 'black' ) )
                  screen.blit( background, ( 0, 0 ) )
                  pygame.display.flip()
                  # check typed letter against word
                  result_string = action_object.update( pygame.key.name( event.key ) )
                  if result_string is not None:
                     word_incomplete = False
                  # update word visually
                  background.blit( score_surface, ( 35, 35 ) )
                  background.blit( timer_surface, timer_rect )
                  background.blit( action_object.bg_surface_obj, temp_rect_obj )
                  screen.blit( background, ( 0, 0 ) )
                  pygame.display.flip()
               if event.type == pygame.USEREVENT + 1:
                  seconds = seconds - 1
                  if seconds > 0:
                     background.fill( colors.get( 'black' ) )
                     screen.blit( background, ( 0, 0 ) )
                     pygame.display.flip()
                     timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
                     timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
                     pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
                     background.blit( timer_surface, timer_rect )
                     background.blit( score_surface, ( 35, 35 ) )
                     background.blit( action_object.bg_surface_obj, temp_rect_obj )
                     screen.blit( background, ( 0, 0 ) )
                     pygame.display.flip()
                  else:
                     time_remains = False
                     game_over = True
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


# testing through __name__ == "__main__"
#--------------------------------------------
if __name__ == "__main__":
   main_two()
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
