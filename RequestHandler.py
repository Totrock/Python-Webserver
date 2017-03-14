import urllib
import http.server

class RequestHandler(http.server.SimpleHTTPRequestHandler):


    def do_GET(self):#https://opensource.apple.com/source/python/python-3/python/Lib/SimpleHTTPServer.py
        """Serve a GET request."""



        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_POST(self):#https://stackoverflow.com/questions/2121481/python3-http-server-post-example
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # You now have a dictionary of the post data
        print(post_data)

        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()