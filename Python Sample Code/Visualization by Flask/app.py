#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:35:54 2024

@author: hy
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')
@app.route('/mlpage')
def mlpage():
    return render_template('ML.html')
    
if __name__ == '__main__':
    app.run(debug=True)

