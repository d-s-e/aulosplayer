"""module to access and manage a single mpd instance"""
from mpd import MPDClient, ConnectionError, CommandError
import socket

_VOLUME_STEP = 5

class Audio:
    """class representing a single player connected to one mpd instance"""
    def __init__(self, config):
        self.pid = config["id"]       
        self.host = config["host"]
        self.port = config.get("port", 6600)
        self.password = config.get("password")
        self.list_mode = config.get("list_mode", False)
        self.playlist_folder = config.get("playlist_folder", '/')
        self.playlists = {}
        self.current = {}
        self.next_song = {}
        self.status = {}
        self.outputs = {}
        self.client = MPDClient()
        self.connected = self.mpd_connect()
        if self.connected:
            if self.list_mode:
                if 'shared' in self.list_mode:
                    playlists = self.client.lsinfo(self.playlist_folder)
                    for pls in playlists:
                        plsid = pls.get("playlist","")
                        if len(plsid) > 0:
                            try:
                                self.playlists['shared'].append((plsid,
                                                                 'shd'+plsid))
                            except KeyError:
                                self.playlists['shared'] = []
                                self.playlists['shared'].append((plsid,
                                                                 'shd_'+plsid))
                if 'server' in self.list_mode:
                    playlists = self.client.lsinfo(self.playlist_folder)
                    for pls in playlists:
                        plsid = pls.get("playlist","")
                        if len(plsid) > 0:
                            try:
                                self.playlists['server'].append((plsid,
                                                                 'srv_'+plsid))
                            except KeyError:
                                self.playlists['server'] = []
                                self.playlists['server'].append((plsid,
                                                                 'srv_'+plsid))
        self.update_data()

    def mpd_connect(self):
        """connect to mpd service"""
        try:
            self.client.connect(self.host, self.port)
        except socket.error:
            return False
        return True

    def mpd_reconnect(self):
        """reconnect to mpd service"""
        self.client.disconnect()
        self.connected = self.mpd_connect()

    def update_data(self):
        """update data from mpd service"""
        if self.connected:
            try:
                status = self.client.status()
                self.status = dict([
                    ('state',status.get('state','stop')),
                    ('time',status.get('time', '0:000')),
                    ('volume',status.get('volume', 0))
                ])
                self.current = self.client.currentsong()
                next_song_id = status.get('nextsong', -1)
                try:
                    self.next_song = self.client.playlistinfo(next_song_id)[0]
                except CommandError:
                    self.next_song = {}
                _decode_utf8(self.current)
                _decode_utf8(self.next_song)
                self.outputs = self.client.outputs()
            except ConnectionError:
                self.mpd_reconnect()

    def ctrl(self, action):
        """execute a mpd command"""
        if self.connected:
            if action == 'ply':
                self.client.play()
            elif action == 'pse':
                self.client.pause()
            elif action == 'vup':
                status = self.client.status()
                volume = int(status.get('volume', 0))
                try:
                    self.client.setvol(min(volume + _VOLUME_STEP, 100))
                except CommandError:
                    pass
            elif action == 'vdn':
                status = self.client.status()
                volume = int(status.get('volume', 0))
                try:
                    self.client.setvol(max(volume - _VOLUME_STEP, 0))
                except CommandError:
                    pass
            elif action == 'rew':
                self.client.previous()
            elif action == 'fwd':
                self.client.next()
            elif action[:1] == 'o':
                outid = int(action[1:])
                for output in self.outputs:
                    if int(output['outputid']) == outid:
                        if output['outputenabled'] == '1':
                            self.client.disableoutput(outid)
                        else:
                            self.client.enableoutput(outid)


def _decode_utf8(data):
    """decode utf-8 encoded data from mpd and set defaults for empty fields"""
    data['title'] = data.get('title', '').decode('utf-8') or u'\u2014'
    data['artist'] = data.get('artist', '').decode('utf-8') or u'\u2014'
    data['album'] = data.get('album', '').decode('utf-8') or u'\u2014'
    data['file'] = data.get('file', '').decode('utf-8') or u'\u2014'


