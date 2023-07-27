# ファイル: Draw_line
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明: 描写プログラム

import angle_calculation
def line_picture(root,canvas,angles):
    """_直線を描写する関数_
    Args:
        root (list): 描写する点の座標が格納されたリスト
        canvas (tkinter.Canvas): 描写するキャンバス
        angles (list): 各点の角度が格納されるリスト
    """
    for i in range(len(root) - 1):
        x1, y1 = root[i]
        x2, y2 = root[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red",
                           dash=(4, 2), width=8, tags="root")
        if(i >= 1):
            canvas.create_text(int(x1)+30, int(y1)+30, text=str(round(angles[i-1], 2)), font=("Arial", 12), tag="angle")
            
def angle_picture(root,angles):
    """_三点の座標から角度を計算し、角度のリストを更新する関数_
    Args:
        root (list): 三点の座標が格納されたリスト
        angles (list): 各点の角度が格納されるリスト
    """
    if len(root) >= 3:
        start_index = len(root) - 3  # 最後の3つの座標のインデックスの開始位置
        for i in range(start_index, len(root)-2):
            x1, y1 = root[i]
            x2, y2 = root[i+1]
            x3, y3 = root[i+2]
            angle = angle_calculation.calculate_angle(x1, y1, x2, y2, x3, y3)
            angles.append(round(angle,2))
    