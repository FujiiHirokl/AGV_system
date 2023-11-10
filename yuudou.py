# 必要なライブラリをインポート
import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk

# 自作モジュールから必要な部分をインポート
from global_variable import selected_value, selected_number, route_name_entry, num, start, half, stop, gool, route_names, angles
import image_resize

# ウィンドウの作成と初期設定
window = tk.Tk()
window.title("無人搬送車経路登録アプリケーション")
window.geometry("1080x600")  # ウィンドウサイズを固定  
    
# 画像の読み込みとリサイズ
image_path = "image.jpg"
image = Image.open(image_path)
image = image.resize((700, 500))
photo = ImageTk.PhotoImage(image)

# 標示画像の変形
start_photo = image_resize.resize_image("start_flag.png", 40, 40)
half_photo = image_resize.resize_image("half.png", 40, 40)
stop_photo = image_resize.resize_image("itiziteisi.png", 40, 40)
gool_photo = image_resize.resize_image("gool.jpg", 40, 40)

# キャンバスの作成と画像の表示
image_path = "image.jpg"  # 画像ファイルのパスを指定してください
image = Image.open(image_path)

photo = ImageTk.PhotoImage(image)

canvas = tk.Canvas(window, width=image.width, height=image.height)
canvas.pack(side=tk.LEFT)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.photo = photo  # 画像がガベージコレクションされないように参照を保持

# メニューバーの作成
menubar = tk.Menu(window)
window.config(menu=menubar)

# ステータスバーの作成
status_bar = tk.Label(window, text="x座標: 0   y座標: 0   角度: 0",
                    bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# データベースから経路名を取得し、ドロップダウンメニューを作成
selected_route = tk.StringVar()

# クリック座標を表示するラベルの作成
coordinate_label = tk.Label(window, text="クリック座標: ")
coordinate_label.pack()

# ウィンドウのメインループ
window.mainloop()
