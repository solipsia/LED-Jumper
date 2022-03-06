#maze solver, GR Oct 2017
#finds the optimal route between two points
#import canvas
import random

numy=16	
numx=16
#start near the top and end near the bottom at random
start=(1,1)
end=(numy-2,1)

wall = -2 #block type
path = -1 #block type
maze = [[path for x in range(numx)] for y in range(numy)] #generate blank maze
maze[0]=[wall for x in maze[0]] #build horizontal outer walls
maze[numy-1]=[wall for x in maze[0]]
for x in range(numy): #build vertical outer walls
	maze[x][0]=wall
	maze[x][numx-1]=wall
	
for y in range(numy):
	for x in range(numx):
		if y==numy/2 and x>numx/4 or y==numy/4 and x<3*numx/4 or y==3*numy/4 and x<3*numx/4:
			maze[y][x]=wall # horizontal inner walls
		if random.random()<0.2: #random blocks
			maze[y][x]=wall


#works as follows: start at the start point (step 0), look at adjacent blocks that are not walls, call them step 1. add all the steps 1 coordinates to a list. go to each of the step blocks in that Step 1 list, look at adjacent cells that are not walls and where we have not been before, then call them step 2. add all their coordinates to a list called step 2. repeat until one of the new coordinates is the end block. Now walk back from the end taking the direction where the steo number is lowest and not a wall. repeat until step=0 then you are at the start. for each of these steps, add the coordinate to a new solution list. reverse that list and that is the solution on how to walk from the start to the end. 
def solvemaze(maze,start,end):
	stepcounter=0
	steps=[]#holds the list of coordinates for each step number
	succeed=False #when this becomes true, solution found. 
	fail=False#when this becomes true, no solution is issible. 
	#avoid start and end being inside a wall
	maze[start[0]][start[1]]=path
	maze[end[0]][end[1]]=path
	steps.append([start]) #start at the start
	maze[start[0]][start[1]]=0

	while not succeed and not fail:
		listofcoordinates=[] # holds all coordinates of current step number
		for step in steps[stepcounter]: #for each of those coordinates
			if maze[step[0]][step[1]-1]==path: #path is left of that block, so add to list of the next step number an update the maze array
				listofcoordinates.append((step[0],step[1]-1))
				maze[step[0]][step[1]-1]=stepcounter+1
			if maze[step[0]][step[1]+1]==path: #path right
				listofcoordinates.append((step[0],step[1]+1))
				maze[step[0]][step[1]+1]=stepcounter+1
			if maze[step[0]-1][step[1]]==path: #path up
				listofcoordinates.append((step[0]-1,step[1]))
				maze[step[0]-1][step[1]]=stepcounter+1
			if maze[step[0]+1][step[1]]==path: #path left
				listofcoordinates.append((step[0]+1,step[1]))
				maze[step[0]+1][step[1]]=stepcounter+1
		steps.append(listofcoordinates)	
		if end in listofcoordinates:
			succeed=True
		if listofcoordinates == []:
			fail=True	
		stepcounter+=1

	#capture solution into new list by walking back from the end to start
	solution=[]
	if succeed:
		pos=[0 for i in range(2)] #pos holds the current position of the walker
		pos[0]=end[0] # start at the end 
		pos[1]=end[1]
		solution.append(pos[:])
		for i in range(stepcounter):
			# check which direction has the lowest step count, i.e. is shortest path to start. 
			up=maze[pos[0]-1][pos[1]]
			down=maze[pos[0]+1][pos[1]]
			left=maze[pos[0]][pos[1]-1]
			right=maze[pos[0]][pos[1]+1]
			direction=0 #0 is up, 1 is right etc
			if (right<=up or up<0) and (right<=down or down<0) and (right<=left or left<0) and right>path:
				direction=1
			if (down<=up or up<0) and (down<=right or right<0) and (down<=left or left<0)and down>path:
				direction=2
			if (left<=up or up<0) and (left<=down or down<0) and (left<=right or right<0) and left>path:
				direction=3
			#move the position in the chosen direction
			if direction==0:#up
				pos[0]=pos[0]-1
				pos[1]=pos[1]
			if direction==1:#right
				pos[0]=pos[0]
				pos[1]=pos[1]+1
			if direction==2:#down
				pos[0]=pos[0]+1
				pos[1]=pos[1]
			if direction==3:#left
				pos[0]=pos[0]
				pos[1]=pos[1]-1
			solution.append(pos[:]) #add the new position to the solution list
		solution= solution[::-1]#reverse the list so its start to end
		return(solution)

solution = solvemaze(maze,start,end)


#show solution
for x in range(numx):
	for y in range(numy):
		if solution and [y,x] in solution:
			print(f'\x1b[38;2;{255};{0};{0}m# \x1b[0m',end='') # print # char in RGB
		else:
			if maze[y][x] == wall:
				print(f'\x1b[38;2;{255};{255};{255}m# \x1b[0m',end='') # print # char in RGB
			else:
				print(f'\x1b[38;2;{20};{20};{20}m# \x1b[0m',end='') # print # char in RGB
	print('') # new line
 


