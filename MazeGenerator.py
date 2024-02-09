import random
from tkinter import *
from enum import Enum
from collections import deque

class Color(Enum):
    
    dark=('gray11','white')
    light=('white','black')
    black=('black','dim gray')
    red=('red3','tomato')
    green=('green4','pale green')
    blue=('DeepSkyBlue4','DeepSkyBlue2')
    yellow=('yellow2','yellow2')

class maze_solver:

    def __init__(self,theMaze,x=None,y=None,shape='square',goal=None,filled=True,steps=False,color:Color=Color.blue):

        self._theMaze=theMaze
        self.color=color
        if(isinstance(color,str)):
            if(color in Color.__members__):
                self.color=Color[color]
            else:
                raise ValueError(f'{color} is not a valid COLOR!')
        self.filled=filled
        self.shape=shape

        if x is None:x=theMaze.rows
        if y is None:y=theMaze.cols
        self.x=x
        self.y=y
        self.steps=steps
        self._theMaze._maze_solvers.append(self)
        if goal==None:
            self.goal=self._theMaze._goal
        else:
            self.goal=goal
        self._body=[]
        self.position=(self.x,self.y)
        
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,newX):
        self._x=newX
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,newY):
        self._y=newY
        w=self._theMaze._cell_width
        x=self.x*w-w+self._theMaze._LabWidth
        y=self.y*w-w+self._theMaze._LabWidth
        if self.shape=='square':
            if self.filled:
                self._coord=(y, x,y + w, x + w)
        else:
            self._coord=(y + w/2, x + 3*w/9,y + w/2, x + 3*w/9+w/4)

        if(hasattr(self,'_head')):
            if self.steps is False:
                self._theMaze._canvas.delete(self._head)
            else:
                if self.shape=='square':
                    self._theMaze._canvas.itemconfig(self._head, fill=self.color.value[1],outline="")
                    self._theMaze._canvas.tag_raise(self._head)
                    try:
                        self._theMaze._canvas.tag_lower(self._head,'ov')
                    except:
                        pass
                    if self.filled:
                        lll=self._theMaze._canvas.coords(self._head)
                        oldcell=(round(((lll[1]-26)/self._theMaze._cell_width)+1),round(((lll[0]-26)/self._theMaze._cell_width)+1))
                        self._theMaze._redrawCell(*oldcell,self._theMaze.theme)

                self._body.append(self._head)

            self._head=self._theMaze._canvas.create_rectangle(*self._coord,fill=self.color.value[0],outline='')#stipple='gray75'
            try:
                self._theMaze._canvas.tag_lower(self._head,'ov')
            except:
                    pass
            self._theMaze._redrawCell(self.x,self.y,theme=self._theMaze.theme)
        else:
            self._head=self._theMaze._canvas.create_rectangle(*self._coord,fill=self.color.value[0],outline='')#stipple='gray75'
            try:
                self._theMaze._canvas.tag_lower(self._head,'ov')
            except:
                pass
            self._theMaze._redrawCell(self.x,self.y,theme=self._theMaze.theme)
    @property
    def position(self):
        return (self.x,self.y)
    @position.setter
    def position(self,newpos):
        self.x=newpos[0]
        self.y=newpos[1]
        self._position=newpos
        
    def moveRight(self,event):
        if self._theMaze.maze_map[self.x,self.y]['E']==True:
            self.y=self.y+1
    def moveLeft(self,event):
        if self._theMaze.maze_map[self.x,self.y]['W']==True:
            self.y=self.y-1
    def moveUp(self,event):
        if self._theMaze.maze_map[self.x,self.y]['N']==True:
            self.x=self.x-1
            self.y=self.y
    def moveDown(self,event):
        if self._theMaze.maze_map[self.x,self.y]['S']==True:
            self.x=self.x+1
            self.y=self.y
            
class maze:
    def __init__(self,rows=10,cols=10):

        self.rows=rows
        self.cols=cols
        self.maze_map={}
        self.grid=[]
        self.path={} 
        self._cell_width=50  
        self._win=None 
        self._canvas=None
        self._maze_solvers=[]
        self.markCells=[]

    @property
    def grid(self):
        return self._grid
    @grid.setter        
    def grid(self,n):
        self._grid=[]
        y=0
        for n in range(self.cols):
            x = 1
            y = 1+y
            for m in range(self.rows):
                self.grid.append((x,y))
                self.maze_map[x,y]={'E':0,'W':0,'N':0,'S':0}
                x = x + 1 
    def _Open_East(self,x, y):

        self.maze_map[x,y]['E']=1
        if y+1<=self.cols:
            self.maze_map[x,y+1]['W']=1
    def _Open_West(self,x, y):
        self.maze_map[x,y]['W']=1
        if y-1>0:
            self.maze_map[x,y-1]['E']=1
    def _Open_North(self,x, y):
        self.maze_map[x,y]['N']=1
        if x-1>0:
            self.maze_map[x-1,y]['S']=1
    def _Open_South(self,x, y):
        self.maze_map[x,y]['S']=1
        if x+1<=self.rows:
            self.maze_map[x+1,y]['N']=1
    
    def CreateMaze(self,x=1,y=1,mazeComplexity=0,loadMaze=None,theme:Color=Color.dark):
        
        _stack=[]
        _closed=[]
        self.theme=theme
        self._goal=(x,y)
        if(isinstance(theme,str)):
            if(theme in Color.__members__):
                self.theme=Color[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')
            
        def blockedNeighbours(cell):
            n=[]
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d]==0:
                    if d=='E' and (cell[0],cell[1]+1) in self.grid:
                        n.append((cell[0],cell[1]+1))
                    elif d=='W' and (cell[0],cell[1]-1) in self.grid:
                        n.append((cell[0],cell[1]-1))
                    elif d=='N' and (cell[0]-1,cell[1]) in self.grid:
                        n.append((cell[0]-1,cell[1]))
                    elif d=='S' and (cell[0]+1,cell[1]) in self.grid:
                        n.append((cell[0]+1,cell[1]))
            return n
        
        def removeWallinBetween(cell1,cell2):
            if cell1[0]==cell2[0]:
                if cell1[1]==cell2[1]+1:
                    self.maze_map[cell1]['W']=1
                    self.maze_map[cell2]['E']=1
                else:
                    self.maze_map[cell1]['E']=1
                    self.maze_map[cell2]['W']=1
            else:
                if cell1[0]==cell2[0]+1:
                    self.maze_map[cell1]['N']=1
                    self.maze_map[cell2]['S']=1
                else:
                    self.maze_map[cell1]['S']=1
                    self.maze_map[cell2]['N']=1
                    
        def isCyclic(cell1,cell2):
            ans=False
            if cell1[0]==cell2[0]:
                if cell1[1]>cell2[1]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['S']==1 and self.maze_map[cell2]['S']==1:
                    if (cell1[0]+1,cell1[1]) in self.grid and self.maze_map[(cell1[0]+1,cell1[1])]['E']==1:
                        ans= True
                if self.maze_map[cell1]['N']==1 and self.maze_map[cell2]['N']==1:
                    if (cell1[0]-1,cell1[1]) in self.grid and self.maze_map[(cell1[0]-1,cell1[1])]['E']==1:
                        ans= True
            else:
                if cell1[0]>cell2[0]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['E']==1 and self.maze_map[cell2]['E']==1:
                    if (cell1[0],cell1[1]+1) in self.grid and self.maze_map[(cell1[0],cell1[1]+1)]['S']==1:
                        ans= True
                if self.maze_map[cell1]['W']==1 and self.maze_map[cell2]['W']==1:
                    if (cell1[0],cell1[1]-1) in self.grid and self.maze_map[(cell1[0],cell1[1]-1)]['S']==1:
                        ans= True
            return ans
        
        _stack.append((x,y))
        _closed.append((x,y))
        biasLength=2 

        bias=0

        while len(_stack) > 0:
            cell = []
            bias+=1
            if(x , y +1) not in _closed and (x , y+1) in self.grid:
                cell.append("E")
            if (x , y-1) not in _closed and (x , y-1) in self.grid:
                cell.append("W")
            if (x+1, y ) not in _closed and (x+1 , y ) in self.grid:
                cell.append("S")
            if (x-1, y ) not in _closed and (x-1 , y) in self.grid:
                cell.append("N") 
            if len(cell) > 0:    

                bias=0
                current_cell = (random.choice(cell))
                if current_cell == "E":
                    self._Open_East(x,y)
                    self.path[x, y+1] = x, y
                    y = y + 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "W":
                    self._Open_West(x, y)
                    self.path[x , y-1] = x, y
                    y = y - 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "N":
                    self._Open_North(x, y)
                    self.path[(x-1 , y)] = x, y
                    x = x - 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "S":
                    self._Open_South(x, y)
                    self.path[(x+1 , y)] = x, y
                    x = x + 1
                    _closed.append((x, y))
                    _stack.append((x, y))

            else:
                x, y = _stack.pop()


        if mazeComplexity!=0:
            
            x,y=self.rows,self.cols
            pathCells=[(x,y)]
            while x!=self.rows or y!=self.cols:
                x,y=self.path[(x,y)]
                pathCells.append((x,y))
            notPathCells=[i for i in self.grid if i not in pathCells]
            random.shuffle(pathCells)
            random.shuffle(notPathCells)
            pathLength=len(pathCells)
            notPathLength=len(notPathCells)
            count1,count2=pathLength/3*mazeComplexity/100,notPathLength/3*mazeComplexity/100

            count=0
            i=0
            while count<count1: 
                if len(blockedNeighbours(pathCells[i]))>0:
                    cell=random.choice(blockedNeighbours(pathCells[i]))
                    if not isCyclic(cell,pathCells[i]):
                        removeWallinBetween(cell,pathCells[i])
                        count+=1
                    i+=1
                        
                else:
                    i+=1
                if i==len(pathCells):
                    break
            if len(notPathCells)>0:
                count=0
                i=0
                while count<count2:
                    if len(blockedNeighbours(notPathCells[i]))>0:
                        cell=random.choice(blockedNeighbours(notPathCells[i]))
                        if not isCyclic(cell,notPathCells[i]):
                            removeWallinBetween(cell,notPathCells[i])
                            count+=1
                        i+=1
                            
                    else:
                        i+=1
                    if i==len(notPathCells):
                        break
            # self.path=BFS((self.rows,self.cols))

        self._drawMaze(self.theme)
        maze_solver(self,*self._goal,shape='square',filled=True,color=Color.green)


    def _drawMaze(self,theme):
        
        self._LabWidth=26
        self._win=Tk()
        self._win.state('zoomed')
        self._win.title('Maze in Python')
        
        scr_width=self._win.winfo_screenwidth()
        scr_height=self._win.winfo_screenheight()
        self._win.geometry(f"{scr_width}x{scr_height}+0+0")
        self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0])
        self._canvas.pack(expand=YES, fill=BOTH)

        k=3.25
        if self.rows>=95 and self.cols>=95:
            k=0
        elif self.rows>=80 and self.cols>=80:
            k=1
        elif self.rows>=70 and self.cols>=70:
            k=1.5
        elif self.rows>=50 and self.cols>=50:
            k=2
        elif self.rows>=35 and self.cols>=35:
            k=2.5
        elif self.rows>=22 and self.cols>=22:
            k=3
        self._cell_width=round(min(((scr_height-self.rows-k*self._LabWidth)/(self.rows)),((scr_width-self.cols-k*self._LabWidth)/(self.cols)),90),3)

        if self._win is not None:
            if self.grid is not None:
                for cell in self.grid:
                    x,y=cell
                    w=self._cell_width
                    x=x*w-w+self._LabWidth
                    y=y*w-w+self._LabWidth
                    if self.maze_map[cell]['E']==False:
                        l=self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['W']==False:
                        l=self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['N']==False:
                        l=self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['S']==False:
                        l=self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1],tag='line')

    def _redrawCell(self,x,y,theme):

        w=self._cell_width
        cell=(x,y)
        x=x*w-w+self._LabWidth
        y=y*w-w+self._LabWidth
        if self.maze_map[cell]['E']==False:
            self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['W']==False:
            self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['N']==False:
            self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1])
        if self.maze_map[cell]['S']==False:
            self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1])


    _tracePathList=[]
    def _tracePathSingle(self,a,p,showMarked,delay):

        w=self._cell_width
        if((a.x,a.y) in self.markCells and showMarked):
            w=self._cell_width
            x=a.x*w-w+self._LabWidth
            y=a.y*w-w+self._LabWidth
            self._canvas.create_oval(y + w/2.5+w/20, x + w/2.5+w/20,y + w/2.5 +w/4-w/20, x + w/2.5 +w/4-w/20,fill='red',outline='red',tag='ov')
            self._canvas.tag_raise('ov')
       
        if (a.x,a.y)==(a.goal):
            del maze._tracePathList[0][0][a]
            if maze._tracePathList[0][0]=={}:
                del maze._tracePathList[0]
                if len(maze._tracePathList)>0:
                    self.tracePath(maze._tracePathList[0][0],delay=maze._tracePathList[0][2])

        if(type(p)==dict):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                return

            a.x,a.y=p[(a.x,a.y)]

        if (type(p)==str):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                if maze._tracePathList[0][0]=={}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList)>0:
                        self.tracePath(maze._tracePathList[0][0],delay=maze._tracePathList[0][2])

            if a.shape=='square':    
                move=p[0]
                if move=='E':
                    if a.y+1<=self.cols:
                        a.y+=1
                elif move=='W':
                    if a.y-1>0:
                        a.y-=1
                elif move=='N':
                    if a.x-1>0:
                        a.x-=1
                        a.y=a.y
                elif move=='S':
                    if a.x+1<=self.rows:
                        a.x+=1
                        a.y=a.y
                elif move=='C':
                    a._RCW()
                elif move=='A':
                    a._RCCW()
                p=p[1:]
        if (type(p)==list):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                if maze._tracePathList[0][0]=={}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList)>0:
                        self.tracePath(maze._tracePathList[0][0],delay=maze._tracePathList[0][2])

            a.x,a.y=p[0]
            del p[0]

        self._win.after(delay, self._tracePathSingle,a,p,showMarked,delay)    

    def tracePath(self,d,delay=300,showMarked=False):

        self._tracePathList.append((d,delay))
        if maze._tracePathList[0][0]==d: 
            for a,p in d.items():
                if a.goal!=(a.x,a.y) and len(p)!=0:
                    self._tracePathSingle(a,p,showMarked,delay)
    def run(self):
        self._win.mainloop()