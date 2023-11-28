import tkinter as tk
from PIL import Image, ImageTk
import os
import mysql.connector
from mysql.connector import Error
import create_image

# 環境変数からデータベースパスワードを取得
db_pass = os.getenv('DB_PASSWORD')

# 初期円の半径をグローバル変数として定義
initial_radius = 0

window_width = 800
window_hight = 600

def monitoring():
    """ メインの監視機能を提供する関数 """
    global initial_radius
    max_radius = 80
    delta = 1
    animation_interval = 10
    angle = 120

    def draw_circle(canvas, x, y, radius):
        """ キャンバス上に円を描画する """
        canvas.delete("circle")
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="blue", tags="circle")

    def rotate_image(image_id, photo):
        """ 画像を回転させる """
        nonlocal angle
        rotated_image = resized_image.rotate(360 - angle + 180, expand=True)
        photo.image = ImageTk.PhotoImage(rotated_image)
        canvas.itemconfigure(image_id, image=photo.image)

    def animate():
        """ アニメーションとデータ更新を行う """
        global initial_radius
        initial_radius += delta
        if initial_radius > max_radius:
            TimeEvent.update_coordinates()
            initial_radius = 0
            update_battery_status()
        x, y = TimeEvent.x_point, TimeEvent.y_point
        if x and y:
            draw_circle(canvas, x, y, initial_radius)
            canvas.delete("car")
            car = canvas.create_image(x, y, anchor=tk.CENTER, image=center_image, tags="car")
            rotate_image(car, center_image)              
        window.after(animation_interval, animate)

    def update_battery_status():
        """ バッテリーステータスの画像を更新する """
        battery_status = TimeEvent.get_battery_status()
        image_tag = f"battery_{battery_status}"
        canvas.delete("battery")
        if battery_status > 0:
            canvas.create_image(840, 60, anchor=tk.CENTER, image=battery_images[battery_status], tags="battery")

    window = tk.Toplevel()
    window.title("データ取得アプリ")
    
    
    window.geometry("900x650")

    canvas = tk.Canvas(window, width=window_width, height=window_hight)
    canvas.pack()

    # 車両の画像の読み込みとリサイズ
    image_path = "car.png"
    original_image = Image.open(image_path)
    resized_image = original_image.resize((30, 30), Image.ANTIALIAS)
    center_image = ImageTk.PhotoImage(resized_image)

    # 背景画像の読み込み
    #background_image = tk.PhotoImage(file="image.jpg")
    create_image.create_pixel_grid_with_alternating_thickness(window_width, window_hight, 10, 100, 1, 4)
    background_image = tk.PhotoImage(file="pixel_grid_with_alternating_thickness.png")
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    # バッテリー画像の読み込み
    battery_images = {}
    for i in range(1, 6):
        image_path = f"battery_{i}.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((46, 95), Image.ANTIALIAS)
        battery_images[i] = ImageTk.PhotoImage(resized_image)

    # メニューバーの設定
    menubar = tk.Menu(window)
    window.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="終了", command=lambda: window.destroy())
    menubar.add_cascade(label="ファイル", menu=file_menu)

    animate()
    window.mainloop()

class TimeEvent:
    """ データベースからの時間イベントを処理するクラス """
    x_point = 0
    y_point = 0

    @classmethod
    def update_coordinates(cls):
        """ データベースから座標を更新する """
        try:
            connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='AGVcondition', charset='utf8mb4')
            cursor = connector.cursor()
            cursor.execute("SELECT Coordinate_x, Coordinate_y FROM AGVstatus WHERE id = 1;")
            result = cursor.fetchone()
            cls.x_point, cls.y_point = result[0], result[1]
        except Error as e:
            print(f"データベースエラー: {e}")
        finally:
            cursor.close()
            connector.close()

    @classmethod
    def get_battery_status(cls):
        """ データベースからバッテリーステータスを取得する """
        try:
            connector = mysql.connector.connect(user='root', password=db_pass, host='localhost', database='AGVcondition', charset='utf8mb4')
            cursor = connector.cursor()
            cursor.execute("SELECT Battery FROM AGVstatus WHERE id = 1;")
            result = cursor.fetchone()
            battery_level = result[0]
            return min(max(battery_level // 20, 1), 5)  # バッテリーレベルを1から5の範囲に変換
        except Error as e:
            print(f"データベースエラー: {e}")
            return 0
        finally:
            cursor.close()
            connector.close()