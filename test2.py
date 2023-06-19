import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

distance_age = 0
i = 0

def trilateration(point1, point2, point3, point4, d1, d2, d3, d4):
    A = np.vstack((2 * (point2 - point1), 2 * (point3 - point1), 2 * (point4 - point1)))
    b = np.array([d1**2 - d2**2 - point1.dot(point1) + point2.dot(point2),
                  d1**2 - d3**2 - point1.dot(point1) + point3.dot(point3),
                  d1**2 - d4**2 - point1.dot(point1) + point4.dot(point4)])
    
    point = np.linalg.lstsq(A, b, rcond=None)[0]
    
    return point

# 測定ポイントの座標
point1 = np.array([10, 10])
point2 = np.array([10, 490])
point3 = np.array([490, 10])
point4 = np.array([490, 490])

# プロットの設定
fig, ax = plt.subplots()
ax.scatter([point1[0], point2[0], point3[0],point4[0]], [point1[1], point2[1], point3[1],point4[1]], color='blue', label='Measurement Points')

plt.xlim(0, 500)
plt.ylim(0, 500)
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.ion()  # インタラクティブモードを有効化
plt.show()


while True:
    # クリックした位置を測位したい位置とする
    print("クリックして測位したい位置を指定してください。右クリックまたはキーボードの 'q' で終了します。")
    clicked_position = np.array(plt.ginput(1, timeout=-1, mouse_stop=3, mouse_pop=2))
    
    if len(clicked_position) == 0:  # 右クリックまたは 'q' が押された場合、ループを終了
        break
    
    clicked_position = clicked_position[0]
    
    # 測定ポイントからの距離にランダムなブレを加える
    d1 = np.linalg.norm(clicked_position - point1) + np.random.normal(0, 0)
    d2 = np.linalg.norm(clicked_position - point2) + np.random.normal(0, 30)
    d3 = np.linalg.norm(clicked_position - point3) + np.random.normal(0, 0)
    d4 = np.linalg.norm(clicked_position - point4) + np.random.normal(0, 0)
    
    # 4点測位の実行
    result = trilateration(point1, point2, point3, point4, d1, d2, d3, d4)
    
    # 結果の表示
    print("推定された位置座標:", result)
    
    # クリックした点と求められた座標の距離を出力
    distance = np.linalg.norm(clicked_position - result)
    distance_age  = distance_age + distance
    print("クリックした点と推定された座標の距離:", distance)
    i = i + 1
    print("クリックした点と推定された座標の距離の平均:", distance_age / i)
    
    # プロットをクリアして再描画
    ax.clear()
    ax.scatter([point1[0], point2[0], point3[0],point4[0]], [point1[1], point2[1], point3[1],point4[1]], color='blue', label='Measurement Points')
    ax.scatter(result[0], result[1], color='red', label='Estimated Position')
    ax.scatter(clicked_position[0], clicked_position[1], color='green', label='Clicked Position')
    ax.add_patch(Circle(point1, d1, fill=False, color='blue', linestyle='--', label='Circle 1'))
    ax.add_patch(Circle(point2, d2, fill=False, color='green', linestyle='--', label='Circle 2'))
    ax.add_patch(Circle(point3, d3, fill=False, color='orange', linestyle='--', label='Circle 3'))
    ax.add_patch(Circle(point4, d4, fill=False, color='orange', linestyle='--', label='Circle 4'))
    plt.xlim(0, 500)
    plt.ylim(0, 500)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.draw()
    plt.pause(0.1)

plt.ioff()  # インタラクティブモードを無効化
plt.close()
