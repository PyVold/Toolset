from logbase import setup_logger, call_logger
from flask import Flask, render_template, request, send_from_directory
from jinja2 import Template
from datetime import date
import yaml, logging
from get_selects import check_template_filenames, template_file_read


def convert():
    folder = 'render'
    logger_uses = logging.getLogger("logger_uses")
    logger_visits = logging.getLogger("logger_visits")
    template_names = check_template_filenames(folder)
    if request.method == 'POST':
        if request.form.get('template_names'):
            if request.form.get('template_names') == 'selects':
                return render_template('convert.html', configresult='', jin='Wrong Selection',
                                       yamlt='your values here',
                                       template_names=template_names)
            file_name = request.form.get('template_names')
            template_content = template_file_read(folder, file_name)
            logger_visits.info("visitor selected a template {}".format(file_name))
            return render_template('convert.html', configresult='', jin=template_content,
                                   yamlt="", template_names=template_names)
        else:
            try:
                yinput = request.form.get('yamlt')
                try:
                    yamlt = yaml.safe_load(yinput)
                except (ScannerError, ParserError):
                    yamlt = "Yaml format is wrong!, please fix it."
                jin = Template(request.form.get('jin'))
                configresult = jin.render(yamlt, Template=jin)
                logger_uses.info(configresult)
                #logger_uses.handler.close()
                return render_template('convert.html', configresult=configresult, jin=request.form['jin'], yamlt=yinput,
                                       template_names=template_names)
            except:
                yinput = request.form.get('yamlt')
                return render_template('convert.html',
                                       configresult="There is something wrong with either the template or the values",
                                       jin=request.form.get('jin'), yamlt=yinput,
                                       template_names=template_names)
    elif request.method == 'GET':
        logger_visits.info("someone visited the tool")
        jin = ""
        yamlt = ""
        return render_template('convert.html', jin=jin, yamlt=yamlt, template_names=template_names)
