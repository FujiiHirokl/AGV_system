# ファイル: Angel_calculation
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明: 3つの座標から角度を計算するプログラム
import math

def calculate_angle(x1, y1, x2, y2, x3, y3):
    """_三つの座標から角度を計算する関数_

    Args:
        x1 (float): 座標1のx座標
        y1 (float): 座標1のy座標
        x2 (float): 座標2のx座標
        y2 (float): 座標2のy座標
        x3 (float): 座標3のx座標
        y3 (float): 座標3のy座標
    Returns:
        float: 計算された角度（度数法）
    """
    # 1つ目の座標から真ん中の座標へのベクトルの成分を求める
    v1_x = int(x2) - int(x1)
    v1_y = int(y2) - int(y1)

    # 真ん中の座標から3つ目の座標へのベクトルの成分を求める
    v2_x = int(x3) - int(x2)
    v2_y = int(y3) - int(y2)

    # ベクトルの内積を計算
    dot_product = v1_x * v2_x + v1_y * v2_y

    # ベクトルの大きさを計算
    v1_length = math.sqrt(v1_x**2 + v1_y**2)
    v2_length = math.sqrt(v2_x**2 + v2_y**2)

    # ゼロ除算が発生する場合に角度を0として扱う
    if v1_length * v2_length == 0:
        return 0

    # ラジアン単位の角度を計算
    angle_rad = math.acos(dot_product / (v1_length * v2_length))

    # 角度を度数法に変換
    angle_deg = math.degrees(angle_rad)

    # 座標1と座標2の線から見た座標2と座標3の線の角度が座標1と座標2の線の右側ならプラス、左側ならマイナスにする
    if v1_x * v2_y - v1_y * v2_x < 0:
        angle_deg *= -1

    return -angle_deg