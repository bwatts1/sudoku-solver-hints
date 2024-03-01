import numpy as np
from tkinter import *
from tkinter import messagebox
import copy
done = False
done1 = False

#sets the users numbers given in sudoku
def set1():
    global grid_solve
    reset()
    row = 0
    column = 0
    for entry in entries:
        result = entry.get()
        try:
            if result == '' or (ord(result) >= 49 and ord(result) <= 57):
                #when entry is reset leave it the value as null
                if result == '': pass
                #when entry is not reset changes the null value to the entered value
                else: grid[row,column] = result
                column+=1
                #when its on the last column goes to the next row
                if column//9 == 1:
                    row += 1
                    column = 0
            #if user inputs non integer characters will return message
            else:messagebox.showinfo('information', 'Incorrect entry type.')
        #if user inputs numbers larger than 2 characters will return message
        except: messagebox.showinfo('information', 'Only integers between 1-9 please.')
    grid_solve = np.array(grid)
#fills in the posible solutions along a row
def pr(row,row_num):
    #checks to see which values are taken in the row
    for n in range(9):
        if row[n] in rows_pos[str(row_num)]:
            rows_pos[str(row_num)].remove(row[n])
    #adds the possibilities to each empty entry
    for n in range(9):
        if np.isnan(row[n]):
            rows_hint[(row_num-1,n)] = rows_pos[str(row_num)]
#fills in the posible solutions along a column
            
def pc(column,column_num):
    #checks to see which values are taken in the column
    for n in range(9):
        if column[n] in columns_pos[str(column_num)]:
            columns_pos[str(column_num)].remove(column[n])
    #adds the possibilities to each empty entry
    for n in range(9):
        if np.isnan(column[n]):
            columns_hint[(n,column_num-1)] = columns_pos[str(column_num)]
            
#fills in the posible solutions in a box
def pb(box,box_num):
    #checks to see which values are taken in the box
    for n in range(9):
        if box[n] in boxes_pos[str(box_num)]:
            boxes_pos[str(box_num)].remove(box[n])
    n = 0
    #adds the possibilities to each empty entry
    for y in range(3):
        for x in range(3):
            if np.isnan(box[n]):
                if box_num < 4: boxes_hint[(y,x+(box_num-1)*3)] = boxes_pos[str(box_num)]
                elif box_num<7: boxes_hint[(y+3,x+(box_num -4)*3)] = boxes_pos[str(box_num)]
                else: boxes_hint[(y+6,x+(box_num -7)*3)] = boxes_pos[str(box_num)]
            n+=1
            
#creates a new window to display the results
def new_window_hint(x):
    newWindow = Toplevel(root)
    newWindow.title("Hint")
    newWindow.geometry("903x910")
    #sets the format of the new requested answers
    for row in range(9):
        for column in range(9):
            #checks to see if user wanted answers or hints and formats respectively
            if x == 0: #hints
                value = grid[column,row]
                #hints are red
                if np.isnan(value):
                    value = str(hints[(column,row)])
                    en = Label(newWindow, text = value, bg = "white",fg = "#FF0000", width = 14, height = 7,relief = "solid").place(x = row*100,y = column*100)
                #answers are blue
                else: en = Label(newWindow, text = int(value), bg = "white",fg = "#000080", width = 14, height = 7,relief = "solid").place(x = row*100,y = column*100)
            else: #answers
                value = grid_solve[column,row]
                en = Label(newWindow, text = int(value), bg = "white",fg = "#000080", width = 14, height = 7,relief = "solid").place(x = row*100,y = column*100)

#gets hints for the user
def hint(): 
    global done1
    #checks and see if the hints for the sudoku had been solved before
    if done1 == True: new_window_hint(0)
    #if not done gets the hints
    else:
        #format the rows
        for x in range(9):
            row = grid[x, :]
            pr(row,x+1)
        #format the columns
        for y in range(9):
            column = grid[:, y]
            pc(column,y+1)
        box_num = 0
        #format the boxes
        for y in range(3):
            for b in range(3):
                box = [grid[3*y,3*b%9],grid[3*y,3*b%9+1],grid[3*y,3*b%9+2],
                       grid[3*y+1,3*b%9],grid[3*y+1,3*b%9+1],grid[3*y+1,3*b%9+2],
                       grid[3*y+2,3*b%9],grid[3*y+2,3*b%9+1],grid[3*y+2,3*b%9+2]]
                pb(box,box_num+1)
                box_num+=1
        for key in rows_hint:
            try:
                r = rows_hint[key]
            except: a = []
            try:
                c = columns_hint[key]
            except: b = []
            try:
                b = boxes_hint[key]
            except: c = []
            #get the comman elements at a square by its row , box, and column
            hints[key] = list(r & b & c)
            #checks to see if there is only one possibility and replaces that spot in the suduko as the answer
            if len(hints[key]) == 1:
                grid[key[0],key[1]]=hints[key][0]
        done1 = True
        new_window_hint(0)

#solves the suduko for the user
def solve():
    #checks and see if the sudoku had been solved before
    if done == True: new_window_hint(1)
    else:
        try:
            #if sudoku inputed cant be solved it will display message
            if len(entries) == 0 or solveSudoku(grid_solve,0,0) == False: messagebox.showinfo('information', 'No solution available.')
            else: new_window_hint(1)
        #if sudoku has not been set it will display this message
        except: messagebox.showinfo('information', 'Board has not been set.')

# https://www.geeksforgeeks.org/sudoku-backtracking-7/ 1/20/2024
# The below code was contributed by sudhanshgupta2019a with minor tweaks by me.

#fills in the grid useing brute force to check and see if the guess is correct
def solveSudoku(grid_solve, row, col):
    N = 9
    #sees if we reached the end of the sudoku if so return True
    if (row == N - 1 and col == N):
        return True
    #when we reach the last column we move to the next row
    if col == N:
        row += 1
        col = 0
    #checks to see if a value is already filled if so goto the next column
    if grid_solve[row][col] > 0:
        return solveSudoku(grid_solve, row, col + 1)
    #checks every possible number from 1-9 to see if it goes in the blank
    for num in range(1, N + 1, 1):
        #checks to see if the number was safe
        if isSafe(grid_solve, row, col, num):
            grid_solve[row][col] = num
            #checks for the next possibole column
            #if it gets through all columns returns
            #true and sets this section as done
            if solveSudoku(grid_solve, row, col + 1):
                done = True
                return True
        #if it gets to this point it removed the guess value
        #and starts again with the next value
        grid_solve[row][col] = 0
    #if it gets to the end there is no possible solution
    return False

#checks to see if number is safe to be asigned given the row and column
def isSafe(grid_solve, row, col, num):
    #checks to see if safe in row
    for x in range(9):
        if grid_solve[row][x] == num:
            return False
    #checks to see if safe in column
    for x in range(9):
        if grid_solve[x][col] == num:
            return False
    #specifies the box
    startRow = row - row % 3
    startCol = col - col % 3
    #sees if the box is safe
    for i in range(3):
        for j in range(3):
            if grid_solve[i + startRow][j + startCol] == num:
                return False
    # if everything is safe it returns true
    return True

# The above code was contributed by sudhanshgupta2019a with minor tweaks by me.

#reset the arrays
def reset():
    #all the global values needed
    global grid
    global rows_pos
    global rows_hint
    global columns_pos
    global columns_hint
    global rows_pos
    global boxes_pos
    global boxes_hint
    global hints
    global entries
    global done
    global done1
    done = False
    done1 = False
    grid = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                     [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]])
    
#test case so you can test it without having to set it
#     grid = np.array([[np.nan, np.nan, np.nan,  5, np.nan, np.nan,  4,  2, np.nan],
#                      [np.nan,  5, np.nan, np.nan, np.nan,  9,  6, np.nan, np.nan],
#                      [ 6,  8,  7, np.nan, np.nan, np.nan, np.nan,  1,  5],
#                      [np.nan, np.nan,  9,  6,  5,  8,  1,  3,  2,],
#                      [np.nan, np.nan,  2, np.nan,  4, np.nan, np.nan, np.nan,  8],
#                      [np.nan, np.nan, np.nan, np.nan,  1,  9, np.nan,  6,  4],
#                      [ 3, np.nan, np.nan, np.nan, np.nan,  2, np.nan, np.nan, np.nan],
#                      [ 7, np.nan, np.nan, np.nan,  1, np.nan,  3,  4,  9],
#                      [ 8,  9,  1, np.nan, np.nan,  7, np.nan,  5, np.nan]]) 

    #used sets to minimalize time complexity when using "in"
    #as well as to ensure no dublicates
    rows_pos = {'1':{1,2,3,4,5,6,7,8,9},
            '2':{1,2,3,4,5,6,7,8,9},
            '3':{1,2,3,4,5,6,7,8,9},
            '4':{1,2,3,4,5,6,7,8,9},
            '5':{1,2,3,4,5,6,7,8,9},
            '6':{1,2,3,4,5,6,7,8,9},
            '7':{1,2,3,4,5,6,7,8,9},
            '8':{1,2,3,4,5,6,7,8,9},
            '9':{1,2,3,4,5,6,7,8,9},}

    rows_hint = {}

    columns_pos = {'1':{1,2,3,4,5,6,7,8,9},
            '2':{1,2,3,4,5,6,7,8,9},
            '3':{1,2,3,4,5,6,7,8,9},
            '4':{1,2,3,4,5,6,7,8,9},
            '5':{1,2,3,4,5,6,7,8,9},
            '6':{1,2,3,4,5,6,7,8,9},
            '7':{1,2,3,4,5,6,7,8,9},
            '8':{1,2,3,4,5,6,7,8,9},
            '9':{1,2,3,4,5,6,7,8,9},}

    columns_hint = {}

    boxes_pos = {'1':{1,2,3,4,5,6,7,8,9},
            '2':{1,2,3,4,5,6,7,8,9},
            '3':{1,2,3,4,5,6,7,8,9},
            '4':{1,2,3,4,5,6,7,8,9},
            '5':{1,2,3,4,5,6,7,8,9},
            '6':{1,2,3,4,5,6,7,8,9},
            '7':{1,2,3,4,5,6,7,8,9},
            '8':{1,2,3,4,5,6,7,8,9},
            '9':{1,2,3,4,5,6,7,8,9},}

    boxes_hint = {}
    hints = {}
    
entries = []
reset()
root = Tk()
root.title("sudoku Solver")
root.geometry("325x400")


#sets the overall design of the sudoku board
for row in range(9):
    for column in range(9):
        en = Entry(root, width = 5)
        if (row+1)%3 == 0 and (column+1)%3 == 0:
            en.grid(row=row, column=column, ipady=10, padx = (1,5),pady = (1,5))
        elif (row+1)%3 == 0:
            en.grid(row=row, column=column, ipady=10,pady = (1,5))
        elif (column+1)%3 == 0:
            en.grid(row=row, column=column,ipady=10,padx = (1,5))
        else:
            en.grid(row=row, column=column,ipady=10)
        entries.append(en)
button=Button(root,text=" Set ",command=set1).grid(row=10,column=3)
button2=Button(root,text="Hints",command=hint).grid(row=10,column=4)
button3=Button(root,text="Solve",command=solve).grid(row=10,column=5)
root.mainloop()
