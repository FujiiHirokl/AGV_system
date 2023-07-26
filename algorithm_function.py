# ファイル: algorithm_function.py
# 作成者: 藤井広輝
# 更新日: 2023/5/20
# 説明: 

# 必要なライブラリをインポート
import math

def shortest_distance(line_start, line_end, point):
    """直線上の最短距離とその点を計算します。

    Args:
        line_start (tuple): 直線の始点の座標 (x1, y1)
        line_end (tuple): 直線の終点の座標 (x2, y2)
        point (tuple): 直線上との最短距離を求める点の座標 (x0, y0)

    Returns:
        tuple: (最短距離, 直線上の最短距離の点の座標)
    """
    x1, y1 = line_start
    x2, y2 = line_end
    x0, y0 = point

    # 直線の方程式を計算
    if x2 - x1 != 0:
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
    else:
        m = float('inf')  # 垂直な直線の場合は傾きを無限大とする
        c = None

    # 直線上の点との距離を計算
    if m != float('inf'):
        distance = abs((m * x0) - y0 + c) / math.sqrt(m**2 + 1)
    else:
        distance = abs(x0 - x1)  # 垂直な直線の場合は x の差分を距離とする

    # 直線上の最短距離の点を計算
    if m != float('inf'):
        x_intercept = (x0 + m * y0 - m * c) / (1 + m**2)
        y_intercept = m * x_intercept + c
        closest_point = (x_intercept, y_intercept)
    else:
        closest_point = (x1, y0)  # 垂直な直線の場合は x 座標は変わらず、y 座標が最短距離の点

    return distance - 5, closest_point

def move_points_along_line(start, end, num_point, distance):
    """直線上の点を指定された距離だけ移動させます。

    Args:
        start (tuple): 直線の始点の座標 (x1, y1)
        end (tuple): 直線の終点の座標 (x2, y2)
        num_point (tuple): 直線上の点の座標 (x, y)
        distance (float): 移動する距離

    Returns:
        tuple: 移動後の点の座標 (新しいx, 新しいy)
    """
    x1, y1 = start
    x2, y2 = end
    z, y = num_point
    if x1 == x2:
        # 直線が垂直な場合
        x_point1 = x_point2 = x1
        y_point1 = y + distance
        y_point2 = y - distance
    else:
        # 直線の傾きを計算
        slope = (y2 - y1) / (x2 - x1)

        # 直線の切片を計算
        intercept = y1 - slope * x1

        if slope == 0:
            # 直線が水平な場合
            x_point1 = z + distance
            x_point2 = z - distance
            y_point1 = y_point2 = y
        else:
            # 直線が一般的な場合
            x_distance = math.sqrt(distance ** 2 / (1 + slope ** 2))
            x_point1 = z + x_distance
            x_point2 = z - x_distance
            y_point1 = slope * x_point1 + intercept
            y_point2 = slope * x_point2 + intercept

    # (x2, y2)に近い方の点を選択
    distance1 = math.sqrt((x_point1 - x2) ** 2 + (y_point1 - y2) ** 2)
    distance2 = math.sqrt((x_point2 - x2) ** 2 + (y_point2 - y2) ** 2)

    if distance1 < distance2:
        return x_point1, y_point1
    else:
        return x_point2, y_point2

def calculate_angle(now, point):
    """2つの点間の直線の角度を計算します。

    Args:
        now (tuple): 始点の座標 (x1, y1)
        point (tuple): 終点の座標 (x2, y2)

    Returns:
        float: 2つの点間の角度（度数法）
    """
    x1, y1 = now
    x2, y2 = point
    dx = x2 - x1
    dy = y2 - y1

    # arctan2関数を使用して角度を計算
    angle_rad = math.atan2(dy, dx)
    # ラジアンから度に変換
    angle_deg = math.degrees(angle_rad)

    return angle_deg
