def check_template_filenames(folder):
    import os
    files = os.listdir('selects/{}/'.format(folder))
    template_names = []
    for file in files:
        template_names.append(file)
    return template_names

def template_file_read(folder, file_name):
    template_file = open('selects/{}'.format(folder) + "/" + file_name, 'r')
    template_content = template_file.read()
    return template_content