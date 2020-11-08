from sys import stdin
from jetbot import Robot
import time

robot = Robot()
N, M = map(int, stdin.readline().split())
# matrix 배열
matrix = [stdin.readline().rstrip() for _ in range(N)]
# 방문경로 배열
visited = [[0]*M for _ in range(N)]
# UP/DOWN/LEFT/RIGHT
dx, dy = [-1, 1, 0, 0], [0, 0, -1, 1]
INF = 500
global mindist
mindist = INF
chardir = ['UP', 'DOWN', 'LEFT', 'RIGHT']
# DFS 경로 탐색

# dir : 0, 1, 2, 3
path = []							# Temp path
Track = []							# Real Path
info = []
result = INF
# 0 : 현재 방향 그대로
# 1 : 왼쪽 방향으로 틀기
# 2 : 오른쪽 방향으로 틀기
# 3 : 뒤로 가기
Changedir = [ [0, 3, 1, 2],	[3, 0, 2, 1],[2, 1, 0, 3],[1, 2, 3, 0]]

curdir = 1

def stop(change):
    robot.stop()
    
def step_forward(change):
    robot.forward(0.4)
    time.sleep(0.5)
    robot.stop()

def step_backward(change):
    robot.backward(0.4)
    time.sleep(0.5)
    robot.stop()

def step_left(change):
    robot.left(0.3)
    time.sleep(0.5)
    robot.stop()

def step_right(change):
    robot.right(0.3)
    time.sleep(0.5)
    robot.stop()
def step_Turn(change):
    robot.right(0.6)
    time.sleep(0.5)
    robot.stop()

def Finddirection():
	path.reverse()
	for i in range(mindist - 1):
#	print(chardir[path[i]], ' ', end='')
		Track.append(path[len(path) - i - 1])

	print(' ')                
	Track.reverse()

	for i in range(len(Track)):
		print(chardir[Track[i]], ' ', end='')
	print(' ')               

def Printvisited():
	for i in range(N):
		for j in range(M):
			print(visited[i][j], ' ', end='')
		print(' ')               

def DFS(x, y,tx,ty, dir):
	# Arrive Target
	if x == tx and y == ty:
		# Arrive
		global mindist
		if visited[x][y] < mindist:
			mindist = visited[x][y]
			path.clear()
			path.append(dir)
			return 0
		else:
			return INF
	result = INF
	mindir = -1
	for i in range(4):
		nx = x + dx[i]
		ny = y + dy[i]
		if 0 <= nx < N and 0 <= ny < M:
			if matrix[nx][ny] == '1':
				if visited[nx][ny] == 0:
					visited[nx][ny] = visited[x][y] + 1 
				else:
					if visited[nx][ny] > visited[x][y] + 1:
						visited[nx][ny] = visited[x][y] + 1
					else:
						continue
				# Among 4 dir min distance append dir 
				cur = DFS(nx, ny, tx, ty, i)
				if result > cur:
					result = cur
					mindir = i
	if result != INF and dir != -1:
		path.append(dir)
	return result

# 0 : 현재 방향 그대로
# 1 : 왼쪽 방향으로 틀기
# 2 : 오른쪽 방향으로 틀기
# 3 : 뒤로 가기
# Changedir = [ [0, 3, 1, 2],	[3, 0, 2, 1],[2, 1, 0, 3],[1, 2, 3, 0]]

# Track index 0,1,2,3 : UP, DOWN, LEFT, RIGHT

def Drive(curx, cury):
	for Dir in Track:
		if(Changedir[curdir][Dir] == 0):
			step_forward()
		else:
			if Changedir[curdir][Dir] == 1:
				step_left()
			else if Changedir[curdir][Dir] == 2:
				step_right()
			step_forward()
			curdir = Dir

		if Dir == 0:
			curx--
		else if Dir == 1:
			curx++
		else if Dir == 2:
			cury--
		else if Dir == 3:
			cury++	

if __name__ == "__main__":

	while(True):
		# Input data from Server
		# info = ConnectServer()    return startRobot flag, current location, target location
		flag = True
		if(flag == True):
			curx = 0
			cury = 0
			tx = N - 1 
			ty = M - 1
			visited[curx][cury] = 1 
			# Path Search
			DFS(curx,cury, tx, ty, -1)
			visited = [[0]*M for _ in range(N)]			# Initialized Visted Map
			print(mindist)
			# Find Path. Track list has direction and destination info
			Finddirection()
			Drive(curx, cury)

			# Turn First Location
			Track.reverse()
			Drive(curx, cury)
		else:
			continue
