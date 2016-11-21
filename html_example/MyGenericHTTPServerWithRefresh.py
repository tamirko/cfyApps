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
import random
from datetime import datetime as dt
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
        f.write("<html>\n<title>After Post Page</title>\n")
        f.write("<body>\n<h2>After Post Page</h2>\n")
        f.write("<hr>\n")
        if r:
            f.write("<strong>Success:</strong>")
        else:
            f.write("<strong>Failed:</strong>")
        f.write(info)
        f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
        f.write("<hr><small>Powerd By: Tamir Korem, GigaSpaces</small></body></html>")
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
        return (False, "Unexpected End of data.")

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
                return self.show_deplyoments(path, self.path)
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


    def show_deplyoments(self, path, testArg="dummy"):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        blueprint_id = "etx_snmp_nov8"
        company_name = "Lego"
        cloudify_manager_ip_address = "xxx.xxx.xx.xxx"
        enable_embed = False
        round_progress = "<{0} class=\"{1}\"></{0}>".format("div", "loader2")
        created_status_html = "<img class=\"status\" src=\"css/ready.jpg\"/>"
        installed_status_html = "<img class=\"status\" src=\"css/installed.png\"/>"
        uninstalled_status_html = "<img class=\"status\" src=\"css/uninstalled.jpg\"/>"

        powered_by_html = "<{0} class=\"{1}\">Powered by<img width=\"71\" height=\"28\" src=\"css/TDC.png\"/></{0}>".format("span", "powered_by")

        title_txt = "{0}'s Operations Console".format(company_name)
        main_headline = "<{0} class=\"{2}\">{1}'s Operations Console - {3}</{0}>".format("h1", company_name, "logo", powered_by_html)
        f = StringIO()

        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        #f.write("<html>\n<title>Cloudify Deployments %s </title>\n" % displaypath)
        f.write("<html>")
        f.write("<head>")
        f.write("<title>{0}</title>".format(title_txt))
        f.write("<meta http-equiv=\"refresh\" content=\"30\"/>".format(title_txt))
        f.write("<meta charset=\"utf-8\"/>")
        #f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"css/style.css\">")
        #f.write("<script type=\"text/javascript\" src=\"https://maps.googleapis.com/maps/api/js?sensor=false\"></script>")
        #f.write("<script type=\"text/javascript\" src=\"js/map.js\"></script>")
        f.write("<link rel=\"stylesheet\" href=\"css/lego.css\">")

        cloudify_client = CloudifyClient(cloudify_manager_ip_address)


        deployment_str = ""
        deployment_str += "<{1} class=\"{2}\">Welcome {0} user !".format(company_name, "h2", "user_headline")

        deployment_str += "<table>"
        deployment_str += "<row>"
        actions = ""
        action1_display = "Add a new vCPE"
        action2_display = "Update a vCPE"
        action3_display = "Provision a FireWall"

        #actions += "<td><button type=\"button\" onclick=\"alert('Hello world1!')\">Click Me1!</button></td>"
        actions += "<td><button type=\"button\" onclick=\"alert('{0}!')\">{0}</button></td>".format(action1_display)
        actions += "<td><button type=\"button\" onclick=\"alert('{0}!')\">{0}</button></td>".format(action2_display)
        actions += "<td><button type=\"button\" onclick=\"alert('{0}!')\">{0}</button></td>".format(action3_display)

        actions += "<td><button type=\"button\" onclick=\"window.location.href = 'http://127.0.0.1:8000?x=1';\">{0}</button></td>".format(testArg)

        deployment_str += "<td><{0} class=\"{1}\">Available actions:</td>{2}</{0}>".format("span", "user_headline", actions)

        deployment_str += "</row>"
        deployment_str += "</table>"


        deployment_str += "<table>"
        deployment_str += "<row>"

        deployment_str += "<td>"
        deployment_str += "<{0} class=\"{1}\">Your current deployments are: </{0}>".format("h4", "user_headline")
#       deployment_str += "<hr>"
        deployment_str += "<ol>"
        deploy_btn_txt = "<button type=\"button\" onclick=\"alert('{1}')\">{0}</button>"
        update_btn_txt = "<button type=\"button\" onclick=\"alert('{1}')\">{0}</button>"

        time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        latest_execution_time_str = "2000-01-01T20:56:56.120Z"

        try:
            cloudify_client.executions.start("asdasdas", 'install')
        except Exception as e:
            deployment_str += "<span>"
#            deployment_str += str(e)
            deployment_str += "<hr/>"
            deployment_str += "</h1>"
            #deployment_str += "<div class=\"loader\">.....</div>"

        for deployment in cloudify_client.deployments.list(blueprint_id=blueprint_id):
            deployment_id = deployment.id
            latest_execution_time = dt.strptime(latest_execution_time_str, time_format)
            all_executions = cloudify_client.executions.list(deployment_id=deployment_id)
            embed_this_deployment = False
            curr_status_class = ""
            curr_progress = ""
            for execution in all_executions:
                wf_id = execution.workflow_id
                created_at = execution.created_at
                created_at_dt = dt.strptime(created_at, time_format)
                if latest_execution_time < created_at_dt:
                    latest_execution_time = created_at_dt
                    curr_delete = "<button type=\"button\" onclick=\"alert('{0} {1}')\">{0}</button>".format("Delete", deployment.id)
                    if "uninstall" == wf_id:
                        curr_undeploy = ""
                        curr_run_wf = ""
                        curr_update = ""
                        wf_status = execution.status
                        embed_this_deployment = False
                        if wf_status == "terminated":
                            curr_deploy = "<button type=\"button\" onclick=\"alert('{0} {1}')\">{0}</button>".format("Deploy", deployment.id)
                            curr_status = "<span class=\"{0}\">Uninstalled</span>".format("unistalled_env")
                            curr_status_class = uninstalled_status_html
                            curr_progress = ""
                            created_at_msg = "Undeployed at {0}".format(created_at)
                        else:
                            curr_deploy = ""
                            curr_status = "<span class=\"{0}\">being uninstalled...</span>".format("being_uninstalled_env")
                            curr_status_class = ""
                            curr_progress = round_progress
                            created_at_msg = "Deployment started at {0}".format(created_at)
                    elif "install" == wf_id:
                        curr_deploy = ""
                        wf_status = execution.status
                        curr_status_class = ""
                        embed_this_deployment = True
                        if wf_status == "terminated":
                            curr_update = "<button type=\"button\" onclick=\"alert('{0} {1}')\">{0}</button>".format("Update", deployment.id)
                            curr_run_wf = "<button type=\"button\" onclick=\"alert('{0}')\">{0}</button>".format("Execute a Workflow")
                            curr_undeploy = "<button type=\"button\" onclick=\"alert('{0} {1}')\">{0}</button>".format("Undeploy", deployment.id)
                            curr_status = "<span class=\"{0}\">Live</span>".format("live_env")
                            curr_status_class = installed_status_html
                            # Remove this later
                            curr_progress = ""
                            created_at_msg = "Deployed at {0}".format(created_at)
                        else:
                            curr_undeploy = ""
                            curr_update = ""
                            curr_run_wf = ""
                            curr_status = "<span class=\"{0}\">being installed...</span>".format("being_installed_env")
                            curr_status_class = ""
                            curr_progress = round_progress
                            created_at_msg = "Deployment started at {0}".format(created_at)
                    elif "create_deployment_environment" == wf_id:
                        curr_undeploy = ""
                        curr_update = ""
                        curr_run_wf = ""
                        wf_status = execution.status
                        curr_status_class = created_status_html

                        embed_this_deployment = False
                        if wf_status == "terminated":
                            curr_deploy = "<button type=\"button\" onclick=\"alert('{0} {1}')\">{0}</button>".format("Deploy", deployment.id)
                            curr_status = "<span class=\"{0}\">Created</span>".format("created_env")
                            curr_progress = ""
                            created_at_msg = "Created at {0}".format(created_at)
                        else:
                            curr_deploy = ""
                            curr_status = "being created..."
                            curr_progress = round_progress
                            created_at_msg = "Creation started at {0}".format(created_at)


#            deployment_str += "<li><{1} class=\"{2}\">{0}</{1}></li>".format(deployment_id, "h4", "deployment_name")
            deployment_str += "<li><{1} class=\"{2}\">{0}</{1}></li>".format(deployment_id, "h4", "deployment_name")


            if 1 == 2:
                deployment_str += "<{1}>--{0}--</{1}>".format('inputs', "h4")
                current_inputs = cloudify_client.deployments.get(deployment_id)['inputs']
                if current_inputs and 1 == 2:
                    deployment_str += "<ul>"
                    for key in current_inputs:
                        deployment_str += "<li><span>{0}:{1}</span></li>".format(key, current_inputs.get(key))
                    deployment_str += "</ul>"

#            deployment_str += "<{2}>--{0} {1}--</{2}>".format(deployment_id, 'outputs', "h5")

            deployment_str += "<table>"
            deployment_str += "<row>"
            deployment_str += "<td>"
            deployment_str += curr_status_class
            deployment_str += "</td>"

            deployment_str += "<td>"
            deployment_str += curr_progress
            deployment_str += "</td>"

            deployment_str += "<td>"
            deployment_str += "<{0} class=\"{1}\"></{0}>".format("span", "deployment_name")
            deployment_str += "</td>"
            deployment_str += "</row>"

            deployment_str += "<row>"
            deployment_str += "<td>"
            deployment_str += "<{0} class=\"{6}\">{4}</{0}>".format("span", curr_deploy, curr_update, curr_undeploy, curr_status, curr_run_wf, "deployment_name", curr_delete)
            deployment_str += "</td>"
            deployment_str += "<td>"
            deployment_str += "<{0} class=\"{6}\">{1} {2} {5} {3} {7} </{0}>".format("span", curr_deploy, curr_update, curr_undeploy, curr_status, curr_run_wf, "deployment_name", curr_delete)
            deployment_str += "</td>"
            deployment_str += "</row>"
            deployment_str += "</table>"

            deployment_str += "<{1}>{0}</{1}>".format(created_at_msg,"span")
            deployment_str += "<br/><u>{0}</u>".format('Outputs')
            current_outputs = cloudify_client.deployments.outputs.get(deployment_id)['outputs']
            if current_outputs:
                deployment_str += "<ul>"
                for key in current_outputs:
                    deployment_str += "<li><span>{0}:{1}</span></li>".format(key, current_outputs.get(key))
                deployment_str += "</ul>"
            deployment_str += "<hr>"
            if enable_embed and embed_this_deployment:
                embed_deployment = "<iframe src=\"http://{0}/#/deployment/{1}/topology?embed=true\" width=\"800px\" height=\"350px\"></iframe>".format(cloudify_manager_ip_address, deployment_id)
                deployment_str += embed_deployment
        deployment_str += "</ol>"
#       deployment_str += "<hr>"

        deployment_str += "</td>"
        deployment_str += "</row>"
        deployment_str += "</table>"

        f.write("<script>")
        f.write("var markersData = 5;")
        f.write("</script>")

        f.write("</head>")
        f.write("<body>{0}".format(main_headline))
#       f.write("<{0}>True to {1}</{0}>".format("span", dt.now()))
        f.write("<hr>")

        f.write(deployment_str)

        f.write("<div id=\"myXXX\"")
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
