import sys
import random
import pandas as pd

class TopicPages():
    def __init__(self):
        self.links = pd.read_csv("links - all.csv")
        self.num_links = len(self.links.index)
        self.topics = ["Movie Reviews"]
        self.topic_map = {"Movie Reviews": "movie review"}
        self.url_map = {"Movie Reviews": "movie_reviews.html"}
        self.topic_colors = {"Movie Reviews": "#E8B018"}
        self.template = "topic_temp.html"
        self.open()
        self.get_topic()

    def open(self):
        try:
            self.file = open(self.template, "r")
        except Exception as e:
            print(e)

    def get_topic(self):
        for topic in self.topics:
            self.populate_page(topic)

    def populate_page(self, topic):
        topic_name = self.topic_map[topic]
        topic_links = self.links.loc[self.links['topic'] == topic_name]
        select_link = list(range(len(topic_links)))
        random.shuffle(select_link)
        data = self.file.read()
        data = data.replace("TOPIC NAME REPLACEMENT", topic)
        # change topic color
        if topic in self.topic_colors.keys():
            topic_color = self.topic_colors[topic]
            data = data.replace("#E8B018", topic_color)

        self.filename = self.url_map[topic]
        print("Saving file %s" % self.filename)

        for i in range(6):
            if len(select_link) > 0:
                link = self.links.iloc[select_link.pop()]
            else:
                link = self.links.iloc[random.randint(0,self.num_links-1)]
            data = data.replace("Pop Post %s Image" % (i+1), link.ref[:-5])
            data = data.replace("Pop Post %s Ref" % (i+1), "%s" % (link.ref))
            data = data.replace("Pop Post %s Date" % (i+1), link.date)
            data = data.replace("Pop Post %s Title" % (i+1), link.title)         

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
    TopicPages()
if __name__=='__main__':
    sys.exit(main())
