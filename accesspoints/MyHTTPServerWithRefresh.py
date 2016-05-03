#!/usr/bin/env python

"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

"""


__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "http://li2z.cn/"

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import datetime
import random
from datetime import datetime
from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "SimpleHTTPWithUpload/" + __version__


    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        print r, info, "by: ", self.client_address
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Upload Result Page</title>\n")
        f.write("<body>\n<h2>Upload Result Page</h2>\n")
        f.write("<hr>\n")
        if r:
            f.write("<strong>Success:</strong>")
        else:
            f.write("<strong>Failed:</strong>")
        f.write(info)
        f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
        f.write("<hr><small>Powerd By: bones7456, check new version at ")
        f.write("<a href=\"http://li2z.cn/?s=SimpleHTTPServerWithUpload\">")
        f.write("here</a>.</small></body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        
    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.show_deplyoments(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    # https://sites.google.com/site/gmapsdevelopment/
    def get_marker_str(self, lat, lng, prefix, name, addr1, addr2, post_code):
        str = " {"
        str += "lat: {0},".format(lat)
        str += "lng: {0},".format(lng)
        str += "name: \"{0} {1}\",".format(prefix, name)
        str += "address1:\"{0} {1}\",".format(prefix, addr1)
        str += "address2: \"{0} {1}\",".format(prefix, addr2)
        str += "postalCode: \"{0} {1}\",".format(prefix, post_code)

        xxx = random.random()*100
        if xxx >80:
            icon_str = "http://maps.google.com/mapfiles/ms/micons/firedept.png"
        elif xxx > 50:
            icon_str = "http://maps.google.com/mapfiles/kml/pal2/icon4.png"
        elif xxx > 20:
            icon_str = "https://upload.wikimedia.org/wikipedia/commons/a/a4/Farm-Fresh_fire.png"
#           icon_str = "https://s3.amazonaws.com/cloud.ohloh.net/attachments/81587/cloudify_med.png"
        else:
            icon_str = "http://www.fancyicons.com/free-icons/108/occupations/png/32/firefighter_male_light_32.png"
        str += "icon: \"{0}\"".format(icon_str)
        str += "}"
        return str


    def show_deplyoments(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        self.geo_list = []
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        #f.write("<html>\n<title>Cloudify Deployments %s </title>\n" % displaypath)
        f.write("<html>")
        f.write("<head><title>Cloudify Deployments Page</title><meta http-equiv=\"refresh\" content=\"20\">")
        f.write("<meta charset=\"utf-8\">")
        f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"css/style.css\">")
        f.write("<script type=\"text/javascript\" src=\"https://maps.googleapis.com/maps/api/js?sensor=false\"></script>")
        f.write("<script type=\"text/javascript\" src=\"js/map.js\"></script>")

        cloudify_client = CloudifyClient('185.43.218.204')
        #cloudify_client = CloudifyClient('xxxxxxxxxxxx')
        blueprint_id = "accesspoints"
        required_inputs = ["longtitude", "altitude"]

        deployment_str = ""
        deployment_str += "<hr>"
        deployment_str += "<ol>"
        for deployment in cloudify_client.deployments.list(blueprint_id=blueprint_id):
            deployment_id = deployment.id
            deployment_str += "<li><span>{0}</span></li>\n".format(deployment_id)
            all_executions = cloudify_client.executions.list(deployment_id=deployment_id)
            deployment_str += "<hr><ul>"
            for execution in all_executions:
                wf_Id = execution.workflow_id
                created_at = execution.created_at
                deployment_str += "<li><span>wf_Id {0}, created_at {1}</span></li>\n".format(wf_Id, created_at)
            deployment_str += "</ul>\n"
            deployment_str += "<span>--{0}--</span>\n".format('inputs')
            current_inputs = cloudify_client.deployments.get(deployment_id)['inputs']
            #if current_inputs:
            #    deployment_str +="<hr><ul>"
            #    for key in current_inputs:
            #        deployment_str += "<li><span>{0}:{1}</span></li>".format(key, current_inputs.get(key))
            #    deployment_str += "</ul>"


            curr_geo = {}
            for required_input in required_inputs:
                curr_geo[required_input] = current_inputs[required_input]
            self.geo_list.append(curr_geo.copy())

            deployment_str += "<span>--{0}--</span>\n".format('outputs')
            current_outputs = cloudify_client.deployments.outputs.get(deployment_id)['outputs']
            if current_outputs:
                deployment_str += "<hr><ul>"
                for key in current_outputs:
                    deployment_str += "<li><span>{0}:{1}</span></li>\n".format(key, current_outputs.get(key))
                    deployment_str += "</ul>\n"

        deployment_str += "</ol><hr>"

        f.write("<script>")
        f.write("markersData = [")
        curr_str = ""
        for item in self.geo_list:
            lat = float(item.get("longtitude"))
            lng = float(item.get("altitude"))
            name = "lat,lng {0},{1}".format(lat, lng)
            addr1 = "addr1 {0}".format(lat)
            addr2 = "addr2 {0}".format(lat)
            post_code = "po code {0}".format(lat)
            prefix = "TA {0}".format(lat)
            curr_str += self.get_marker_str(lat, lng, prefix, name, addr1, addr2, post_code)
            curr_str += ","

        f.write(curr_str[:-1])
        f.write("];")
        f.write("google.maps.event.addDomListener(window, 'load', initialize);")
        f.write("</script>")

        f.write("</head>")
        f.write("<body>\n<h2>Cloudify Deployments and Executions v2604 {0}</h2>".format(datetime.now()))
        f.write("<hr>")

        f.write(deployment_str)
        f.write("<div id=\"map-canvas\"")
        f.write("</body></html>")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


def test(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    test()
