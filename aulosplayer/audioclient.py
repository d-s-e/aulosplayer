from mpd import MPDClient, ConnectionError, CommandError
from socket import error as SocketError

_VOLUME_STEP = 5

class Audio:
    def __init__(self, config):
        self.pid = config["id"]       
        self.host = config["host"]
        self.port = config.get("port",6600)
        self.password = config.get("password")
        self.single_list_mode = config.get("single_list_mode", False)
        self.playlist_folder = config.get("playlist_folder", '/')
        self.playlists = []
        self.current = {}
        self.next_song = {}
        self.status = {}
        self.client = MPDClient()
        self.connected = self.mpd_connect()
        if self.connected:
            if self.single_list_mode:
                pls = self.client.lsinfo(self.playlist_folder)
                for l in pls:
                    p = l.get("playlist","")
                    if len(p) > 0:
                        self.playlists.append(p)
        self.update_data()

    def mpd_connect(self):
        try:
        	self.client.connect(self.host,self.port)
        except SocketError:
            return False
        return True

    def mpd_reconnect(self):
        self.client.disconnect()
        self.connected = self.mpd_connect()

    def update_data(self):
        if self.connected:
            try:
                status = self.client.status()
                self.status = dict([
                    ('state',status.get('state','stop')),
                    ('time',status.get('time', '0:000')),
                    ('volume',status.get('volume', 0))
                ])
                self.current = self.client.currentsong()
                next_song_id = status.get('nextsong',-1)
                try:
                    self.next_song = self.client.playlistinfo(next_song_id)[0]
                except CommandError:
                    self.next_song = {}
                self._decode_utf8(self.current)
                self.outputs = self.client.outputs()
            except ConnectionError:
                self.mpd_reconnect()

    def ctrl(self, action):
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
                co = int(action[1:])
                for o in self.outputs:
                    if int(o['outputid']) == co:
                        if o['outputenabled'] == '1':
                            self.client.disableoutput(co)
                        else:
                            self.client.enableoutput(co)

    def _decode_utf8(self,dict):
        dict['title'] = dict.get('title','unknown title').decode('utf-8')
        dict['artist'] = dict.get('artist','unknown artist').decode('utf-8')
        dict['album'] = dict.get('album','unknown album').decode('utf-8')
        dict['file'] = dict.get('file','unknown file').decode('utf-8')


