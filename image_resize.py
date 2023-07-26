# ファイル: image_resize
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明: 画像の大きさを変更する関数
from PIL import ImageTk, Image

def resize_image(image_path, width, height):
    """_指定した画像のパスから画像を読み込み、指定した幅と高さにリサイズした後、TkinterのImageTk.PhotoImageオブジェクトとして返す関数_

    Args:
        image_path (str): 画像のファイルパス
        width (int): リサイズ後の幅
        height (int): リサイズ後の高さ

    Returns:
        ImageTk.PhotoImage: リサイズされた画像のTkinterオブジェクト
    """
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)