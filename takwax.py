#!/usr/bin/env python

#-----------------------------------------------------------------------
# registrar.py
# Author: Sreeniketh Vogoti
#-----------------------------------------------------------------------

import flask
#import database
import sys
import contextlib
from flask import Flask, jsonify, request
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/search', methods=['GET'])
def search():
    entry = flask.request.args.get('entry')

    if entry is None:
        entry = ''
    entry = entry.strip()

    request_json = {'entry':entry}
    output_json = database.get_entry(request_json)
    # output_json: entry underlying	pos	definition	semantic category	etymology	related	examples	tags	notes	source
    #prev_entry = flask.request.cookies.get('prev_entry')
    
    html_code = flask.render_template('index.html',
        #prev_entry=prev_entry,
        output_json=output_json[1])
    response = flask.make_response(html_code)
    #response.set_cookie('prev_entry', entry)
    return response

#-----------------------------------------------------------------------

@app.route('/entry', methods=['GET'])
def get_entry():
    entry = flask.request.args.get('classid')
    request_json = {'entry':entry}
    output_json = database.get_entry(request_json)

    #boolean finding whether there is an error
    all_clear = output_json[0]

    output_json_dict = output_json[1]
    html_code = flask.render_template('entry.html',
        all_clear=all_clear, output=output_json_dict[0])
    response = flask.make_response(html_code)

    return response
