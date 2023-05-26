# ファイル: main_window
# 作成者: 藤井広輝
# 更新日: 2023/5/20
# 説明: AGV監視システムのメイン

# 必要なライブラリをインポート
import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
import sub_window
import Algorithm_test_window
import delete
import tkinter.messagebox as messagebox
from tkinter import messagebox, simpledialog
from tkinter import ttk
"""
データベース設計
CREATE TABLE route_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  経路番号 INT,
  経路名 VARCHAR(255),
  順番 INT,
  x INT,
  y INT
);
"""
# MySQLデータベースへの接続
connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='root', charset='utf8mb4')
cursor = connector.cursor()

def open_sub_window(status_bar):
    """
    open_sub_window関数は、sub_windowモジュールのcreate_sub_windowメソッドを呼び出して、
    サブウィンドウを開く役割を果たします。canvasとstatus_barを引数として渡しています。
    """
    sub_window.create_sub_window(canvas, status_bar)
    
def delete_route_info():
    # 経路情報の削除処理を実装する
    delete.delete_window(canvas)


def open_path_selection_algorithm():
    def handle_selection():
        if selected_item == "経路を選択":
            messagebox.showinfo("エラー", "経路を選択してください。")
        else:
            perform_processing(selected_item, coordinates)
            path_selection_window.destroy()

    # 経路名を格納する配列
    route_names = []

    # 経路番号の少ない順に経路名を取得するクエリを実行
    query = "SELECT DISTINCT 経路名 FROM route_data ORDER BY 経路番号 ASC"
    cursor.execute(query)
    results = cursor.fetchall()


    # 経路名を配列に格納
    for row in results:
        route_names.append(row[0])

    # ドロップダウンメニューを作成するための新しいウィンドウを作成
    path_selection_window = tk.Toplevel(window)
    path_selection_window.title("経路選択アルゴリズム")
    path_selection_window.geometry("400x200")

    def handle_dropdown_selection(*args):
        selected_item = selected_route.get()
        coordinates = []

        # 特定の項目名の座標x, yを順番が少ない順に取得するクエリを実行
        query = "SELECT x, y FROM route_data WHERE 経路名 = '{}' ORDER BY 順番 ASC".format(selected_item)
        cursor.execute(query)
        results = cursor.fetchall()

        # 結果を(x, y)形式の配列に格納
        for row in results:
            coordinates.append((row[0], row[1]))

        # 現在描画されている線を削除
        canvas.delete("root")

        # キャンバスを更新して削除した線が即座に表示されないようにする
        canvas.update()

        # 座標情報を利用して線を描画
        for i in range(len(coordinates) - 1):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill="red", dash=(4, 2), width=8, tags="root")

        canvas.delete("start")
        p1, p2 = coordinates[0]
        canvas.create_image(p1, p2, anchor=tk.CENTER, image=start_photo, tag="start")
        canvas.delete("gool")
        p3, p4 = coordinates[-1]
        canvas.create_image(p3, p4, anchor=tk.CENTER, image=gool_photo, tag="gool")

    # ドロップダウンメニューを作成
    selected_route.set("経路を選択")
    dropdown = tk.OptionMenu(path_selection_window, selected_route, *route_names, command=handle_dropdown_selection)
    dropdown.pack(pady=20)

    # 経路選択ボタンを作成
    select_button = tk.Button(path_selection_window, text="経路選択", command=handle_selection)
    select_button.pack()

def perform_processing(selected_route, coordinates):
    Algorithm_test_window.create_Algorithm_window(canvas, selected_route, coordinates,status_bar)
    print(f"Selected Route: {selected_route}")
    # Perform the desired processing here

def select_action2(selected_action):
    """
    select_action2関数は、新しいドロップダウンメニューの選択イベントを処理するためのコールバック関数です。
    選択されたアクションを取得し、それに応じて異なる処理を行います。
    """
    global selected_value
    if selected_action == "スタート地点":
        # スタート地点の処理
        print("スタート地点が選択されました。")
        # ここにスタート地点の処理を追加するコードを記述します。
        selected_value = 1

    elif selected_action == "中間地点":
        # ゴール地点の処理
        print("ゴール地点が選択されました。")
        # ここにゴール地点の処理を追加するコードを記述します。
        selected_value = 2

    elif selected_action == "ゴール地点":
        # 中間地点の処理
        print("中間地点が選択されました。")
        # ここに中間地点の処理を追加するコードを記述します。
        selected_value = 3

    else:
        # その他のアクションの処理
        print("選択されたアクション2:", selected_action)
        # ここにその他のアクションの処理を追加するコードを記述します。

def handle_click(event):
    """
    handle_click関数は、マウスのクリックイベントを処理するためのコールバック関数です。
    イベントオブジェクトからクリックされた位置座標を取得し、表示します。
    """
    # グローバル変数として宣言
    global selected_value, start, gool, half,num
    # クリックされた位置座標を取得
    x = event.x
    y = event.y
    coordinate_label.config(text=f"クリック座標: ({x}, {y})")
    print("クリック位置座標:", x, y)

    # 画像を読み込む
    if selected_value == 1:
        start = (x, y)
        p1, p2 = start
        print(start)
        canvas.delete("start")
        canvas.create_image(p1, p2, anchor=tk.CENTER, image=start_photo, tag="start")

    elif selected_value == 2:
        num = num + 1
        half.append((x, y))
        for coordinate in half:
            x, y = coordinate
            canvas.create_text(x, y, text=str(num), font=("Arial", 24),tag="flag")
    elif selected_value == 3:
        gool = (x, y)
        canvas.delete("gool")
        canvas.create_image(x, y, anchor=tk.CENTER, image=gool_photo, tag="gool")
        
    root = []
    if start != (0, 0):
        root.append(start)
    for coordinate in half:
        if coordinate != (0, 0):
            root.append(coordinate)
    if gool != (0, 0):
        root.append(gool)
    
    # 現在描画されている線を削除
    canvas.delete("root")

    # 座標情報を利用して線を描画
    for i in range(len(root) - 1):
        x1, y1 = root[i]
        x2, y2 = root[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", dash=(4, 2), width=8, tags="root")
    print(selected_value)

def change_image():
    """
    この関数は、ユーザーが新しい画像を選択するためのファイルダイアログを表示し、選択された画像をキャンバス上に表示する役割を持ちます。
    """
    global image, photo

    # 画像の選択ダイアログを表示し、新しい画像ファイルを選択
    new_image_path = tk.filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

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
    print(selected_item)
    # 選択された項目に基づいた処理を行う
    # ここに処理のコードを記述してください
    # 結果を格納する配列
    coordinates = []

    # 特定の項目名の座標x, yを順番が少ない順に取得するクエリを実行
    query = "SELECT x, y FROM route_data WHERE 経路名 = '{}' ORDER BY 順番 ASC".format(selected_item)
    cursor.execute(query)
    results = cursor.fetchall()

    # 結果を(x, y)形式の配列に格納
    for row in results:
        coordinates.append((row[0], row[1]))

    # 結果の出力
    for coordinate in coordinates:
        print(coordinate)

    # 現在描画されている線を削除
    canvas.delete("root")

    # 座標情報を利用して線を描画
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", dash=(4, 2), width=8, tags="root")


"""
この部分はメインウィンドウの作成と設定を行っています。tkinterのTkクラスを使ってウィンドウを作成し、
ウィンドウのタイトルやサイズを設定します。また、画像を読み込んで表示するためにtkinterのCanvasク
ラスを使い、キャンバス上に画像を表示します。メニューバーやラベル、オプションメニューなども追加し
ています。最後に、マウスクリックイベントのバインドとウィンドウのメインループを開始します。
"""
# ウィンドウの作成
window = tk.Tk()
window.title("無人搬送車制御アプリケーション ver1.0.0")
window.geometry("880x600")  # ウィンドウサイズを固定

# ボタンのコマンドとなる関数を定義
def on_decision_button_click():
    global num
    # スタート地点かゴール地点が初期化されている場合、メッセージを表示して処理を中断
    if start == (0, 0):
        messagebox.showinfo("入力エラー", "スタート地点を入力してください")
        return
    if gool == (0, 0):
        messagebox.showinfo("入力エラー", "ゴール地点を入力してください")
        return
    
    # ボタンがクリックされたときの処理を記述
    route_name = simpledialog.askstring("経路名入力", "経路名を入力してください:")
    if route_name is None:
        return
    messagebox.showinfo("決定ボタン", "決定ボタンがクリックされました！")
    num = 0

    # 経路番号の最大値を取得するクエリを実行
    query = "SELECT MAX(経路番号) FROM route_data"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    max_route_number = result if result else 0
    max_route_number += 1

    root = []
    root.append(start)
    for coordinate in half:
        root.append(coordinate)
    root.append(gool)

    i = 0
    for coordinate in root:
        i += 1
        x, y = coordinate
        values = (max_route_number, route_name, i, x, y)
        insert_query = "INSERT INTO route_data (経路番号, 経路名, 順番, x, y) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, values)

    connector.commit()

    print(root)
    canvas.delete("start")
    canvas.delete("flag")
    canvas.delete("gool")
    canvas.delete("root")
    # 初期化
    initialize()

# 画像の読み込み
image_path = "image.jpg"
image = Image.open(image_path)
image = image.resize((700, 500))
photo = ImageTk.PhotoImage(image)

# スタート地点設定用の配列
start = (0, 0)

# 中間地点設定用の配列
half = []

# ゴール地点設定用の配列
gool = (0, 0)


# 初期化関数
def initialize():
    global start, half, gool
    start = (0, 0)
    half = []
    gool = (0, 0)

# キャンバスの作成
canvas = tk.Canvas(window, width=image.width, height=image.height)
canvas.pack(side=tk.LEFT)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# メニューバーの作成
menubar = tk.Menu(window)
window.config(menu=menubar)

# ファイルメニュー
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="搬送車信号テスト", command=lambda: open_sub_window(status_bar))
file_menu.add_command(label="経路選択アルゴリズム", command=open_path_selection_algorithm)
file_menu.add_command(label="経路情報削除", command=delete_route_info)
file_menu.add_command(label="画像を変更", command=change_image)
menubar.add_cascade(label="デバッグ", menu=file_menu)

# メニューバーに座標を表示するラベルを追加
status_bar = tk.Label(window, text="x座標: 0   y座標: 0   角度: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# 決定ボタンを作成
decision_button = tk.Button(window, text="決定", command=on_decision_button_click)
decision_button.pack(side=tk.RIGHT)

# 経路作成用ドロップダウンメニューの作成
action_var2 = tk.StringVar()
action_var2.set("アクションを選択")
action_menu2 = tk.OptionMenu(window, action_var2, "スタート地点", "中間地点", "ゴール地点", command=select_action2)
action_menu2.pack(side=tk.RIGHT)

# ドロップダウンメニューを作成
# 経路名を格納する配列
route_names = []

# 経路番号の少ない順に経路名を取得するクエリを実行
query = "SELECT DISTINCT 経路名 FROM route_data ORDER BY 経路番号 ASC"
cursor.execute(query)
results = cursor.fetchall()

# 経路名を配列に格納
for row in results:
    route_names.append(row[0])

# ドロップダウンメニューを作成
selected_route = tk.StringVar()

# 選択されている経路選択用ドロップダウンメニューを見る変数
selected_value = 0

#中間座標の数字
num = 0

# マウスクリックイベントのバインド
last_click_position = None  # 前回のクリック位置を保存する変数
canvas.bind("<Button-1>", handle_click)

# クリック座標を表示するラベルの作成
coordinate_label = tk.Label(window, text="クリック座標: ")
coordinate_label.pack()

# ドロップダウンメニューの選択変更時に呼ばれる関数を設定
selected_route.trace('w', lambda *args: handle_selection())

# 標示画像の変形
start_image_path = "start_flag.png"
start_image = Image.open(start_image_path)
start_image = start_image.resize((40, 40))
start_photo = ImageTk.PhotoImage(start_image)

half_image_path = "half.png"
half_image = Image.open(half_image_path)
half_image = half_image.resize((40, 40))
half_photo = ImageTk.PhotoImage(half_image)

gool_image_path = "gool.jpg"
gool_image = Image.open(gool_image_path)
gool_image = gool_image.resize((40, 40))
gool_photo = ImageTk.PhotoImage(gool_image)


def handle_submit():
    global start,half,gool
    x = x_entry.get()
    y = y_entry.get()
    if selected_value == 1:
        start = (x, y)
        p1, p2 = start
        print(start)
        canvas.delete("start")
        canvas.create_image(p1, p2, anchor=tk.CENTER, image=start_photo, tag="start")

    elif selected_value == 2:
        half.append((x, y))
        for coordinate in half:
            x, y = coordinate
            canvas.create_image(x, y, anchor=tk.CENTER, image=half_photo, tag="flag")
    elif selected_value == 3:
        gool = (x, y)
        canvas.delete("gool")
        canvas.create_image(x, y, anchor=tk.CENTER, image=gool_photo, tag="gool")

    root = []
    if start != (0, 0):
        root.append(start)
    for coordinate in half:
        if coordinate != (0, 0):
            root.append(coordinate)
    if gool != (0, 0):
        root.append(gool)
    
    # 現在描画されている線を削除
    canvas.delete("root")

    # 座標情報を利用して線を描画
    for i in range(len(root) - 1):
        x1, y1 = root[i]
        x2, y2 = root[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", dash=(4, 2), width=8, tags="root")

# x座標の入力欄
x_label = tk.Label(window, text="x座標:")
x_label.pack()
x_entry = tk.Entry(window)
x_entry.pack()

# y座標の入力欄
y_label = tk.Label(window, text="y座標:")
y_label.pack()
y_entry = tk.Entry(window)
y_entry.pack()

# 送信ボタン
submit_button = tk.Button(window, text="送信", command=handle_submit)
submit_button.pack()

# ウィンドウのメインループ
window.mainloop()
