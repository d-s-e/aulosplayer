"""aulosplayer main module"""
import json
from flask import Flask
from flask import render_template, get_template_attribute, request, jsonify

from audioclient import Audio


DEBUG = True


_app = Flask(__name__)
_audiolist = []


@_app.route('/')
def overview():
    """display overview page with multiple players"""
    debug = request.args.get('debug', False)
    for player in _audiolist:
        player.update_data()
    return render_template('overview.html', players = _audiolist,
                           main_title = 'Overview', debug = debug)


@_app.route('/about')
def about():
    """display program information"""
    return render_template('about.html')


@_app.route('/view/', defaults={'pid': 0})
@_app.route('/view/<int:pid>')
def view(pid):
    """display big info for one player"""
    for player in _audiolist:
        player.update_data()
        if player.pid == pid:
            return render_template('view.html', player = player,
                                   main_title = player.pid)
    else:
        return render_template('view_all.html', players = _audiolist)


@_app.route('/ajax/<method>/', methods=['POST'])
def ajax_get(method):
    """handle ajax requests"""
    resp = {}
    for player in _audiolist:
        if str(player.pid) in request.json:
            if method == 'ctrl':
                action = request.json[str(player.pid)]
                player.ctrl(action)
            player.update_data()
            resp[player.pid] = {}
            resp[player.pid]['current'] = player.current
            resp[player.pid]['status'] = player.status
            resp[player.pid]['outputs'] = player.outputs
            resp[player.pid]['next_song'] = player.next_song
            playerstatus = get_template_attribute('player_macros.html',
                                          'playerstatus')
            resp[player.pid]['playerstatus'] = playerstatus(player)
            maininfo = get_template_attribute('player_macros.html',
                                              'maininfo')
            resp[player.pid]['maininfo'] = maininfo(player)
            subinfo = get_template_attribute('player_macros.html',
                                             'subinfo')
            resp[player.pid]['subinfo'] = subinfo(player)
    return jsonify(resp)


def main(configfile):
    """init and start aulosplayer"""
    config = json.load(open(configfile, "r"))
    for audiocfg in config["audio"]:
        if audiocfg['enabled']:
            _audiolist.append(Audio(audiocfg))
    _app.debug = DEBUG
    _app.run(host = config["general"]["host"],
            port = config["general"]["port"])


if __name__ == '__main__':
    main("config/players.json")

