import sys
import random
import pandas as pd

class HomePage():
    def __init__(self):
        self.links = pd.read_csv("links - all.csv")
        self.num_links = len(self.links.index)
        self.filename = "index.html"
        self.template = "index_temp.html"
        self.open()
        self.populate_page()

    def open(self):
        try:
            self.file = open(self.template, "r")
        except Exception as e:
            print(e)

    def populate_page(self):
        select_link = list(range(self.num_links))
        random.shuffle(select_link)
        data = self.file.read()
        for i in range(6):
            if len(select_link) > 0:
                link = self.links.iloc[select_link.pop()]
            else:
                link = self.links.iloc[random.randint(0,self.num_links-1)]
            data = data.replace("Pop Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Pop Post %s Ref" % (i+1), "%s" % (link.ref))
            data = data.replace("Pop Post %s Date" % (i+1), link.date)
            data = data.replace("Pop Post %s Title" % (i+1), link.title)
        
        select_link = list(range(self.num_links))
        random.shuffle(select_link)
        for i in range(3):
            link = self.links.iloc[select_link.pop()]
            data = data.replace("Feat Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Feat Post %s Ref" % (i+1), link.ref)
            data = data.replace("Feat Post %s Date" % (i+1), link.date)
            data = data.replace("Feat Post %s Title" % (i+1), link.title)
            data = data.replace("Feat Post %s Category" % (i+1), link.topic)
            data = data.replace("Feat Post %s Desc" % (i+1), link.desc)           

        for i in range(6):
            if i < self.num_links:
                link = self.links.iloc[i]
            else:
                link = self.links.iloc[random.randint(0,self.num_links-1)]
            data = data.replace("Lat Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Lat Post %s Ref" % (i+1), link.ref)
            data = data.replace("Lat Post %s Date" % (i+1), link.date)
            data = data.replace("Lat Post %s Title" % (i+1), link.title)


        write = open(self.filename, "w")
        write.write(data)

def main():
    HomePage()
if __name__=='__main__':
    sys.exit(main())
