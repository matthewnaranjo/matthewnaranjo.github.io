import sys
import os
from add_posts import AddPosts

class UpdatePosts():
    def __init__(self, filename=None):
        self.template = 'blog_temp.html'
        self.folders = ["text reviews/"]

    def find_posts(self):
        for folder in self.folders:
            for filename in os.listdir(folder):
                if filename.endswith(".txt"):
                    self.extract_post_data(folder + filename)

    def extract_post_data(self, filepath):
        read = open(filepath, "r")
        data = read.readlines()
        title = data[0]
        date = data[2]
        paragraphs = data[4:]
        post_data = (title, date, paragraphs)
        self.write_posts(filepath, post_data)

    def write_posts(self, filepath, post_data):
        title = post_data[0]
        date = post_data[1]
        paragraphs = post_data[2]
        filename = filepath.split("/")[-1]
        filename = filename.split(".")[0]
        read = open(self.template,'r')
        data = read.read()
        data = data.replace("REPLACE IMAGE REF", filename)
        data = data.replace("REPLACE TWITTER IMAGE", filename)
        data = data.replace("FIND AND REPLACE PATH", filename)
        data = data.replace("FIND AND REPLACE TITLE", title)
        data = data.replace("FIND AND REPLACE TWITTER TITLE", title)    
        data = data.replace("FIND AND REPLACE DATE", date)

        t = []
        if len(paragraphs) > 0:
            for p in paragraphs:
                print(p)
                if p != '':
                    if p.startswith("image*"):
                        image_ref = p.split("*")[1]
                        t.append("""<img src="%s" alt="Image" class="img-fluid">""" % image_ref)
                    elif p.startswith("h2:"):
                        title_text = p.split("h2:")[1]
                        t.append("""<h2>%s</h2>""" % title_text)
                    elif p.startswith("h3:"):
                        title_text = p.split("h3:")[1]
                        t.append("""<h3>%s</h3>""" % title_text)
                    elif p.startswith("h4:"):
                        title_text = p.split("h4:")[1]
                        t.append("""<h4>%s</h4>""" % title_text)
                    else:
                        t.append("<p>%s</p>" % p)
            data = data.replace("FIND AND REPLACE BODY", "\n".join(t))
            self.currFile = filename
            if not self.currFile.endswith(".html"):
                self.currFile += ".html"
            write = open(self.currFile, 'w')
            write.write(data)
            read.close()

        AddPosts(self.currFile)     

def main():
    update_posts = UpdatePosts()
    update_posts.find_posts()

if __name__=='__main__':
    sys.exit(main())
