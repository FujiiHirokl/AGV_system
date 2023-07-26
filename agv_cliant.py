# ファイル: agv_client.py
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明: UDPプロトコルを使用してサーバーにメッセージを送信し、
#       サーバーからのメッセージを受信して表示するUDPクライアントアプリケーション

# 必要なライブラリをインポート
import tkinter as tk  # TkinterをGUIの作成に使用
import socket  # ソケット通信のためのライブラリをインポート

import image_resize

# グローバル変数としてクライアントソケットを定義
client_socket = None

def send_message():
    """メッセージの送信を行う関数"""
    global client_socket  # グローバルのクライアントソケットを使用

    if client_socket is None:
        update_message_label("接続していません。接続を開始してください。")
        return

    # ユーザーが入力したメッセージを取得
    message = message_entry.get()

    # サーバーにメッセージを送信する
    client_socket.sendto(message.encode(), (HOST, PORT))

    # サーバーからのメッセージを受信し、表示する
    data, _ = client_socket.recvfrom(1024)
    update_message_label(f"サーバーからのメッセージ: {data.decode()}")

def start_connection():
    """サーバーとの接続を開始する関数"""
    global client_socket  # グローバルのクライアントソケットを使用

    # ホストとポート
    global HOST, PORT
    HOST = '127.0.0.1'  # ホストIPアドレス
    PORT = 8080  # ポート番号

    if client_socket is None:
        # ソケットを作成し、ホストとポートにバインド
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        update_message_label("サーバーに接続しました。")

def close_connection():
    """サーバーとの接続を閉じる関数"""
    global client_socket

    if client_socket:
        client_socket.close()
        update_message_label("接続を閉じました。")
        client_socket = None  # クライアントソケットをリセット

def update_message_label(new_message):
    """メッセージ表示ラベルを更新する関数"""
    message_label.config(text=new_message)

# ウィンドウを作成
window = tk.Tk()
window.title("UDPクライアント")

# ラベルを作成してウィンドウに配置
message_label = tk.Label(window, text="サーバーからのメッセージを受信します。", font=("Helvetica", 12))
message_label.pack(pady=10)

# メッセージ入力用のテキストボックスを作成してウィンドウに配置
message_entry = tk.Entry(window, font=("Helvetica", 12))
message_entry.pack(pady=5)

# 送信ボタンを作成してウィンドウに配置
send_button = tk.Button(window, text="送信", command=send_message)
send_button.pack(pady=10)

# 接続開始ボタンを作成してウィンドウに配置
connect_button = tk.Button(window, text="接続開始", command=start_connection)
connect_button.pack(pady=5)

# 接続を閉じるボタンを作成してウィンドウに配置
close_button = tk.Button(window, text="接続を閉じる", command=close_connection)
close_button.pack(pady=5)

# ウィンドウを表示してイベントループを開始
window.mainloop()
