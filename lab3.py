from flask import Blueprint, url_for, request, redirect, make_response, abort, render_template
import datetime

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    return render_template('lab3.html')