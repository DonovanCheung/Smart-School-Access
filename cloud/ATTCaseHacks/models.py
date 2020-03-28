import logging

import model
import utils
import datetime


class SmartUserAccess(object):
    def __init__(self):
        pass

    def grant(self, **data):
        self.check_validity(method='add', data=data)

        access, access_exists = self.get_datastore_entity(data)
        access.put()

    def verify(self, **data):
        self.check_validity(method='verify', data=data)

        key_name = "{}/{}".format(data["user_id"], data['lock_id'])
        access = model.SmartUserAccess.get_by_key_name(key_name)
        if not access:
            return False
        if access.access_until < datetime.datetime.now():
            return False
        if Emergency().is_emergency() and not access.is_firstnet_user:
            return False
        return True

    @staticmethod
    def get(debug=False, **filters):
        query_string = "select * from SmartUserAccess"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "user_id": datastore_entity.user_id,
            "lock_id": datastore_entity.lock_id,
            "granted_by": datastore_entity.granted_by,
            "is_firstnet_user": datastore_entity.is_firstnet_user,
            "access_until": datastore_entity.access_until.strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        access_exists = True
        key_name = "{}/{}".format(json_object["user_id"], json_object['lock_id'])
        datastore_entity = model.SmartUserAccess.get_by_key_name(key_name)
        if not datastore_entity:
            access_exists = False
            datastore_entity = model.SmartUserAccess(key_name=key_name)

        datastore_entity.user_id = json_object["user_id"]
        datastore_entity.lock_id = json_object["lock_id"]
        datastore_entity.granted_by = json_object["granted_by"]
        datastore_entity.access_until = json_object["access_until"]
        datastore_entity.is_firstnet_user = json_object["is_firstnet_user"]

        return datastore_entity, access_exists

    @staticmethod
    def check_validity(method, data):
        error = []

        if error:
            raise Exception(error)


class OpenLock(object):
    def __init__(self):
        pass

    def open(self, **data):
        self.check_validity(method='open', data=data)

        lock = self.get_datastore_entity(data)
        lock.last_access_time = datetime.datetime.now()
        lock.put()

    def is_open(self, **data):
        self.check_validity(method='is_open', data=data)

        key_name = data['lock_id']
        lock = model.OpenLock.get_by_key_name(key_name)
        if not lock:
            return False
        if lock.last_access_time + datetime.timedelta(seconds=5) < datetime.datetime.now():
            return False
        return True

    @staticmethod
    def get(debug=False, **filters):
        query_string = "select * from OpenLock"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "lock_id": datastore_entity.lock_id,
            "last_access_time": datastore_entity.access_until.strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        key_name = json_object["lock_id"]
        datastore_entity = model.OpenLock.get_by_key_name(key_name)
        if not datastore_entity:
            datastore_entity = model.OpenLock(key_name=key_name)

        datastore_entity.lock_id = json_object["lock_id"]
        datastore_entity.access_until = json_object["last_access_time"]

        return datastore_entity

    @staticmethod
    def check_validity(method, data):
        error = []

        if error:
            raise Exception(error)


class AuditLog(object):
    def __init__(self):
        pass

    def add(self, **data):
        self.check_validity(method='add', data=data)

        access_log = self.get_datastore_entity(data)
        access_log.put()

    @staticmethod
    def get(debug=False, **filters):
        query_string = "select * from AuditLog"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "user_id": datastore_entity.user_id,
            "lock_id": datastore_entity.lock_id,
            "action": datastore_entity.action,
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        datastore_entity = model.AuditLog()
        datastore_entity.user_id = json_object["user_id"]
        datastore_entity.lock_id = json_object["lock_id"]
        datastore_entity.action = json_object["action"]

        return datastore_entity

    @staticmethod
    def check_validity(method, data):
        error = []

        if error:
            raise Exception(error)


class Emergency(object):
    def __init__(self):
        pass

    def update(self, **data):
        self.check_validity(method='update', data=data)

        emergency = self.get_datastore_entity(data)
        emergency.put()

    def is_emergency(self):
        emergency = self.get()
        if emergency and emergency[0].is_locked:
            return True
        return False

    @staticmethod
    def get(debug=False, **filters):
        query_string = "select * from Emergency"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "is_locked": datastore_entity.lock_id,
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        datastore_entity = model.Emergency.get_by_key_name('emergency')
        if not datastore_entity:
            datastore_entity = model.Emergency(key_name='emergency')

        datastore_entity.is_locked = json_object["is_locked"]

        return datastore_entity

    @staticmethod
    def check_validity(method, data):
        error = []

        if error:
            raise Exception(error)
