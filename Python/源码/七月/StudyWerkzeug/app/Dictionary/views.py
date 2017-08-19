from flask import render_template
from . import dictionary

@dictionary.route('/dictionary')
def index():
    return render_template('/dictionaryTemplates/index.html')
