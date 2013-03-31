# aulosplayer

**ATTENTION: aulosplayer is still ALPHA software!**

aulosplayer is a web application powered by flask, that provides a status and
control frontend to manage multiple MPD servers.

The primary focus of aulosplayer is to be installed on a server running
multiple mpd instances that serve different rooms but share their library
and some predefined playlists.


## Dependencies (Debian-Packages):
 * python2.7
 * python-flask
 * python-mpd
 

## Quickstart:

 * Edit config/players.json
 * Execute `python aulosplayer.py`

