from flask import Flask, render_template, request, send_from_directory
from jinja2 import Template
from datetime import date
from logbase import setup_logger, call_logger
import yaml, logging
from modules import main, jschema, render

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
call_logger()

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)



app.add_url_rule('/', view_func=main.main)
app.add_url_rule('/render', view_func=render.convert, methods=['GET', 'POST'])
app.add_url_rule('/schema', view_func=jschema.jschema, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(host="0.0.0.0")
