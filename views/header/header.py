from flask import Flask, render_template, redirect, url_for, request, session, flash, g, Blueprint, abort
header = Blueprint('header_page', __name__ , template_folder='templates')

@header.route('/', defaults={'page' : 'header'})
@header.route('/<page>')
def show(page):
    try: 
        return render_template('templates/%s.html' % page)
    except:
        abort(404)
