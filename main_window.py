"""""""""""""""""""""""""""""""""""""""""""""
ファイル:main_window
作成者:藤井広輝
更新日:2023/5/20
説明
AGV監視システムのメイン
"""""""""""""""""""""""""""""""""""""""""""""
import tkinter as tk
from PIL import ImageTk, Image
import sub_window
import Algorithm_test_window


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
    
"""
handle_click関数は、マウスのクリックイベントを処理するためのコールバック関数です。
イベントオブジェクトからクリックされた位置座標を取得し、表示します。
""" 
def handle_click(event):
    # クリックされた位置座標を取得
    x = event.x
    y = event.y
    print("クリック位置座標:", x, y)

     
"""
select_action関数は、オプションメニューの選択イベントを処理するためのコールバック関数です。
選択されたアクションを取得し、それに応じて座標情報を設定します。そして、canvas上に現在描画
されている線を削除し、新たに座標情報を利用して線を描画します。描画される線は赤色で、点線で表示されます。
"""
def select_action(event):
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

# 画像の読み込み
image_path = "image.jpg"
image = Image.open(image_path)
image = image.resize((700, 500))
photo = ImageTk.PhotoImage(image)

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
menubar.add_cascade(label="デバッグ", menu=file_menu)

# メニューバーに座標を表示するラベルを追加
status_bar = tk.Label(window, text="x座標: 0   y座標: 0   角度: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ドロップダウンメニューの作成
action_var = tk.StringVar()
action_var.set("アクションを選択")
action_menu = tk.OptionMenu(window, action_var, "AB経路", "BC経路", "CA経路", command=select_action)
action_menu.pack(side=tk.RIGHT)


# マウスクリックイベントのバインド
last_click_position = None  # 前回のクリック位置を保存する変数
canvas.bind("<Button-1>", handle_click)

# ウィンドウのメインループ
window.mainloop()