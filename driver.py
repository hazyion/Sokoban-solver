from sokoban import Sokoban
import sys

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Invalid arguments. Please provide just the filename with extension.')
		exit()

	filename = sys.argv[1]
	try:
		file = open(filename, 'r')
	except FileNotFoundError:
		print(filename,'does not exist.')
		exit()

	try:
		lines = file.read()
		lines = lines.split('\n\n')
		for i in range(len(lines)):
			lines[i] = lines[i].split('\n')
			for j in range(len(lines[i])):
				lines[i][j] = lines[i][j].rstrip()
		file.close()
	except:
		print('Error parsing contents; please refer the README and ensure input specifications are met.')
		exit()
	

	writefile = 'sokosolution.txt'
	try:
		file = open(writefile, 'x')
	except FileExistsError:
		file = open(writefile, 'w')

	for i in lines:
		game = Sokoban(i)
		
		# to print initial game state, use this
		game.print_easy()

		solution = game.gpsearch()
		if solution is None:
			solution = 'Could not solve'
		file.write(solution)
		file.write('\n')

	file.close()