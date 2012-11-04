Number.implement({
	zeroPad: function(zeros){
		var str = '' + this;
		var z = zeros - str.length
		if (z > 0)
			z.times(function(){ str = '0'+str; });
		return str;
	}
});


String.implement({
	zeroPad: function(zeros){
		return this.toInt().zeroPad(zeros);
	}
});


var Player = new Class({
	_player: null,

	Implements: [Options, Events],
	
	options: {
		pid: 0
	},
	
	initialize: function(options){
		this.setOptions(options);
		this._player = $('player' + this.options.pid);
		this._playerstatusEl = this._player.getElements('.playerstatus');
		this._maininfoEl = this._player.getElements('.maininfo');
		this._subinfoEl = this._player.getElements('.subinfo');
	},

	update: function(values){
		var cid = this.options.pid;

/*
		this._player.getElements('.title .text').set('html', values['current']['title']);
		this._player.getElements('.artist .text').set('html', values['current']['artist']);
		this._player.getElements('.album .text').set('html', values['current']['album']);
*/
		this._player.getElements('.volume').set('html', values['status']['volume'] || '0');
		this._player.getElements('.volumebar .bar').setStyle('height', 100-Math.abs(values['status']['volume']) + '%' || '0');
		if (values['status']['volume']<3)
			this._player.getElements('.volumebar .bar').addClass('vol_min');
		else
			this._player.getElements('.volumebar .bar').removeClass('vol_min');
		play_state = values['status']['state'];
		if (play_state == 'play')
			this._player.getElements('.status_icon').set('src','/static/images/status_green.png');
		else if (play_state == 'stop')
			this._player.getElements('.status_icon').set('src','/static/images/status_red.png');
		else if (play_state == 'pause')
			this._player.getElements('.status_icon').set('src','/static/images/status_red.png');
		values['outputs'].each(function(o){
			e = $('ctrl_o' + o['outputid'].zeroPad(2) + cid);
			if (e){
				if (o['outputenabled'] == 1)
					e.addClass('active');
				else
					e.removeClass('active');
			}
		});

		this._playerstatusEl.set('html', values['playerstatus']);
		this._maininfoEl.set('html', values['maininfo']);
		this._subinfoEl.set('html', values['subinfo']);


	}
});

var players = new Hash;
var interval = 0;
var req_update;
var req_ctrl;

function update_players(){
	req_update.send(JSON.encode(players.getKeys()));
}

function ctrl_event(ev){
	evid = ev.target.id;
	req_ctrl.send('{"' + evid.substr(8) + '":"' + evid.substr(5,3) + '"}');
}

function success_cb(response){
	players.each(function(plr){
		var val = response[plr.options.pid]
		if (val && Object.getLength(val) != 0)
			plr.update(val);
		});
}

window.addEvent('domready', function(){
	$$('.ctrl').addEvent('click', ctrl_event);

	req_update = new Request.JSON({
		url: '/ajax/update/',
		urlEncoded: false,
		headers: {'Content-Type': 'application/json'},
		onSuccess: success_cb
	});
	
	req_ctrl = new Request.JSON({
		url: '/ajax/ctrl/',
		urlEncoded: false,
		headers: {'Content-Type': 'application/json'},
		onSuccess: success_cb
	});
	interval = update_players.periodical(2000);
});



