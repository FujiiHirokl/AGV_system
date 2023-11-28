from PIL import Image, ImageDraw

def create_pixel_grid_with_alternating_thickness(width, height, thin_line_spacing, thick_line_spacing, thin_line_thickness, thick_line_thickness):
    """
    指定された幅と高さの画像に、細い線と太い線を交互に描画する関数です。

    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        thin_line_spacing (int): 細い線のピクセル間隔
        thick_line_spacing (int): 太い線のピクセル間隔
        thin_line_thickness (int): 細い線の太さ
        thick_line_thickness (int): 太い線の太さ
    """
    # 画像を作成します
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 細い線を描画します
    for y in range(0, height, thin_line_spacing):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=thin_line_thickness)

    for x in range(0, width, thin_line_spacing):
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0), width=thin_line_thickness)

    # 太い線を描画します
    for y in range(0, height, thick_line_spacing):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=thick_line_thickness)

    for x in range(0, width, thick_line_spacing):
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0), width=thick_line_thickness)

    # 画像を保存します
    image.save("pixel_grid_with_alternating_thickness.png")

    # 画像を表示します
    image.show()

if __name__ == "__main__":
    # 細い線と太い線のピクセル間隔と太さを指定して画像を生成します
    create_pixel_grid_with_alternating_thickness(800, 600, 10, 100, 1, 4)
