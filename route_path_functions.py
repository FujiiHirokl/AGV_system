# ファイル: route_path_function.py
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明:経路情報の設定と管理を行う

#必要なモジュールをインポート
import tkinter as tk
from global_variable import start, gool


def root_set(start,half,gool,root):
    """経路を順番に並べる関数

    この関数は、スタート地点、中間地点、ゴール地点の座標を受け取り、それらを提供された root リストに
    順番に追加して、正しい順序で経路を表現します。

    Args:
        start (Tuple[int, int]): スタート地点の座標 (x, y)。
        half (List[Tuple[int, int]]): 中間地点の座標 (x, y) を格納するリスト。
        gool (Tuple[int, int]): ゴール地点の座標 (x, y)。
        root (List[Tuple[int, int]]): 経路の点を順番に格納するリスト。
    """
    if start != (0, 0):
        root.append(start)
        
    for coordinate in half:
        if coordinate != (0, 0):
            root.append(coordinate)
    if gool != (0, 0):
        root.append(gool)


def handle_start(x, y, start_photo, canvas):
    """
    スタート地点の設定を処理する関数

    この関数は、クリックした位置の座標をグローバル変数 start に更新し、その座標を使ってキャンバス上で
    新しいスタート地点を表示します。

    Args:
        x (int): クリックされた位置の x 座標。
        y (int): クリックされた位置の y 座標。
        start_photo (PhotoImage): スタート地点を表現するイメージ。
        canvas (Canvas): Tkinter のキャンバスオブジェクト。

    Returns:
        Tuple[int, int]: 更新されたスタート地点の座標 (x, y)。
    """
    global start
    start = (x, y)
    p1, p2 = start
    canvas.delete("start")
    canvas.create_image(p1, p2, anchor=tk.CENTER, image=start_photo, tag="start")
    return start


def handle_half(x, y, canvas, num, half):
    """
    中間地点の設定を処理する関数

    この関数は、クリックした位置の座標を中間地点のリスト (half) に追加し、キャンバス上で中間地点の
    ナンバーを表示します。

    Args:
        x (int): クリックされた位置の x 座標。
        y (int): クリックされた位置の y 座標。
        canvas (Canvas): Tkinter のキャンバスオブジェクト。
        num (int): 現在の中間地点の数。
        half (List[Tuple[int, int]]): 中間地点の座標 (x, y) を格納するリスト。
    """
    num += 1
    half.append((x, y))
    for i, coordinate in enumerate(half):
        x1, y1 = coordinate
        canvas.create_text(x1, y1, text=str(i + 1), font=("Arial", 24), tag="flag")


def handle_stop(x, y, canvas, num, half, stop, stop_photo):
    """
    一時停止地点の設定を処理する関数

    この関数は、クリックした位置の座標を中間地点のリスト (half) に追加し、キャンバス上で中間地点の
    ナンバーを表示します。また、一時停止地点のインデックスを stop リストに追加します。

    Args:
        x (int): クリックされた位置の x 座標。
        y (int): クリックされた位置の y 座標。
        canvas (Canvas): Tkinter のキャンバスオブジェクト。
        num (int): 現在の中間地点の数。
        half (List[Tuple[int, int]]): 中間地点の座標 (x, y) を格納するリスト。
        stop (List[int]): 一時停止地点のインデックスを格納するリスト。
        stop_photo (PhotoImage): 一時停止地点を表現するイメージ。
    """
    canvas.create_image(x, y, anchor=tk.CENTER, image=stop_photo, tag="stop")
    num += 1
    half.append((x, y))
    stop.append(num + 1)
    for i, coordinate in enumerate(half):
        x1, y1 = coordinate
        canvas.create_text(x1, y1, text=str(i + 1), font=("Arial", 24), tag="flag")


def handle_goal(x, y, gool_photo, canvas):
    """
    ゴール地点の設定を処理する関数

    この関数は、クリックした位置の座標をグローバル変数 gool に更新し、その座標を使ってキャンバス上で
    新しいゴール地点を表示します。

    Args:
        x (int): クリックされた位置の x 座標。
        y (int): クリックされた位置の y 座標。
        gool_photo (PhotoImage): ゴール地点を表現するイメージ。
        canvas (Canvas): Tkinter のキャンバスオブジェクト。

    Returns:
        Tuple[int, int]: 更新されたゴール地点の座標 (x, y)。
    """
    global gool
    gool = (x, y)
    canvas.delete("gool")
    canvas.create_image(x, y, anchor=tk.CENTER, image=gool_photo, tag="gool")
    return gool
