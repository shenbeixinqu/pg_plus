from flask import Blueprint, request, jsonify, render_template

bp = Blueprint('NetSecurity', __name__, url_prefix='/NetSecurity')


@bp.route('/')
def index():
	return render_template('NetSecurity/index.html')


@bp.route('/hello')
def index_one():
	return "123456"