== players.json


=== general
 * host: IP-Address for aulosplayer to listen, Default: "0.0.0.0"
 * port: Port for aulosplayer to listen, Default: 5000


=== audio
For each player:
 * id: numeric id for MPD service
 * name: name for MPD service (optional)
 * host: ip-address or hostname of MPD service
 * port: port of MPD service (optional, default: 6600)
 * enabled: use this MPD service in aulosplayer (true/false)
 * list_mode: display a select box with different types of playlists
   (optional, allowed values: shared, server)
 * playlist_folder: path for MPD playlists
   (only necessary when list_mode "server" has been chosen)


