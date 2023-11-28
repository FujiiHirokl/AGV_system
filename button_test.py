import tkinter as tk

def main():
    window = tk.Tk()

    image_start = tk.PhotoImage(file="start_button.png")
    image_middle = tk.PhotoImage(file="tyuukan_button.png")
    image_itizi = tk.PhotoImage(file="itizi_button.png")
    image_target = tk.PhotoImage(file="target_button.png")
    
    image_start_touch = tk.PhotoImage(file="start_button_touch.png")
    image_middle_touch = tk.PhotoImage(file="tyuukan_button_touch.png")
    image_itizi_touch = tk.PhotoImage(file="itizi_button_touch.png")
    image_target_touch = tk.PhotoImage(file="target_button_touch.png")
    
    image_start_clicked = tk.PhotoImage(file="start_button_clicked.png")
    image_middle_clicked = tk.PhotoImage(file="tyuukan_button_clicked.png")
    image_itizi_clicked = tk.PhotoImage(file="itizi_button_clicked.png")
    image_target_clicked = tk.PhotoImage(file="target_button_clicked.png")

    option1_clicked = False
    option2_clicked = False
    option3_clicked = False
    option4_clicked = False

    def show_selection(value):
        print("選択された値:", value)

    def change_image(widget, new_image):
        widget.configure(image=new_image)

    def reset_button_state():
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option1_clicked = False
        option2_clicked = False
        option3_clicked = False
        option4_clicked = False
        change_image(option1, image_start)
        change_image(option2, image_middle)
        change_image(option3, image_itizi)
        change_image(option4, image_target)
        option1.configure(state=tk.NORMAL)
        option2.configure(state=tk.NORMAL)
        option3.configure(state=tk.NORMAL)
        option4.configure(state=tk.NORMAL)

    def on_option1_click(event):
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option1_clicked = not option1_clicked

        if option1_clicked:
            change_image(option1, image_start_clicked)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)
        else:
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option2.configure(state=tk.NORMAL)
            option3.configure(state=tk.NORMAL)
            option4.configure(state=tk.NORMAL)

        if option2_clicked or option3_clicked or option4_clicked:
            reset_button_state()
            option1_clicked = not option1_clicked
            change_image(option1, image_start_clicked)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)

        show_selection(1)

    def on_option2_click(event):
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option2_clicked = not option2_clicked

        if option2_clicked:
            change_image(option2, image_middle_clicked)
            change_image(option1, image_start)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option1.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)
        else:
            change_image(option2, image_middle)
            change_image(option1, image_start)
            change_image(option3, image_itizi)
            change_image(option4, image_target)
            option1.configure(state=tk.NORMAL)
            option3.configure(state=tk.NORMAL)
            option4.configure(state=tk.NORMAL)

        if option1_clicked or option3_clicked or option4_clicked:
            reset_button_state()
            option2_clicked = not option2_clicked
            change_image(option2, image_middle_clicked)
            option1.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)

        show_selection(2)

    def on_option3_click(event):
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option3_clicked = not option3_clicked

        if option3_clicked:
            change_image(option3, image_itizi_clicked)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option4, image_target)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)
        else:
            change_image(option3, image_itizi)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option4, image_target)
            option1.configure(state=tk.NORMAL)
            option2.configure(state=tk.NORMAL)
            option4.configure(state=tk.NORMAL)

        if option1_clicked or option2_clicked or option4_clicked:
            reset_button_state()
            option3_clicked = not option3_clicked
            change_image(option3, image_itizi_clicked)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option4.configure(state=tk.DISABLED)

        show_selection(3)

    def on_option4_click(event):
        nonlocal option1_clicked, option2_clicked, option3_clicked, option4_clicked
        option4_clicked = not option4_clicked

        if option4_clicked:
            change_image(option4, image_target_clicked)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)
        else:
            change_image(option4, image_target)
            change_image(option1, image_start)
            change_image(option2, image_middle)
            change_image(option3, image_itizi)
            option1.configure(state=tk.NORMAL)
            option2.configure(state=tk.NORMAL)
            option3.configure(state=tk.NORMAL)

        if option1_clicked or option2_clicked or option3_clicked:
            reset_button_state()
            option4_clicked = not option4_clicked
            change_image(option4, image_target_clicked)
            option1.configure(state=tk.DISABLED)
            option2.configure(state=tk.DISABLED)
            option3.configure(state=tk.DISABLED)

        show_selection(4)

    def on_option1_leave(event):
        if not option1_clicked:
            change_image(option1, image_start)

    def on_option2_leave(event):
        if not option2_clicked:
            change_image(option2, image_middle)

    def on_option3_leave(event):
        if not option3_clicked:
            change_image(option3, image_itizi)

    def on_option4_leave(event):
        if not option4_clicked:
            change_image(option4, image_target)

    def on_option1_enter(event):
        if not option1_clicked:
            change_image(option1, image_start_touch)
        else:
            change_image(option1, image_start_clicked)

    def on_option2_enter(event):
        if not option2_clicked:
            change_image(option2, image_middle_touch)
        else:
            change_image(option2, image_middle_clicked)

    def on_option3_enter(event):
        if not option3_clicked:
            change_image(option3, image_itizi_touch)
        else:
            change_image(option3, image_itizi_clicked)

    def on_option4_enter(event):
        if not option4_clicked:
            change_image(option4, image_target_touch)
        else:
            change_image(option4, image_target_clicked)

    option1 = tk.Label(window, image=image_start, compound="left", cursor="hand2")
    option2 = tk.Label(window, image=image_middle, compound="left", cursor="hand2")
    option3 = tk.Label(window, image=image_itizi, compound="left", cursor="hand2")
    option4 = tk.Label(window, image=image_target, compound="left", cursor="hand2")

    option1.bind("<Button-1>", on_option1_click)
    option1.bind("<Leave>", on_option1_leave)
    option1.bind("<Enter>", on_option1_enter)

    option2.bind("<Button-1>", on_option2_click)
    option2.bind("<Leave>", on_option2_leave)
    option2.bind("<Enter>", on_option2_enter)

    option3.bind("<Button-1>", on_option3_click)
    option3.bind("<Leave>", on_option3_leave)
    option3.bind("<Enter>", on_option3_enter)

    option4.bind("<Button-1>", on_option4_click)
    option4.bind("<Leave>", on_option4_leave)
    option4.bind("<Enter>", on_option4_enter)

    option1.pack()
    option2.pack()
    option3.pack()
    option4.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
