from google.appengine.ext import db
import datetime


class SmartUserAccess(db.Model):
    user_id = db.StringProperty()
    lock_id = db.StringProperty()
    granted_by = db.StringProperty()
    is_firstnet_user = db.BooleanProperty(default=False)
    access_until = db.DateTimeProperty(default=datetime.datetime.today()+datetime.timedelta(days=365))
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class Emergency(db.Model):
    is_locked = db.BooleanProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class OpenLock(db.Model):
    lock_id = db.StringProperty()
    last_access_time = db.DateTimeProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class AuditLog(db.Model):
    user_id = db.StringProperty()
    lock_id = db.StringProperty()
    action = db.TextProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


