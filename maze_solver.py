#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

def solveMazeGeneral(maze, algorithm):
	#select the right queue for each algorithm
	if algorithm == "BFS":
		fr = Fringe("FIFO")
	elif algorithm == "DFS":
		fr = Fringe("STACK")
	elif algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
		fr = Fringe("PRIO")
	else:
		print("algorithm not found/implemented, exit")
		return
	
	goal = maze.getGoal()
	room = maze.getRoom(*maze.getStart())
	prio = 0
	for x in range(0,3):
		dist = goal[x]-room.coords[x]
		if x == 2 and not dist:
			dist *= 3 if goal[x] > room.coords[x] else 2
		prio += (dist) ** 2
	prio **= 0.5
	state = State(room=room, parent=None, cost = 0, prio = prio)
	fr.push((prio, state))	
	
	#creates a list of all visited rooms
	visited_rooms = [str(room.coords)]

	while not fr.isEmpty():
	
		priority_tuple = fr.pop()
		cost = priority_tuple[0]
		state = priority_tuple[1]
		room = state.getRoom()
		print(str(room.coords)+ " " + str(cost))

		if room.isGoal():
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			return

		#loop through every possible move
		for d in room.getConnections():
			#get new room after move and cost to get there
			newRoom, cost = room.makeMove(d, state.getCost())
			newState = State(newRoom, state, cost)
			if algorithm == "GREEDY" or algorithm == "ASTAR":
				cost = 0
				for x in range(0,3):
					cost += abs(goal[x]-newRoom.coords[x]) ** 2
				cost **= 0.5
				if algorithm == "ASTAR":
					cost += state.cost
			priority_tuple = (cost, newState)
			#before pushing a new state, checks if it's in our list
			if not str(newRoom.coords) in visited_rooms:
				visited_rooms.append(str(newRoom.coords))
				fr.push(priority_tuple)

	print("not solved")
	fr.printStats()
