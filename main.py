"""
This is the main file for the GUI of the application.
The App converts the user given prompt to an image.

Developed By : Mujtaba Shafqat

"""

from tkinter import *
from tkinter import ttk
from Engine import AppEngine
from tkinter import filedialog
from PIL import ImageTk, Image
import threading

# env variables
_primary = '#f2f2f2'
_secondary = '#e6e6e6'
_alert = '#0F9552'
_jazz = '#c42f23'
_topBar = '#2c2f33'
_title = 'Powers Artjourney'
_buttons = "#ffb31a"
_placeHolder = "A tree in the middle of a field..."


class App:
    """Main GUI class"""
    root = Tk()
    def __init__(self):
        """constructor for GUI class"""
        root = self.root
        root.minsize(500, 600)
        root.state('zoomed')
        root.title(_title)
        self._status_ = 0
        
        def remove_focus(e):
            e.widget.focus()
        
        self.root.bind("<Button-1>", remove_focus)
        
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight() 
        
        image = Image.open("assets/home.png")
        image = image.resize((self.width, self.height-15))
        self.img = ImageTk.PhotoImage(image)
        
        self.sampleImg = self.resize_image("assets/home1.png")
        
        wel = Image.open("assets/welcome.png")
        wel = wel.resize((int(3*(self.width/7)), 200))
        self.wel = ImageTk.PhotoImage(wel)
        
        self.main1Frame = Frame(root, width=self.width+2, height=self.height)
        self.main1Frame.place(x=0, y=0)
        
        imgLabel = Label(self.main1Frame, image=self.img)
        imgLabel.place(x=-2, y=-1)
        
        self.main2Frame = Frame(root, bg='red', width=self.width, height=self.height)
        self.main2Frame.place(x=0, y=0)
        
        tryNowButton = Button(self.main1Frame, text="Try Now", font=("Arial", 14), 
                              bg=_jazz, fg="white", width=14, height=2, relief='flat',
                              activebackground=_jazz, highlightthickness=0,
                              activeforeground="white",
                              command=self.main2Frame.tkraise)
        tryNowButton.place(x=self.width/2-80, y=self.height/2-35)
        
        topBar =  Frame(self.main2Frame, bg=_jazz, width=self.width, height=30)
        topBar.pack(side=TOP, fill=Y)
        topBar.pack_propagate(0)
                
        homeLabel = Label(topBar, text="Home", width=10, font="Arial 10", height=2
                        , bg=_jazz, fg="white")
        homeLabel.place(x=20, y=-5)
        
        portalLabel = Label(topBar, text="App", width=10, font="Arial 10", height=2
                        , bg=_secondary, fg="black")
        portalLabel.place(x=105, y=-5)
        
        appLogo = Label(topBar, text=_title, font="Arial 11 bold", height=2
                        , bg=_jazz, fg="white")
        appLogo.place(x=(self.width/2)-70, y=-5)
        
        def e(e):
            self.main1Frame.tkraise()
        def E(e):
            e.widget.config(bg="#b11b2c", cursor="hand2")
        def L(e):
            e.widget.config(bg=_jazz, cursor="arrow")
        homeLabel.bind("<Button>", e)
        homeLabel.bind("<Enter>", E)
        homeLabel.bind("<Leave>", L)
        
        self.RenderLeftFrame()
        self.RenderRightFrame()
        
        self.main1Frame.tkraise()
        
    def resize_image(self, image_path):

        canvas_width = int(4*(self.width/7)-65)
        canvas_height = int(self.height-315)
        
        original_img = Image.open(image_path)
        aspect_ratio = original_img.width / original_img.height
        if aspect_ratio > 1:
            new_width = canvas_width
            new_height = int(canvas_width / aspect_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * aspect_ratio)

        resized_img = original_img.resize((new_width, new_height))
        return ImageTk.PhotoImage(resized_img)       
        

    def RenderLeftFrame(self):

        leftFrame = Frame(self.main2Frame, bg=_secondary, width=3*(self.width/7), height=self.height)
        leftFrame.pack(side=LEFT, fill=Y)
        leftFrame.pack_propagate(0)
        
        
        Label(leftFrame, image=self.wel, bg=_secondary).pack(pady=(0,25))
        
        
        Label (leftFrame, text="Enter your prompt below", font=("Arial", 12),
                bg=_secondary, fg="black").pack(pady=10, padx=30,  anchor="w")
       
        self.textBox = Text(leftFrame, relief='flat', bg='#f2f2f2', fg="grey", padx=10, pady=10,
                       highlightbackground="#b3b3b3", highlightthickness=1, 
                       height=10, font=("Arial", 12))
        self.textBox.pack(fill=X, padx=30)        
        self.textBox.insert("1.0", _placeHolder) 
        
        self.checkVar = 0
        
        def reset(e):
            if self.textBox.get("1.0", END).strip() == "":
                self.textBox.insert("1.0", _placeHolder)
                self.textBox.config(fg="grey")
                self.checkVar = 0
        
        def clear(e):
            if self.textBox.get("1.0", END).strip() == _placeHolder:
                self.textBox.delete("1.0", END)
                self.textBox.config(fg="black")
                self.checkVar = 1
            
        # self.textBox.bind("<Button-1>", reset)
        self.textBox.bind("<FocusIn>", clear)
        self.textBox.bind("<FocusOut>", reset)
        
        Button(leftFrame, text="Convert", font=("Arial", 13),
                bg=_jazz, fg="white", width=14, height=2, relief='flat',
                activebackground=_jazz, highlightthickness=0,
                activeforeground="white",
                command=self.Convert).pack(pady=20)
        
        pass
    
    def Convert(self):
        """Convert the prompt to output"""
        self.root.focus()
        t1 = threading.Thread(target=self._process)
        t1.start()
        
        
    def _process(self):
        """Process the prompt and generate the output"""
        if self.checkVar == 0:
            self.notify("Please enter a prompt", 0)
            return
        
        prompt = self.textBox.get("1.0", END)
        prompt = prompt.strip()
        if prompt == "":
            self.notify("Please enter a prompt", 0)
            return
        
        self.PAlert = Label(self.root,font=("Arial", 12),
                            fg="white", height=2, width=20)
        scWidth = self.root.winfo_width()
        self.PAlert.place(x=scWidth-150, y=70, anchor=CENTER)
        
        self.PAlert.config(text="Processing...", bg=_alert)
        
        appEngine = AppEngine(self, prompt)
        
        self.img2 = Image.open("assets/home1.png")
        self.img2 = self.img2.resize((int(4*(self.width/7)), int(self.height-300)))
        self.img2 = ImageTk.PhotoImage(self.img2)
        
        self.canvas.create_image(0, 0, anchor=NW, image=self.img2)
        
        self.Label1.config(text="Here's your artwork")
            
    
    '''
    utils
    
    '''
   
   
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.selected_region = None

    def on_drag(self, event):
        self.canvas.delete("selection_box")
        self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black", tags="selection_box")

    def on_release(self, event):
        self.selected_region = (self.start_x, self.start_y, event.x, event.y)
    
    
    def RenderRightFrame(self):
    
        rightFrame = Frame(self.main2Frame, bg=_primary, width=4*(self.width/7), height=self.height)
        rightFrame.pack(side=LEFT, fill=Y)
        rightFrame.pack_propagate(0)
        
        self.Label1 = Label(rightFrame, text="Explore your Creativity", font=("Century Gothic", 15),
              bg=_primary, fg="black")
        self.Label1.pack(pady=(25,0), anchor="w", padx=30)
        
        self.canvas = Canvas(rightFrame, bg=_primary, width=4*(self.width/7), height=400)
        self.canvas.pack(fill=X, padx=30, pady=20)
        
        self.canvas.create_image(2, 2, anchor=NW, image=self.sampleImg)
        
        if not self._status_:
            self.canvas.bind("<Button>", self.openImage)
      
        frame = Frame(rightFrame, bg=_secondary, width=4*(self.width/7), height=80)
        frame.pack(fill=X, padx=30, pady=10)
        frame.pack_propagate(0)
        
        self.selectImg = Image.open("assets/Select.png")
        self.selectImg = self.selectImg.resize((40, 40))
        self.selectImg = ImageTk.PhotoImage(self.selectImg)
        
        self.uploadIco = Image.open("assets/upload.png")
        self.uploadIco = self.uploadIco.resize((40, 40))
        self.uploadIco = ImageTk.PhotoImage(self.uploadIco)
        
        self._allow_ = 1
        self.SelectAllow = Button(frame,image=self.selectImg, 
                                  relief='flat', bg="white", activebackground="white",
                                  command=self._allowSelect)
        self.SelectAllow.pack(side=LEFT, padx=20)
    
        self.uploadBtn = Button(frame,image=self.uploadIco, 
                                  relief='flat', bg="white", activebackground="white",
                                  command=lambda:self.openImage(1))
        self.uploadBtn.pack(side=LEFT)
    
    def openImage(self, e):
            img = filedialog.askopenfilename(initialdir = "/",
                    title = "Select file",
                    filetypes = (("png files","*.png"),
                                ("jpeg files","*.jpg"),
                                ("all files","*.*")))
        
            if img == "":
                self.notify("No Image Selected", 0)
                return
            
            self.canvas.delete("all")
            
            self.img2 = self.resize_image(img)
            self.canvas.create_image(2, 2, anchor=NW, image=self.img2)
            self._status_ = 1
            self.canvas.unbind("<ButtonPress-1>")
    
    
    def _allowSelect(self):
        if self._allow_ and self._status_:
            self.canvas.bind("<ButtonPress-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)
            self.SelectAllow.config(bg="grey")
            self._allow_ = 0
        else:
            if not self._status_:
                self.notify("No Image to Select", 0)
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.SelectAllow.config(bg="white")
            self.canvas.delete("selection_box")
            self._allow_ = 1
        
    def notify(self, message:str, flag:bool=1):
        """
        Shows the passed message as notification alert
        - flag = 1 for success
        - flag = 0 for error
        """
        alert = Label(self.root,font=("Arial", 12),
                            fg="white", height=2, width=20)
        scWidth = self.root.winfo_width()
       
        if flag:
            alert.config(text=message, bg=_alert)
            alert.place(x=scWidth-150, y=70, anchor=CENTER)
            self.root.after(1500, alert.place_forget)
        else:
            alert.config(text=message, bg="red")
            alert.place(x=scWidth-150, y=70 , anchor=CENTER)
            self.root.after(1500, alert.place_forget)
           

    def _enter(self, e):
        """Utility function for mouse hover effect"""
        e.widget.config(cursor='hand2')
        
    def _leave(self, e):
        """Utility function for mouse hover effect"""
        e.widget.config(cursor='arrow')
                    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()
                
if __name__ == '__main__':
    """Main function"""
    app = App()
    app.run()