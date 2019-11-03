import sys
import random
import pandas as pd

class TopicPages():
    def __init__(self):
        self.links = pd.read_csv("links - all.csv")
        self.num_links = len(self.links.index)

        self.sections = ["Movies", "Video Games", "Outdoors", "Hockey"]
        self.section_map = {"Movies": "movie", "Video Games": "video game", "Outdoors": "outdoors", "Hockey": "hockey"}

        self.topics = ["Movie Reviews", "Xbox Game Pass", "Video Game Reviews", "Rock Climbing", "NHL News"]       
        self.topic_map = {"Movie Reviews": "movie review", "Xbox Game Pass": "xbox game pass", "Video Game Reviews": "video game review", "Rock Climbing": "rock climbing", "NHL News": "nhl news"}
        self.url_map = {"Movie Reviews": "movie_reviews.html", "Movies": "movies.html", "Video Games": "videogames.html", "Xbox Game Pass": "gamepass.html",
                        "Video Game Reviews": "videogame_reviews.html", "Outdoors": "outdoors.html", "Rock Climbing": "rock_climbing.html", "Hockey": "hockey.html", "NHL News": "nhl_news.html"}
        self.topic_colors = {"Movie Reviews": "#ffce2f", "Movies": "#ffce2f", "Video Games": "#ffce2f", "Video Game Reviews": "#ffce2f"}

        self.template = "topic_temp.html"
        self.get_topic()
        self.get_section()

    def open(self, custom_template=None):
        if not custom_template:
            try:
                self.file = open(self.template, "r")
            except Exception as e:
                print(e)
        else:
            try:
                self.file = open(custom_template, "r")
            except Exception as e:
                print(e)

    def get_topic(self):
        for topic in self.topics:
            self.open()
            self.populate_page(topic, "topic")

    def get_section(self):
        for section in self.sections:
            self.open()
            self.populate_page(section, "section")

    def populate_page(self, topic, page_type):
        if page_type == "topic":
            page_map = self.topic_map
        elif page_type == "section":
            page_map = self.section_map
        else:
            print("Error")
            return

        topic_name = page_map[topic]
        topic_links = self.links.loc[[topic_name in topic for topic in self.links[page_type]]]
        select_link = list(range(len(topic_links)))
        random.shuffle(select_link)

        # if sports section
        if topic == "Hockey" or topic == "NHL News":
            self.open("sports" + self.template)
        data = self.file.read()
        data = data.replace("TOPIC NAME REPLACEMENT", topic)
        # change topic color
        if topic in self.topic_colors.keys():
            topic_color = self.topic_colors[topic]
            data = data.replace("#ffce2f", topic_color)

        self.filename = self.url_map[topic]
        print("Saving file %s" % self.filename)

        for i in range(6):
            template = ""
            if len(select_link) > 0:
                link = topic_links.iloc[select_link.pop()]
                template = """<li>
                        <a href="%s">
                          <img src="images/%s.jpg" alt="Image placeholder" class="mr-4">
                          <div class="text">
                            <h4>%s</h4>
                            <div class="post-meta">
                              <span class="mr-2">%s</span>
                            </div>
                          </div>
                        </a>
                      </li>""" % (link.ref, link.ref[:-5], link.title, link.date)

            data = data.replace("<!-- Pop Post %s Ref -->" % (i+1), template)      

        for i in range(6):
            template = ""
            if i < len(topic_links):
                link = topic_links.iloc[i]

                template = """<div class="col-md-12">
                      <a href="%s" class="blog-entry element-animate" data-animate-effect="fadeIn">
                        <img src="images/%s.jpg" alt="" width="265" height="148" class="float-left mr-2 rounded">
                        <div class="blog-content-body" style="height: 148px;">
                          <h2>%s</h2>
                          <div class="post-meta">
                            <span class="mr-2">%s</span>
                          </div>
                        </div>
                      </a>
                    </div>""" % (link.ref, link.ref[:-5], link.title, link.date)

            data = data.replace("<!-- Lat Post %s Ref -->" % (i+1), template)


        write = open(self.filename, "w")
        write.write(data)

def main():
    TopicPages()
if __name__=='__main__':
    sys.exit(main())
