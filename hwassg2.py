import math
import operator
import copy
import time
begin = time.time()
inputfile = open("input1.txt", "r").readlines()
gametype = str(inputfile[0]).strip()
playername = str(inputfile[1]).strip()

playtime = float(inputfile[2])
if playername == "WHITE":
	opponent = "BLACK"
else:
	opponent = "WHITE"
#x is columns and y is rows
#  Initial position of pieces while starting game
# positions of black camp and white camp
whitestart = [[14, 11], [15, 11], [13, 12], [14, 12], [15, 12], [12, 13], [13, 13], [14, 13], [15, 13], [11, 14], [12, 14], [13, 14], [14, 14], [15, 14], [11, 15], [12, 15], [13, 15], [14, 15], [15, 15]]
blackstart = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [0, 2], [1, 2], [2, 2], [3, 2], [0, 3], [1, 3], [2, 3], [0, 4], [1, 4]]

def makeboard():
	board = []
	for i in range(16):
		row = []
		for j in range(16):
			row.append(str(inputfile[i+3][j]))
		board.append(row)
	return board
board = makeboard()


def athome(coords, playername):
	if playername == "WHITE":
		if coords in whitestart:
			return True
	elif playername == "BLACK":
		if coords in blackstart:
			return True
	return False

def inopponent(coords, playername):
	if playername == "WHITE":
		if coords in blackstart:
			return True
		else:
			return False
	elif playername == "BLACK":
		if coords in whitestart:
			return True
		else:
			return False
	return False

def calcmanhattendist(coords, playername):
	if playername == "WHITE":
		start = [15,15]
	else:
		start = [0,0]
	return abs(coords[0] - start[0]) + abs(coords[1] - start[1])

def makelists(player): # Needs black and white positions
	hlist = []
	olist = []
	alist = []
	if player == "WHITE":
		for i in whitepositions:
			if athome(i, player):
				hlist.append(i)
			elif inopponent(i, player):
				olist.append(i)
			else:
				alist.append(i)

	elif player == "BLACK":
		for i in blackpositions:
			if athome(i, player):
				hlist.append(i)
			elif inopponent(i, player):
				olist.append(i)
			else:
				alist.append(i)
	return hlist, olist, alist

usedlistglobal = [[]]
def findallmoves(coords):
	op = []
	usedlist = [[0 for i in range(16)] for j in range(16)]
	yarr = [0,0,1,1,1,-1,-1,-1]
	xarr = [1,-1,1,-1,0,1,-1,0]
	x = coords[0]
	y = coords[1]
	usedlist[y][x] = 1
	for j in range(8):
		newx = x + xarr[j]
		newy = y + yarr[j]
		if 0<= newx < 16 and 0 <= newy < 16 and board[newy][newx] == "." and usedlist[newy][newx] == 0:
			op.append([[newx,newy], "E"])
			usedlist[newy][newx] = 1
	global usedlistglobal 
	usedlistglobal = copy.deepcopy(usedlist)
	if op:
		return op
	else:
		return False

def findjumps(coords):
	op = []
	jusedlist = copy.deepcopy(usedlistglobal)
	yarr = [0,0,1,1,1,-1,-1,-1]
	xarr = [1,-1,1,-1,0,1,-1,0]
	x = coords[0]
	y = coords[1]
	dicti = {(x,y): [[x,y]]}
	openlist = [[x,y]]
	
	while openlist:
		p = openlist.pop(0)
		x = p[0]
		y = p[1]
		for j in range(8):
			newx = x + xarr[j]
			newy = y + yarr[j]
			newx2 = newx + xarr[j]
			newy2 = newy + yarr[j]
			if 0 <= newx < 16 and 0 <= newy < 16 and board[newy][newx] != '.':
				if 0 <= newx2 < 16 and 0 <= newy2 < 16 and jusedlist[newy2][newx2] == 0 and board[newy2][newx2] == '.':
					a = copy.deepcopy(dicti[(x,y)])
					a.append([newx2, newy2])
					dicti[(newx2, newy2)] = a
					openlist.append([newx2, newy2])
					jusedlist[newy2][newx2] = 1
	for v in dicti.values():
		op.append(v)
	op = op[1:]
	if op:
		return op
	else:
		return False

def findlegalmoves(player):
	legal = []
	homelist, opponentlist, awaylist = makelists(player)
	if homelist:
		outofhome = []
		inhome = []
		for h in homelist:
			moves = findallmoves(h) # Normal Moves only
			if moves:
				for hmove in moves:
					if athome(hmove[0], player) == False:
						st = hmove[1] + " " + str(h[0]) + "," + str(h[1]) + " " + str(hmove[0][0]) + "," + str(hmove[0][1])
						legal.append(st)
						outofhome.append([[h[0], h[1]], hmove])
					else:
						inhome.append([[h[0], h[1]], hmove]) # move  = [[newx,newy], "E"]

			jmoves = findjumps(h) #Jump moves
			if jmoves:
				for jmove in jmoves:
					endpoint = jmove[-1]
					if athome(endpoint, player) == False:
						s = ""
						for e in range(len(jmove)-1):
							s = s + "J" + " " + str(jmove[e][0]) + "," + str(jmove[e][1]) + " " + str(jmove[e+1][0]) + "," + str(jmove[e+1][1])
							if e != len(jmove)-2:
								s = s + "\n"
						legal.append(s)
						outofhome.append([[h[0], h[1]], [endpoint, "J"]])
					else:
						inhome.append([[h[0], h[1]], [jmove, "J"]])


		if not outofhome:
			for ih in inhome:
				if ih[1][-1] != "J":
					if calcmanhattendist(ih[0], player) < calcmanhattendist(ih[1][0], player):
						st = ih[1][1] + " " + str(ih[0][0]) + "," + str(ih[0][1]) + " " + str(ih[1][0][0]) + "," + str(ih[1][0][1])
						legal.append(st)
				else:
					jm = ih[1][0]
					endpoint = jm[-1]
					st = jm[0]
					if calcmanhattendist(st, player) < calcmanhattendist(endpoint, player):
						s = ""
						for e in range(len(jm)-1):
							s = s + "J" + " " + str(jm[e][0]) + "," + str(jm[e][1]) + " " + str(jm[e+1][0]) + "," + str(jm[e+1][1])
							if e != len(jm)-2:
								s = s + "\n"
						legal.append(s)
	if not legal:
		if awaylist:
			for a in awaylist:
				moves = findallmoves(a)
				if moves:
					for amove in moves:
						if athome(amove[0], player) == False or inopponent(amove[0], player) == True:
							st = amove[1] + " " + str(a[0]) + "," + str(a[1]) + " " + str(amove[0][0]) + "," + str(amove[0][1])
							legal.append(st)

				jmoves = findjumps(a)
				if jmoves:
					for jmove in jmoves:
						endpoint = jmove[-1]
						if inopponent(endpoint, player) == True or athome(endpoint, player) == False:
							s = ""
							for e in range(len(jmove)-1):
								s = s + "J" + " " + str(jmove[e][0]) + "," + str(jmove[e][1]) + " " + str(jmove[e+1][0]) + "," + str(jmove[e+1][1])
								if e != len(jmove)-2:
									s = s + "\n"
							legal.append(s)
							s
		if opponentlist:	
			for o in opponentlist:
				moves = findallmoves(o)
				if moves:
					for omove in moves:
						if inopponent(omove[0], player) == True:
							st = omove[1] + " " + str(o[0]) + "," + str(o[1]) + " " + str(omove[0][0]) + "," + str(omove[0][1])
							legal.append(st)
				jmoves = findjumps(o)
				if jmoves:
					for jmove in jmoves:
						endpoint = jmove[-1]
						if inopponent(endpoint, player) == True:
							s = ""
							for e in range(len(jmove)-1):
								s = s + "J" + " " + str(jmove[e][0]) + "," + str(jmove[e][1]) + " " + str(jmove[e+1][0]) + "," + str(jmove[e+1][1])
								if e != len(jmove)-2:
									s = s + "\n"
							legal.append(s)
	if player == "BLACK":
		for l in legal:
			s = l.split()
			source = s[1].split(",")
			destination = s[-1].split(",")
			if int(source[0]) >= 9 and int(source[1]) >= 9:
				if int(destination[0]) <= int(source[0]) or int(destination[1]) <= int(source[1]):
					legal.remove(l)
		return legal
	elif player == "WHITE":
		for l in legal:
			s = l.split()
			source = s[1].split(",")
			destination = s[-1].split(",")
			if int(source[0]) <= 7 and int(source[1]) <= 7:
				if int(destination[0]) >= int(source[0]) or int(destination[1]) >= int(source[1]):
					legal.remove(l)
		return legal
	# return legal

#White + and black - so if white is closer (to winning) then board becomes more -ve and vice versa

def findboardvalnew(liw, lib, player):
	if player == "WHITE":
		result = 0 
		wval = 0
		countw = 0
		for l in liw:
			if 0<= l[0] < 8 and 0 <= l[1] < 8 and l:
				countw = countw + 1
			
		if countw == 19:
			for l in liw:
				piecedist = []
				for bs in blackstart:
					if board[bs[1]][bs[0]] != "W":
						piecedist.append(math.sqrt((l[0] - bs[0]) ** 2 + (l[1] - bs[1]) ** 2))
				if piecedist:
					result += max(piecedist)
				else:
					result += 50
			return result * -1

		else:
			for l in liw:
				wval += math.sqrt(l[0]**2 + l[1]**2)
			return -1 * wval

	elif player == "BLACK":
		result = 0
		bval = 0
		countb = 0
		for l in lib:
			if 10 <= l[0] < 16 and 10 <= l[1] < 16 and l:
				countb = countb + 1
			
		if countb == 19:
			for l in lib:
				piecedist = []
				for ws in whitestart:
					if board[ws[1]][ws[0]] != "B":
						piecedist.append(math.sqrt((l[0] - ws[0]) ** 2 + (l[1] - ws[1]) ** 2))
				if piecedist:
					result += max(piecedist)
				else:
					result += 50
			return result * -1
		
		else:
			for l in lib:
				bval += math.sqrt((l[0]-15)**2 + (l[1]-15)**2)
			return -1 * bval

	
def makemove(bd, st):
	if st[0] == "E":
		s = st.split()[1:]
		source = s[0].split(",")
		destination = s[1].split(",")
		a = bd[int(source[1])][int(source[0])]
		bd[int(source[1])][int(source[0])] = "."
		bd[int(destination[1])][int(destination[0])] = a
		return bd
	else:
		s = st.split()
		if s[0] == "J":
			source = s[1].split(",")
			destination = s[-1].split(",")
			a = bd[int(source[1])][int(source[0])]
			bd[int(source[1])][int(source[0])] = "."
			bd[int(destination[1])][int(destination[0])] = a
			return bd


def findpieceposition(board):
	whitepos = []
	blackpos = []
	for i in range(16):
		for j in range(16):
			if board[i][j] == "W":
				whitepos.append([j,i])
			elif board[i][j] == "B":
				blackpos.append([j,i])
	return whitepos, blackpos


whitepositions, blackpositions = findpieceposition(board)

class Node:
	def __init__(self, currentboard, parent, evaluationval, children, play):
		self. currentboard = currentboard
		self.parent = parent
		self.evaluationval = evaluationval
		self.children = children
		self.play = play

def makechildren(node, player):
	lmoves = findlegalmoves(player)
	sboard = node.currentboard
	children = []
	for l in lmoves:
		# s = l.split()
		c = Node([], node, 0, [], l)
		c.currentboard = makemove(copy.deepcopy(sboard), l)
		w,b = findpieceposition(c.currentboard)
		c.evaluationval = findboardvalnew(w,b, player)
		
		children.append(c)
	
	keyfun = operator.attrgetter("evaluationval")
	children.sort(key = keyfun, reverse = True)
	return children

def single(player):
	homelist, opponentlist, awaylist = makelists(playername)
	if homelist:
		outofhome = []
		inhome = []
		for h in homelist:
			moves = findallmoves(h)
			if moves:
				for move in moves:
					if athome(move[0], playername) == False:
						st = move[1] + " " + str(h[0]) + "," + str(h[1]) + " " + str(move[0][0]) + "," + str(move[0][1])
						return st
						outofhome.append([[h[0], h[1]], move])
					else:
						inhome.append([[h[0], h[1]], move]) # move  = [[newx,newy], "E"]
			jmoves = findjumps(h)
			if jmoves:
				for jmove in jmoves:
					endpoint = jmove[-1]
					if athome(endpoint, player) == False:
						s = ""
						for e in range(len(jmove)-1):
							s = s + "J" + " " + str(jmove[e][0]) + "," + str(jmove[e][1]) + " " + str(jmove[e+1][0]) + "," + str(jmove[e+1][1])
							if e != len(jmove)-2:
								s = s + "\n"
						return s
						outofhome.append([[h[0], h[1]], [endpoint, "J"]])
					else:
						inhome.append([[h[0], h[1]], [jmove, "J"]])

		if not outofhome:
			for ih in inhome:
				if ih[1][-1] != "J":
					if calcmanhattendist(ih[0], player) < calcmanhattendist(ih[1][0], player):
						st = ih[1][1] + " " + str(ih[0][0]) + "," + str(ih[0][1]) + " " + str(ih[1][0][0]) + "," + str(ih[1][0][1])
						return st
				else:
					jm = ih[1][0]
					endpoint = jm[-1]
					st = jm[0]
					if calcmanhattendist(st, player) < calcmanhattendist(endpoint, player):
						s = ""
						for e in range(len(jm)-1):
							s = s + "J" + " " + str(jm[e][0]) + "," + str(jm[e][1]) + " " + str(jm[e+1][0]) + "," + str(jm[e+1][1])
							if e != len(jm)-2:
								s = s + "\n"
						return s

	if awaylist:
		for a in awaylist:
			moves = findallmoves(a)
			if moves:
				for amove in moves:
					if athome(amove[0], player) == False or inopponent(amove[0], player) == True:
						st = amove[1] + " " + str(a[0]) + "," + str(a[1]) + " " + str(amove[0][0]) + "," + str(amove[0][1])
						return st

			jmoves = findjumps(a)
			if jmoves:
				for jmove in jmoves:
					endpoint = jmove[-1]
					if inopponent(endpoint, player) == True or athome(endpoint, player) == False:
						s = ""
						for e in range(len(jmove)-1):
							s = s + "J" + " " + str(jmove[e][0]) + "," + str(jmove[e][1]) + " " + str(jmove[e+1][0]) + "," + str(jmove[e+1][1])
							if e != len(jmove)-2:
								s = s + "\n"
						return s
	
	if opponentlist:	
		for o in opponentlist:
			moves = findallmoves(o)
			if moves:
				for omove in moves:
					if inopponent(omove[0], player) == True:
						st = omove[1] + " " + str(o[0]) + "," + str(o[1]) + " " + str(omove[0][0]) + "," + str(omove[0][1])
						return st
			jmoves = findjumps(o)
			if jmoves:
				for jmove in jmoves:
					endpoint = jmove[-1]
					if inopponent(endpoint, player) == True:
						s = ""
						for e in range(len(jmove)-1):
							s = s + "J" + " " + str(jmove[e][0]) + "," + str(jmove[e][1]) + " " + str(jmove[e+1][0]) + "," + str(jmove[e+1][1])
							if e != len(jmove)-2:
								s = s + "\n"
						return s

	return False

def agent():
	Source = Node(board, None, 0, [], "")		
	Source.evaluationval = findboardvalnew(whitepositions, blackpositions, playername)
	Source.children = makechildren(Source, playername)
	if playername == "WHITE":
		whiteintarget = 0
		for wp in whitepositions:
			if 0 <= wp[0] < 7 and 0<= wp[1] < 7:
				whiteintarget+= 1
		if whiteintarget >= 17:
			
			mp = True
			val, playmove = minimaxendgame(Source, 2, -999999, 999999, True, "WHITE")
			return playmove
		else:
		
			mp = True
			val, playmove = minimax(Source, 1, -999999, 999999, mp, "WHITE")
	
			return playmove

	elif playername == "BLACK":
		
		blackintarget = 0
		for bp in blackpositions:
			if 10 <= bp[0] < 16 and 10 <= bp[1] < 16:
				blackintarget+= 1

		if blackintarget >= 17:
			
			mp = False
			val, playmove = minimaxendgame(Source, 2, -999999, 999999, True, "BLACK")
	
			return playmove
		else:
			
			mp = False
			val, playmove = minimax(Source, 1, -999999, 999999, mp, "BLACK")
	
			return playmove


def minimax(position, depth, alpha, beta, maximizingPlayer, player):
	
	if depth == 0:
		wh, bl = findpieceposition(position.currentboard)
		#return evaluation value of node
		if player == "WHITE":
			position.evaluationval = findboardvalnew(wh, bl, "BLACK")
		else:
			position.evaluationval = findboardvalnew(wh, bl, "WHITE")
		return position.evaluationval, position.play
	
	if maximizingPlayer:
		maxEval = -999999
		
		lg = findlegalmoves(player)
		for lmove in lg:
			child = Node([], position, 0, [], lmove)
			child.currentboard = makemove(copy.deepcopy(position.currentboard), lmove)
			wh, bl = findpieceposition(child.currentboard)
			if player == "WHITE":
				evaluation, play = minimax(child, depth-1, alpha, beta, False, "BLACK")
			else:
				evaluation, play = minimax(child, depth-1, alpha, beta, False, "WHITE")
			if evaluation >= maxEval:
				maxEval = evaluation
				playmove = child.play
			alpha = max(alpha, evaluation)
			if beta <= alpha:
				break
		return maxEval, playmove

	else:
		minEval = 999999
		lg = findlegalmoves(player)
		for lmove in lg:
			child = Node([], position, 0, [], lmove)
			child.currentboard = makemove(copy.deepcopy(position.currentboard), lmove)
			if player == "WHITE":
				evaluation, play = minimax(child, depth-1, alpha, beta, True, "BLACK")
			else:
				evaluation, play = minimax(child, depth-1, alpha, beta, True, "WHITE")
			if evaluation <= minEval:
				minEval = evaluation
				playmove = child.play
			beta = min(beta, evaluation)
			if beta <= alpha:
				break
		return minEval, playmove

def minimaxendgame(position, depth, alpha, beta, maximizingPlayer, player):
	if depth == 0:
		wh, bl = findpieceposition(position.currentboard)
		#return evaluation value of node
		if player == "WHITE":
			position.evaluationval = findboardvalnew(wh, bl, "WHITE")
		elif player == "BLACK":
			position.evaluationval = findboardvalnew(wh, bl, "BLACK")
		return position.evaluationval, position.play
	
	if maximizingPlayer:
		maxEval = -999999
		lg = findlegalmoves(player)
		for lmove in lg:
			child = Node([], position, 0, [], lmove)
			child.currentboard = makemove(copy.deepcopy(position.currentboard), lmove)
			wh, bl = findpieceposition(child.currentboard)
			# if maximizingPlayer == True:
			child.evaluationval = findboardvalnew(wh, bl, player)
			evaluation, play = minimax(child, depth-1, alpha, beta, True, player)
			if evaluation >= maxEval:
				maxEval = evaluation
				playmove = child.play
			alpha = max(alpha, evaluation)
			if beta <= alpha:
				break
		return maxEval, playmove

opf = open("output.txt", "w")

if gametype == "SINGLE":
	sing = single(playername)
	opf.write(sing)
	
elif gametype == "GAME":
	ag = agent()
	opf.write(ag)
	












				
















