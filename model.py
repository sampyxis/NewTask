#!/usr/bin/env python
from google.appengine.ext import db
from google.appengine.api import users

class TaskList(db.Model):
  """A TaskList is the entity tasks refer to to form a list.

  Other than the tasks referring to it, a TaskList just has meta-data, like
  whether it is published and the date at which it was last updated.
  """
  name = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  archived = db.BooleanProperty(default=False)
  published = db.BooleanProperty(default=False)

  @staticmethod
  def get_current_user_lists():
    """Returns the task lists that the current user has access to."""
    return TaskList.get_user_lists(users.get_current_user())

  @staticmethod
  def get_user_lists(user):
    """Returns the task lists that the given user has access to."""
    if not user: return []
    memberships = db.Query(TaskListMember).filter('user =', user)
    return [m.task_list for m in memberships]

  def current_user_has_access(self):
    """Returns true if the current user has access to this task list."""
    return self.user_has_access(users.get_current_user())

  def user_has_access(self, user):
    """Returns true if the given user has access to this task list."""
    if not user: return False
    query = db.Query(TaskListMember)
    query.filter('task_list =', self)
    query.filter('user =', user)
    return query.get()


class TaskListMember(db.Model):
  """Represents the many-to-many relationship between TaskLists and Users.

  This is essentially the task list Access Control List (ACL).
  """
  task_list = db.Reference(TaskList, required=True)
  user = db.UserProperty(required=True)


class Task(db.Model):
  """Represents a single task in a task list.

  A task basically only has a description. We use the priority field to
  order the tasks so that users can specify task order manually.

  The completed field is a DateTime, not a bool; if it is not None, the
  task is completed, and the timestamp represents the time at which it was
  marked completed.
  """
  description = db.TextProperty(required=True)
  completed = db.DateTimeProperty()
  archived = db.BooleanProperty(default=False)
  priority = db.IntegerProperty(required=True, default=0)
  task_list = db.Reference(TaskList)
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)