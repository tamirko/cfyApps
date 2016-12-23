#!/usr/bin/env python

"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

"""


__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "tamirko"
__home_page__ = "http://docs.getcloudify.org/3.4.0/intro/what-is-cloudify/"

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import sys
import random
import threading
import subprocess
from datetime import datetime as dt
from urlparse import urlparse, parse_qs

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
    #def __init__(self, cloudify_manager_ip_address, first_blueprint_id, scnd_blueprint_id):
        #BaseHTTPServer.BaseHTTPRequestHandler.__init__(self)
    #    self.cloudify_manager_ip_address1 = cloudify_manager_ip_address
    #    self.first_blueprint_id1 = first_blueprint_id
    #    self.scnd_blueprint_id1 = scnd_blueprint_id
    #    print "SimpleHTTPRequestHandler cloudify_manager_ip_address is: {0}".format(self.cloudify_manager_ip_address1)
    #    print "SimpleHTTPRequestHandler first_blueprint_id is           {0}".format(self.first_blueprint_id1)
    #    print "SimpleHTTPRequestHandler scnd_blueprint_id is            {0}".format(self.scnd_blueprint_id1)

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
        f.write("<hr/>\n")
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
                query = urlparse(self.path).query

                #query_components = parse_qs(urlparse(self.path).query)
                if query:
                    query_components = dict(qc.split("=") for qc in query.split("&"))
                else:
                    query_components = None
                return self.show_deplyoments(path, query_components)
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


    def show_deplyoments(self, path, query_components=None):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        # You can change only the values in these three lines :

        all_instances_str = get_all_instances_str()

        first_blueprint_id = "etx1412_v1"
        scnd_blueprint_id = "drupal_telia_19_12"
        cloudify_manager_ip_address = "185.98.150.211"


        # Yoram, please use these two lines (used well in 3.4 GA)
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        latest_execution_time_str = "2000-01-01 20:56:56.120"

        # Yoram, please comment these two lines (used well in 4.0.0m1)
        #time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        #latest_execution_time_str = "2000-01-01T20:56:56.120Z"

        company_name = "Taldor"
        enable_embed = False
        round_progress = "<{0} class=\"{1}\"></{0}>".format("div", "loader2")
        created_status_html = "<img class=\"status\" src=\"css/ready.jpg\"/>"
        installed_status_html = "<img class=\"status\" src=\"css/installed.png\"/>"
        uninstalled_status_html = "<img class=\"status\" src=\"css/uninstalled.jpg\"/>"

#        powered_by_html = "<{0} class=\"{1}\">Powered by<img width=\"71\" height=\"28\" src=\"css/xglobe.png\"/></{0}>".format("span", "powered_by")

        powered_by_html = "<td><{0} class=\"{1}\">Powered by</{0}></td>".format("span", "powered_by_style")
        powered_by_html += "<td><img src=\"css/xglobe200x200.png\"/></td>"


        title_txt = "{0}'s Operations Console".format(company_name)
        start_table_and_row = "<table class=\"{0}\"><tr>".format("logo")
        end_table_and_row = "</tr></table>"
        main_headline = "{0}".format(start_table_and_row)
        main_headline += "<td><{0} class=\"{2}\">{1}'s Operations Console </{0}></td>{3}".format("h1", company_name, "logo", powered_by_html)
        main_headline += "{0}".format(end_table_and_row)
        f = StringIO()

        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        #f.write("<html>\n<title>Cloudify Deployments %s </title>\n" % displaypath)
        f.write("<html>")
        f.write("<head>")
        f.write("<title>{0}</title>".format(title_txt))
        f.write("<meta http-equiv=\"refresh\" content=\"2990\"/>".format(title_txt))
        f.write("<meta charset=\"utf-8\"/>")
        f.write("<link rel=\"stylesheet\" href=\"css/xglobe.css\" />")

        cloudify_client = CloudifyClient(cloudify_manager_ip_address)

        first_blueprint_installed, first_bp_execution_is_running = self.is_deployment_installed(cloudify_client, first_blueprint_id, latest_execution_time_str, time_format)
        scnd_blueprint_installed, scnd_bp_execution_is_running = self.is_deployment_installed(cloudify_client, scnd_blueprint_id, latest_execution_time_str, time_format)

        referer_is_me = False
        referer_exists = False
        show_scnd_deployment = False

        if 'referer' in self.headers:
            referer_exists = True
            ref_q = urlparse(self.headers['referer']).query
            curr_q = urlparse(self.path).query
            if "{0}={1}".format("show", scnd_blueprint_id) in curr_q:
                show_scnd_deployment = True
            if ref_q == curr_q:
                referer_is_me = True

        if referer_exists:
            if not referer_is_me:
                if not first_bp_execution_is_running and not scnd_bp_execution_is_running:
                    if query_components:
                        for current_action in query_components:
                            if current_action != "show":
                                current_deployment = query_components[current_action]
                                if current_deployment.endswith('/'):
                                    current_deployment = current_deployment[:-1]
                                if current_action == "install":
                                    # if current_deployment exists for scnd_blueprint_id
                                    show_scnd_deployment = self.does_deployment_exists(cloudify_client, scnd_blueprint_id, current_deployment)
                                self.start_thread_execution(cloudify_client, current_deployment, current_action)

        if first_bp_execution_is_running or not first_blueprint_installed:
            show_scnd_deployment = False

        deployment_str = ""
        deployment_str += "<{1} class=\"{2}\">Welcome {0} user !</{1}>".format(company_name, "h2", "user_headline")

        deployment_str += "<table>"
        deployment_str += "<tr>"
        actions = ""
        action1_display = "Add a new Branch"
        action2_display = "Update Branch"
        action3_display = "Provision FireWall"

        actions_display = [action1_display, action2_display]

        for ad in actions_display:
            actions += "<td><button type=\"button\" onclick=\"alert('{0}!');\">{0}</button></td>".format(ad)

        enable_scnd = "var scnd_elem = document.getElementById('{0}'); ".format(scnd_blueprint_id)
        #enable_scnd += "scnd_elem.style.display= ''; "
        #enable_scnd += "scnd_elem.style.visibility= 'visible';"
        #actions += "<td><button type=\"button\" onclick=\"{0}\">{1}</button></td>".format(enable_scnd, action3_display)
        if show_scnd_deployment:
            actions += "<td><button type=\"button\" onclick=\"window.location.href = 'http://127.0.0.1:8000?{0}={1}';\">{2}</button></td>".format("show", scnd_blueprint_id, action3_display)



        deployment_str += "<td><{0} class=\"{1}\">Available actions:{2}</{0}></td>".format("span", "user_headline", actions)

        deployment_str += "</tr>"
        deployment_str += "</table>"


        #if scbd_bp_execution_is_running:
        #    blueprint_list = [scnd_blueprint_id]
        #elif first_bp_execution_is_running:
        #    blueprint_list = [first_blueprint_id]
        #elif first_blueprint_installed:
        #    if scnd_blueprint_installed:
        #        blueprint_list = [scnd_blueprint_id]
        #    else:
        #       blueprint_list = [first_blueprint_id, scnd_blueprint_id]
        #else:
        #    blueprint_list = [first_blueprint_id]

        blueprint_list = [first_blueprint_id, scnd_blueprint_id]

        for blueprint_id in blueprint_list:
            if show_scnd_deployment or blueprint_id == first_blueprint_id or scnd_blueprint_installed or scnd_bp_execution_is_running or first_blueprint_installed:
                deployment_str += "<table id=\"{0}\">".format(blueprint_id)
            else:
                deployment_str += "<table id=\"{0}\" style=\"display:none; visibility:hidden;\">".format(blueprint_id)

            deployment_str += "<tr>"
            deployment_str += "<td>"
            #deployment_str += "<{0} class=\"{1}\">The deployments of '{2}' are: </{0}>".format("h4", "user_headline", blueprint_id)
            #deployment_str += "<ol>"
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
                        if first_bp_execution_is_running or scnd_bp_execution_is_running:
                            curr_delete = ""
                        else:
                            # Remove later
                            curr_delete = self.get_button_html("delete", deployment.id)
                            curr_delete = ""
                        if "uninstall" == wf_id:
                            curr_undeploy = ""
                            curr_run_wf = ""
                            curr_update = ""
                            wf_status = execution.status
                            embed_this_deployment = False
                            if wf_status in ("terminated", "failed", "cancelled") :
                                curr_deploy = self.get_button_html("install", deployment.id)
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
                            if wf_status in ("terminated", "failed", "cancelled") :
                                curr_update = self.get_button_html("Update", deployment.id)
                                # Remove later
                                curr_update = ""
                                curr_run_wf = self.get_button_html("Execute a Workflow", deployment.id)
                                # Remove later
                                curr_run_wf = ""
                                curr_undeploy = self.get_button_html("uninstall", deployment.id)
                                # Remove later
                                curr_undeploy = ""
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
                            if wf_status in ("terminated", "failed", "cancelled") :
                                curr_deploy = self.get_button_html("install", deployment.id)
                                curr_status = "<span class=\"{0}\">Created</span>".format("created_env")
                                curr_progress = ""
                                created_at_msg = "Created at {0}".format(created_at)
                            else:
                                curr_deploy = ""
                                curr_status = "being created..."
                                curr_progress = round_progress
                                created_at_msg = "Creation started at {0}".format(created_at)

                deployment_str += "<li><{1} class=\"{2}\">{0}</{1}></li>".format(deployment_id, "h4", "deployment_name")

                deployment_str += "<table>"
                deployment_str += "<tr>"
                deployment_str += "<td>"
                deployment_str += curr_status_class
                deployment_str += "</td>"

                deployment_str += "<td>"
                deployment_str += curr_progress
                deployment_str += "</td>"

                deployment_str += "<td>"
                deployment_str += "<{0} class=\"{1}\"></{0}>".format("span", "deployment_name")
                deployment_str += "</td>"
                deployment_str += "</tr>"

                deployment_str += "<tr>"
                deployment_str += "<td>"
                deployment_str += "<{0} class=\"{6}\">{4}</{0}>".format("span", curr_deploy, curr_update, curr_undeploy, curr_status, curr_run_wf, "deployment_name", curr_delete)
                deployment_str += "</td>"
                deployment_str += "<td>"
                deployment_str += "<{0} class=\"{6}\">{1} {2} {5} {3} {7} </{0}>".format("span", curr_deploy, curr_update, curr_undeploy, curr_status, curr_run_wf, "deployment_name", curr_delete)
                deployment_str += "</td>"
                deployment_str += "</tr>"
                deployment_str += "</table>"

                deployment_str += "<{1}>{0}</{1}>".format(created_at_msg, "span")
                deployment_str += "<br/><u>{0}</u>".format('Outputs')
                current_outputs = cloudify_client.deployments.outputs.get(deployment_id)['outputs']
                if current_outputs:
                    deployment_str += "<ul>"
                    for key in current_outputs:
                        deployment_str += "<li><span>{0}:{1}</span></li>".format(key, current_outputs.get(key))
                    deployment_str += "</ul>"
                deployment_str += "<hr/>"
                if enable_embed and embed_this_deployment:
                    embed_deployment = "<iframe src=\"http://{0}/#/deployment/{1}/topology?embed=true\" width=\"800px\" height=\"350px\"></iframe>".format(cloudify_manager_ip_address, deployment_id)
                    deployment_str += embed_deployment
            #deployment_str += "</ol>"

            deployment_str += "</td>"
            deployment_str += "</tr>"
            deployment_str += "</table>"

        f.write("<script>")
        f.write("var markersData = 5;")
        f.write("</script>")

        f.write("</head>")
        f.write("<body>{0}".format(main_headline))
#       f.write("<{0}>True to {1}</{0}>".format("span", dt.now()))
        f.write("<hr/>")
        f.write(all_instances_str)
        f.write(deployment_str)

        f.write("<div id=\"myXXX\"/>")

        f.write("</body></html>")


        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f


    def start_execution(self, cloudify_client, deployment_name, current_action):
        cloudify_client.executions.start(deployment_name, current_action)

    def start_thread_execution(self, cloudify_client, deployment_name, current_action):
        try:
            t = threading.Thread(target=self.start_execution, args=(cloudify_client, deployment_name, current_action))
            t.start()
        except Exception as e:
            print str(e)

    def get_button_html(self, btn_text, deployment_id):
        #return "<button type=\"button\" onclick=\"alert('{0} {1}')\">{0}</button>".format(btn_text, deployment_id)
        return "<td><button type=\"button\" onclick=\"window.location.href = 'http://127.0.0.1:8000?{0}={1}';\">{0}</button></td>".format(btn_text, deployment_id)

    def does_deployment_exists(self, cloudify_client, blueprint_id, deployment_id):
        all_bp_deployments = cloudify_client.deployments.list(blueprint_id=blueprint_id)
        if any(t.id in deployment_id for t in all_bp_deployments):
            return True

    def is_deployment_installed(self, cloudify_client, blueprint_id, latest_execution_time_str, time_format):
        INSTALL_STR = "install"
        latest_wf = ""
        execution_is_running = False
        for deployment in cloudify_client.deployments.list(blueprint_id=blueprint_id):
            deployment_id = deployment.id
            latest_execution_time = dt.strptime(latest_execution_time_str, time_format)
            all_executions = cloudify_client.executions.list(deployment_id=deployment_id)
            if any(t.status in ('pending', 'started') for t in all_executions):
                execution_is_running = True
            latest_wf = ""
            for execution in all_executions:
                wf_id = execution.workflow_id
                created_at = execution.created_at
                created_at_dt = dt.strptime(created_at, time_format)
                if latest_execution_time < created_at_dt:
                    latest_execution_time = created_at_dt
                    if wf_id == INSTALL_STR and execution.status == "terminated":
                        latest_wf = wf_id
                    else:
                        latest_wf = ""
        return latest_wf == INSTALL_STR, execution_is_running

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


def _aws_instances_html():

    aws_instance1 = [' joe_vm_aw4fe_call_center_jan_5th ', ' Running ', ' 2016-12-04T14:39:05Z ', ' US-East ', 'AWS']
    aws_instance2 = [' tamir_vm_gfee45_crm_dep_oct_15th ', 'Running', ' 2016-11-04T09:12:25Z ', ' EU-West ', 'AWS']
    aws_instance3 = [' James_server_dsdf55_jira_dep_June_1st    ', ' Stopped  ', ' 2016-10-21T10:25:47Z ', ' US-East ', 'AWS']

    all_aws_instances = [aws_instance1 , aws_instance2, aws_instance3]
    all_aws_instances_str = ""
    for curr_instance in all_aws_instances:
        all_aws_instances_str += _open_elem("tr", "aws")
        for curr_field in curr_instance:
            all_aws_instances_str += _open_elem("td")
            all_aws_instances_str += curr_field.strip()
            all_aws_instances_str += _close_elem("td")
        all_aws_instances_str += _close_elem("tr")
    return all_aws_instances_str


def get_all_instances_str():
    all_instances_str = _open_elem("table", "metrics_table")
    all_instances_str += _open_elem("tbody")
    instances_str, metrics_header_str = _nova_instances_html()
    all_instances_str += metrics_header_str
    all_instances_str += instances_str
    all_instances_str += _aws_instances_html()
    all_instances_str += _close_elem("tbody")
    all_instances_str += _close_elem("table")
    return all_instances_str


def get_metrics_header_str(metrics_table_header):
    metrics_header_str = _open_elem("th")
    metrics_header_str += _open_elem("tr", "metrics_header")
    for curr_field in metrics_table_header:
        metrics_header_str += _open_elem("td")
        metrics_header_str += curr_field.strip()
        metrics_header_str += _close_elem("td")
    metrics_header_str += _close_elem("th")
    return metrics_header_str


def _nova_instances_html():
    first_command = ['nova', 'list', '--fields=name,status,created,OS-EXT-AZ:availability_zone']
    second_command = ['grep', '-vE', '\-\-\-']
    all_openstack_instances = _get_nova_instances(first_command, second_command)
    metrics_table_header = all_openstack_instances[0]
    all_openstack_instances.pop()
    all_openstack_instances_str = ""
    for curr_instance in all_openstack_instances[1:]:
        all_openstack_instances_str += _open_elem("tr", "openstack")
        for curr_field in curr_instance:
            all_openstack_instances_str += _open_elem("td")
            all_openstack_instances_str += curr_field.strip()
            all_openstack_instances_str += _close_elem("td")
        all_openstack_instances_str += _close_elem("tr")
    return all_openstack_instances_str, get_metrics_header_str(metrics_table_header)


def _get_nova_instances(first_command, second_command):
    #nova list --fields=name,status,created,OS-EXT-AZ:availability_zone | grep -vE "\-\-\-" | awk -F"\|" '{ print $3 $4 $5 $6}'
    #curr_command=['nova', 'list', '--fields=name,status,created,OS-EXT-AZ:availability_zone', '|', 'grep', '-vE', '"\-\-\-"', '|' ,'awk' '-F"\|"', "'{ print $3 $4 $5 $6}'"]
    p1 = subprocess.Popen(first_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(second_command, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    p1.stderr.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output, err = p2.communicate()
    #print "zzz b4out\n{0}\n- after out".format(output)
    output_lines = output.split("\n")
    all_lines = []
    for curr_line in output_lines:
        curr_fields = curr_line.split("|")
        if len(curr_fields) > 2:
            curr_fields = curr_fields[2:-1]
            curr_fields.append("OpenStack")
            all_lines.append(curr_fields)
            #for curr_field in curr_fields:
            #    print "curr_field {0}".format(curr_field)
    all_lines[0][-1] = "Cloud"
    all_lines[0][-2] = "Region/Zone"
    for curr_line in all_lines:
        print curr_line
    print "Error:\n{0}".format(err)
    return all_lines


def _open_elem(elem_name, css_class=None):
    if css_class:
        return "<{0} class=\"{1}\">".format(elem_name, css_class)
    return "<{0}>".format(elem_name)


def _close_elem(elem_name):
    return "</{0}>".format(elem_name)


def test(cloudify_manager_ip_address, first_blueprint_id,
         scnd_blueprint_id, HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):

    # HandlerClass = SimpleHTTPRequestHandler(cloudify_manager_ip_address, first_blueprint_id, scnd_blueprint_id)
    BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    #if len(sys.argv) != 5:
    #    print "Error: Wrong number of arguments\nUsage:\n {0} port cloudify_manager_ip_address first_blueprint_id scnd_blueprint_id".format(sys.argv[0])
    #    sys.exit(-1)

    #cloudify_manager_ip_address = sys.argv[2]
    #first_blueprint_id = sys.argv[3]
    #scnd_blueprint_id = sys.argv[4]

    cloudify_manager_ip_address = "Dummy"
    first_blueprint_id = "Dummy"
    scnd_blueprint_id = "Dummy"
    test(cloudify_manager_ip_address, first_blueprint_id, scnd_blueprint_id)
