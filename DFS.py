from MazeGenerator import maze,maze_solver,Color

def DFS(m):
    start=(m.rows,m.cols)
    explored=[start]
    cells_list=[start]
    dfsPath={}
    while len(cells_list)>0:
        currCell=cells_list.pop()
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in explored:
                    continue
                explored.append(childCell)
                cells_list.append(childCell)
                dfsPath[childCell]=currCell
    finalPath={}
    cell=(1,1)
    while cell!=start:
        finalPath[dfsPath[cell]]=cell
        cell=dfsPath[cell]
    return finalPath


if __name__=='__main__':
    m=maze(10,10)
    m.CreateMaze(mazeComplexity=0,theme=Color.light)
    path=DFS(m)
    a=maze_solver(m,steps=True,color=Color.yellow)
    m.tracePath({a:path},delay=300)

    m.run()