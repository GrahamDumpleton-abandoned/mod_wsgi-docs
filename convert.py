import os

files = os.listdir('originals')

for original in files:
    if original[-5:] == '.wiki':
        print original
        target = original.replace('.wiki', '.rst')
        fds = open(target, 'w')
        codeblock = False
        for line in open('originals/%s' % original, 'r').readlines():
            if line[:1] == chr(239):
                index = line.find('#')
                line = line[index:]
            if codeblock and line.startswith('}}}\n'):
                fds.write('\n')
                codeblock = False
            elif codeblock:
                fds.write('    ')
                fds.write(line)
            elif line.startswith('{{{\n'):
                codeblock = True
                fds.write('::\n\n')
            elif line.startswith('=='):
                index = line.find(' ')
                line = line[index+1:]
                index = line.rfind(' ')
                line = line[:index]
                fds.write(line)
                fds.write('\n')
                fds.write(len(line)*'-')
                fds.write('\n')
            elif line.startswith('='):
                index = line.find(' ')
                line = line[index+1:]
                index = line.rfind(' ')
                line = line[:index]
                fds.write(len(line)*'=')
                fds.write('\n')
                fds.write(line)
                fds.write('\n')
                fds.write(len(line)*'=')
                fds.write('\n')
            elif line.startswith('#summary'):
                pass
            elif line.startswith('#labels'):
                pass
            elif line.startswith('_*If you are using mod_wsgi'):
                pass
            elif line.startswith('[HowToContributeBack donation]'):
                pass
            else:
                line = line.replace('{{{', '``')
                line = line.replace('}}}', '``')
                fds.write(line)
