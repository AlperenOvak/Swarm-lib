#!!IMPORTANT! 
#In this .py file we open mission_planner.py and owerwrite it form the 9th line. 
#Therefore, mission_planner.py must include only "import" and "apf" variable until 9th line.
#The designed number(in our case, it is 9) can be changed later(or all method can be changed either).

import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os.path

class SampleApp(tk.Tk):

    with open("mission_planner.py","r+") as fp:
        lines = fp.readlines()# read an store all lines into list
        fp.seek(0)# move file pointer to the beginning of a file
        fp.truncate()# truncate the file
        fp.writelines(lines[:9])#start writing first 10 lines 

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo,PageThree,PageFour,PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MetuRone Missions", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="3B Formasyon",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Görev Degisimi",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Engelden Kacinma",
                            command=lambda: controller.show_frame("PageThree"))
        button4 = tk.Button(self, text="Kargo Tasima",
                            command=lambda: controller.show_frame("PageFour"))
        button5 = tk.Button(self, text="Yangin Söndürme",
                            command=lambda: controller.show_frame("PageFive"))
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()


class PageOne(tk.Frame):

    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="3B Formasyon", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        def Add_mission():
            
            shape=Num_Edges.get().split(",")
            if shape[0]=="prism":
                num='"prism"'
            elif shape[0]=="cylinder":
                num='"cylinder"'
            else:num=int(Num_Edges.get())
            rad=float(Radius.get())
            h=float(Height.get())
            with open("mission_planner.py", "a") as f:
                        f.write(f"\napf.form_3d({rad}, {num},{h})" )
                        f.write(f"\ntime.sleep({Time_sleep.get()})")
                        f.write(f"\napf.go({(Go.get())})" )
                        f.write(f"\napf.rotate({(Rotation.get())})" )

        def Run():
            Add_mission()
            import os
            os.system("./3d_gui.sh")
            #print(str(Num_Edges.get()))

        def Add_fly(in_num,out_num,id=195,x=1.0,y=1.0,z=0.0): #append new flies (!!!set crazyflies.yaml file to be have only 3 flies and last one's id must be 195!!!)
            print(in_num,out_num)
            while in_num!=out_num:
                id+=1
                x=x+1 if x!=1 else (-1)
                if in_num%3==0: #should be fixed!!
                    y+=1
                with open(os.path.dirname(__file__) +"/../config/crazyflies.yaml", "a") as f:
                    f.write(f"""\n- channel: 125
  id: {id}
  initialPosition:
  - {x}
  - {y}
  - {z}
  type: default""".format(id=id,x=x,y=y,z=z))
                in_num-=1

        def Num_3D():
            with open(os.path.dirname(__file__) +"/../config/crazyflies.yaml","r+") as yaml:
                lines = yaml.readlines()# read an store all lines into list
                yaml.seek(0)# move file pointer to the beginning of a file
                yaml.truncate()# truncate the file
                yaml.writelines(lines[:23])#start writing first 23 lines 
            try:
                num=(2*int(Num_Edges.get()))
                if num<6:
                    messagebox.showerror("Num_3D","Number of Drones must be bigger than 2")
                    answer.config(text="Number of Drones must be bigger than 2")
                elif num-3>0: 
                    id,x,y,z=195,-1.0,1.0,0.0  #our data about new drone
                    Add_fly(num,3)
                h=int(Height.get())
                answer.config(text="Processing")
                if h<0.1: answer.config(text="Input is not invalid")

                    
            except:
                shape=Num_Edges.get().split(",")
                if shape[0]=="prism":
                    Add_fly(int(shape[1]),3)
                    answer.config(text="Processing")
                else:
                    answer.config(text="Input is not invalid")
        
        my_label=tk.Label(self, text="1-->radius")
        my_label.pack(pady=5)
    
        Radius = tk.Entry(self)
        Radius.pack()
        label1 = tk.Label(self, text="2-->num_edges", font=controller.title_font)
        label1.pack(side="top", fill="x", pady=10)
        Num_Edges = tk.Entry(self)
        Num_Edges.pack()

        label1_1 = tk.Label(self, text="3-->height of the prism", font=controller.title_font)
        label1_1.pack(side="top", fill="x", pady=10)
        Height = tk.Entry(self)
        Height.pack()

        label2 = tk.Label(self, text="Check your num firstly", font=controller.title_font)
        label2.pack(fill="x", pady=10)
        debug = tk.Button(self, text="Debug",
                           command=Num_3D )
        debug.pack(pady=10)

        label3=tk.Label(self, text="3-->Time-Sleep")
        label3.pack(pady=5)
        Time_sleep = tk.Entry(self)
        Time_sleep.pack()
        
        label4 = tk.Label(self, text="4-->go ex: [0.0,0.0,0.0]", font=controller.title_font)
        label4.pack(side="top", fill="x", pady=10)
        Go = tk.Entry(self)
        Go.pack()
        
        label5 = tk.Label(self, text="5-->rotation  ex: (degree, step=10(default), duration=3(default)) ", font=controller.title_font)
        label5.pack(side="top", fill="x", pady=10)
        Rotation = tk.Entry(self)
        Rotation.pack()


        button1 = tk.Button(self, text="Run",
                           command=Run )
        button1.pack(pady=5)
        answer=tk.Label(text="")
        answer.pack()


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)
    
    
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Görev Degisimi", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        label1 = tk.Label(self, text="Bu görev teknofestte henüz yok", font=controller.title_font)
        label1.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Engelden Kacinma", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Kargo Tasima", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        label1 = tk.Label(self, text="Bu görev teknofestte henüz yok", font=controller.title_font)
        label1.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Yangin Söndürme", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        i=0

        def mirror():
            nonlocal i
            i=i^1

        cap= cv2.VideoCapture(0)
        
        # Define function to show frame
        def show_frames():
           nonlocal i
           # Get the latest frame and convert into Image
           cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
           cv2image=cv2image[:,::-1] if i==1 else cv2image[:,::]
           img = Image.fromarray(cv2image)
           # Convert image to PhotoImage
           imgtk = ImageTk.PhotoImage(image = img)
           label.imgtk = imgtk
           label.configure(image=imgtk)
           # Repeat after an interval to capture continiously
           label.after(20, show_frames)
        
        show_frames()

        button1 = tk.Button(self, text="Mirror",
                            command=mirror)
        button1.pack(pady=5) 
        
        button2 = tk.Button(self, text="Run", bg="red")
        button2.pack(pady=5)

        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack() 
        


if __name__ == "__main__":
    app = SampleApp()
    app.title('MetuRone Swarm')
    app.mainloop()
