# ファイル: sub_window
# 作成者: 藤井広輝
# 更新日: 2023/5/20
# 説明: AGVからの信号テスト

# 必要なライブラリをインポート
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
import math

# サブウィンドウを作成する関数
def create_sub_window(canvas, status_bar):
    global sub_window
    x = 615  # 初期X座標
    y = 245  # 初期Y座標
    angle = 0  # 初期角度

    # 座標と角度を更新する関数
    def update_coordinates():
        main_x.set(str(x))
        main_y.set(str(y))
        main_angle.set(str(angle))
        status_bar.config(text="x座標: {}   y座標: {}   角度: {}".format(x, y, angle))

    # 確定ボタンを処理する関数
    def handle_confirm(event=None):
        nonlocal angle
        try:
            angle = int(angle_entry.get())
        except ValueError:
            angle = 0
        handle_keypress(None)

    # キーボードの入力を処理する関数
    def handle_keypress(event):
        nonlocal x, y, angle

        if event:
            if event.keysym == "Up":
                y = max(y - 5, 0)
            elif event.keysym == "Down":
                y = min(y + 5, 500)
            elif event.keysym == "Left":
                x = max(x - 5, 0)
            elif event.keysym == "Right":
                x = min(x + 5, 700)

        if event is not None and event.keysym == "q":
            angle = (angle + 5) % 360
        elif event is not None and event.keysym == "w":
            angle = (angle - 5) % 360

        # 画像と線を更新する
        canvas.delete("image")
        canvas.delete("line")

        # 画像を回転させる
        rotated_image = image.rotate(angle)
        photo = ImageTk.PhotoImage(rotated_image)
        canvas.create_image(x, y, anchor=tk.CENTER, image=photo, tags="image")
        canvas.image = photo
        update_coordinates()

        line_length = 120
        center_angle = angle + 90
        side_angle = 45

        # 中心線を描画する
        center_end_x = x + int(line_length * math.cos(math.radians(center_angle)))
        center_end_y = y - int(line_length * math.sin(math.radians(center_angle)))
        canvas.create_line(x, y, center_end_x, center_end_y, fill="red", width=2, tags="line")

        # 右側の線を描画する
        right_angle = center_angle + side_angle
        right_end_x = x + int(line_length * math.cos(math.radians(right_angle)))
        right_end_y = y - int(line_length * math.sin(math.radians(right_angle)))
        canvas.create_line(x, y, right_end_x, right_end_y, fill="red", width=2, tags="line")

        # 左側の線を描画する
        left_angle = center_angle - side_angle
        left_end_x = x + int(line_length * math.cos(math.radians(left_angle)))
        left_end_y = y - int(line_length * math.sin(math.radians(left_angle)))
        canvas.create_line(x, y, left_end_x, left_end_y, fill="red", width=2, tags="line")

    # ウィンドウが閉じられたときの処理
    def on_close():
        if not messagebox.askyesno("確認", "信号シミュレーションを終了しますか？"):
            return
        canvas.delete("image")
        canvas.delete("line")
        sub_window.destroy()

    sub_window = tk.Toplevel()
    sub_window.title("搬送車信号テスト")
    sub_window.geometry("400x300")

    main_x = tk.StringVar()
    main_y = tk.StringVar()
    main_angle = tk.StringVar()

    # X軸のラベルとエントリーを作成する
    x_label = tk.Label(sub_window, text="X軸(0-700):")
    x_label.pack()
    x_entry = tk.Entry(sub_window, textvariable=main_x)
    x_entry.pack()

    # Y軸のラベルとエントリーを作成する
    y_label = tk.Label(sub_window, text="Y軸(0-500):")
    y_label.pack()
    y_entry = tk.Entry(sub_window, textvariable=main_y)
    y_entry.pack()

    # 角度のラベルとエントリーを作成する
    angle_label = tk.Label(sub_window, text="角度(0-360):")
    angle_label.pack()
    angle_entry = tk.Entry(sub_window, textvariable=main_angle)
    angle_entry.pack()

    # 確定ボタンを作成する
    confirm_button = tk.Button(sub_window, text="確定", command=handle_confirm)
    confirm_button.pack()

    # キーボードのイベントをバインドする
    sub_window.bind("<Return>", handle_confirm)
    sub_window.bind("<Up>", handle_keypress)
    sub_window.bind("<Down>", handle_keypress)
    sub_window.bind("<Left>", handle_keypress)
    sub_window.bind("<Right>", handle_keypress)
    sub_window.bind("q", handle_keypress)
    sub_window.bind("w", handle_keypress)

    # 画像を読み込む
    image_path = "car.png"
    image = Image.open(image_path)
    image = image.resize((80, 80))

    # ウィンドウが閉じられたときの処理を設定する
    sub_window.protocol("WM_DELETE_WINDOW", on_close)

    # サブウィンドウをメインループで実行する
    sub_window.mainloop()
