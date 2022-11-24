from flask import Blueprint, url_for, render_template, redirect

main_blueprint = Blueprint('main', __name__, template_folder='../templates/main')


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))
