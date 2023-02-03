import heapq
import time
import queue

# Priority queue
class Pqueue:
    def  __init__(self):
        self.Heap = []
        self.Count = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap)
        return item

    def isEmpty(self):
        return len(self.Heap) == 0


class Sokoban:
	def __init__(self, lines):
		self.lookup = {' ': '0', '#': '1', '@': '2', '$': '3', '.': '9'}
		self.rev_lookup = {'0': ' ', '1': '#', '2': '@', '3': '$', '9': '.'}
		self.__gameState = [list(i) for i in lines]
		self.__dimensions = ()
		self.__goalIndices = []
		self.__deadIndices = set()
		self.__boxIndices = []


		# convert to numbers
		maxlen = 0
		for i in range(len(self.__gameState)):
			for j in range(len(self.__gameState[i])):
				if self.__gameState[i][j] == '\n':
					self.__gameState[i].pop()
					continue
				self.__gameState[i][j] = self.lookup[self.__gameState[i][j]]
			if len(self.__gameState[i]) > maxlen:
				maxlen = len(self.__gameState[i])

		self.__dimensions = (len(self.__gameState),maxlen)


		# pad rows
		for i in range(len(self.__gameState)):
			lendif = maxlen - len(self.__gameState[i])
			for j in range(lendif):
				self.__gameState[i].append('0')

		
		# find goalIndices and boxIndices
		self.__gameTwine = self.makeTwine(self.__gameState)
		for i in range(len(self.__gameTwine)):
			if self.__gameTwine[i] == '9':
				self.__goalIndices.append(i)
			if self.__gameTwine[i] == '3':
				self.__boxIndices.append(i)


		# finds goalpull distance and deadlock positions
		self.goaldist = {}
		setlist = []
		for i in self.__goalIndices:
			deads = set()
			row, col = self.__dimensions
			l = [[row*col for x in range(col)] for j in range(row)]
			l[int(i/col)][i%col] = 0
			q = queue.Queue()
			q.put(i)
			while not q.empty():
				pos = q.get()
				for x in [1, -1, col, -col]:
					boxpos = pos+x
					plpos = pos+2*x
					if l[int(boxpos/col)][boxpos%col] == row*col:
						if self.__gameTwine[boxpos] != '1' and self.__gameTwine[plpos] != '1':
							l[int(boxpos/col)][boxpos%col] = l[int(pos/col)][pos%col] + 1
							q.put(boxpos)
			newl = []
			for x in range(row):
				for h in range(col):
					newl.append(l[x][h])
					if self.__gameTwine[x*col+h] != '1' and l[x][h] == row*col:
							deads.add(x*col+h)
			self.goaldist[i] = newl
			setlist.append(deads)

		self.__deadIndices = setlist[0]
		for i in range(1,len(setlist)):
			self.__deadIndices = self.__deadIndices.intersection(setlist[i])


		# box-goal assignment (greedy)
		self.boxgoalgraph = {}
		edges = Pqueue()
		for i in self.__boxIndices:
			for j in self.__goalIndices:
				edges.push((i,j), self.goaldist[j][i])
		matchedBoxes = set()
		matchedGoals = set()
		while not edges.isEmpty():
			edge = edges.pop()
			if edge[0] not in matchedBoxes and edge[1] not in matchedGoals:
				self.boxgoalgraph[edge[0]] = edge[1]
				matchedBoxes.add(edge[0])
				matchedGoals.add(edge[1])
		
		for x in self.__boxIndices:
			if x not in matchedBoxes:
				j = min(self.__goalIndices, key= lambda y: self.goaldist[y][x])
				self.boxgoalgraph[x] = j


	def makeTwine(self, state):
		'''append to make single string of numbers'''
		newStr = ''
		for i in state:
			for j in i:
				newStr += j
		return newStr


	def print_state(self, opt=None):
		'''print state from matrix'''
		if opt is not None:
			x = opt
		else:
			x = self.__gameState
		print()
		for i in x:
			for j in i:
				print(j, end='')
			print()
		print()


	def print_twine(self, opt=None):
		'''print state from twine'''
		if opt is not None:
			x = opt
		else:
			x = self.__gameTwine
		print()
		for i in range(len(x)):
			if i % self.__dimensions[1] == 0:
				print()
			print(x[i], end='')
		print('\n')


	def print_easy(self, twine=None, dead=False):
		'''print an understandable state from twine using original symbols'''
		if twine is None:
			twine = self.__gameTwine
		for i in range(len(twine)):
			if i % self.__dimensions[1] == 0:
				print()
			if dead and i in self.__deadIndices:
				print('X',end='')
			else:
				print(self.rev_lookup[twine[i]], end='')
		print('\n')


	def move(self, twine, val, dead=False):
		'''make a move'''
		# If dead is set, returns None if box is moved to deadlock state

		boxmove = False
		boxIndex = -1
		for i in range(len(twine)):
			if twine[i] == '2':
				plIndex = i
				break
		
		newTwine = None
		if val == 0:
			if twine[plIndex-1] == '9' or twine[plIndex-1] == '0':
				if plIndex in self.__goalIndices:
					newTwine = twine[:plIndex-1] + '2' + '9' + twine[plIndex+1:]
				else:
					newTwine = twine[:plIndex-1] + '2' + '0' + twine[plIndex+1:]
				plIndex -= 1

			elif twine[plIndex-1] == '3':
				if twine[plIndex-2] != '1' and twine[plIndex-2] != '3':
					if dead and plIndex-2 in self.__deadIndices:
						return None
					if plIndex in self.__goalIndices:
						newTwine = twine[:plIndex-2] + '3' + '2' + '9' + twine[plIndex+1:]
					else:
						newTwine = twine[:plIndex-2] + '3' + '2' + '0' + twine[plIndex+1:]
					boxIndex = plIndex-1
					boxmove = True
					plIndex -= 1
		
		elif val == 1:
			if twine[plIndex+1] == '9' or twine[plIndex+1] == '0':
				if plIndex in self.__goalIndices:
					newTwine = twine[:plIndex] + '9' + '2' + twine[plIndex+2:]
				else:
					newTwine = twine[:plIndex] + '0' + '2' + twine[plIndex+2:]
				plIndex += 1
			
			elif twine[plIndex+1] == '3':
				if twine[plIndex+2] != '1' and twine[plIndex+2] != '3':
					if dead and plIndex+2 in self.__deadIndices:
						return None
					if plIndex in self.__goalIndices:
						newTwine = twine[:plIndex] + '9' + '2' + '3' + twine[plIndex+3:]
					else:
						newTwine = twine[:plIndex] + '0' + '2' + '3' + twine[plIndex+3:]
					boxIndex = plIndex+1
					boxmove = True
					plIndex += 1

		elif val == 2:
			row, col = self.__dimensions
			if twine[plIndex-col] == '9' or twine[plIndex-col] == '0':
				if plIndex in self.__goalIndices:
					newTwine = twine[:plIndex-col] + '2' + twine[plIndex-col+1:plIndex] + '9' + twine[plIndex+1:]
				else:
					newTwine = twine[:plIndex-col] + '2' + twine[plIndex-col+1:plIndex] + '0' + twine[plIndex+1:]
				plIndex -= col

			elif twine[plIndex-col] == '3':
				if twine[plIndex-2*col] != '1' and twine[plIndex-2*col] != '3':
					if dead and plIndex-2*col in self.__deadIndices:
						return None
					if plIndex in self.__goalIndices:
						newTwine = twine[:plIndex-2*col] + '3' + twine[plIndex-2*col+1:plIndex-col] + '2' + twine[plIndex-col+1:plIndex] + '9' + twine[plIndex+1:]
					else:
						newTwine = twine[:plIndex-2*col] + '3' + twine[plIndex-2*col+1:plIndex-col] + '2' + twine[plIndex-col+1:plIndex] + '0' + twine[plIndex+1:]
					boxIndex = plIndex-col
					boxmove = True
					plIndex -= col

		elif val == 3:
			row, col = self.__dimensions
			if twine[plIndex+col] == '9' or twine[plIndex+col] == '0':
				if plIndex in self.__goalIndices:
					newTwine = twine[:plIndex] + '9' + twine[plIndex+1:plIndex+col] + '2' + twine[plIndex+col+1:]
				else:
					newTwine = twine[:plIndex] + '0' + twine[plIndex+1:plIndex+col] + '2' + twine[plIndex+col+1:]
				plIndex += col

			elif twine[plIndex+col] == '3':
				if twine[plIndex+2*col] != '1' and twine[plIndex+2*col] != '3':
					if dead and plIndex+2*col in self.__deadIndices:
						return None
					if plIndex in self.__goalIndices:
						newTwine = twine[:plIndex] + '9' + twine[plIndex+1:plIndex+col] + '2' + twine[plIndex+col+1:plIndex+2*col] + '3' + twine[plIndex+2*col+1:]
					else:
						newTwine = twine[:plIndex] + '0' + twine[plIndex+1:plIndex+col] + '2' + twine[plIndex+col+1:plIndex+2*col] + '3' + twine[plIndex+2*col+1:]
					boxIndex = plIndex+col
					boxmove = True
					plIndex += col

		return (newTwine, boxmove, boxIndex)


	def checkGoal(self, twine):
		'''check if the all boxes sit on goal positions'''
		for i in self.__goalIndices:
			if twine[i] != '3':
				return False
		return True


	def successors(self, twine, blist):
		'''generate list of successors'''
		children = []
		for i in range(4):
			newblist = blist.copy()
			m = self.move(twine, i, True)
			if m is not None and m[0] is not None:
				(x, boxmove, boxIndex) = m
				if boxmove:
					ind = blist.index(boxIndex)
					if i == 0:
						newblist[ind] -= 1
					elif i == 1:
						newblist[ind] += 1
					elif i == 2:
						newblist[ind] -= self.__dimensions[1]
					elif i == 3:
						newblist[ind] += self.__dimensions[1]
				children.append((x, newblist))
		return children


	def blist_calc(self, twine):
		'''calculates indices of boxes'''
		l = []
		for i in range(len(twine)):
			if twine[i] == '3':
				l.append(i)
		return l


	def find_move(self, parent, child):
		'''finds move made between parent and child'''
		boxmove, par, chi = False, False, False
		for i in range(len(parent)):
			if parent[i] == '2':
				parIndex = i
				par = True
			if child[i] == '2':
				chiIndex = i
				chi = True
			if parent[i] == '3':
				if child[i] != '3':
					boxmove = True
					if par and chi:
						break

		if (chiIndex - parIndex) > 0:
			if (chiIndex - parIndex) > 1:
				res = 'd'
			else:
				res = 'r'
		elif (chiIndex - parIndex) < 0:
			if (chiIndex - parIndex) < -1:
				res = 'u'
			else:
				res = 'l'
		else:
			return None

		if boxmove:
			return res.upper()
		else:
			return res


	def __aStarSearch(self, heuristic, h_weight = 1):
		'''A* search algorithm'''

		graph = {self.__gameTwine : (None, self.__boxIndices)}
		fScore = {self.__gameTwine: h_weight * heuristic(self.__gameTwine, self.__boxIndices)}
		gScore = {self.__gameTwine: 0}
		OPEN = Pqueue()
		OPEN.push((self.__gameTwine, self.__boxIndices), fScore[self.__gameTwine])
		insCount = {self.__gameTwine : OPEN.Count}
		expandCount = 0
		
		while not OPEN.isEmpty():
			item = OPEN.pop()
			n = item[0]
			if self.checkGoal(n):
				path = []
				(parent, _) = graph.get(n)
				current = n
				while parent is not None:
					path.append(self.find_move(parent, current))
					current = parent
					(parent,_) = graph[current]
				newStr = ''
				for i in path:
					newStr = i + newStr
				return newStr
			
			expandCount += 1
			for (child, blist) in self.successors(n, item[1]):
				tempgScore = gScore.get(n) + 1
				childgScore = gScore.get(child)
				if (childgScore is not None and tempgScore < childgScore):
					gScore[child] = tempgScore
					temp = fScore[child]
					fScore[child] = tempgScore + h_weight * heuristic(child, blist)
					insCount[child] = OPEN.Count
					OPEN.push((child, blist), fScore[child])
					graph[child] = (n, blist)

				elif childgScore is None:
					gScore[child] = tempgScore
					graph[child] = (n, blist)
					fScore[child] = tempgScore + h_weight * heuristic(child, blist)
					insCount[child] = OPEN.Count
					OPEN.push((child, blist), fScore[child])
		return None

	def CBD_calc(self, a, b):
		'''calculate city block distance between two indices'''
		return abs((b % self.__dimensions[1]) - (a % self.__dimensions[1])) + abs(int(b/self.__dimensions[1]) - int(a/self.__dimensions[1]))


	def CBD_Heuristic(self, twine, _):
		'''City block distance heuristic'''
		goals = self.__goalIndices.copy()
		sum = 0
		for i in range(len(twine)):
			if twine[i] == '3':
				if i not in goals:
					dist = list(map(self.CBD_calc, goals, [i for j in range(len(goals))]))
					min = 0
					for j in range(len(dist)):
						if dist[min] > dist[j]:
							min = j
					sum += dist[min]
					goals.pop(min)
				else:
					goals.remove(i)
			if len(goals) == 0:
				break
		return sum


	def cbdsearch(self, h=1):
		return self.__aStarSearch(self.CBD_Heuristic, h)

	def goalpull_Heuristic(self, twine, blist):
		'''goalpull Heuristic'''
		sum = 0
		for i in range(len(blist)):
			sum += self.goaldist[self.boxgoalgraph[self.__boxIndices[i]]][blist[i]]
		return sum


	def gpsearch(self, h=1):
		return self.__aStarSearch(self.goalpull_Heuristic, h)


	def playout(self, sol, verbose=False):
		'''make moves according to the solution passed'''
		# set verbose to show every move
		
		newTwine = self.__gameTwine
		lookup = {'u' : 2, 'U' : 2, 'd' : 3, 'D' : 3, 'l' : 0, 'L' : 0, 'r' : 1, 'R' : 1}
		for i in sol:
			(newTwine, _, _) = self.move(newTwine, lookup[i])
			if verbose:
				time.sleep(0.5)
				self.print_easy(newTwine)
		return newTwine