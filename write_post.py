from tkinter import *
from tkinter import filedialog as fd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import webbrowser
import os
from update_posts import UpdatePosts
from image_editor import ImageEditor

class Gui:
    def __init__(self,root):

        def focus_next_window(event):
            event.widget.tk_focusNext().focus()
            return("break")

        self.root=root
        self.currFile=''
        self.textPath='/Users/mattnaranjo/documents/fannotated/text reviews/'
        self.root.wm_title('No file selected')
        self.f=Frame(self.root,bd=3,height=30,relief=RAISED)
        self.f.pack(fill=BOTH,expand=True)
        self.newBut=Button(self.f,text='New', command=lambda : self.openNewPopup())
        self.newSave=Button(self.f,text='Save',command=lambda : self.saveF(self.currFile))
        self.newLoad=Button(self.f,text='Load',command=lambda: self.loadF())
        self.newSaveAs=Button(self.f,text='Save As',command=lambda: self.saveAsF())
        self.newPreview=Button(self.f,text='Preview',command=lambda: self.preview())
        self.newImage=Button(self.f,text='New Image', command=lambda: self.addImage())
        self.newMainImage=Button(self.f,text='Add Main Image', command=lambda: self.addMainImage())
        self.newBut.pack(side=LEFT)
        self.newSave.pack(side=LEFT)
        self.newSaveAs.pack(side=LEFT)
        self.newLoad.pack(side=LEFT)
        self.newPreview.pack(side=LEFT)
        self.newImage.pack(side=LEFT)
        self.newMainImage.pack(side=LEFT)
        self.title = Text(self.root,height=1,width=150)
        self.title.bind("<Tab>", focus_next_window)
        self.title.pack(fill=BOTH,expand=True)
        self.date = Text(self.root,height=1,width=150)
        self.date.bind("<Tab>", focus_next_window)
        self.date.pack(fill=BOTH,expand=True)
        self.text=Text(self.root,height=50, width=150)
        self.scroll=Scrollbar(self.root,command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(fill=BOTH,expand=True)
        self.scroll.pack(side=RIGHT,fill=Y)

        self.file_opt = options = {}
        options['defaultextension'] = '.html'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'
        
    def openNewPopup(self):
        self.popup = Tk()
        self.popup.wm_title("!")
        self.labp=Label(self.popup,text='Contents will be lost. Do you want to save your work?')
        self.butp1=Button(self.popup,text='Yes',command=lambda n=True: self.openNew(n))
        self.butp2=Button(self.popup,text='No',command=lambda n=False: self.openNew(n))
        self.labp.pack(fill=X)
        self.butp1.pack(side=LEFT, padx=20)
        self.butp2.pack(side=RIGHT,padx=20)
        self.popup.mainloop()

    def openNew(self,boo):
        self.popup.destroy()
        if boo:
            self.saveF(self.currFile)
            self.title.delete(1.0,END)
            self.date.delete(1.0,END)
            self.text.delete(1.0,END)
            
        else:
            inp=self.text.get(1.0,END)
            print(inp)
            self.title.delete(1.0,END)
            self.date.delete(1.0,END)
            self.text.delete(1.0,END)
            
    # maybe use update post class for this?
    def saveF(self, filename):
        
        #get text from editor and split into paragraphs
        t = self.text.get("1.0", END)
        title = self.title.get("1.0", END)
        date = self.date.get("1.0", END)
        paragraphs = t.split('\n\n')
        post_data = [title, date, paragraphs]
        update_posts = UpdatePosts()
        update_posts.write_posts(filename, post_data)

        #save plain text
        text_name = self.currFile.split('/')
        text_name = text_name[-1].split('.')
        text_path = self.textPath + text_name[0] + ".txt"
        print(text_path)
        f=open(text_path,'w')
        text = self.text.get("1.0", END)
        f.write(title + '\n')
        f.write(date + '\n')
        f.write(text)
        f.close()    
            
    def loadF(self):
        inp=self.text.get(1.0,END)
        print()
        if inp!='\n':
            self.openNewPopup()
        self.file_opt['title']='Load'
        self.currFile=fd.askopenfilename(**self.file_opt)
        if self.currFile:
            f=open(self.currFile,'r')
            data = f.readlines()
            inp=self.title.insert(1.0,data[0])
            inp=self.date.insert(1.0,data[2])
            text = data[4:]
            text.reverse()
            for line in text:
                inp=self.text.insert(1.0,line)
            self.root.wm_title(self.currFile)
            f.close()

    #convert file to blog html page
    def saveAsF(self):
        try:
            self.currFile=fd.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".html")
            if self.currFile:
                self.saveF(self.currFile)
        except Exception as e: 
            print("caught %s" % e)  

    def preview(self):
        if self.currFile == '':
            self.saveAsF()
        webbrowser.open_new('file://' + self.currFile)

    #adds chosen photo to images folder, distinguishes text from photos, ensures it is jpg
    def addImage(self):
        try:
            self.image_name=fd.askopenfilename()
            save_image = ImageEditor()
            new_photopath = save_image.copyPhoto(self.image_name)
            self.text.insert(END,"\n\nimage*" + new_photopath)
        except Exception as e: 
            print("caught in addImage: %s" % e)

    #adds chosen photo to images folder, distinguishes text from photos, ensures it is jpg
    def addMainImage(self):
        try:
            self.image_name=fd.askopenfilename()
            save_image = ImageEditor()
            if self.currFile == '':
                self.saveAsF()
            new_photopath = save_image.addMainPhoto(self.image_name, self.currFile)
            print("successfully saved %s." % new_photopath)
        except Exception as e: 
            print("caught in addMainImage: %s" % e)

def main():
    root=Tk()
    root.title("Blog Writer")
    gui=Gui(root)  
    root.mainloop()
if __name__=='__main__':
    sys.exit(main())