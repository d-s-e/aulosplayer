import json
from flask import Flask
from flask import render_template, get_template_attribute, request, jsonify

from audioclient import Audio

app = Flask(__name__)
audiolist = []

app.debug = True


@app.route('/')
def overview():
    debug = request.args.get('debug', False)
    for p in audiolist:
        p.update_data()
    return render_template('overview.html', players = audiolist, main_title = 'Overview', debug = debug)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/view/', defaults={'pid': 0})
@app.route('/view/<int:pid>')
def view(pid):
    for p in audiolist:
        p.update_data()
        if p.pid == pid:
            return render_template('view.html', player = p, main_title = p.pid)
            break
    else:
        return render_template('view_all.html', players = audiolist)


@app.route('/ajax/<method>/', methods=['POST'])
def ajax_get(method):
    resp = {}
    for p in audiolist:
        if str(p.pid) in request.json:
            if method == 'ctrl':
                action = request.json[str(p.pid)]
                p.ctrl(action)
            p.update_data()
            resp[p.pid] = {}
            resp[p.pid]['current'] = p.current
            resp[p.pid]['status'] = p.status
            resp[p.pid]['outputs'] = p.outputs
            resp[p.pid]['next_song'] = p.next_song
            playerstatus = get_template_attribute('player_macros.html', 'playerstatus')
            resp[p.pid]['playerstatus'] = playerstatus(p)
            maininfo = get_template_attribute('player_macros.html', 'maininfo')
            resp[p.pid]['maininfo'] = maininfo(p)
            subinfo = get_template_attribute('player_macros.html', 'subinfo')
            resp[p.pid]['subinfo'] = subinfo(p)
    return jsonify(resp)


def read_config():
    return json.load(open("config/players.json", "r"))


if __name__ == '__main__':
    cfg = read_config()
    for a in cfg["audio"]:
        if a['enabled']:
            audiolist.append(Audio(a))
    app.run(host = cfg["general"]["host"], port = cfg["general"]["port"])

