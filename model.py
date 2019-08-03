from google.appengine.ext import ndb

class Meme(ndb.Model):
    line1 = ndb.StringProperty()
    line2 = ndb.StringProperty()
    image_url = ndb.StringProperty()
    dark_mode = ndb.BooleanProperty()

    def get_lines(self):
        return self.line1 + " " + self.line2
