# ファイル: Algorithm_test_windows.py
# 作成者: 藤井広輝
# 更新日: 2023/5/20
# 説明: アルゴリズムのテストを行うウィンドウのプログラム

#必要なライブラリをインポート
import tkinter as tk
from PIL import ImageTk, Image
import math
import random
import algorithm_function
import tkinter.messagebox as messagebox

def create_Algorithm_window(canvas,coordinates):
    """アルゴリズムのテストウィンドウを作成します。

    Args:
        canvas (tk.Canvas): アルゴリズムの動作を可視化するためのキャンバスオブジェクト
        selected_action (any): 選択されたアクション（未使用）
        coordinates (list): アクションの座標情報
        status_bar (tk.Label): ステータスバーに表示するテキスト情報
    """
    algorithm_window = tk.Toplevel()
    algorithm_window.title("経路選択アルゴリズム")
    algorithm_window.geometry("400x100")


    # メインウィンドウのキャンバスに車の画像を表示
    x, y = coordinates[0]
    car_image_path = "car.png"
    car_image = Image.open(car_image_path)
    car_image = car_image.resize((80, 80))  # 画像のサイズを調整
    car_photo = ImageTk.PhotoImage(car_image)
    car = canvas.create_image(x, y, image=car_photo, anchor=tk.CENTER, tag="car")

    # カウントの初期化
    count = 0
    is_running = False  # タイマーが実行中かどうかのフラグ

    # 車の角度と移動量を保持する変数
    angle = 180
    move_x = 0
    move_y = 0
    i = 0

    def arrival():
        """目的地に到着した際の処理を行います。スタート位置に帰還するか終了するかを選択します。"""
        nonlocal i, angle, move_x, move_y
        if len(coordinates) >= 3 + i:
            i = i + 1
        else:
            result = messagebox.showwarning("到着", "目的地に到着しました！スタート位置に帰りますか？", type=messagebox.YESNO)
            if result == messagebox.YES:
                # リスタートボタンが押された場合の処理
                coordinates.reverse()
                i = 0
                angle = 180
                move_x = 0
                move_y = 0
                pass
            else:
                # 終了ボタンが押された場合の処理
                # ...
                canvas.delete("root")
                canvas.delete("car")
                canvas.delete("start")
                canvas.delete("gool")
                algorithm_window.destroy()
                pass

    def start_algorithm():
        """アルゴリズムの実行を開始します。"""
        nonlocal count, is_running
        if not is_running:
            count = 0
            is_running = True
            count_up()

    def stop_algorithm():
        """アルゴリズムの実行を停止します。"""
        nonlocal is_running
        is_running = False

    def count_up():
        """アルゴリズムのカウントを増やし、画像の回転と移動を行います。"""
        nonlocal count, is_running
        if is_running:
            count += 1
            count_label.config(text=f"実行中... カウント: {count}")
            rotate_image(car, car_photo)  # 画像の回転
            move_image(car)  # 画像の移動
            algorithm_window.after(100, count_up)  # 1秒後に再度呼び出す

    def rotate_image(image_id, photo):
        """画像を回転させます。

        Args:
            image_id (int): 画像オブジェクトのID
            photo (tk.PhotoImage): 回転する画像
        """
        nonlocal angle
        rotated_image = car_image.rotate(360 - angle + 180, expand=True)
        photo.image = ImageTk.PhotoImage(rotated_image)
        canvas.itemconfigure(image_id, image=photo.image)

    def move_image(image_id):
        """画像を移動させます。

        Args:
            image_id (int): 画像オブジェクトのID
        """
        nonlocal x, y, move_x, move_y, angle, i
        move_x = 5 * math.cos(math.radians(angle + 90))  # x軸方向の移動量を修正
        move_y = 5 * math.sin(math.radians(angle + 90))  # y軸方向の移動量を修正
        canvas.move(image_id, move_x, move_y)
        x += move_x
        y += move_y
        distance, closest_point = algorithm_function.shortest_distance(coordinates[0 + i], coordinates[1 + i], (x, y))
        print("distance: {}".format(distance))

        # 目標の座標距離をどうするかを決める
        moved_points = algorithm_function.move_points_along_line(coordinates[0 + i], coordinates[1 + i], closest_point, 10)

        # どのくらいの角度搬送車の誤差を出すかを決めるlamdamがある
        angle = algorithm_function.calculate_angle((x, y), moved_points) + 240 + random.randrange(-5, 5)

        # 到着とされる距離以内にいるか判断
        if math.sqrt((coordinates[1 + i][0] - x) ** 2 + (coordinates[1 + i][1] - y) ** 2) <= 30:
            arrival()

    def on_close():
        """ウィンドウが閉じられる際の処理を行います。"""
        if not messagebox.askyesno("確認", "アルゴリズムシミュレーションを終了しますか？"):
            return
        canvas.delete("root")
        canvas.delete("start")
        canvas.delete("gool")
        canvas.delete("car")
        algorithm_window.destroy()

    # ウィンドウが閉じられたときの処理を設定する
    algorithm_window.protocol("WM_DELETE_WINDOW", on_close)

    # スタートボタンの作成
    start_button = tk.Button(algorithm_window, text="スタート", command=start_algorithm, width=10, height=2, bg="#4CAF50", fg="white")
    start_button.pack(side=tk.LEFT, padx=10, pady=10)

    # ストップボタンの作成
    stop_button = tk.Button(algorithm_window, text="ストップ", command=stop_algorithm, width=10, height=2, bg="#F44336", fg="white")
    stop_button.pack(side=tk.LEFT, padx=10, pady=10)

    # カウント表示のラベル
    count_label = tk.Label(algorithm_window, text=" カウント(処理数): 0", font=("Helvetica", 14))
    count_label.pack(pady=10)
