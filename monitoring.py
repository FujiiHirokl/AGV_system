import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk

# 初期_radius変数をグローバル変数として定義
initial_radius = 0
def monitaring():
    # 初期円の半径と増加するサイズ
    global initial_radius
    max_radius = 80
    delta = 1
    animation_interval = 10


    def draw_circle(canvas, x, y, radius):
        canvas.delete("circle")
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="blue", tags="circle")

    def animate():
        global initial_radius
        initial_radius += delta
        if initial_radius > max_radius:
            time_event.time_event()
            initial_radius = 0
        x_text = time_event.x_point
        y_text = time_event.y_point
        if x_text and y_text:
            x = int(x_text)
            y = int(y_text)
            draw_circle(canvas, x, y, initial_radius)
            canvas.delete("car")
            canvas.create_image(x, y, anchor=tk.CENTER, image=center_image, tags="car")
        window.after(animation_interval, animate)

    def set_circle():
        print(123)

    def exit_program():
        print(111)

    window = tk.Toplevel()
    window.title("データ取得アプリ")
    window.geometry("900x650")

    canvas = tk.Canvas(window, width=900, height=549)
    canvas.pack()

    image_path = "car.png"
    original_image = Image.open(image_path)
    new_width = 30
    new_height = 30
    resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)

    background_image = tk.PhotoImage(file="image.jpg")
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    center_image = ImageTk.PhotoImage(resized_image)

    set_button = tk.Button(window, text="円を設定", command=set_circle)
    set_button.pack()

    # メニューバーを作成
    menubar = Menu(window)
    window.config(menu=menubar)

    # ファイルメニューを作成
    file_menu = Menu(menubar)
    menubar.add_cascade(label="ファイル", menu=file_menu)

    # 終了オプションをファイルメニューに追加
    file_menu.add_command(label="終了", command=exit_program)

    animate()
    window.mainloop()
    
class time_event:
    x_point = 100
    y_point = 100

    @classmethod
    def set_x_point(cls, new_x):
        cls.x_point = new_x
        
    @classmethod
    def set_y_point(cls, new_y):
        cls.y_point = new_y

    def time_event():
        if not hasattr(time_event, "count"):
            time_event.count = 0
        time_event.count += 2
        time_event.set_x_point(200)
        time_event.set_y_point(200 + time_event.count)
        print(1)
