import os

from google.appengine.api import users
from google.appengine.ext import db


def template(file_name, directory="templates"):
    return os.path.join(os.path.dirname(__file__), directory, file_name)


def fetch_gql(query_string, fetch_size=50):
    q = db.GqlQuery(query_string)
    cursor = None
    results = []
    while True:
        q.with_cursor(cursor)
        intermediate_result = q.fetch(fetch_size)
        if len(intermediate_result) == 0:
            break
        cursor = q.cursor()
        results += intermediate_result

    return results


def authenticate_user(self, target_url, email_list=None):
    if 'http://localhost' in self.request.url:
        return 'local-user'

    if not email_list:
        email_list = []

    user = users.get_current_user()
    if user:
        if user.email().find('@usc.edu') != -1 or user.email() in email_list:
            return user.email()
        else:
            self.response.out.write(user.email() +
                                    " is not authorized.  Please <a href=" + users.create_login_url(target_url) +
                                    ">Logout</a> and re-login.")
            return False
    else:
        self.response.out.write(
            'Please <a href=' + users.create_login_url(target_url) + ">Login...</a>")
        return False
