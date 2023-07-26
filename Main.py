# ファイル: Main.py
# 作成者: 藤井広輝
# 更新日: 2023/5/20
# 説明: AGV経路登録システムのメイン

# 必要なライブラリをインポート
import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk

# 自作モジュールから必要な部分をインポート
from global_variable import selected_value, selected_number, route_name_entry, num, start, half, stop, gool, route_names, angles
import algorithm_test_window
import delete
import agv_location
import image_resize
import route_path_functions
import draw_line
"""
データベース設計
CREATE TABLE route_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  経路番号 INT,
  経路名 VARCHAR(255),
  順番 INT,
  x INT,
  y INT
  一時停止 INT
  角度 DECIMAL(5, 2)
);
"""

# MySQLデータベースへの接続
connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='root', charset='utf8mb4')
cursor = connector.cursor()

def delete_route_info():
    """経路情報削除windowが閉じられたときの処理"""
    # 経路情報の削除処理
    delete.delete_window(canvas)


def perform_processing(selected_route, coordinates):
    algorithm_test_window.create_Algorithm_window(
        canvas, selected_route, coordinates, status_bar)
    print(f"Selected Route: {selected_route}")
    


def handle_click(event):
    """マウスのクリックイベントを処理するためのコールバック関数。

    Args:
        event (Event): イベントオブジェクト。マウスのクリックに関する情報が含まれています。
            event.x (int): クリックされた位置のx座標。
            event.y (int): クリックされた位置のy座標。
    """
    # グローバル変数として宣言
    global selected_value, start, gool, half, num, stop, angles

    # クリック座標を表示
    coordinate_label.config(text=f"クリック座標: ({event.x}, {event.y})")
    print("クリック位置座標:", event.x, event.y)

    # 画像を読み込み、対応する関数を呼び出す
    if selected_value == 1:
        start = route_path_functions.handle_start(event.x, event.y, start_photo, canvas)
    elif selected_value == 2:
        route_path_functions.handle_half(event.x, event.y, canvas, num, half)
    elif selected_value == 3:
        route_path_functions.handle_stop(event.x, event.y, canvas, num, half, stop, stop_photo)
    elif selected_value == 4:
        gool = route_path_functions.handle_goal(event.x, event.y, gool_photo, canvas)

    # 経路をまとめる
    root = []
    route_path_functions.root_set(start, half, gool, root)

    # 現在描画されている線を削除
    canvas.delete("root")
    canvas.delete("angle")

    # 角度描写と線描写
    draw_line.angle_picture(root, angles)
    draw_line.line_picture(root, canvas, angles)



def change_image():
    """
    この関数は、ユーザーが新しい画像を選択するためのファイルダイアログを表示し、選択された画像をキャンバス上に表示する役割を持ちます。
    """
    global image, photo

    # 画像の選択ダイアログを表示し、新しい画像ファイルを選択
    new_image_path = tk.filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    # 新しい画像を読み込み、キャンバス上の画像を更新
    image = Image.open(new_image_path)
    image = image.resize((700, 500))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)


def handle_selection():
    """
    select_action関数は、オプションメニューの選択イベントを処理するためのコールバック関数です。
    選択されたアクションを取得し、それに応じて座標情報を設定します。そして、canvas上に現在描画
    されている線を削除し、新たに座標情報を利用して線を描画します。描画される線は赤色で、点線で表示されます。
    """
    global coordinates, selected_item
    selected_item = selected_route.get()

    # 結果を格納する配列
    coordinates = []

    # 特定の項目名の座標x, yを順番が少ない順に取得するクエリを実行
    query = "SELECT x, y FROM route_data WHERE 経路名 = '{}' ORDER BY 順番 ASC".format(
        selected_item)
    cursor.execute(query)
    results = cursor.fetchall()

    # 結果を(x, y)形式の配列に格納
    for row in results:
        coordinates.append((row[0], row[1]))

    # 現在描画されている線を削除
    canvas.delete("root")

    # 座標情報を利用して線を描画
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red",
                           dash=(4, 2), width=8, tags="root")




def on_decision_button_click():
    """
    ユーザーが決定ボタンをクリックしたときの処理を行うコールバック関数です。
    スタート地点かゴール地点が初期化されている場合、メッセージを表示して処理を中断します。
    それ以外の場合、新しいウィンドウを作成し、経路名の入力とオプションメニューの設定を行います。
    決定ボタンをクリックすると、`on_select_button_click` 関数が呼び出されます。
    """
    global num, route_name_entry, selected_number, select_window

    # スタート地点かゴール地点が初期化されている場合、メッセージを表示して処理を中断
    if start == (0, 0):
        messagebox.showinfo("入力エラー", "スタート地点を入力してください")
        return
    if gool == (0, 0):
        messagebox.showinfo("入力エラー", "ゴール地点を入力してください")
        return

    # 新しいウィンドウの作成
    select_window = tk.Tk()

    # ラベルとエントリーの作成
    route_name_label = tk.Label(select_window, text="経路名を入力してください:")
    route_name_label.pack()
    route_name_entry = tk.Entry(select_window)
    route_name_entry.pack()

    # オプションメニューの作成
    selected_number = tk.StringVar(select_window)
    selected_number.set("")  # 初期値を空に設定
    dropdown = tk.OptionMenu(select_window, selected_number, "1", "2", "3", "4", "5")
    dropdown.pack()

    # 決定ボタンの作成とクリック時の処理の設定
    decision_button = tk.Button(select_window, text="決定", command=on_select_button_click)
    decision_button.pack()

    num = 0

def on_select_button_click():
    """
    ユーザーが選択ボタンをクリックしたときの処理を行うコールバック関数です。
    経路番号の最大値を取得し、選択された経路番号に基づいてデータベースの更新を行います。
    また、入力された座標情報をデータベースに挿入します。
    最後に、描画されていた線と画像をキャンバスから削除して、初期化を行い、登録完了メッセージを表示します。
    """
    global route_name_entry, selected_number, select_window

    # 経路番号の最大値を取得するクエリを実行
    query = "SELECT MAX(経路番号) FROM route_data"
    cursor.execute(query)
    result = cursor.fetchone()[0]

    # 選択された経路番号に基づいてデータベースの更新を行うクエリを実行
    query = "DELETE FROM route_data WHERE 経路番号 = " + selected_number.get() + ";"
    cursor.execute(query)
    connector.commit()

    max_route_number = result if result else 0
    max_route_number += 1

    root = [start] + half + [gool]

    i = 0
    for coordinate in root:
        i += 1
        x, y = coordinate
        values = (selected_number.get(), route_name_entry.get(), i, x, y)
        insert_query = "INSERT INTO route_data (経路番号, 経路名, 順番, x, y) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, values)
        connector.commit()

    for stop_num in stop:
        query = "UPDATE route_data SET 一時停止 = 1 WHERE 順番 = %s and 経路番号 = %s"
        cursor.execute(query, (stop_num, selected_number.get()))
        connector.commit()

    for a in range(len(angles) + 1):
        if a > 0:
            query = "UPDATE route_data SET 角度 = %s WHERE 順番 = %s and 経路番号 = %s"
            cursor.execute(query, (angles[a - 1], a + 1, selected_number.get()))
            connector.commit()

    print(root)
    canvas.delete("start")
    canvas.delete("flag")
    canvas.delete("gool")
    canvas.delete("stop")
    canvas.delete("root")
    canvas.delete("angle")
    # 初期化
    initialize()
    messagebox.showinfo("登録完了", "経路登録が完了しました。")
    select_window.destroy()


def initialize():
    """
    特定のグローバルを初期化する関数
    """
    global start, half, gool
    start = (0, 0)
    half = []
    gool = (0, 0)
    
def handle_submit():
    """_summary_
    """
    global start, half, stop, gool,num
    x = x_entry.get()
    y = y_entry.get()
    
    
    # 画像を読み込み、対応する関数を呼び出す
    if selected_value == 1:
        start = route_path_functions.handle_start(x, y, start_photo, canvas)
    elif selected_value == 2:
        route_path_functions.handle_half(x, y, canvas, num, half)
    elif selected_value == 3:
        route_path_functions.handle_stop(x, y, canvas, num, half, stop, stop_photo)
    elif selected_value == 4:
        gool = route_path_functions.handle_goal(x, y, gool_photo, canvas)

    root = []
    
    # 経路をまとめる
    route_path_functions.root_set(start, half, gool, root)
        
    # 現在描画されている線を削除
    canvas.delete("root")
    canvas.delete("angle")

    # 角度計算
    draw_line.angle_picture(root, angles)
    
    # 線表示
    draw_line.line_picture(root, canvas, angles)


# ウィンドウの作成
window = tk.Tk()
window.title("無人搬送車制御アプリケーション ver1.0.0")
window.geometry("880x600")  # ウィンドウサイズを固定  
    
# 画像の読み込み
image_path = "image.jpg"
image = Image.open(image_path)
image = image.resize((700, 500))
photo = ImageTk.PhotoImage(image)
# 標示画像の変形
start_photo = image_resize.resize_image("start_flag.png", 40, 40)
half_photo = image_resize.resize_image("half.png", 40, 40)
stop_photo = image_resize.resize_image("itiziteisi.png", 40, 40)
gool_photo = image_resize.resize_image("gool.jpg", 40, 40)


# キャンバスの作成
canvas = tk.Canvas(window, width=image.width, height=image.height)
canvas.pack(side=tk.LEFT)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# メニューバーの作成
menubar = tk.Menu(window)
window.config(menu=menubar)

# ファイルメニュー
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="経路情報削除", command=delete_route_info)
file_menu.add_command(label="画像を変更", command=change_image)
menubar.add_cascade(label="デバッグ", menu=file_menu)

# メニューバーに座標を表示するラベルを追加
status_bar = tk.Label(window, text="x座標: 0   y座標: 0   角度: 0",
                      bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)


# 経路番号の少ない順に経路名を取得するクエリを実行
query = "SELECT DISTINCT SQL_NO_CACHE 経路名 FROM route_data ORDER BY 経路番号 ASC"
cursor.execute(query)
results = cursor.fetchall()
connector.commit()

# 経路名を配列に格納
for row in results:
    route_names.append(row[0])

# ドロップダウンメニューを作成
selected_route = tk.StringVar()

# マウスクリックイベントのバインド
last_click_position = None  # 前回のクリック位置を保存する変数
canvas.bind("<Button-1>", handle_click)

# クリック座標を表示するラベルの作成
coordinate_label = tk.Label(window, text="クリック座標: ")
coordinate_label.pack()

# ドロップダウンメニューの選択変更時に呼ばれる関数を設定
selected_route.trace('w', lambda *args: handle_selection())


    

def show_selection():
    global selected_value
    selected_option = var.get()
    if selected_option == 1:
        label.config(text="Option 1 selected", foreground="green")
        selected_value = 1
    elif selected_option == 2:
        label.config(text="Option 2 selected", foreground="blue")
        selected_value = 2
    elif selected_option == 3:
        label.config(text="Option 3 selected", foreground="red")
        selected_value = 3
    elif selected_option == 4:
        label.config(text="Option 4 selected", foreground="red")
        selected_value = 4


# ラジオボタンの選択結果を格納するための変数を作成
var = tk.IntVar()

# 選択結果を表示するためのラベルを作成
label = ttk.Label(window, text="Please make a selection", foreground="gray")
label.pack(pady=10)

# ラジオボタンを作成
option1 = ttk.Radiobutton(window, text="スタート", variable=var, value=1, command=show_selection)
option1.pack()

option2 = ttk.Radiobutton(window, text="中間地点", variable=var, value=2, command=show_selection)
option2.pack()

option3 = ttk.Radiobutton(window, text="一時停止", variable=var, value=3, command=show_selection)
option3.pack()

option4 = ttk.Radiobutton(window, text="ゴール", variable=var, value=4, command=show_selection)
option4.pack()


# x座標の入力欄とy座標の入力欄を同じ行に配置するフレームを作成
input_frame = tk.Frame(window)
input_frame.pack()

# x座標の入力欄
x_label = tk.Label(input_frame, text="座標(x,y):")
x_label.pack(side="left")
x_entry = tk.Entry(input_frame)
x_entry = tk.Entry(input_frame, width=7)  # 幅を10に設定
x_entry.pack(side="left")

# y座標の入力欄
y_label = tk.Label(input_frame)
y_label.pack(side="left")
y_entry = tk.Entry(input_frame)
y_entry = tk.Entry(input_frame, width=7)  # 幅を10に設定
y_entry.pack(side="left")

# 座標決定ボタン
submit_button = tk.Button(window, text="座標決定", command=handle_submit)
submit_button.pack()


def AGV_handle_submit1():
    agv_location.AGV_handle_submit(canvas,start_photo)
    
# AGV座標取得ボタン
submit_button = tk.Button(window, text="AGV座標取得", command=AGV_handle_submit1)
submit_button.pack()

# 決定ボタンを作成
decision_button = tk.Button(window, text="決定", command=on_decision_button_click)
decision_button.pack()


# ウィンドウのメインループ
window.mainloop()

