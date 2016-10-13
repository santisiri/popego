// This Popego library allows you to load and parse Twitter quotes

// sets the quote in popcard home
// TODO: this function should be Popego.setTwitterQuoteInPopcard
function setTwitterQuote(obj) {
	var quote = new Popego.Quote(obj[0]);
	var t = $('quote_date');
	if (t) t.setText(quote.getTimeInWords());
	var t = $('quote_text');
	if (t) t.setHTML(quote.getText());
	// show quote service and date
	if (t) while (t = t.getNext()) t.setStyle('display', '');
}

// sets the quote in widget content (flashing facts)
Popego.setTwitterQuote = function (obj) {
	var span = $('quote_text');
	if (!span) return; // should not
	var quote = obj[0]; // Popego.Quote not necessary here
	var t = quote.text;
	if (t.length > 84) t = t.substr(0, 80) + '...';
	span.setText(t);
}

// Quote class
Popego.Quote = new Class({

	created_at: undefined,
	text: undefined,
	external_ur: undefined,

	initialize: function (obj) {
		this.created_at = new Date();
		this.created_at.setTime(Date.parse(obj.created_at));
		var div = new Element('div');
		div.setText(obj.text); // escapes HTML
		this.text = div.getText().replace(/"/g, '&quot;');
		this.text = this.autolink(this.text);
		this.external_url = Popego.Env.quoteAccount
			? 'http://twitter.com/' // TODO: hard-coded
			+ Popego.Env.quoteAccount.username
			+ '/statuses/' + obj.id : '';
	},

	getText: function () {
		return this.text;
	},

	getExternalURL: function () {
		return this.external_url;
	},

	getTimeInWords: function () {
		return this.intervalInWords(this.created_at) + ' ago';
	},

	// expresses a time interval in words
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

	// generates links (anchors) for email, urls (http://...)
	// and twitter replies (@...)
	autolink: function (s) {
		var re = /((https?|ftp|irc|nntp)\:\/\/[_.a-z0-9-]+\.[a-z0-9\/_:@=.+&\;\?,##%&~-]*[^.|\'|\# |!|\(|?|,| |>|<|\)])/ig;
		s = s.replace(re, '<a href="$1" target="_blank">$1</a>');
		var re = /(^|\W)@([_.a-z0-9-]+)/ig;
		s = s.replace(re, '@<a href="http://twitter.com/$2" target="_blank">$2</a>');
		var re = /([_.a-z0-9-]+@[_.a-z0-9-]+\.[a-z]{2,3})/ig;
		s = s.replace(re, '<a href="mailto:$1">$1</a>');
		return s;
	}

});

// stores twitter quotes for media/quotes
Popego.userQuotes = new Array();
Popego.setTwitterQuotes = function (obj) {
	for (var i = 0; i < obj.length; i++)
		Popego.userQuotes.push(new Popego.Quote(obj[i]));
};

