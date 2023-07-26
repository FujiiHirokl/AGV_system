# ファイル: agv_locattion.py
# 作成者: 藤井広輝
# 更新日: 2023/7/25
# 説明: AGV (Automated Guided Vehicle) の位置情報を管理し、UDPサーバーとして動作するGUIアプリケーションです。

# 必要なライブラリをインポート
import tkinter as tk
import socket
import threading

def AGV_handle_submit(canvas, start_photo):
    """UDPサーバーアプリケーションのGUIを作成します。

    Args:
        canvas (tk.Canvas): キャンバスウィジェット
        start_photo (ImageTk.PhotoImage): 画像のためのPhotoImageオブジェクト
    """
    # 以下の関数内で使う変数を初期化
    HOST = '127.0.0.1'  # ホストIPアドレス
    PORT = 8080  # ポート番号
    server_socket = None  # グローバル変数としてサーバーソケットを定義

    def start_server():
        """UDPサーバーの待機とメッセージの受信を行います。"""
        nonlocal server_socket  # ローカル変数ではなく外側の変数を参照するためのnonlocal宣言

        # ソケットを作成し、ホストとポートにバインド
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((HOST, PORT))

        update_message_label("サーバーを開始しました。")

        while True:
            # データを受信する
            data, client_address = server_socket.recvfrom(1024)
            data = data.decode()
            update_message_label(f"クライアントからのメッセージ: {data}")

            # ドロップダウンメニューにデータを追加
            add_data_to_drop_menu(data)

            # クライアントにメッセージを送信する
            message = "サーバーからのメッセージ: データが送信できました！"
            server_socket.sendto(message.encode(), client_address)

    def start_server_thread():
        """サーバースレッドを開始します。"""
        threading.Thread(target=start_server).start()

    def close_connection():
        """サーバーソケットを閉じます。"""
        nonlocal server_socket
        if server_socket:
            server_socket.close()
            update_message_label("接続を閉じました。")
            server_socket = None  # サーバーソケットをリセット

    def add_data_to_drop_menu(data):
        """ドロップダウンメニューにデータを追加します。

        Args:
            data (str): ドロップダウンメニューに追加するデータ
        """
        drop_menu['menu'].add_command(label=data, command=lambda value=data: selected_data.set(value))
        
    def on_decision_button_click():
        """決定ボタンがクリックされたときの処理を行います。"""
        selected_value = selected_data.get()
        # この例では、選択された項目をラベルに表示するだけ
        # 選択された値に応じて任意の処理を追加することができます
        
    def on_selection_change(*args):
        """ドロップダウンメニューの選択が変更されたときの処理を行います。"""
        selected_value = selected_data.get()
        # 選択された項目の処理を行う
        data = selected_value  # 例として与えられたデータ

        # カンマでデータを分割してint型に変換
        data_list = data.split(',')
        num1 = int(data_list[0])
        num2 = int(data_list[1])
        
        # キャンバス上の選択用オブジェクトを更新
        canvas.delete("select")
        if start_photo:
            canvas.create_image(num1, num2, anchor=tk.CENTER, image=start_photo, tag="select")
            
        # この例では、選択したデータをラベルに表示するだけ
        update_message_label(f"選択したデータ: {selected_value}")

    # ウィンドウを作成
    window = tk.Tk()
    window.title("UDPサーバー")

    # 接続待機ボタンを作成
    start_button = tk.Button(window, text="接続待機", command=start_server_thread)
    start_button.pack(pady=10)

    # 接続を閉じるボタンを作成
    close_button = tk.Button(window, text="接続を閉じる", command=close_connection)
    close_button.pack(pady=5)

    # ラベルを作成してウィンドウに配置
    message_label = tk.Label(window, text="サーバーが待機中です。", font=("Helvetica", 12))
    message_label.pack(pady=10)

    def update_message_label(new_message):
        """メッセージ表示ラベルを更新する関数"""
        message_label.config(text=new_message)

    # ドロップダウンメニューに表示される選択肢リストを管理する変数
    selected_data = tk.StringVar(window)
    selected_data.set("選択したデータ")
    
    # 選択されたタイミングで動作する関数を登録
    selected_data.trace("w", on_selection_change)

    # ドロップダウンメニューを作成
    drop_menu = tk.OptionMenu(window, selected_data, "選択したデータ")
    drop_menu.pack(pady=5)
    
    # 決定ボタンを作成
    decision_button = tk.Button(window, text="決定", command=on_decision_button_click)
    decision_button.pack(pady=5)

    # ウィンドウを表示してイベントループを開始
    window.mainloop()

