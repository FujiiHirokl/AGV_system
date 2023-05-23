"""""""""""""""""""""""""""""""""""""""""""""
ファイル:algorithm_function.py
作成者:藤井広輝
更新日:2023/5/20
説明
経路選択アルゴリズムに使った関数が格納されている
"""""""""""""""""""""""""""""""""""""""""""""
import math
"""
直線と点の最短距離を求める関数
引数:line_start((x,y))、line_end((x,y)),point(x,y)
line_startはスタート地点,line_endはゴール。pointはAGVの現在座標
戻り値:distance(x), closest_point(x,y)
distanceは最短の距離、closest_pointは最短の点
"""
def shortest_distance(line_start, line_end, point):
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

    return distance, closest_point


"""
与えられた2点の座標をつなぐ直線上にある点を指定した数だけ2点の後者側に移動させる関数
引数:line_start((x,y))、line_end((x,y)),numpoint(x),point((x,y))
line_startはスタート地点,line_endはゴール。numpointは最短の点,distanceは指定する距離
戻り値:distance(x), closest_point(x,y)
distanceは最短の距離、closest_pointは最短の点
"""

def move_points_along_line(stert,end,numpoint, distance):
    x1,y1 = stert
    x2,y2 = end
    z,y = numpoint
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
        return (x_point1, y_point1)
    else:
        return (x_point2, y_point2)


"""
#現在の座標と角度から、目標座標の方向を向くために回転する角度を求める関数
引数:now((x,y)),point((x,y))
nowは今のAGVの位置、pointは目標地点
戻り値:distance(x), closest_point(x,y)
distanceは最短の距離、closest_pointは最短の点
"""

#現在の座標と角度から、目標座標の方向を向くために回転する角度を求める関数
def calculate_angle(now, point):
    x1,y1=now
    x2,y2=point
    dx = x2 - x1
    dy = y2 - y1

    # arctan2関数を使用して角度を計算
    angle_rad = math.atan2(dy, dx)
    # ラジアンから度に変換
    angle_deg = math.degrees(angle_rad)

    return angle_deg