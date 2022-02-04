import tkinter as tk

 # tk.Frameを継承したApplicationクラスを作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ウィンドウの設定
        self.master = master
        self.master.title("ウィンドウのタイトル")
        self.master.geometry("300x200")

        # 実行内容
        self.pack()
        self.create_widget()

    # create_widgetメソッドを定義
    def create_widget(self):

        # ウィジェット変数を生成
        self.msg = tk.StringVar()
        self.msg.set("")

        # print_keysymメソッドを定義
        def print_keysym(event):
            self.keysym = event.keysym
            self.msg.set(self.keysym)

        # label1ウィジェットを作成
        self.label1 = tk.Label(self,text="あなたが押した\nキーは", font=("MSゴシック", "24", "bold"))
        self.label1.pack()

        # label2ウィジェットを作成
        self.label2 = tk.Label(self,textvariable=self.msg, font=("MSゴシック", "24", "bold"))
        self.label2.bind("<Any-KeyPress>", print_keysym)
        self.label2.pack()
        self.label2.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
