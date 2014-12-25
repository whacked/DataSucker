from flask import Flask, request
import json
from os.path import join as pjoin, exists as pexists
import datetime

app = Flask(__name__)
app.config['DATA_DIR'] = '.'


@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catchall(path=''):
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
            ofile.write(json.dumps(d))
        return output_filepath
    return ''

if __name__ == '__main__':
    app.run(debug=True)

