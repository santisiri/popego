// avatar_uploader.js

if (typeof(Popego) == 'undefined') Popego = {};

Popego.AjaxUploader = new Class({

	form: undefined,
	iframe: undefined,
	onSubmit: function () {},
	onComplete: function () {},

	initialize: function (form, iframe, onSubmit, onComplete) {
	try {
		// form and iframe elements setup
		this.form = $(form);
		this.iframe = $(iframe);
		if (!$defined(iframe))
			this.createIframe('ajax_uploader_iframe');
		else if (!this.iframe)
			this.createIframe(iframe.toString());

		// form-iframe targetting
		this.form.setProperty('target', this.iframe.id);
		// event setup
		if ($type(onSubmit) == 'function')
			this.onSubmit = onSubmit; 
		if ($type(onComplete) == 'function')
			this.onComplete = onComplete;
		this.form.addEvent('submit', this.onSubmit.bind(this));
		this.iframe.addEvent('load', this.onComplete.bind(this));
	} catch (e) {
		// alert(debug(e));
	}
	},

	createIframe: function (id) {
		this.iframe = new Element('iframe');
		this.iframe.setStyle('display', 'none');
		this.iframe.setProperty('src', 'about:blank');
		this.iframe.setProperty('id', id);
		this.iframe.setProperty('name', id);
		this.iframe.injectInside(this.form);
	}

});

Popego.AvatarUploader = Popego.AjaxUploader.extend({
	
	message: undefined,

	avatar: undefined,

	img_spinner: undefined,

	// Se podrian pasar como parametros los siguientes Element ids:
	// 'upload_avatar' (form), 'upload_iframe' (iframe; puede no existir),
	// 'upload_message' (para mostrar errores), 'avatar_img' (img)
	initialize: function () {
		this.parent('upload_avatar', 'upload_iframe',
				this.onSubmit, this.onComplete);
		this.message = $('upload_message');
		this.avatar = $('avatar_img');
		this.img_spinner = $ES('img', this.form).getLast();
		// submit form on change event of the file input field
		var input = $ES('input', this.form)[0];
		if (input) input.addEvent('change', function (e) {
			var f = e.target.form;
			f.fireEvent('submit');
			f.submit();
		}.bindWithEvent(input));
	},

	onSubmit: function () {
		this.message.setStyle('opacity', 1);
		this.message.setText('Uploading avatar...');
		if (this.img_spinner)
			this.img_spinner.setStyle('display', 'inline');
		return true;
	},
	
	onComplete: function () {
		try {
			var t = this.getIframeText();
			if (t.length > 255) {
				t = 'Failed to upload your avatar '
					+ '(Internal Server Error)';
			}
			if (this.img_spinner)
				this.img_spinner.setStyle('display', 'none');
			this.refreshMessage(t);
			this.refreshImage();
		} catch (e) {
			// alert(debug(e));
		}
		return true;
	},
	
	refreshMessage: function (t) {
		var m = this.message;
		if (m.getText() != '' && t.replace(/^\s+|\s+$/g, '') == '') {
			t = 'Done! Your avatar was updated.';
			(function () {
				var fadeout = new Fx.Style(m, 'opacity', {
					onComplete: function() { m.empty(); },
					duration: 1000
				});
				fadeout.start(1, 0);
			}).delay(3000, this);
		}
		m.setText(t);
	},

	refreshImage: function (img) {
		img = $pick(img, this.avatar);
		if (!$defined(img)) return false;
		var src = img.getProperty('src').toString();
		var i = src.lastIndexOf('?');
		if (i >= 0) src = src.substr(0, i);
		src += '?' + new Date().getTime().toString();
		img.setProperty('src', src);
		return true;
	},

	getIframeText: function (iframe) {
		var f = $pick(iframe, this.iframe);
		var doc = undefined;
		if (f.contentDocument) { // For NS6
			doc = f.contentDocument; 
		} else if (f.contentWindow) { // For IE5.5 and IE6
			doc = f.contentWindow.document;
		} else if (f.document) { // For IE5
			doc = f.document;
		}
		return (doc && doc.body) ? doc.body.innerHTML : '';
	}

});

function debug(o) {
	var s = '';
	for (i in o)
		s += i + ': ' + o[i] + '\n';
	return s;
}

