#!/usr/bin/env python
#
# webapp2 code copyright 2007 Google Inc.
# Handler class courtesy of Udacity

import os
import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    permalink = db.StringProperty()


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render('front.html')


class NewPost(Handler):
    def get(self):
        self.render('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            new_post = Post(subject=subject, content=content)
            new_post.put()
            new_id = new_post.key().id()
            new_post.permalink = "/entries/" + new_id
            new_post.put()
            self.redirect()
        else:
            error = 'Subject and content are required inputs.'
            self.render('newpost.html', error=error, subject=subject, content=content)

class SinglePost(Handler):
    

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/entries', SinglePost)
], debug=True)
