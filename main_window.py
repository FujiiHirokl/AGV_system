"""""""""""""""""""""""""""""""""""""""""""""
ファイル:main_window
作成者:藤井広輝
更新日:2023/5/20
説明
AGV監視システムのメイン
"""""""""""""""""""""""""""""""""""""""""""""
import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk, Image
import sub_window
import Algorithm_test_window
import tkinter.messagebox as messagebox




def open_sub_window(status_ber):
    """
    open_sub_windows関数は、sub_windowモジュールのcreate_sub_windowメソッドを呼び出して、   
    サブウィンドウを開く役割を果たします。canvasとstatus_barを引数として渡しています。
    """   
    sub_window.create_sub_window(canvas,status_ber)

def open_path_selection_algorithm():
    selected_action = action_var.get()
    coordinates = []

    if selected_action == "AB経路":
        coordinates = [(612, 252), (612, 73)]
    elif selected_action == "BC経路":
        coordinates = [(612, 75), (256, 75)]
    elif selected_action == "CA経路":
        coordinates = [(257, 72), (76, 72), (72, 254), (612, 254)]
    Algorithm_test_window.create_Algorithm_window(canvas, selected_action, coordinates)        
        
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
    global car_photo,selected_value,start,gool

    # クリックされた位置座標を取得
    x = event.x
    y = event.y
    print("クリック位置座標:", x, y)

    # 画像を読み込む
    if selected_value == 1:
        start = (x,y)
        p1,p2 = start
        print(start)
        canvas.delete("start")
        canvas.create_image(p1, p2, anchor=tk.CENTER, image=start_photo, tag="start")
        
    elif selected_value == 2:
        half.append((x, y))
        for coordinate in  half:
            x, y = coordinate
            canvas.create_image(x, y, anchor=tk.CENTER, image=half_photo,tag="flag")
    elif selected_value == 3:
        gool = (x,y)
        canvas.delete("gool")
        canvas.create_image(x, y, anchor=tk.CENTER, image=gool_photo,tag="gool")
    
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
    

     
def select_action(event):
    """
    select_action関数は、オプションメニューの選択イベントを処理するためのコールバック関数です。
    選択されたアクションを取得し、それに応じて座標情報を設定します。そして、canvas上に現在描画
    されている線を削除し、新たに座標情報を利用して線を描画します。描画される線は赤色で、点線で表示されます。
    """
    selected_action = action_var.get()
    print("選択されたアクション:", selected_action)

    # 配列の座標情報を取得
    coordinates = []
    if selected_action == "AB経路":
        coordinates = [(612, 252), (612, 73)]
    elif selected_action == "BC経路":
        coordinates = [(612, 75), (256, 75)]
    elif selected_action == "CA経路":
        coordinates = [(257, 72), (76, 72), (72, 254), (612, 254)]

    # 現在描画されている線を削除
    canvas.delete("root")

    # 座標情報を利用して線を描画
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        
        """reate_lineのオプション
        fill: 線の色を指定します。カラーコード（"#RRGGBB"）を使用します。
        outline: 線の外枠の色を指定します。
        width: 線の太さを指定します。整数値を指定し、単位はピクセルです。
        dash: 線のスタイルを指定します。(4, 2)は4ピクセルの線、2ピクセルの点線のパターンになります。
        dashoffset: 点線の開始位置を指定します。デフォルトでは0です。
        capstyle: 線の端点のスタイルを指定します。"butt"（デフォルト）、"projecting"、"round"のいずれかを指定します。
        joinstyle: 線の角のスタイルを指定します。"miter"（デフォルト）、"round"、"bevel"のいずれかを指定します。
        smooth: 線をなめらかに描画するかどうかを指定します。デフォルトではFalseで、直線が描画されます。Trueに設定すると、なめらかな曲線が描画されます。
        splinesteps: smoothオプションがTrueの場合に、曲線を描画する際のステップ数を指定します。デフォルトでは12です。
        tags: 線にタグを付けることができます。タグは文字列またはタグのリストとして指定します。タグを指定することで、後で線を特定のタグで検索したり操作したりすることができます。
        """
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
    # ボタンがクリックされたときの処理を記述
    messagebox.showinfo("決定ボタン", "決定ボタンがクリックされました！")
    root = []
    root.append(start)
    for coordinate in  half:
        root.append(coordinate)
    root.append(gool)
    
    print(root)
    
# 画像の読み込み
image_path = "image.jpg"
image = Image.open(image_path)
image = image.resize((700, 500))
photo = ImageTk.PhotoImage(image)

#スタート地点設定用の配列
start =(0,0)

#中間地点設定用の配列
half = []

#ゴール地点設定用の配列
gool = (0,0)

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
file_menu.add_command(label="画像を変更", command=change_image)
menubar.add_cascade(label="デバッグ", menu=file_menu)

# メニューバーに座標を表示するラベルを追加
status_bar = tk.Label(window, text="x座標: 0   y座標: 0   角度: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ドロップダウンメニューの作成
action_var = tk.StringVar()
action_var.set("アクションを選択")
action_menu = tk.OptionMenu(window, action_var, "AB経路", "BC経路", "CA経路", command=select_action)
action_menu.pack(side=tk.RIGHT)

# 決定ボタンを作成
decision_button = tk.Button(window, text="決定", command=on_decision_button_click)
decision_button.pack(side=tk.RIGHT)


# 経路作成用ドロップダウンメニューの作成
action_var2 = tk.StringVar()
action_var2.set("アクションを選択")
action_menu2 = tk.OptionMenu(window, action_var2, "スタート地点", "中間地点", "ゴール地点", command=select_action2)
action_menu2.pack(side=tk.RIGHT)

#選択されている経路選択用ドロップダウンメニューを見る変数
selected_value = 0

# マウスクリックイベントのバインド
last_click_position = None  # 前回のクリック位置を保存する変数
canvas.bind("<Button-1>", handle_click)

#標示画像の変形
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

# ウィンドウのメインループ
window.mainloop()