# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import jinja2
import os
from model import Meme

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


meme_img = {
    "annoyed_gavin": {"name": "Annoyed Gavin",
                        "url": "https://pbs.twimg.com/media/CsEo-0LW8AAneK2.jpg"},
    "baby_reading": {"name": "Baby Reading Fast",
                        "url": "https://confessionsofabookgeek.files.wordpress.com/2014/11/fast-reading-gif.gif?w=282&zoom=2"},
    "spongebob": {"name": "Spongebob",
                        "url": "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/mocking-spongebob-1556133078.jpg?crop=0.785xw:0.770xh;0.111xw,0.230xh&resize=1200:*"},
    "success_baby": {"name": "Success Kid",
                        "url": "https://i2.wp.com/i.pinimg.com/736x/b1/f3/fd/b1f3fd3f5947020d80fd88a872aee9eb--success-meme-teacher-memes.jpg?w=640&ssl=1"},
    "angry_arthur": {"name": "Angry Arthur",
                        "url": "https://imgflip.com/s/meme/Arthur-Fist.jpg"},
    }

class MainPage(webapp2.RequestHandler):
    def get(self):
        welcome_template = the_jinja_env.get_template('templates/welcome.html')
        greeting_dict = {
        "greeting": "Welcome",
        "adjective": "amazing",
        "meme_imgs": meme_img,
        }
        self.response.write(welcome_template.render(greeting_dict))

class MemeProd(webapp2.RequestHandler):
    def post(self):
        results_template = the_jinja_env.get_template('templates/results.html')

        line1 = self.request.get("line_one")
        line2 = self.request.get("line_two")
        meme = self.request.get("meme_pic")
        img_url = meme_img[meme]["url"]
        dark_mode = bool(self.request.get("dark_mode"))

        user_meme = Meme(line1=line1, line2=line2, image_url=img_url, dark_mode=dark_mode)
        user_meme.put()

        meme_query = Meme.query()
        memes=meme_query.fetch()

        the_variable_dict = {
            "line1": line1,
            "line2": line2,
            "img_url": img_url,
            "dark_mode": dark_mode,
            "all_memes": memes,
        }
        self.response.write(results_template.render(the_variable_dict))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/meme', MemeProd),
], debug=True)
