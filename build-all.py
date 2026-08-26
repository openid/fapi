#!/usr/bin/env python3
#
# Calls the docker build for each spec
# builds an index.html that links to them all
# reports any that fail
# exits with appropriate success / failure return code

import glob
import json
import os
import re
import sys
import subprocess
from datetime import date


dirs_exclude = [
    ".git",
    ".idea",
    "cds-spec-analysis"
]

# This list is currently a list of files that fail to process
# Some of them we likely don't care about, but some of them should be fixed and removed from the list
files_exclude = [
    './FAPI_2_0_Advanced_Profile.md',
    './FAPI_2_0_Advanced_Authorization_Profile.md',
    './FAPI_2_0_Baseline_Profile.md',
    './Financial_API_JWT_Secured_Authorization_Response_Mode.md',
    './Financial_API_Lodging_Intent.md',
    './Financial_API_Pushed_Request_Object.md',
    './Financial_API_Simple_HTTP_Message_Integrity_Protocol.md',
    './Financial_API_WD_000.md',
    './Financial_API_WD_001.md',
    './Financial_API_WD_002.md',
    './Financial_API_WD_003.md',
    './Financial_API_WD_004.md',
    './Financial_API_WD_005.md',
    './TR-Cross_browser_payment_initiation_attack.md',
    './fapi-grant-management.md',
    './FAPI_1.0/changes-between-id2-and-final.md',
    './FAPI_2_0_Message_Signing.md',
    './FAPI_2_0_Security_Profile.md'
]

fapi1_files = [
    './FAPI_1.0/openid-financial-api-part-1-1_0.md',
    './FAPI_1.0/openid-financial-api-part-2-1_0.md'
]

# Pinned by digest so the rendering is reproducible: an untagged/:latest image
# could silently change the output between identical commits. Regenerate the
# digest with `docker buildx imagetools inspect danielfett/markdown2rfc:latest`.
MD2RFC_IMAGE = 'danielfett/markdown2rfc@sha256:7b4412559d6ba5db45a14174a28da5b240512e7c2a886a5e4adb44e5e67f34ca'

failed = []

files_generated = []

# source .md -> generated .html, written to manifest.json for CI to link the
# drafts changed in a pull request from the preview comment
manifest = {}

def get_output_filename(fname):
    # get the output filename, i.e. do what https://github.com/oauthstuff/markdown2rfc/blob/master/make.sh#L18 does
    # and find the line like: value = "fapi-2_0-baseline-01"
    regex = r'^value[\W]*=[\W]*"(.*)"'
    return get_output_filename_impl(fname, regex)

def get_fapi1_output_filename(fname):
    # get the fapi1 output filename, i.e. do what https://github.com/oauthstuff/markdown2rfc/blob/master/make.sh#L18 does
    # and find the line like:  value: openid-financial-api-part-2-1_0-01
    regex = r'^[\W]*value[\W]*:[\W]*(.*)$'
    return get_output_filename_impl(fname, regex)

def get_output_filename_impl(fname, regex):
    with open(fname, 'r') as f:
        for line in f:
            matches = re.search(regex, line)
            if matches:
                return matches.group(1)

def execute_command(cmd, fname, outputfname):
    retcode = subprocess.call(cmd)
    if retcode != 0:
        failed.append(fname)
        print("docker run returned failure for "+fname)
        return
    if not os.path.isfile(outputfname):
        print("expected output file of "+outputfname+" not found for "+fname)
        failed.append(fname)
        return

    # the generated html contains a version number that we don't want to end up in the url; remove it
    m = re.search(r'^(.*)-\d\d\.html$', outputfname)
    if m:
        newoutputfname = m.group(1)+".html"
        os.rename(outputfname, newoutputfname)
        outputfname = newoutputfname
        print("Renamed output to "+outputfname)
    files_generated.append(outputfname)
    manifest[fname[2:] if fname.startswith('./') else fname] = outputfname
    print()

def process_spec(fname):
    currentdir = os.getcwd()
    cmd = [ 'docker', 'run', '-v', currentdir+':/data', MD2RFC_IMAGE, fname ]
    print("Running: " + ' '.join(cmd))
    outputfname = get_output_filename(fname)
    outputfname += ".html"
    execute_command(cmd, fname, outputfname)


def process_fapi1_spec(fname):
    outputfname = get_fapi1_output_filename(fname)
    outputfname += ".html"
    formatted_date = date.today().strftime('%B %d, %Y')
    currentdir = os.getcwd()
    cmd = [ './pandoc-3.1.9/bin/pandoc', '-V', 'current_date=' + formatted_date, '--toc', '--embed-resources', '-c',  './FAPI_1.0/templates/site.css', '--template=./FAPI_1.0/templates/draft-template.html', '-f', 'markdown', '-t', 'html',  '--section-divs', '--standalone', '--verbose', '-o', outputfname, fname ]
    print("Running: " + ' '.join(cmd))
    execute_command(cmd, fname, outputfname)


def walk_tree():
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in dirs_exclude]
        for file in sorted(files):
            if not file.endswith(".md"):
                continue
            if file.casefold() == "readme.md".casefold():
                continue
            fullfname = os.path.join(root, file)
            if fullfname in files_exclude:
                continue
            if fullfname in fapi1_files:
                process_fapi1_spec(fullfname)
            else:
                process_spec(fullfname)

def generate_index():
    print("Creating index.html")
    header = '''
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <title>OpenID Foundation FAPI Working Group Drafts</title>
  <style type="text/css">
<!--
body {
	font-family: sans-serif;
	margin: 2em;
}
.navigation li {
	display: inline;
	margin-right: 1.5em;
}
.style1 {
	color: #FF0000;
	font-weight: bold;
}
.logo {
	max-width: 10%;
	max-height: auto;
	float: left;
	margin-right: 2em;
}
.not-active {
   pointer-events: none;
   cursor: default;
   color: #aF0000;
}
-->
  </style>
</head>
<body>
<div id="nav" class="column span-18 append-1 prepend-1">
  <ul class="navigation">
    <li><a href='https://openid.net/wg/fapi/'>About</a></li>
    <li><a href='https://github.com/openid/fapi'>Repository</a></li>
    <li><a href='https://github.com/openid/fapi/issues'>Issues</a></li>
  </ul>
</div>
<div id="content">
<h1>OpenID Foundation FAPI Working Group Drafts</h1>
<h2>List of Draft Specifications</h2>
<p>Below are links to the HTML versions of the working groups draft documents:</p>
<ul>
'''
    footer = '''
</ul>
</div>
</body>
</html>
'''
    with open('index.html', 'w') as f:
        print(header, file = f)
        for fname in files_generated:
            print('	 <li><a href="{}">{}</a></li>'.format(fname, os.path.splitext(fname)[0]), file = f)
        print(footer, file = f)
    return

walk_tree()
generate_index()
with open('manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2, sort_keys=True)
if failed:
    print("The processing of some specifications failed:")
    for f in failed:
        print(f)
    sys.exit(1)

sys.exit(0)
