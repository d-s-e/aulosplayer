== audio configuration
The configuration described here is based on accessing ALSA directly without
using an intermediate layer like pulseaudio.


=== /etc/mpd.conf

==== dummy device
To prevent mpd from stopping the playback when all outputs are disabled,
we need to use a dummy output that is always active and not accessible
from the aulosplayer frontend.

	audio_output {
	    type    "null"
	    name    "dummy"
	}


==== software mixing
If aulosplayer should only set the volume for a specific MPD output without
affecting the volume of other applications using the same output device,
software mizing has to be enabled. This is done by adding a line containing
`mixer_type "software"` to your device config.

Example:

	audio_output {
	    type            "alsa"
	    name            "ALSA Default"
	    device          "hw:0,0"
	    mixer_device    "default"
	    mixer_control   "MPD"
	    mixer_index     "0"
	    mixer_type      "software"
	}


=== /etc/asound.conf

TODO


