from flask import Flask, request
from flask.ext.cors import CORS
import json
import os
from os.path import join as pjoin, exists as pexists
import datetime

app = Flask(__name__)
app.config['DATA_DIR'] = '.'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catchall(path=''):
    if request.headers.get('Content-Type') == 'application/json':
        d = request.json
    else:
        d = request.values.to_dict()
    if d:
        if path and pexists(pjoin(app.config['DATA_DIR'], path)):
            filename = path
        else:
            filename = '{0}-{1}.json'.format(
                    request.remote_addr,
                    datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S.%f'))
        output_filepath = pjoin(app.config['DATA_DIR'], filename)
        with open(output_filepath, 'a') as ofile:
            data = json.dumps(d)
            ofile.write(data)
            print('wrote {0} bytes to {1}'.format(len(data), ofile.name))
        return output_filepath
    return ''

if __name__ == '__main__':
    import sys
    port = 8000
    for arg in sys.argv[1:]:
        if arg.isdigit():
            print('setting port to %s' % arg)
            port = int(arg)
        else:
            if arg.startswith(os.path.sep):
                path = arg
            else:
                path = os.path.abspath(pjoin(os.getcwd(), arg))
            if not pexists(path):
                print('does not exist: %s.\ncreating it...' % path)
                os.mkdir(path)
            app.config['DATA_DIR'] = path
    print('setting output directory to %s' % os.path.abspath(app.config['DATA_DIR']))
    app.run('0.0.0.0', port)

