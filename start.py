import tkinter as tk
import Main
import monitoring
# メインウィンドウを作成
root = tk.Tk()
root.title("無人搬送車制御アプリケーション ver1.0.0")

# ウィンドウサイズを固定
root.geometry("501x340")
root.resizable(False, False)  # サイズ変更を無効にする

# 画像を読み込む
bg_image = tk.PhotoImage(file="haguruma.png")

# 画像をリサイズ
resized_bg_image = bg_image.zoom(1, 1)

# ラベルにリサイズした画像を設定
bg_label = tk.Label(root, image=resized_bg_image)
bg_label.place(x=0, y=0)

def open_next_window1():
    Main.aaa()

def open_next_window2():
    monitoring.monitaring()

# ボタンのスタイルをカスタマイズ（かっこいいデザイン）
button1 = tk.Button(root, text="経路登録画面へ", command=open_next_window1, bg="navy", fg="white", font=("Helvetica", 14), padx=10, pady=5, borderwidth=3, relief="ridge", width=20)
button1.place(x=90, y=210)

# 別のボタンを追加
button2 = tk.Button(root, text="モニタリング画面へ", command=open_next_window2, bg="darkorange", fg="white", font=("Helvetica", 14), padx=10, pady=5, borderwidth=3, relief="ridge", width=20)
button2.place(x=90, y=150)

root.mainloop()
