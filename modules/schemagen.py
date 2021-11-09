from flask import Flask, render_template, request, send_from_directory
from genson import SchemaBuilder
import yaml
import logging
from get_selects import check_template_filenames, template_file_read
from logbase import setup_logger, call_logger


def schemagen():
    folder = "schemagen"
    data = ""
    logger_uses = logging.getLogger("logger_uses")
    logger_visits = logging.getLogger("logger_visits")
    template_names = check_template_filenames(folder)
    if request.method == 'POST':
        if request.form.get('template_names'):
            if request.form.get('template_names') == 'selects':
                return render_template('schemagen.html', template_names=template_names, notification="Wrong selection")
            else:
                file_name = request.form.get('template_names')
                logger_uses.info("a visitor just selected a schemagen yml")
                template_content = template_file_read(folder, file_name)
                notification = "you selected {}".format(file_name)
                return render_template('schemagen.html', template_names=template_names, notification=notification, yamlt=template_content)

        yinput = request.form.get('yamlt')
        jschema = request.form.get('jschema')
        if len(yinput) == 0:
            data = "<span style=\"color:red;font-weight:bold\">You can't leave Yaml box empty!</span>"
            return render_template('schemagen.html', notification = data, yamlt = yinput, jschema = jschema, template_names=template_names)
        
        try:
            yamlinput = yaml.safe_load(yinput)
        except:
            data = "<span style=\"color:red;font-weight:bold\">Yaml decoding Failed, please check the syntax</span>"
            return render_template('schemagen.html', notification = data, yamlt = yinput, jschema = jschema, template_names=template_names)

        builder = SchemaBuilder()
        builder.add_object(yamlinput)
        builder.to_schema()
        schema = builder.to_json(indent=2)
        data = "Schema is ready!"
        return render_template('schemagen.html', notification = data, yamlt = yinput, jschema = schema, template_names=template_names)



    elif request.method == 'GET':
        logger_visits.info("a visitor just visited the schemaGen")
        return render_template('schemagen.html', template_names=template_names)
