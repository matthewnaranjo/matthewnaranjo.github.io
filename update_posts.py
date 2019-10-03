import sys
import os
from add_posts import AddPosts

class UpdatePosts():
    def __init__(self, filename=None):
        self.template = 'blog_temp.html'
        self.folders = ["text reviews/"]        
        self.find_posts()

    def find_posts(self):
        for folder in self.folders:
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    read = open(folder + file, "r")
                    data = read.readlines()
                    title = data[0]
                    date = data[2]
                    paragraphs = data[4:]
                    post_data = (title, date, paragraphs)
                    self.write_posts(file, post_data)

    def write_posts(self, filename, post_data):
        title = post_data[0]
        date = post_data[1]
        paragraphs = post_data[2]
        image_name = filename[:-4]
        # if sports, use sports logo
        if 'sports' == filename[:6]:
            template = "sports" + self.template
        else:
            template = self.template
        read = open(template,'r')
        data = read.read()
        data = data.replace("REPLACE IMAGE REF", image_name)
        data = data.replace("FIND AND REPLACE TITLE", title)
        data = data.replace("FIND AND REPLACE DATE", date)

        if len(paragraphs) > 0:
            t = ["<p>%s</p>" % p for p in paragraphs if p != '']
            data = data.replace("FIND AND REPLACE BODY", "\n".join(t))
            self.currFile = filename[:-4] + ".html"
            write = open(self.currFile, 'w')
            write.write(data)
            read.close()

        AddPosts(self.currFile)     

def main():
    UpdatePosts()
if __name__=='__main__':
    sys.exit(main())
