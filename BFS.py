from MazeGenerator import maze,maze_solver,Color

def BFS(m):
    start=(m.rows,m.cols)
    cells_list=[start]
    explored=[start]
    bfsPath={}
    while len(cells_list)>0:
        currCell=cells_list.pop(0)
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                if childCell in explored:
                    continue
                cells_list.append(childCell)
                explored.append(childCell)
                bfsPath[childCell]=currCell
    finalPath={}
    cell=(1,1)
    while cell!=start:
        finalPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
    return finalPath

if __name__=='__main__':
    m=maze(15,15)
    m.CreateMaze(mazeComplexity=40,theme=Color.light)
    path=BFS(m)
    a=maze_solver(m,steps=True,filled=True,color=Color.yellow)
    m.tracePath({a:path},delay=300)
    m.run()