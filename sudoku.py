from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from dokusan import generators,solvers,renderers
import numpy as np
from dokusan.boards import BoxSize, Sudoku
root =tk.Tk()
root.title("Sudoku")
fts=Font(family='Tohoma',size=14,weight="bold")

puzzle = tk.Frame(root, bg='white')
puzzle.pack()

frames = []
for i in range (9):
    frames.append(tk.Frame(puzzle, highlightbackground='light blue', highlightcolor='light blue', highlightthickness=1))
    frames[i].grid(row = i // 3, column = i % 3, sticky='nsew')

bt = [[Button() for _ in range(9)] for _ in range(9)]
cnt = [1]
pre = [None]

def on_click(i, j, b):
    color = ['yellow', 'white']
    color2 = ['#0047ab', 'gray']
    color3 = ['green', 'white']
    if pre[0] != b and b['bg'] not in ('yellow', 'white'):
        cnt[0] ^= 1
    if pre[0] != None and pre[0] != b and pre[0]['bg'] == 'green':
        cnt[0] ^= 1
    if b['bg'] in color2:
        for k in range(9):
            for l in range(9):
                if bt[k][l]['bg'] in color or bt[k][l]['bg'] in color3:
                    bt[k][l].config(bg='white')
                if bt[k][l]['bg'] in color2:
                    bt[k][l].config(bg='gray')
        for k in range(9):
            for l in range(9):
                if bt[k][l]['text'] == b['text'] and bt[k][l]['bg'] == 'gray':
                    bt[k][l].config(bg=color2[cnt[0]])
                if (k == i and l == j) or bt[k][l]['bg'] in color2:
                    continue
                if k == i or l == j:
                    bt[k][l].config(bg=color[cnt[0]])
        cnt[0] ^= 1
        pre[0] = b
        return
    if b['bg'] in ('white', 'yellow', 'green'):
        check_ = False
        for k in range(9):
            for l in range(9):
                if bt[k][l]['bg'] in ('green', 'yellow'):
                    check_ = True
                if bt[k][l]['bg'] in color or bt[k][l]['bg'] in color3:
                    bt[k][l].config(bg='white')
                if bt[k][l]['bg'] in color2:
                    bt[k][l].config(bg='gray')
        if b['text'] == '' or b['bg'] == 'white':
            b.config(bg=color3[cnt[0] ^ 1])
        cnt[0] ^= 1
        pre[0] = b
        return
    if b['bg'] == 'red':
        b.config(bg='white', text='')
        cnt[0] ^= 1
        pre[0] = b
        return
    cnt[0] ^= 1
    pre[0] = b


for i in range(0, 9):
    for j in range(0, 9):
        bt[i][j] = Button(frames[i // 3 * 3 + j // 3], width=6, height=3, command=lambda i=i, j=j: on_click(i, j, bt[i][j]))
        bt[i][j].grid(row = i % 3,column = j % 3)

def get_key(k):
    cnt[0] = 1
    print(k['text'])
    for i in range(9):
        for j in range(9):
            if(bt[i][j]['bg'] == 'green'):
                if (k['text'] != 'DEL'):
                    bt[i][j].config(text = k['text'], bg = 'white')
                else:
                    bt[i][j].config(text = '', bg = 'white')

frame_key = tk.Frame(root)
frame_key.pack(pady = 30)
keyboards = [Button() for _ in range(10)]
for i in range(9):
    keyboards[i] = Button(frame_key, width=6, height=3, text=str(i + 1), command=lambda i=i: get_key(keyboards[i]))
    keyboards[i].grid(row = 0, column = i)
keyboards[9] = Button(frame_key, width=6, height=3, text='DEL', command=lambda: get_key(keyboards[9]))
keyboards[9].grid(row = 0, column = 10)

def generator():
    global solution,sudoku1,error
    cnt[0] = 1
    pre[0] = None
    er.config(text="ERROR: 0")
    error=0
    temp=[[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            bt[i][j].config(state=NORMAL,bg="white")
            bt[i][j].config(text="")
    gnrt=generators.random_sudoku(avg_rank=250)
    sudoku=np.array(list(str(gnrt)))
    sudoku1=sudoku.reshape(9,9)
    for i in range(9):
        for j in range(9):
            temp[i][j]=int(sudoku1[i][j])
    for i in range(9):
        for j in range(9):
            if sudoku1[i][j]!="0":
                bt[i][j].config(text=sudoku1[i][j], bg = "gray")
            else:
                bt[i][j].config(bg='white')
    temp1 = Sudoku.from_list(temp,box_size=BoxSize(3, 3),)
    temp2 = solvers.backtrack(temp1)
    solution=np.array(list(str(temp2))).reshape(9,9)
    # print(solution)

def check():
    color2 = ['#0047ab', 'gray']
    for k in range(0, 9):
        for l in range(0, 9):
            if(bt[k][l]['bg'] == 'yellow'):
                bt[k][l].config(bg = 'white')
            if (bt[k][l]['bg'] in color2):
                bt[k][l].config(bg = 'gray')
    global solution,sudoku1,error
    dem=0
    so=['1','2','3','4','5','6','7','8','9']
    demso=[0 for i in range (9)]
    for i in range(9):
        for j in range(9):
            temp = bt[i][j]['text']
            if temp in so:  
                demso[int(temp)-1]+=1 
            if temp!="" and temp!=sudoku1[i][j]:
                if temp != solution[i][j]:
                    if bt[i][j]["bg"] != "red":
                        error += 1
                        er.config(text="ERROR: "+str(error))
                    bt[i][j].config(bg="red")
                else: 
                    bt[i][j].config(bg="gray") 
            if temp!="": dem+=1
            if temp=="": bt[i][j].config(bg="white")
    for i in range(9):
        for j in range(9):
            if demso[j]==9:
                if bt[i][j]["text"] == str(j+1):
                    bt[i][j].config(state=NORMAL)
                    bt[i][j].config(bg="gray")
    if error==3:
        for i in range(9):
            for j in range(9):
                bt[i][j].config(state=DISABLED)
        messagebox.showinfo("END","LOSE")
    
    elif dem==81:
        for i in range(9):
            for j in range(9):
                bt[i][j].config(state=DISABLED)
        messagebox.showinfo("END","Win")

conf_frame = tk.Frame(root)
conf_frame.pack(pady=0)
er=Label(conf_frame,width=12,height=0,font=fts)
er.grid(row=0, column=15)
er.config(text="ERROR: 0")
btreset=Button(conf_frame,text="reset",width=10, height=5, command = generator)
btreset.grid(row=0, column=0)
btcheck=Button(conf_frame, text="check",width=10, height=5, command = check)
btcheck.grid(row=0, column=30)

generator()
root.mainloop()
