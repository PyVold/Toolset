from jsonschema import Draft7Validator, draft7_format_checker, validate
from jsonschema.exceptions import ValidationError
from flask import Flask, render_template, request, send_from_directory
from logbase import setup_logger, call_logger
from get_selects import check_template_filenames, template_file_read

import yaml, json, os

def jschema():
    folder = 'schema'
    data = []
    template_names = check_template_filenames(folder)
    if request.method == 'POST':
        if request.form.get('template_names'):
            if request.form.get('template_names') == 'selects':
                return render_template('schema.html', template_names=template_names, jschemaresult = "Wrong selection")
            else:
                file_name = request.form.get('template_names')
                template_content = template_file_read(folder, file_name)
                return render_template('schema.html', template_names=template_names, jschemaresult = "Wrong selection", jschema = template_content)
        yinput = request.form.get('yamlt')
        jschema = request.form.get('jschema')

        if len(yinput) == 0 and len(jschema) == 0:
            data = "<span style=\"color:red;font-weight:bold\">You can't leave both Schema or Yaml empty!</span>"
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)
        elif len(yinput) == 0:
            data = "<span style=\"color:red;font-weight:bold\">You can't leave Yaml box empty!</span>"
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)
        elif len(jschema) == 0:
            data = "<span style=\"color:red;font-weight:bold\">You can't leave Schema box empty!</span>"
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)
        try:
            schema = json.loads(jschema)
        except json.decoder.JSONDecodeError as e:
            data = "<span style=\"color:red;font-weight:bold\">JsonSchema decoding Failed, please check the syntax</span>"
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)
        
        try:
            input_yml = yaml.load(yinput, Loader=yaml.FullLoader)
        except:
            data = "<span style=\"color:red;font-weight:bold\">Yaml decoding Failed, please check the syntax</span>"
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)

        validator = Draft7Validator(schema, format_checker=draft7_format_checker)
        try:
            validator.validate(input_yml)
            data = ""
        except ValidationError as e:
            data = e.message

        if len(data) != 0:
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)
        else:
            data = "<span style=\"color:green;font-weight:bold\">Everything is OK!</span>"
            return render_template('schema.html', jschemaresult = data, yamlt = yinput, jschema = jschema, template_names=template_names)
    
    elif request.method == 'GET':
        return render_template('schema.html', template_names=template_names)
