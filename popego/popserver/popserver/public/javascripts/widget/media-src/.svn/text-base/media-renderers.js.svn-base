Popego.Media.ItemRenderer = new Class({
	
	initialize: function(){
		this.itemHTML = "<div>Item default</div>";
		this.titleHTML = "this is the <strong>title</strong>"
		this.data = {};		
	},
	
	draw: function(data) {
		var s = '';
		for (var i in data) {
			s += i + ': ' + data[i] + '<br/>';
		}
		return '<div>' + s + '</div>';
	},
	
	formatDate: function(s) {
		var a = s.split(" ").join(",").split("-").join(",").split(":").join(",").split(",");
		var d = new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]);
		return d.format('mediumDate');
	},
	
	formatDateAsIntervalInWords: function(s) {
		var a = s.split(" ").join(",").split("-").join(",").split(":").join(",").split(",");
		var d = new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]);
		return this.intervalInWords(d);
	},

	intervalInWords: function (from, to) {
		if (!to) to = new Date();
		var millisec_per_minute = 1000 * 60;
		var millisec_interval = Math.abs(to.getTime() - from.getTime());
		var i = Math.ceil(millisec_interval / millisec_per_minute); // interval in minutes
		if (i < 1) return ('less than a minute');
		if (i < 50) return (i + ' minute' + (i == 1 ? '' : 's'));
		if (i < 90) return ('about one hour');
		if (i < 1080) return (Math.round(i / 60) + ' hours');
		if (i < 1440) return ('one day');
		if (i < 2100) return ('about one day');
		if (i < 2880) return ('almost two days');
		else return (Math.round(i / 1440) + ' days');
	},

	truncate: function(s, maxlen) {
		return s.length > maxlen ? s.substr(0, maxlen - 3) + '...' : s;
	},
	
	escapeHTML: function(s) {
		var div = new Element('div').setText(s);
		return div.innerHTML.replace(/"/g, '&quot;');
	},
	
	generateTitle: function(data) {
		var title = this.titleHTML.replace("${ASSET:FAVICON_SERVICE}", "/images/icons/" + data.service.toLowerCase() + "_favicon.png"); //TODO: Usar Popego.Config
		title = title.replace("${TITLE}", this.escapeHTML(data.title));
		title = title.replace("${DATE}", this.formatDate(data.date));
		return title;
	}

});

Popego.Media.PictureThumbsRenderer = Popego.Media.ItemRenderer.extend({
	initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}';
		
		var n = 0, itemHTML = [];
		//TODO: Ver performance por el tema replace!!
		itemHTML[n++] = '<div class="item" title="' + this.titleHTML + '" style="background:url(/images/widget/spinner_box_medium.gif) no-repeat;">';
		itemHTML[n++] = '<a href="#">';
		itemHTML[n++] = '<img style="background-image:url(${THUMBNAIL});" id="${ID}" src="/images/widget/blank.gif"/>';
		itemHTML[n++] = '</a>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${ID}", data.url);
		html = html.replace("${TITLE}", this.escapeHTML(data.title));
		html = html.replace("${DESCRIPTION}", data.description);
		html = html.replace("${DATE}", this.formatDate(data.date));
		html = html.replace("${THUMBNAIL}", data.thumbnail);
		html = html.replace("${URL}", data.url);
		html = html.replace("${EXTERNAL_URL}", data.external_url);
		html = html.replace("${ASSET:FAVICON_SERVICE}", "/images/icons/" + data.service.toLowerCase() + "_favicon.png"); //TODO: Usar Popego.Config
		html = html.replace("${SERVICE}", data.service);
		
		this.data = data;
		return html;
	}
});

Popego.Media.PictureDetailRenderer = Popego.Media.ItemRenderer.extend({
    initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}';
		
		var n = 0, itemHTML = [];
		itemHTML[n++] = '<div class="item" style=" #position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">';
		itemHTML[n++] = '<a href="${EXTERNAL_URL}" target="_blank">';
		itemHTML[n++] = '<img src="${URL}"  style=" #position: relative; #top: -50%">';
		itemHTML[n++] = '</a>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${EXTERNAL_URL}", data.external_url);
		html = html.replace("${URL}", data.url);
		
		this.data = data;
		return html;
	}
});


Popego.Media.VideoThumbsRenderer = Popego.Media.ItemRenderer.extend({
	initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}"';
		
		var n = 0, itemHTML = [];
		itemHTML[n++] = '<div class="item" title="<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}" style="background:url(/images/widget/spinner_box_large.gif) no-repeat;">';
		itemHTML[n++] = '<a href="#">';
		itemHTML[n++] = '<div class="image_strip">';
		itemHTML[n++] = '<img id="${ID}" style="background:url(${THUMBNAILS[0]}) no-repeat;" src="/images/widget/blank.gif" />';
		itemHTML[n++] = '<img id="${ID}" style="background:url(${THUMBNAILS[1]}) no-repeat; display:none;"/>';
		itemHTML[n++] = '<img id="${ID}" style="background:url(${THUMBNAILS[2]}) no-repeat; display:none;"/>';
		itemHTML[n++] = '</div>';
		itemHTML[n++] = '</a>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${ID}", data.url);
		html = html.replace("${ID}", data.url);
		html = html.replace("${ID}", data.url);
		html = html.replace("${TITLE}", this.escapeHTML(data.title));
		html = html.replace("${DESCRIPTION}", data.description);
		html = html.replace("${DATE}", this.formatDate(data.date));
		html = html.replace("${THUMBNAILS[0]}", data.thumbnails[0]);
		html = html.replace("${THUMBNAILS[1]}", data.thumbnails[0]);
		html = html.replace("${THUMBNAILS[2]}", data.thumbnails[0]);
		html = html.replace("${URL}", data.url);
		html = html.replace("${ASSET:FAVICON_SERVICE}", "/images/icons/" + data.service.toLowerCase() + "_favicon.png"); //TODO: Usar Popego.Config
		
		this.data = data;
		return html;
	}
});


Popego.Media.VideoDetailRenderer = Popego.Media.ItemRenderer.extend({
    initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}';
		
		var n = 0, itemHTML = [];
		itemHTML[n++] = '<div class="item" style="#position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">';
		itemHTML[n++] = '<object width="400" height="336px">';
		itemHTML[n++] = '<param name="movie" value="${URL}"></param>';
		itemHTML[n++] = '<param name="wmode" value="transparent"></param>';
        itemHTML[n++] = '<embed width="400" height="336" src="${URL}" type="application/x-shockwave-flash" wmode="transparent"></embed>';
        itemHTML[n++] = '</object>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${URL}", data.url);
        html = html.replace("${URL}", data.url); //reemplaza la primer aparicion
        
		this.data = data;
		return html;
	}
});

Popego.Media.BookmarksRenderer = Popego.Media.ItemRenderer.extend({

	initialize: function() {
		this.parent();
		this.itemHTML = this.getItemHTMLTemplate();
		this.tagHTML = '<li class="hits_lowest"><a href="javascript:void(0);">${TAG}</a></li>';
	},

	getItemHTMLTemplate: function() {
		var t = [], i = 0;
		// TODO: revisar css y estilos inline
		//<!--style="width: 95%; height: 37px;"-->
		t[i++] = '<div id="bookmark-${ID}" class="item">';
		t[i++] = '<div class="link_delicious" style="float: left;">';
		t[i++] = '<a href="${EXTERNAL_URL}" target="_blank">';
		t[i++] = '<h3>${POPULARITY}</h3> people</a></div>';
		t[i++] = '<div class="detail" style="width: 330px;">';
		t[i++] = '<img src="/images/icons/${SERVICE}_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">${DATE}</span>';
		t[i++] = '<h3><a href="${URL}" title="${TITLE}" target="_blank">${TRUNCATED_TITLE}</a></h3>';
		t[i++] = '<div class="tag_cloud"><ul>${TAGS}</ul></div></div></div>';
		return t.join('');
	},

	draw: function(data) {
		// gathering data attributes in r
		var r = {};
		['id', 'external_url', 'popularity', 'service', 'date', 'url',
				'title', 'tags'].each(function (i) {
			r[i] = data[i];
		});
		// attribute conversions
		r.service = r.service.toLowerCase();
		r.date = this.formatDate(r.date);
		r.tags = this.formatTags(r.tags);
		r.truncated_title = this.truncate($pick(r.title, ''), 36);
		// replacing in template
		var html = this.itemHTML;
		for (var i in r) {
			var s = '${' + i.toUpperCase() +'}';
			html = html.replace(s, r[i]);
		}
		return html;
	},

	formatTags: function(tags) {
		var s = '';
		if (tags.length > 6) {
			tags = Array.copy(tags, 0, 5);
			tags.push('...');
		}
		if ($type(tags) == $type([])) {
			tags.each(function (i) {
				if (s) s += ' + ';
				s += this.tagHTML.replace('${TAG}', i);
			}.bind(this));
		}
		return s;
	}
});

Popego.Media.BlogsRenderer = Popego.Media.ItemRenderer.extend({

	initialize: function() {
		this.parent();
		this.itemHTML = this.getItemHTMLTemplate();
		this.tagHTML = '<li class="hits_lowest"><a href="javascript:void(0);">${TAG}</a></li>';
		// TODO: este javascript inline para el show more/less es horrible
		this.lessHTML = '(<a href="javascript:void(0);" onclick="javascript: '
			+ 'var shortdesc = $E(\'span.shortdesc\', this.getParent().getParent()); '
			+ 'var fulldesc = this.getParent(); '
			+ 'if (shortdesc) shortdesc.setStyle(\'display\', \'block\'); '
			+ 'if (fulldesc) fulldesc.setStyle(\'display\', \'none\'); '
			+ 'return false;">less</a>)';
		this.moreHTML = '(<a href="javascript:void(0);" onclick="javascript: '
			+ 'var fulldesc = $E(\'span.fulldesc\', this.getParent().getParent()); '
			+ 'var shortdesc = this.getParent(); '
			+ 'if (fulldesc) fulldesc.setStyle(\'display\', \'block\'); '
			+ 'if (shortdesc) shortdesc.setStyle(\'display\', \'none\'); '
			+ 'return false;">more</a>)';
	},

	getItemHTMLTemplate: function() {
		var t = [], i = 0;
		t[i++] = '<div id="article-${ID}" class="item">';
		t[i++] = '<img class="icon" src="/images/icons/blog_favicon.png"/>';
		t[i++] = '<span class="date">${DATE}</span>';
		t[i++] = '<h3><a title="Read entire post." href="${EXTERNAL_URL}" target="_blank">${TITLE}</a></h3>';
		t[i++] = '<span class="fulldesc" style="display: none;">${DESCRIPTION} ${LESS}</span>';
		t[i++] = '<span class="shortdesc">${TRUNCATED_DESCRIPTION} ${MORE}</span>';
		//TODO: se necesitaria la account
		//t[i++] = '<div style="margin-top: 6px;">';
		//t[i++] = '<strong>Source:</strong>';
		//t[i++] = '<a href="#">www.gamesareart.com</a>';
		//t[i++] = '</div>';
		t[i++] = '<div class="tag_cloud"><ul style="text-align: left;">';
		t[i++] = '<li class="hits_lowest"><strong>Tags:</strong></li> ';
		t[i++] = '${TAGS}</ul></div></div>';
		return t.join('');
	},

	draw: function(data) {
		// gathering data attributes in r
		var r = {};
		['id', 'external_url', 'description', 'date', 'title', 'tags']
			.each(function (i) {
			r[i] = data[i];
		});
		// attribute conversions
		r.date = this.formatDate(r.date);
		r.tags = this.formatTags(r.tags);
		r.description = $pick(r.description, '(no summary available)');
		r.truncated_description = this.truncate(r.description, 120);
		r.more = (r.description.length == r.truncated_description.length)
			? '' : this.moreHTML;
		r.less = (r.description.length == r.truncated_description.length)
			? '' : this.lessHTML;
		// replacing in template
		var html = this.itemHTML;
		for (var i in r) {
			var s = '${' + i.toUpperCase() +'}';
			html = html.replace(s, r[i]);
		}

		return html;
	},

	formatTags: function(tags) {
		var s = '';
		if (tags.length > 6) {
			tags = Array.copy(tags, 0, 5);
			tags.push('...');
		}
		if ($type(tags) == $type([])) {
			tags.each(function (i) {
				if (s) s += ' + ';
				s += this.tagHTML.replace('${TAG}', i);
			}.bind(this));

		}
		return s;
	}

});

Popego.Media.QuotesRenderer = Popego.Media.ItemRenderer.extend({

	initialize: function() {
		this.parent();
		this.itemHTML = this.getItemHTMLTemplate();
	},

	getItemHTMLTemplate: function() {
		// TODO: en el ${TITLE} se podrian detectar los links
		// (http://...) y los replies (@username)
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post">';
		t[i++] = '<div class="index_item_detail">';
		t[i++] = '<a title="Read this quote at ${SERVICE}" href="${EXTERNAL_URL}" target="_blank">';
		t[i++] = '<img class="icon" src="/images/icons/${SERVICE_LOWERCASE}_favicon.png"/></a>';
		t[i++] = '<span class="date">${DATE}</span>';
		t[i++] = '<p>${TITLE}</p>';
		t[i++] = '</div></div>';
		return t.join('');
	},

	draw: function(data) {
 		r = {}
 		r.external_url = data.getExternalURL();
 		r.service = 'Twitter'; // TODO: un-hard-code
 		r.title = data.getText();
 		r.date = data.getTimeInWords();
 		r.service_lowercase = $pick(r.service).toLowerCase();

		// replacing in template
		var html = this.itemHTML;
		for (var i in r) {
			var s = '${' + i.toUpperCase() +'}';
			html = html.replace(s, r[i]);
		}

		return html;
	}

});

Popego.Media.MusicRankingRenderer = Popego.Media.ItemRenderer.extend({

	drawRankedMusic: function(data, index) {
		var t = [], i = 0;
		t[i++] = '<div class="item">';
		t[i++] = '<div class="artist spinner_box_small">';
		t[i++] = '<a href="'+data.external_url+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.title+'"></a>';
		t[i++] = '</div>';
		t[i++] = '<div class="detail">';
		// Nota: Randomizar la palabra 'interpreted by' ademas por 'sung by',  'in the voice of'
		t[i++] = '<a href="'+data.external_url+'" target="_blank">'+data.title+'</a> ';
		t[i++] = 'by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank"><strong>'+data.artist.name+'</strong></a>';
		t[i++] = '<p><span class="ranking_score">Listened '+this.formatDateAsIntervalInWords(data.date)+' ago.</span></p>';
		t[i++] = '</div>';
		t[i++] = '<div class="ranking_position">#'+(index+1)+'</div>';
		t[i++] = '</div>';
		return t.join('');
	},

	drawRankedSong: function(data, index) {
		var t = [], i = 0;
		t[i++] = '<div class="item">';
		t[i++] = '<div class="artist spinner_box_small">';
		t[i++] = '<a href="'+data.external_url+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.title+'"></a>';
		t[i++] = '</div>';
		t[i++] = '<div class="detail">';
		t[i++] = '<a href="'+data.external_url+'" target="_blank">'+data.title+'</a> ';
		t[i++] = 'by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank"><strong>'+data.artist.name+'</strong></a>';
		t[i++] = '<p><span class="ranking_score">Listened '+this.formatDateAsIntervalInWords(data.date)+' ago.</span></p>';
		t[i++] = '</div>';
		t[i++] = '<div class="ranking_position">#'+(index+1)+'</div>';
		t[i++] = '</div>';
		return t.join('');
	},

	drawRankedArtist: function (data, index) {
		var t = [], i = 0;
		t[i++] = '<div class="item">';
		t[i++] = '<div class="artist spinner_box_small">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank">';
		t[i++] = '<img src="'+data.thumbnail+'" title="'+data.title+'"></a></div>';
		t[i++] = '<div class="detail">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank">'+data.title+'</a>';
		t[i++] = '<p><span class="ranking_score">Listened '+data.playcount+' times.</span></p></div>';
		t[i++] = '<div class="ranking_position">#'+(index+1)+'</div></div>';
		return t.join('');
	},

	draw: function (data, index) {
		if (data.type == 'artist') {
			return this.drawRankedArtist(data, index);
		} else if (data.type == 'song') {
			return data.playcount ? this.drawRankedSong(data, index) : this.drawRankedMusic(data, index);
		}
		return '<div>No music information available</div>';
	}
});

Popego.Media.MusicRenderer = Popego.Media.ItemRenderer.extend({

	// TODO: descablear lastfm...
	drawArtist: function(data, data2) {
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post" style="width:390px">';
		t[i++] = '<div class="artist spinner_box">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank"><img src="'+data.thumbnail+'" title="'+data.title+'"></a>';
		t[i++] = '</div><div class="index_item_detail">';
		t[i++] = '<img src="http://assets1.popego.com/images/icons/lastfm_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">'+this.formatDate(data.date)+'</span>';
		t[i++] = '<h3>Favorite Artists</h3>';
		t[i++] = '<p style="margin-bottom:0px;margin-top:5px"><a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank"><strong>'+data.title+'</strong></a> ';
		if (data2) t[i++] = 'and <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data2.title)+'" target="_blank"><strong>'+data2.title+'</strong></a> ';
		t[i++] = (data2 ? 'are among': 'is one of') + ' the favorites.';
		t[i++] = '</p><p style="margin-top:0px"><span class="see_more btn_next">';
		t[i++] = '<a id="show_artists" href="javascript:void(0);">See Top 10 Artists</a></span></p>';
		t[i++] = '</div></div>';
		return t.join('');
	},

	drawSong: function(data) { // Favorite Songs
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post" style="width:390px">';
		t[i++] = '<div class="artist spinner_box">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.artist.name+'"></a></div>';
		t[i++] = '<div class="index_item_detail">';
		t[i++] = '<img src="http://assets1.popego.com/images/icons/lastfm_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">'+this.formatDate(data.date)+'</span>';
		t[i++] = '<h3>Favorite Songs </h3>';
		t[i++] = '<p style="margin-bottom:0px;margin-top:5px"><a href="'+data.external_url+'" target="_blank">'+data.title+'</a>, ';
		t[i++] = 'interpreted by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<strong>'+data.artist.name+'</strong></a>';
		t[i++] = ' has been listened <strong>'+data.playcount+'</strong> times.</p>'; // TODO:  "by ' + Popego.Env.username + ' " ??
		t[i++] = '<p style="margin-top:0px"><span class="see_more btn_next">';
		t[i++] = '<a id="show_songs" href="javascript:void(0);">See Top 10 Songs</a></span></p>';
		t[i++] = '</div>';
		t[i++] = '</div>';
		return t.join('');
	},

	drawMusic: function(data) { // Recently Listened
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post" style="width:390px">';
		t[i++] = '<div class="artist spinner_box">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.artist.name+'"></a>';
		t[i++] = '</div><div class="index_item_detail">';
		t[i++] = '<img src="http://assets1.popego.com/images/icons/lastfm_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">'+this.formatDate(data.date)+'</span>';
		t[i++] = '<h3>Last Songs Listened</h3>';
		t[i++] = '<p style="margin-bottom:0px;margin-top:5px"><a href="'+data.external_url+'" target="_blank">'+data.title+'</a>, ';
		t[i++] = 'interpreted by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<strong>'+data.artist.name+'</strong></a> just about '+this.formatDateAsIntervalInWords(data.date)+' ago.</p>';
		t[i++] = '<p style="margin-top:0px"><span class="see_more btn_next"><a id="show_music" href="javascript:void(0);">Last 10 tracks played</a></span></p>';
		t[i++] = '</div></div>';
		return t.join('');
	},

	draw: function(data) {
		var html = '<div>No music available</div>';
		var item = data[0];
		if (!item)
			return html;
		if (item.type == 'artist') {
			html = this.drawArtist(data[0], data[1]);
		} else if (item.type == 'song') {
			html = item.playcount ? this.drawSong(item)
				: this.drawMusic(item);
		}
		return html;
	}

});
