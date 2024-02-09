from MazeGenerator import maze,maze_solver,Color
from queue import PriorityQueue

def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2
    return abs(x1-x2) + abs(y1-y2)


def aStar(m):
    start=(m.rows,m.cols)
    curr_Cost={cell:float('inf') for cell in m.grid}
    curr_Cost[start]=0
    total_Cost={cell:float('inf') for cell in m.grid}
    total_Cost[start]=h(start,(1,1))

    cells_list=PriorityQueue()
    cells_list.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    while not cells_list.empty():
        currCell=cells_list.get()[2]
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_curr_Cost=curr_Cost[currCell]+1
                temp_total_Cost=temp_curr_Cost+h(childCell,(1,1))

                if temp_total_Cost < total_Cost[childCell]:
                    curr_Cost[childCell]= temp_curr_Cost
                    total_Cost[childCell]= temp_total_Cost
                    cells_list.put((temp_total_Cost,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
    finalPath={}
    cell=(1,1)
    while cell!=start:
        finalPath[aPath[cell]]=cell
        cell=aPath[cell]
    return finalPath

if __name__=='__main__':
    m=maze(10,10)
    m.CreateMaze(theme=Color.light)
    path=aStar(m)

    a=maze_solver(m,steps=True,color=Color.yellow)
    m.tracePath({a:path},delay=300)

    m.run()