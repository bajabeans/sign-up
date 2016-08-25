#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import re

page_header="""
<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <style>
            .er{
            color: red;
            }
            th{
            text-align: left;
            }
        </style>
    </head>
    <body>
        <h1>Sign-Up</h1>
    </body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    def get(self):

        sign_up_form = """
        <form method="post">
            <table>
                <tr>
                    <th>Username</th>
                    <td><input type="text" name="username" ></td>

                </tr>
                <tr>
                    <th>Password</th>
                    <td><input type="password" name="password"/></td>

                </tr>
                <tr>
                    <th>Verify password</th>
                    <td><input type="password" name="v-password"/></td>

                </tr>
                <tr>
                    <th>Email (Optional)</th>
                    <td><input type="text" name="email"/></td>

                </tr>
            </table>
            <input type="submit"/>
        </form>
        """


        response = page_header + sign_up_form
        self.response.write(response)

    def post(self):
        user_name = self.request.get("username")
        user_password = self.request.get("password")
        verify = self.request.get("v-password")
        email = self.request.get("email")
        error = ""
        error2 = ""
        error3 = ""
        error4 = ""

        has_error = False


        if not valid_username(user_name):
            error = "<b>not a valid username</b>"
            has_error = True


        if not valid_password(user_password):
            error2 = "<b>not a valid password</b>"
            has_error = True


        if not user_password == verify:
            error3 = "<b>password does not match</b>"
            has_error = True


        if not valid_email(email):
            error4 = "<b>not a valid email</b>"
            has_error = True



        sign_up_form2 = """
        <form method="post">
            <table>
                <tr>
                    <th>Username</th>
                    <td><input type="text" name="username" value="%s" ></td>
                    <td class="er">%s</td>
                </tr>
                <tr>
                    <th>Password</th>
                    <td><input type="password" name="password"/></td>
                    <td class="er">%s</td>
                </tr>
                <tr>
                    <th>Verify password</th>
                    <td><input type="password" name="v-password"/></td>
                    <td class="er">%s</td>
                </tr>
                <tr>
                    <th>Email (Optional)</th>
                    <td><input type="text" name="email" value="%s"></td>
                    <td class="er">%s</td>
                </tr>
            </table>
            <input type="submit"/>
        </form>
        """ % (user_name, error, error2, error3, email, error4)

        if has_error == False:
            self.redirect("/success")

        response = page_header + sign_up_form2
        self.response.write(response)

class Success(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get("username")
        sentence = "<h1>" + "Congrats, You filled out the form correctly!" + "</h1>"
        self.response.write(sentence)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/success', Success)
], debug=True)
