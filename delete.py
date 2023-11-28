# ファイル: delete.py
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明: データベースから経路情報を削除するウィンドウプログラム

# 必要なライブラリをインポート
import tkinter as tk
from tkinter import messagebox
import mysql.connector


# 必要な自作ライブラリをインポート
import image_resize

# データベースへの接続を確立
connector = mysql.connector.connect(
    user='root', 
    password='wlcm2T4' ,
    host='localhost', 
    database='route', 
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'  # ここを変更
)

cursor = connector.cursor()


def delete_window(canvas):
    """経路情報削除ウィンドウを作成します。

    Args:
        canvas (tk.Canvas): キャンバスオブジェクト
    """
    def on_window_close():
        """ウィンドウが閉じられた際の処理を行います。"""
        canvas.delete("start")
        canvas.delete("root")
        canvas.delete("stop")
        canvas.delete("flag")
        canvas.delete("gool")
        canvas.delete("angle")
        delete_window.destroy()

    # 新しいウィンドウを作成
    delete_window = tk.Toplevel()
    delete_window.title("経路情報削除")
    delete_window.protocol("WM_DELETE_WINDOW", on_window_close)

    # トランザクションの開始
    connector.start_transaction()

    # 経路名の取得クエリを実行
    query = "SELECT DISTINCT SQL_NO_CACHE 経路番号, 経路名 FROM route_data ORDER BY 経路番号 ASC"
    cursor.execute(query)
    results = cursor.fetchall()

    # トランザクションのコミット
    connector.commit()

    # 経路番号と経路名の形式の文字列配列に変換
    route_names = [f"{row[0]}:{row[1]}" for row in results]

    # ドロップダウンメニューの作成
    selected_route = tk.StringVar(delete_window)
    selected_route.set("経路を選択してください")  # 初期選択値

    dropdown_menu = tk.OptionMenu(delete_window, selected_route, *route_names)
    dropdown_menu.pack()

    def handle_selection(*args):
        """経路選択時の処理を行います。"""
        selected_item = selected_route.get()
        coordinates = []

        # トランザクションの開始
        connector.start_transaction()

        # 特定の項目名の座標x, yを順番が少ない順に取得するクエリを実行
        query = "SELECT SQL_NO_CACHE x, y FROM route_data WHERE 経路名 = '{}' ORDER BY 順番 ASC".format(selected_item.split(":")[1])
        cursor.execute(query)
        results = cursor.fetchall()

        # トランザクションのコミット
        connector.commit()

        # 結果を(x, y)形式の配列に格納
        for row in results:
            coordinates.append((row[0], row[1]))

        angles = []
        
        query = "SELECT 角度 FROM route_data WHERE 経路名 = '{}' AND 角度 IS NOT NULL ORDER BY 順番 ASC".format(selected_item.split(":")[1])
        cursor.execute(query,)
        results = cursor.fetchall()
        connector.commit()
        angles = [row[0] for row in results if row[0] is not None]

        print(angles)

        # 現在描画されている線を削除
        canvas.delete("root")
        canvas.delete("flag")
        canvas.delete("stop")
        canvas.delete("angle")

        # キャンバスを更新して削除した線が即座に表示されないようにする
        canvas.update()

        # 座標情報を利用して線を描画
        for i in range(len(coordinates) - 1):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill="red", dash=(4, 2), width=8, tags="root")
            canvas.create_text(x1, y1, text=str(i), font=("Arial", 24), tag="flag")
            if(i >= 1):
                canvas.create_text(x1+30, y1+30, text=str(round(angles[i-1], 2)), font=("Arial", 12), tag="angle")

        canvas.delete("start")
        p1, p2 = coordinates[0]
        canvas.create_image(p1, p2, anchor=tk.CENTER, image=start_photo, tag="start")
        canvas.delete("gool")
        p3, p4 = coordinates[-1]
        canvas.create_image(p3, p4, anchor=tk.CENTER, image=gool_photo, tag="gool")

        query = "SELECT x, y FROM route_data WHERE 経路名 = %s AND 一時停止 = 1"
        cursor.execute(query, (format(selected_item.split(":")[1]),))
        results = cursor.fetchall()

        # トランザクションのコミット
        connector.commit()
        route_coordinates = []

        # 結果を(x, y)形式の配列に格納
        canvas.delete("stop")
        for row in results:
            print(row)
            route_coordinates.append((row[0], row[1]))

        for i in range(len(route_coordinates)):
            x1, y1 = route_coordinates[i]
            canvas.create_image(x1, y1, anchor=tk.CENTER, image=stop_photo, tag="stop")

    def handle_delete():
        """削除ボタンが押された際の処理を行います。"""
        selected_item = selected_route.get()
        messagebox.showinfo("削除完了", "経路が削除されました。")
        selected_route_name = selected_item.split(":")[1]

        # トランザクションの開始
        connector.start_transaction()

        # SQLクエリを動的に構築
        query = "DELETE FROM route_data WHERE 経路名 = '{}'".format(selected_route_name)
        # クエリを実行
        cursor.execute(query)

        # トランザクションのコミット
        connector.commit()

        canvas.delete("start")
        canvas.delete("root")
        canvas.delete("flag")
        canvas.delete("gool")
        canvas.delete("stop")
        canvas.delete("angle")
        # ウィンドウを閉じる
        delete_window.destroy()

    # 選択変更時のイベントハンドラを設定
    selected_route.trace('w', handle_selection)

    # 標示画像の変形
    start_photo = image_resize.resize_image("start_flag.png", 40, 40)
    stop_photo = image_resize.resize_image("itiziteisi.png", 40, 40)
    gool_photo = image_resize.resize_image("gool.jpg", 40, 40)

    # 以下はGUIの初期化やキャンバスの作成などのコードです
    # 削除ボタンの作成
    delete_button = tk.Button(delete_window, text="削除", command=handle_delete)
    delete_button.pack()
