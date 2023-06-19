import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

distance_age = 0
i = 0

def calculate_distance(point1, point2):
    return np.abs(np.linalg.norm(point1 - point2))



def trilateration(point1, point2, point3, d1, d2, d3):
    A = 2 * np.abs(point2 - point1)  # ベクトル A の計算
    B = 2 * np.abs(point3 - point1)  # ベクトル B の計算


    # 行列 C の計算
    C = d1**2 -  np.dot(point1, point1) - d2**2 + np.dot(point2, point2)


    # 行列 D 
    # の計算
    D = d1**2 - d3**2 - np.dot(point1, point1) + np.dot(point3, point3)

    print("ベクトル A:", A)
    print("ベクトル B:", B)
    print("行列 C:", C)
    print("行列 D:", D)

    # 行列方程式を解く
    coefficients = np.vstack((A, B)).T
    constants = np.array([C, D])
    point = np.linalg.solve(coefficients, constants)
    q,w = point
    if q > 0 and w > 0:
        point = (q, w)
    elif q > 0 and w < 0:
        point = (q,w*-1)
    elif q < 0 and w > 0:
        point = (q*-1,w)
    elif q < 0 and w < 0:
        point = (q*-1,w*-1)
        

    print("行列方程式の解:", point)

    return point

# 測定ポイントの座標
point1 = np.array([10, 10])
point2 = np.array([10, 490])
point3 = np.array([490, 10])
point4 = np.array([490,490])


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
    print(clicked_position)
    
    # 測定ポイントからの距離にランダムなブレを加える
    d1 = np.linalg.norm(clicked_position - point1) + np.random.normal(-20, 20)
    d2 = np.linalg.norm(clicked_position - point2) + np.random.normal(-20, 20)
    d3 = np.linalg.norm(clicked_position - point3) + np.random.normal(-20, 20)
    d4 = np.linalg.norm(clicked_position - point4) + np.random.normal(-20, 20)
    
    # 3点測位の実行
    result = trilateration(point1, point2, point3, d1, d2, d3)
    result_value = calculate_distance(calculate_distance(result, point1), d1) + calculate_distance(calculate_distance(result, point2), d2) + calculate_distance(calculate_distance(result, point3), d3)

    result2 = trilateration(point2, point3, point4, d2, d3, d4)
    result2_value = calculate_distance(calculate_distance(result2, point2), d2) + calculate_distance(calculate_distance(result2, point3), d3) + calculate_distance(calculate_distance(result2, point4), d4)

    result3 = trilateration(point3, point4, point1, d3, d4, d1)
    result3_value = calculate_distance(calculate_distance(result3, point1), d1) + calculate_distance(calculate_distance(result3, point3), d3) + calculate_distance(calculate_distance(result3, point4), d4)

    result4 = trilateration(point4, point1, point2, d4, d1, d2)
    result4_value = calculate_distance(calculate_distance(result4, point1), d1) + calculate_distance(calculate_distance(result4, point2), d2) + calculate_distance(calculate_distance(result4, point4), d4)

    min_result = min(result_value, result2_value, result3_value, result4_value)

    # 結果の表示s
    print("推定された位置座標:", result)
    print("推定された位置座標:", result2)
    print("推定された位置座標:", result3)
    print("推定された位置座標:", result4)
    
    
    # クリックした点と求められた座標の距離を出力
    distance = np.linalg.norm(clicked_position - result)
    print("クリックした点と推定された座標の距離:", distance)
    distance = np.linalg.norm(clicked_position - result2)
    print("クリックした点と推定された座標の距離:", distance)
    distance = np.linalg.norm(clicked_position - result3)
    print("クリックした点と推定された座標の距離:", distance)
    distance = np.linalg.norm(clicked_position - result4)
    print("クリックした点と推定された座標の距離:", distance)
    # i = i + 1
    #distance_age = distance_age + distance
    # print("クリックした点と推定された座標の距離の平均:", distance_age / i)
    
    # プロットをクリアして再描画
    ax.clear()
    ax.scatter([point1[0], point2[0], point3[0],point4[0]], [point1[1], point2[1], point3[1],point4[1]], color='blue', label='Measurement Points')
    if min_result == result_value:
        print("Minimum value is from result:", result)
        ax.scatter(result[0], result[1], color='red', label='Estimated Position')
    elif min_result == result2_value:
        print("Minimum value is from result2:", result2)
        ax.scatter(result2[0], result2[1], color='green', label='Estimated Position')
    elif min_result == result3_value:
        print("Minimum value is from result3:", result3)
        ax.scatter(result3[0], result3[1], color='orange', label='Estimated Position')
    else:
        print("Minimum value is from result4:", result4)
        ax.scatter(result4[0], result4[1], color='blue', label='Estimated Position')


    #ax.scatter(clicked_position[0], clicked_position[1], color='green', label='Clicked Position')
    ax.add_patch(Circle(point1, d1, fill=False, color='red', linestyle='--', label='Circle 1'))
    ax.add_patch(Circle(point2, d2, fill=False, color='red', linestyle='--', label='Circle 2'))
    ax.add_patch(Circle(point3, d3, fill=False, color='red', linestyle='--', label='Circle 3'))
    ax.add_patch(Circle(point4, d4, fill=False, color='red', linestyle='--', label='Circle 4'))
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
