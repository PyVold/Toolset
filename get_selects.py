import os
dir = os.path.dirname(__file__)

def check_template_filenames(folder):
    selects_path = os.path.join(dir, 'selects/{}'.format(folder))
    files = os.listdir(selects_path)
    template_names = []
    for file in files:
        template_names.append(file)
    return template_names

def template_file_read(folder, file_name):
    template_file = open(os.path.join(dir, 'selects/{}'.format(folder)) + "/" + file_name, 'r')
    template_content = template_file.read()
    return template_content