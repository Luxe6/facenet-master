import tkinter as tk

global i
i = 0


def refreshText():
    global i
    i += 1
    text1.delete(0.0, tk.END)
    text1.insert(tk.INSERT, i)
    text1.update()
    windows.after(1000, refreshText)

windows = tk.Tk()
windows.geometry('500x500')  ## 规定窗口大小500*500像素
#windows.resizable(False, False)  ## 规定窗口不可缩放

li = ['C', 'python', 'php', 'html', 'SQL', 'java']
movie = ['CSS', 'jQuery', 'Bootstrap']
li.append('B')
li.append("C")
listb = tk.Listbox(windows)  # 创建两个列表组件
listb2 = tk.Listbox(windows)
for item in li:  # 第一个小部件插入数据
    listb.insert(0, item)

for item in movie:  # 第二个小部件插入数据
    listb2.insert(0, item)

listb.pack()  # 将小部件放置到主窗口中
listb2.pack()

text1 = tk.Text(windows, width=15, height=1)
text1.pack()
windows.after(1000, refreshText)
windows.mainloop()
