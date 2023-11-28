# ファイル: Main.py
# 作成者: 藤井広輝
# 更新日: 2023/6/20
# 説明: AGV経路登録システムのメイン

# 必要なライブラリをインポート
import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk

# 自作モジュールから必要な部分をインポート
from global_variable import selected_value, selected_number, route_name_entry, num, start, half, stop, gool, route_names, angles
import delete
import agv_location
import image_resize
import route_path_functions
import draw_line

# データベース設計
# CREATE TABLE route_data (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   経路番号 INT,
#   経路名 VARCHAR(255),
#   順番 INT,
#   x INT,
#   y INT,
#   一時停止 INT,
#   角度 DECIMAL(5, 2)
# );
def aaa():
    angle = 180
    # MySQLデータベースへの接続
    connector = mysql.connector.connect(user='root', password='wlcm2T4', host='localhost', database='root', charset='utf8mb4')
    cursor = connector.cursor()

    def delete_route_info():
        """経路情報削除windowが閉じられたときの処理"""
        # 経路情報の削除処理
        delete.delete_window(canvas)


    def perform_processing():
        """選択された経路と座標情報を元に、アルゴリズムテストウィンドウを作成します。

        Args:
            selected_route (str): 選択された経路名。
            coordinates (list): 座標情報を格納したリスト。各要素はタプル (x, y) 形式となります。
        """
        # algorithm_test_windowモジュールのcreate_Algorithm_window関数を呼び出し、アルゴリズムテストウィンドウを作成します。
        #sub_window.create_sub_window(canvas, status_bar)
        coordinates = [(100, 100), (200, 200), (300, 300)]  # これは例です。実際の座標に合わせてください。

        # create_Algorithm_window関数の呼び出し
        #algorithm_test_window.create_Algorithm_window(canvas, coordinates)
        #algorithm_test_window.create_Algorithm_window(canvas,coordinates)

        # 選択された経路番号をコンソールに出力します。
        print(f"Selected Route: {selected_route}")
        


    def handle_click(event):
        """マウスのクリックイベントを処理するためのコールバック関数。

        Args:
            event (Event): イベントオブジェクト。マウスのクリックに関する情報が含まれています。
                event.x (int): クリックされた位置のx座標。
                event.y (int): クリックされた位置のy座標。
        
        グローバル変数:
            start (tuple): スタート地点の座標 (x, y) を表すタプル。
            half (list): 中間地点の座標を格納するリスト。各要素はタプル (x, y) 形式となります。
            gool (tuple): ゴール地点の座標 (x, y) を表すタプル。
            stop (list): 一時停止地点の順番を格納するリスト。一時停止地点の順番は整数値としてリストに格納されます。
            angles (list): 各線分の角度を格納するリスト。各角度は小数値としてリストに格納されます。
            selected_value (int): 選択された値を格納する変数。1から4の整数値が入ります。
            num (int): 数値を格納する変数。整数値が入ります。
        """
        
        # グローバル変数として宣言
        global start, half, gool, stop, angles, selected_value, num

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



    def handle_selection():
        """
        select_action関数は、オプションメニューの選択イベントを処理するためのコールバック関数です。

        グローバル変数:
            coordinates (list): 選択された経路に対応する座標情報を格納するリスト。各要素はタプル (x, y) 形式となります。
            selected_item (str): 選択された経路名を表す文字列。
            
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

        グローバル変数:
            num (int): 中間地点の順番を表す整数値。新しい経路を作成する場合に、中間地点の順番を初期化します。
            route_name_entry (Entry): 経路名を入力するためのエントリーウィジェット。
            selected_number (StringVar): オプションメニューで選択された経路番号を格納する文字列変数。
            select_window (Tk): 新しいウィンドウを表す Tk インスタンス。
            
        この関数は、スタート地点かゴール地点が初期化されていない場合、メッセージボックスを表示して処理を中断します。
        それ以外の場合、新しいウィンドウを作成し、経路名の入力とオプションメニューの設定を行います。決定ボタンをクリックすると、
        on_select_button_click 関数が呼び出されます。
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
        """経路情報の登録を確定するためのコールバック関数。
        
        グローバル変数:
            route_name_entry (tk.Entry): 経路名を入力するためのEntryウィジェットです。
            selected_number (tk.StringVar): 選択された経路番号を格納するためのStringVarオブジェクトです。
            select_window (tk.Tk): 新しいウィンドウを作成するためのTkオブジェクトです。


        選択された経路番号に基づいてデータベースの更新を行います。
        経路情報をデータベースに挿入します。具体的には、経路番号、経路名、順番、x座標、y座標をデータベースに挿入します。
        一時停止フラグと角度情報をデータベースに更新します。
        最後に、登録が完了した旨のメッセージを表示し、ウィンドウを閉じます。
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

        # 経路番号の最大値を取得し、選択された経路番号に1を加えて新しい経路番号を決定
        max_route_number = result if result else 0
        max_route_number += 1

        # start、half、goolを順に結合して経路情報をまとめる
        root = [start] + half + [gool]

        i = 0
        for coordinate in root:
            i += 1
            x, y = coordinate
            values = (selected_number.get(), route_name_entry.get(), i, x, y)
            insert_query = "INSERT INTO route_data (経路番号, 経路名, 順番, x, y) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, values)
            connector.commit()

        # 一時停止フラグの更新
        for stop_num in stop:
            query = "UPDATE route_data SET 一時停止 = 1 WHERE 順番 = %s and 経路番号 = %s"
            cursor.execute(query, (stop_num, selected_number.get()))
            connector.commit()

        # 角度情報の更新
        for a in range(len(angles) + 1):
            if a > 0:
                query = "UPDATE route_data SET 角度 = %s WHERE 順番 = %s and 経路番号 = %s"
                cursor.execute(query, (angles[a - 1], a + 1, selected_number.get()))
                connector.commit()

        # グラフィック描画関連のオブジェクトを削除し、初期化を行う
        canvas.delete("start")
        canvas.delete("flag")
        canvas.delete("gool")
        canvas.delete("stop")
        canvas.delete("root")
        canvas.delete("angle")
        initialize()  # グローバル変数の初期化

        # 登録完了メッセージを表示し、ウィンドウを閉じる
        messagebox.showinfo("登録完了", "経路登録が完了しました。")
        select_window.destroy()



    def initialize():
        """
        特定のグローバル変数を初期化する関数

        グローバル変数:
            start (tuple): スタート地点の座標 (x, y) を表すタプル。
            half (list): 中間地点の座標を格納するリスト。各要素はタプル (x, y) 形式となります。
            gool (tuple): ゴール地点の座標 (x, y) を表すタプル。

        この関数では、特定のグローバル変数 start、half、gool を初期化します。
        start を (0, 0)、half を空のリスト、gool を (0, 0) に設定します。
        これにより、経路情報の登録をリセットして新たな経路の作成が可能となります。
        """
        # グローバル変数 start、half、gool を初期化
        global start, half, gool
        start = (0, 0)
        half = []
        gool = (0, 0)

        
    def handle_submit():
        """座標の入力欄から値を取得し、選択された値に応じて対応する関数を呼び出します。

        グローバル変数:
            start (tuple): スタート地点の座標 (x, y) を表すタプル。
            half (list): 中間地点の座標を格納するリスト。各要素はタプル (x, y) 形式となります。
            stop (list): 一時停止地点の座標を格納するリスト。各要素はタプル (x, y) 形式となります。
            gool (tuple): ゴール地点の座標 (x, y) を表すタプル。
            num (int): 現在の経路番号を表す整数。
            selected_value (int): 選択されたオプションの値。

        この関数では、x_entryとy_entryから入力された座標情報を取得し、選択された値に応じて
        適切な関数を呼び出します。関数が呼び出された結果、スタート地点、中間地点、ゴール地点を
        まとめ、リスト "root" に格納します。そして、描画されている線と角度情報をキャンバス上から
        削除し、新たに計算された角度情報を用いて線を描画します。
        """
        
        # グローバル変数として宣言
        global start, half, gool, stop, angles, selected_value, num
        
        # x_entryとy_entryから入力された座標情報を取得
        x = x_entry.get()
        y = y_entry.get()

        # 選択された値に応じて対応する関数を呼び出し、スタート地点、中間地点、ゴール地点を更新
        if selected_value == 1:
            start = route_path_functions.handle_start(x, y, start_photo, canvas)
        elif selected_value == 2:
            route_path_functions.handle_half(x, y, canvas, num, half)
        elif selected_value == 3:
            route_path_functions.handle_stop(x, y, canvas, num, half, stop, stop_photo)
        elif selected_value == 4:
            gool = route_path_functions.handle_goal(x, y, gool_photo, canvas)

        # 経路をまとめる
        root = []
        route_path_functions.root_set(start, half, gool, root)
        print(root)

        # 現在描画されている線と角度情報をキャンバス上から削除
        canvas.delete("root")
        canvas.delete("angle")

        # 角度計算と線表示
        draw_line.angle_picture(root, angles)
        draw_line.line_picture(root, canvas, angles)
        
        print(root)

    def show_selection():
        """
        ラジオボタンの選択結果に応じて、ラベルに選択されたオプションを表示します。
        選択されたオプションに応じて、ラベルのテキストと文字色を変更します。
        """
        global selected_value
        selected_option = var.get()
        if selected_option == 1:
            selected_value = 1
        elif selected_option == 2:
            selected_value = 2
        elif selected_option == 3:
            selected_value = 3
        elif selected_option == 4:
            selected_value = 4
            
    # AGV座標取得ボタンのコールバック関数
    def AGV_handle_submit1():
        """AGVの座標取得を行うためのコールバック関数です。
        agv_location モジュールの AGV_handle_submit 関数を呼び出します。
        """
        agv_location.AGV_handle_submit(canvas, start_photo , x_entry, y_entry, submit_button)
        
    # ウィンドウの作成と初期設定
    window = tk.Toplevel()
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
    gool_photo = image_resize.resize_image("gool.png", 40, 40)

    # キャンバスの作成と画像の表示
    """
    canvas = tk.Canvas(window, width=image.width, height=image.height)
    canvas.pack(side=tk.LEFT)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    photo = ImageTk.PhotoImage(image)
    """
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

    # ファイルメニュー
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="経路情報削除", command=delete_route_info)
    file_menu.add_command(label="オプション", command=perform_processing)
    menubar.add_cascade(label="デバッグ", menu=file_menu)

    # ステータスバーの作成
    status_bar = tk.Label(window, text="x座標: 0   y座標: 0   角度: 0",
                        bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # データベースから経路名を取得し、ドロップダウンメニューを作成
    selected_route = tk.StringVar()

    # マウスクリックイベントのバインド
    last_click_position = None  # 前回のクリック位置を保存する変数
    canvas.bind("<Button-1>", handle_click)

    # クリック座標を表示するラベルの作成
    coordinate_label = tk.Label(window, text="クリック座標: ")
    coordinate_label.pack()

    # ドロップダウンメニューの選択変更時に呼ばれる関数を設定
    selected_route.trace('w', lambda *args: handle_selection())

    # ラジオボタンの選択結果を格納するための変数を作成
    var = tk.IntVar()
    
    # 画像データの保存
    image_start = tk.PhotoImage(file="start_button.png")
    image_middle = tk.PhotoImage(file="tyuukan_button.png")
    image_itizi = tk.PhotoImage(file="itizi_button.png")
    image_target = tk.PhotoImage(file="target_button.png")

    # タッチ時の画像データの保存
    image_start_touch = tk.PhotoImage(file="start_button_touch.png")
    image_middle_touch = tk.PhotoImage(file="tyuukan_button_touch.png")
    image_itizi_touch = tk.PhotoImage(file="itizi_button_touch.png")
    image_target_touch = tk.PhotoImage(file="target_button_touch.png")

    # クリック時の画像データの保存
    image_start_clicked = tk.PhotoImage(file="start_button_clicked.png")
    image_middle_clicked = tk.PhotoImage(file="tyuukan_button_clicked.png")
    image_itizi_clicked = tk.PhotoImage(file="itizi_button_clicked.png")
    image_target_clicked = tk.PhotoImage(file="target_button_clicked.png")

    # 選択状態の管理用の変数
    option1_clicked = False
    option2_clicked = False
    option3_clicked = False
    option4_clicked = False

    def show_selection(value):
        """選択された値を表示する関数

        Args:
            value (int): 選択された値
        """
        global selected_value
        print("選択された値:", value)
        selected_value = value

    def change_image(widget, new_image):
        """ウィジェットの画像を変更する関数

        Args:
            widget (tk.Label): 画像を変更する対象のウィジェット
            new_image (tk.PhotoImage): 新しい画像
        """
        widget.configure(image=new_image)

    def reset_button_state():
        """ボタンの状態をリセットする関数
        """
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option1_clicked = False
        option2_clicked = False
        option3_clicked = False
        option4_clicked = False
        change_image(option1, image_start)
        change_image(option2, image_middle)
        change_image(option3, image_itizi)
        change_image(option4, image_target)
        option1.configure(state=tk.NORMAL)
        option2.configure(state=tk.NORMAL)
        option3.configure(state=tk.NORMAL)
        option4.configure(state=tk.NORMAL)

    # 各オプションがクリックされたときの処理
    def on_option1_click(event):
        """オプション1がクリックされたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option1_clicked = not option1_clicked

        if option1_clicked:
            change_image(option1, image_start_clicked)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)
        else:
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option2.configure(state=tk.NORMAL)
            option3.configure(state=tk.NORMAL)
            option4.configure(state=tk.NORMAL)

        # 他のオプションが選択されていればリセット
        if option2_clicked or option3_clicked or option4_clicked:
            reset_button_state()
            option1_clicked = not option1_clicked
            change_image(option1, image_start_clicked)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)

        show_selection(1)

    def on_option2_click(event):
        """オプション2がクリックされたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option2_clicked = not option2_clicked

        if option2_clicked:
            change_image(option2, image_middle_clicked)
            change_image(option1, image_start)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option1.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)
        else:
            change_image(option2, image_middle)
            change_image(option1, image_start)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option1.configure(state=tk.NORMAL)
            option3.configure(state=tk.NORMAL)
            option4.configure(state=tk.NORMAL)

        if option1_clicked or option3_clicked or option4_clicked:
            reset_button_state()
            option2_clicked = not option2_clicked
            change_image(option2, image_middle_clicked)
            option1.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)

        show_selection(2)

    def on_option3_click(event):
        """オプション3がクリックされたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option3_clicked = not option3_clicked

        if option3_clicked:
            change_image(option3, image_itizi_clicked)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option4, image_target)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)
        else:
            change_image(option3, image_itizi)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option4, image_target)
            option1.configure(state=tk.NORMAL)
            option2.configure(state=tk.NORMAL)
            option4.configure(state=tk.NORMAL)

        if option1_clicked or option2_clicked or option4_clicked:
            reset_button_state()
            option3_clicked = not option3_clicked
            change_image(option3, image_itizi_clicked)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)

        show_selection(3)

    def on_option4_click(event):
        """オプション4がクリックされたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option4_clicked = not option4_clicked

        if option4_clicked:
            change_image(option4, image_target_clicked)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
        else:
            change_image(option4, image_target)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            option1.configure(state=tk.NORMAL)
            option2.configure(state=tk.NORMAL)
            option3.configure(state=tk.NORMAL)

        if option1_clicked or option2_clicked or option3_clicked:
            reset_button_state()
            option4_clicked = not option4_clicked
            change_image(option4, image_target_clicked)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)

        show_selection(4)

    def on_option1_leave(event):
        """オプション1からマウスが離れたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option1_clicked:
            change_image(option1, image_start)

    def on_option2_leave(event):
        """オプション2からマウスが離れたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option2_clicked:
            change_image(option2, image_middle)

    def on_option3_leave(event):
        """オプション3からマウスが離れたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option3_clicked:
            change_image(option3, image_itizi)

    def on_option4_leave(event):
        """オプション4からマウスが離れたときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option4_clicked:
            change_image(option4, image_target)

    def on_option1_enter(event):
        """オプション1にマウスが乗ったときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option1_clicked:
            change_image(option1, image_start_touch)
        else:
            change_image(option1, image_start_clicked)

    def on_option2_enter(event):
        """オプション2にマウスが乗ったときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option2_clicked:
            change_image(option2, image_middle_touch)
        else:
            change_image(option2, image_middle_clicked)

    def on_option3_enter(event):
        """オプション3にマウスが乗ったときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option3_clicked:
            change_image(option3, image_itizi_touch)
        else:
            change_image(option3, image_itizi_clicked)

    def on_option4_enter(event):
        """オプション4にマウスが乗ったときの処理

        Args:
            event (tk.Event): イベントオブジェクト
        """
        if not option4_clicked:
            change_image(option4, image_target_touch)
        else:
            change_image(option4, image_target_clicked)


    # オプションのウィジェットの作成
    option1 = tk.Label(window, image=image_start, compound="left", cursor="hand2")
    option2 = tk.Label(window, image=image_middle, compound="left", cursor="hand2")
    option3 = tk.Label(window, image=image_itizi, compound="left", cursor="hand2")
    option4 = tk.Label(window, image=image_target, compound="left", cursor="hand2")

    # イベントのバインディング
    option1.bind("<Button-1>", on_option1_click)
    option1.bind("<Leave>", on_option1_leave)
    option1.bind("<Enter>", on_option1_enter)

    option2.bind("<Button-1>", on_option2_click)
    option2.bind("<Leave>", on_option2_leave)
    option2.bind("<Enter>", on_option2_enter)

    option3.bind("<Button-1>", on_option3_click)
    option3.bind("<Leave>", on_option3_leave)
    option3.bind("<Enter>", on_option3_enter)

    option4.bind("<Button-1>", on_option4_click)
    option4.bind("<Leave>", on_option4_leave)
    option4.bind("<Enter>", on_option4_enter)

    # オプションの配置
    option1.pack()
    option2.pack()
    option3.pack()
    option4.pack()

    # 座標入力フレームの作成と配置
    input_frame = tk.Frame(window)
    input_frame.pack()

    # x座標の入力欄
    x_label = tk.Label(input_frame, text="X座標:")  # ラベルにテキストを追加
    x_label.pack(side="left")
    x_entry = tk.Entry(input_frame, width=5)  # 幅を10に設定
    x_entry.pack(side="left")

    # y座標の入力欄
    y_label = tk.Label(input_frame, text="Y座標:")  # ラベルにテキストを追加
    y_label.pack(side="left")
    y_entry = tk.Entry(input_frame, width=5)  # 幅を10に設定
    y_entry.pack(side="left")

    # 座標決定ボタン
    submit_button = tk.Button(window, text="座標決定", command=handle_submit, width=20)
    submit_button.pack()

    # AGV座標取得ボタン
    get_coordinates_button = tk.Button(window, text="AGV座標取得", command=AGV_handle_submit1, width=20)
    get_coordinates_button.pack()

    # 決定ボタンを作成
    decision_button = tk.Button(window, text="決定", command=on_decision_button_click, width=20)
    decision_button.pack()


    # ウィンドウのメインループ
    window.mainloop()
