import datetime
import json
import logging
import traceback

import webapp2
from google.appengine.ext.webapp import template

import utils
from models import SmartUserAccess, AuditLog, Emergency, OpenLock


class SmartUserAccessHandler(webapp2.RequestHandler):
    def home(self):
        template_values = {
            "emergency_status": "true" if Emergency().is_emergency() else "false",
        }
        page = utils.template("index.html", "ATTCaseHacks/html")
        self.response.out.write(template.render(page, template_values))

    def grant(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_id = self.request.get('user_id')
            lock_id = self.request.get('lock_id')
            granted_by = self.request.get('granted_by', 'admin')
            is_firstnet_user = True if self.request.get('is_firstnet_user') == 'true' else False
            access_time = self.request.get('access_time')
            if not access_time:
                access_time = 365 * 24 * 60 * 60
            else:
                access_time = int(access_time)
            access_until = datetime.datetime.today() + datetime.timedelta(seconds=access_time)
            response = SmartUserAccess().grant(
                user_id=user_id,
                lock_id=lock_id,
                granted_by=granted_by,
                is_firstnet_user=is_firstnet_user,
                access_until=access_until,
            )

            AuditLog().add(
                user_id=user_id,
                lock_id=lock_id,
                action='User {} received access to lock {} from {} until {}'.format(
                    user_id, lock_id, granted_by, access_until
                )
            )

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def open_lock(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_id = self.request.get('user_id')
            lock_id = self.request.get('lock_id')
            success = SmartUserAccess().verify(
                user_id=user_id,
                lock_id=lock_id,
            )
            logging.error(success)
            if success:
                action = 'successful attempt to unlock {} by {}'.format(lock_id, user_id)
                OpenLock().open(
                    lock_id=lock_id,
                    last_access_time=datetime.datetime.now()
                )
            else:
                action = 'failed attempt to unlock {} by {}'.format(lock_id, user_id)
            logging.error(action)
            AuditLog().add(
                user_id=user_id,
                lock_id=lock_id,
                action=action
            )

            self.response.out.write(json.dumps({'success': success, 'error': [], 'response': None}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def get_lock_status(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            lock_id = self.request.get('lock_id')
            success = OpenLock().is_open(
                lock_id=lock_id,
            )

            self.response.out.write(json.dumps({'success': success, 'error': [], 'response': None}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())


    def verify(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_id = self.request.get('user_id')
            lock_id = self.request.get('lock_id')
            success = SmartUserAccess().verify(
                user_id=user_id,
                lock_id=lock_id,
            )
            if success:
                action = 'successful attempt to unlock {} by {}'.format(lock_id, user_id)
            else:
                action = 'failed attempt to unlock {} by {}'.format(lock_id, user_id)

            AuditLog().add(
                user_id=user_id,
                lock_id=lock_id,
                action=action
            )

            self.response.out.write(json.dumps({'success': success, 'error': [], 'response': None}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def fetch_all(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            all_access = SmartUserAccess.get()
            response = []
            for access in all_access:
                response.append(SmartUserAccess.get_json_object(access))

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())


class AuditLogHandler(webapp2.RequestHandler):
    def home(self):
        pass

    def fetch_all(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            all_logs = AuditLog.get()
            response = []
            for log in all_logs:
                response.append(AuditLog.get_json_object(log))
            response.sort(key=lambda k: k['created_at'], reverse=True)
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())


class EmergencyHandler(webapp2.RequestHandler):
    def update(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            lock = True if self.request.get('lock', 'false') == 'true' else False
            response = Emergency().update(
                is_locked=lock,
            )
            AuditLog().add(
                user_id='',
                lock_id='emergency',
                action='Emergency is set to {}'.format(lock)
            )

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())
