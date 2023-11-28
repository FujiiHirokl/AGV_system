import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk
import os
from urllib.parse import parse_qs
import mysql.connector
from mysql.connector import Error
import math


db_pass = os.getenv('DB_PASSWORD')

# 初期_radius変数をグローバル変数として定義
initial_radius = 0
def monitaring():
    # 初期円の半径と増加するサイズ
    global initial_radius
    max_radius = 80
    delta = 1
    animation_interval = 10
    angle = 120


    def draw_circle(canvas, x, y, radius):
        canvas.delete("circle")
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="blue", tags="circle")
        
    def rotate_image(image_id, photo):
        """画像を回転させます。

        Args:
            image_id (int): 画像オブジェクトのID
            photo (tk.PhotoImage): 回転する画像
        """
        nonlocal angle

        rotated_image = resized_image.rotate(360 - angle + 180, expand=True)
        photo.image = ImageTk.PhotoImage(rotated_image)
        canvas.itemconfigure(image_id, image=photo.image)

    def animate():
        global initial_radius
        initial_radius += delta
        if initial_radius > max_radius:
            time_event.time_event()
            initial_radius = 0
            canvas.delete("battery")
            if time_event.battery_event() == 1:
                canvas.create_image(840, 60, anchor=tk.CENTER, image=battery_image1, tags="battery")
            elif time_event.battery_event() == 2:
                canvas.create_image(840, 60, anchor=tk.CENTER, image=battery_image2, tags="battery")
            elif time_event.battery_event() == 3:
                canvas.create_image(840, 60, anchor=tk.CENTER, image=battery_image3, tags="battery")
            elif time_event.battery_event() == 4:
                canvas.create_image(840, 60, anchor=tk.CENTER, image=battery_image4, tags="battery")
            elif time_event.battery_event() == 5:
                canvas.create_image(840, 60, anchor=tk.CENTER, image=battery_image5, tags="battery")  
        x_text = time_event.x_point
        y_text = time_event.y_point
        if x_text and y_text:
            x = int(x_text)
            y = int(y_text)
            draw_circle(canvas, x, y, initial_radius)
            canvas.delete("car")
            car= canvas.create_image(x, y, anchor=tk.CENTER, image=center_image, tags="car")
            rotate_image(car, center_image)              
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
    
    # batteryフル画像
    image_path_additional = "battery_5.png"  # 追加画像のパスに置き換えてください
    original_image_additional = Image.open(image_path_additional)
    new_width_additional = 46  # 必要に応じてサイズを調整してください
    new_height_additional = 95  # 必要に応じてサイズを調整してください
    resized_image_additional = original_image_additional.resize((new_width_additional, new_height_additional), Image.ANTIALIAS)
    battery_image5 = ImageTk.PhotoImage(resized_image_additional)
    
    # battery4画像
    image_path_additional = "battery_4.png"  # 追加画像のパスに置き換えてください
    original_image_additional = Image.open(image_path_additional)
    new_width_additional = 46  # 必要に応じてサイズを調整してください
    new_height_additional = 95  # 必要に応じてサイズを調整してください
    resized_image_additional = original_image_additional.resize((new_width_additional, new_height_additional), Image.ANTIALIAS)
    battery_image4 = ImageTk.PhotoImage(resized_image_additional)
    
    # battery3画像
    image_path_additional = "battery_3.png"  # 追加画像のパスに置き換えてください
    original_image_additional = Image.open(image_path_additional)
    new_width_additional = 46  # 必要に応じてサイズを調整してください
    new_height_additional = 95  # 必要に応じてサイズを調整してください
    resized_image_additional = original_image_additional.resize((new_width_additional, new_height_additional), Image.ANTIALIAS)
    battery_image3 = ImageTk.PhotoImage(resized_image_additional)
    
    # batter23画像
    image_path_additional = "battery_2.png"  # 追加画像のパスに置き換えてください
    original_image_additional = Image.open(image_path_additional)
    new_width_additional = 46  # 必要に応じてサイズを調整してください
    new_height_additional = 95  # 必要に応じてサイズを調整してください
    resized_image_additional = original_image_additional.resize((new_width_additional, new_height_additional), Image.ANTIALIAS)
    battery_image2 = ImageTk.PhotoImage(resized_image_additional)
    
    # batter23画像
    image_path_additional = "battery_1.png"  # 追加画像のパスに置き換えてください
    original_image_additional = Image.open(image_path_additional)
    new_width_additional = 46  # 必要に応じてサイズを調整してください
    new_height_additional = 95  # 必要に応じてサイズを調整してください
    resized_image_additional = original_image_additional.resize((new_width_additional, new_height_additional), Image.ANTIALIAS)
    battery_image1 = ImageTk.PhotoImage(resized_image_additional)


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
    x_point = 0
    y_point = 0

    @classmethod
    def set_x_point(cls, new_x):
        cls.x_point = new_x
        
    @classmethod
    def set_y_point(cls, new_y):
        cls.y_point = new_y

    def time_event():
        try:
            # データベースに接続
            connector = mysql.connector.connect(
                user='root', 
                password=db_pass,
                host='localhost', 
                database='AGVcondition', 
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            cursor = connector.cursor()
            
            # SELECTクエリの作成と実行
            select_query = "SELECT Coordinate_x, Coordinate_y FROM AGVstatus WHERE id = 1;"
            cursor.execute(select_query)
            
            # 結果の取得
            result = cursor.fetchone()
            
            # リソースを解放
            cursor.close()
            connector.close()

            time_event.set_x_point(result[0])
            time_event.set_y_point(result[1])
            
            #値調節要SQL
            
            #UPDATE coordinates SET x = 300, y = 250 WHERE id = 1;
        except Error as e:
            # エラーメッセージを返す
            return {"error": str(e)}
    
    def battery_event():
        try:
            # データベースに接続
            connector = mysql.connector.connect(
                user='root', 
                password=db_pass,
                host='localhost', 
                database='AGVcondition', 
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            cursor = connector.cursor()
            
            # SELECTクエリの作成と実行
            select_query = "SELECT Battery FROM AGVstatus WHERE id = 1;"
            cursor.execute(select_query)
            
            # 結果の取得
            result = cursor.fetchone()
            
            # リソースを解放
            cursor.close()
            connector.close()
            #バッテリー状況を５段階で表示
            if result[0] >= 100:
                num_bat = 5
            elif result[0] >= 80:
                num_bat = 4
            elif result[0] >= 60:
                num_bat = 3
            elif result[0] >= 40:
                num_bat = 2
            elif result[0] >= 20:
                num_bat = 1
            else:
                num_bat = 0 
            return num_bat      
        except Error as e:
            return {"error": str(e)}
