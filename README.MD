# Sokoban Solver

This Sokoban solver uses A* search to solve sokoban puzzles.

Input format:

     #########
   ###  #    #
   # $ $# $# #
  ##   $   # #
###. ### $ $ #
# ...$@#   # #
# #. #$###$  #
#   #..    ###
#    ..  ###
##### # ##
    #   #
    #####

       #####
 #######   ##
## # @## $$ #
#    $      #
#  $  ###   #
### #####$###
# $  ### ..#
# $ $ $ ...#
#    ###...#
# $$ # #...#
#  ### #####
####

The game state should start at the first line.
There should be a empty line between two levels.
Make sure there are no unnecessary empty lines at the end of the file.
Check levels folder for sample levels.

Each symbol represents:
# - walls
$ - box
. - goal
@ - player


How to run:

python driver.py <path_to_file>

Examples:

python driver.py levels/lvl1.txt

python driver.py lvl2.txt


Output format:

Output is written to a new file 'sokosolution.txt' created in the same directory.
Its contents are overwritten if it already exists.
Each line contains the solution to one level, in the same order as in the input file.

Letters l, r, u and d correspond to left, right, up and down movements respectively.
Lowercase letters l, r, u, d are used to denote player movement without pushing a box.
Uppercase letters L, R, U, D are used to denote box pushes.