# scookie = http.cookies.SimpleCookie()
           # scookie["session"] = random.randint(1,1000000000)
           # scookie["session"]["expires"] = expiration_date.strftime("%a, %d-%b-%Y %H:%M:%S PST")

            # self.send_header(scookie.output().split(":", 1)[0], scookie.output().split(":", 1)[1])
            #print(scookie.output().split(":",1)[0],scookie.output().split(":",1)[1])


#expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=self.COOKIE_LIFESPAN / self.SEC_PER_MIN)
###############################################################################################################################################################################################
import urllib
import http.server
import http.cookies
import json
import datetime


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    JSONFILE = "data.json"
    MAX_CLIENTS = 1
    COOKIE_LIFESPAN = 900  # seconds
    sendcookies = 1  # true
    onlyupdate = 0  # false
    id_of_cookie_to_update = 0
    Cookie_Box = []

    def do_GET(self):  # https://opensource.apple.com/source/python/python-3/python/Lib/SimpleHTTPServer.py
        """Serve a GET request."""
        self.sendcookies = 1
        self.onlyupdate = 0
        self.delete_old_cookies()

        if self.headers["cookie"]:
            if self.Cookie_Box.__contains__(int(str(self.headers).split("Cookie: id=")[1].splitlines()[0])):
                self.onlyupdate = 1
                self.sendcookies = 0
                self.id_of_cookie_to_update = int(str(self.headers).split("Cookie: id=")[1].splitlines()[0])
        else:
            if len(self.Cookie_Box) >= self.MAX_CLIENTS:
                self.sendcookies = 0
                self.send_error(503)
                return

        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_POST(self):  # https://stackoverflow.com/questions/2121481/python3-http-server-post-example
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # dictionary of the post data
        # print(post_data)

        with open('data.json', 'a') as jsontemp:
            json.dump(post_data, jsontemp, indent=3)

        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def append_dict_to_json(self, dict, jsonfile):
        # https://stackoverflow.com/questions/7100125/storing-python-dictionaries
        with open('data.json', 'w') as jsontemp:
            json.dump(dict, jsontemp, indent=3)

    def read_json_to_dict(jsonfile):
        with open(jsonfile, 'a') as jsontemp:
            datadict = json.load(jsontemp)
        # print(datadict["name"])
        return datadict

    def end_headers(
            self):  # https://stackoverflow.com/questions/12499171/can-i-set-a-header-with-pythons-simplehttpserver
        self.send_cookies_header()
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def send_cookies_header(self):
        if self.sendcookies:
            print(self.Cookie_Box)
            self.Cookie_Box.append(len(self.Cookie_Box) + 1)
            self.send_header("Set-Cookie", "id=%s; Max-Age=%s;path=/" % (len(self.Cookie_Box), self.COOKIE_LIFESPAN))
            print("sent: ", "Set-Cookie", "id=%s; Max-Age=%s;path=/" % (len(self.Cookie_Box), self.COOKIE_LIFESPAN))
        if self.onlyupdate:
            print(self.Cookie_Box)
            self.send_header("Set-Cookie",
                             "id=%s; Max-Age=%s;path=/" % (self.id_of_cookie_to_update, self.COOKIE_LIFESPAN))
            print("updated: ", "Set-Cookie",
                  "id=%s; Max-Age=%s;path=/" % (self.id_of_cookie_to_update, self.COOKIE_LIFESPAN))

    def delete_old_cookies(self):
     print("d")