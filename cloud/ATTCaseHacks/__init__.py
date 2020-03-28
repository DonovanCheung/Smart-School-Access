from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/att_case_hacks',
                  handler=SmartUserAccessHandler,
                  handler_method='home',
                  methods=['GET']),
    webapp2.Route(template='/att_case_hacks/smart_access/grant',
                  handler=SmartUserAccessHandler,
                  handler_method='grant',
                  methods=['GET', 'POST']),
    webapp2.Route(template='/att_case_hacks/smart_access/verify',
                  handler=SmartUserAccessHandler,
                  handler_method='verify',
                  methods=['GET', 'POST']),
    webapp2.Route(template='/att_case_hacks/smart_access/fetch_all',
                  handler=SmartUserAccessHandler,
                  handler_method='fetch_all',
                  methods=['GET']),
    webapp2.Route(template='/att_case_hacks/smart_access/open_lock',
                  handler=SmartUserAccessHandler,
                  handler_method='open_lock',
                  methods=['GET', 'POST']),
    webapp2.Route(template='/att_case_hacks/smart_access/get_lock_status',
                  handler=SmartUserAccessHandler,
                  handler_method='get_lock_status',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/att_case_hacks/audit_log/fetch_all',
                  handler=AuditLogHandler,
                  handler_method='fetch_all',
                  methods=['GET']),

    webapp2.Route(template='/att_case_hacks/emergency',
                  handler=EmergencyHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

])
