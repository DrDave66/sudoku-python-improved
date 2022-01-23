import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_214=tk.Button(root)
        GButton_214["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_214["font"] = ft
        GButton_214["fg"] = "#000000"
        GButton_214["justify"] = "center"
        GButton_214["text"] = "Button"
        GButton_214.place(x=50,y=50,width=171,height=30)
        GButton_214["command"] = self.GButton_214_command

        GLabel_618=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_618["font"] = ft
        GLabel_618["fg"] = "#333333"
        GLabel_618["justify"] = "center"
        GLabel_618["text"] = "label"
        GLabel_618.place(x=20,y=10,width=70,height=25)

        GLabel_222=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_222["font"] = ft
        GLabel_222["fg"] = "#333333"
        GLabel_222["justify"] = "center"
        GLabel_222["text"] = "label"
        GLabel_222.place(x=90,y=150,width=70,height=25)

        GCheckBox_966=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GCheckBox_966["font"] = ft
        GCheckBox_966["fg"] = "#333333"
        GCheckBox_966["justify"] = "center"
        GCheckBox_966["text"] = "CheckBox"
        GCheckBox_966.place(x=170,y=110,width=70,height=25)
        GCheckBox_966["offvalue"] = "0"
        GCheckBox_966["onvalue"] = "1"
        GCheckBox_966["command"] = self.GCheckBox_966_command

        GRadio_807=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_807["font"] = ft
        GRadio_807["fg"] = "#333333"
        GRadio_807["justify"] = "center"
        GRadio_807["text"] = "RadioButton"
        GRadio_807.place(x=320,y=180,width=85,height=25)
        GRadio_807["command"] = self.GRadio_807_command

        GRadio_970=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_970["font"] = ft
        GRadio_970["fg"] = "#333333"
        GRadio_970["justify"] = "center"
        GRadio_970["text"] = "RadioButton"
        GRadio_970.place(x=310,y=210,width=85,height=25)
        GRadio_970["command"] = self.GRadio_970_command

        GRadio_917=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_917["font"] = ft
        GRadio_917["fg"] = "#333333"
        GRadio_917["justify"] = "center"
        GRadio_917["text"] = "RadioButton"
        GRadio_917.place(x=300,y=160,width=85,height=25)
        GRadio_917["command"] = self.GRadio_917_command

    def GButton_214_command(self):
        print("command")


    def GCheckBox_966_command(self):
        print("command")


    def GRadio_807_command(self):
        print("command")


    def GRadio_970_command(self):
        print("command")


    def GRadio_917_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
