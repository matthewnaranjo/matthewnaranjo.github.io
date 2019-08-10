import sys
import pandas as pd
import random

class AddPosts():
    def __init__(self, filename=None):
        if not filename:
            try:
                self.filename = sys.argv[1]
            except Exception:
                self.retry_filename()
        else:
            self.filename = filename

        self.open()
        self.get_links()

    def retry_filename(self):
        self.filename = input("Error: Please provide filename.\nFilename: ")
        self.open()

    def open(self):
        try:
            self.file = open(self.filename, "r")
        except Exception as e:
            print(e)
            self.retry_filename()

    def get_links(self):
        self.links = pd.read_csv("links - all.csv")
        self.num_links = len(self.links.index)
        self.populate_links()

    def populate_links(self):
        select_link = list(range(self.num_links))
        random.shuffle(select_link)
        data = self.file.read()
        for i in range(3):
            link = self.links.iloc[select_link.pop()]
            data = data.replace("Pop Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Pop Post %s Ref" % (i+1), link.ref)
            data = data.replace("Pop Post %s Date" % (i+1), link.date)
            data = data.replace("Pop Post %s Title" % (i+1), link.title)
        
        select_link = list(range(self.num_links))
        random.shuffle(select_link)
        for i in range(3):
            link = self.links.iloc[select_link.pop()]
            data = data.replace("Rel Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Rel Post %s Ref" % (i+1), link.ref)
            data = data.replace("Rel Post %s Date" % (i+1), link.date)
            data = data.replace("Rel Post %s Title" % (i+1), link.title)

        for i in range(3):
            link = self.links.iloc[i]
            data = data.replace("Lat Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Lat Post %s Ref" % (i+1), link.ref)
            data = data.replace("Lat Post %s Date" % (i+1), link.date)
            data = data.replace("Lat Post %s Title" % (i+1), link.title)

        write = open(self.filename, "w")
        write.write(data)

def main():
    AddPosts()
if __name__=='__main__':
    sys.exit(main())