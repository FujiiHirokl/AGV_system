import tkinter as tk
from tkinter import ttk

def show_selection():
    selected_option = var.get()
    if selected_option == 1:
        label.config(text="Option 1 selected", foreground="green")
    elif selected_option == 2:
        label.config(text="Option 2 selected", foreground="blue")
    elif selected_option == 3:
        label.config(text="Option 3 selected", foreground="red")

# ウィンドウを作成
window = tk.Tk()

# ラジオボタンの選択結果を格納するための変数を作成
var = tk.IntVar()

# 選択結果を表示するためのラベルを作成
label = ttk.Label(window, text="Please make a selection", foreground="gray")
label.pack(pady=10)

# ラジオボタンを作成
option1 = ttk.Radiobutton(window, text="Option 1", variable=var, value=1, command=show_selection)
option1.pack()

option2 = ttk.Radiobutton(window, text="Option 2", variable=var, value=2, command=show_selection)
option2.pack()

option3 = ttk.Radiobutton(window, text="Option 3", variable=var, value=3, command=show_selection)
option3.pack()

# ウィンドウを表示
window.mainloop()

