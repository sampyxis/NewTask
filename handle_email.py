#!/usr/bin/env python

import logging, email, model

from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from email.utils import parseaddr

class IncomingMailHandler(webapp.RequestHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        logging.info("got the mail!")
        #sender = message.sender
        # recipients = message.to
        # body = list(message.bodies(content_type 'text/plain'))[0]
        #
        #user = users.get_current_user()
        user_email = parseaddr(message.sender)[1]
        logging.info(user_email)
        user = users.User(user_email)
        #name = self.request.get('name')
        #if not user or not name:
        #  self.error(403)
        #  return

        task_list = model.TaskList(name=message.subject)
        task_list.put()
        task_list_member = model.TaskListMember(task_list=task_list, user=user)
        task_list_member.put()
        
application = webapp.WSGIApplication([('/_ah/mail/.+', IncomingMailHandler),
                                      ('/_ah/mail/sampyxis@sampyxis-tasks.appspotmail.com', IncomingMailHandler)],debug=True)

def main():
   run_wsgi_app(application)
 
if __name__ == '__main__':
    main()   

"""
import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        
        
application = webapp.WSGIApplication([LogSenderHandler.mapping()], debug=True)

def main():
   run_wsgi_app(application)
 
if __name__ == '__main__':
    main()
""" 