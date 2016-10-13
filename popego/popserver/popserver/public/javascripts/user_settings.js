// avatar_uploader.js

if (typeof(Popego) == 'undefined') Popego = {};

Popego.PersonalSettings = new Class({
	
	form: undefined,

	messages: undefined,

	img_spinner: undefined,

	initialize: function (form, messages) {
		this.form = $(form);
		this.messages = $(messages);
		this.img_spinner = $ES('img', this.form).getLast();
		this.addSubmitEvent();
	},

	addSubmitEvent: function (o) {
		var ps = this;
		this.form.addEvent('submit', function (e) {
			if (ps.messages)
				ps.messages.empty();
			if (ps.img_spinner)
				ps.img_spinner.setStyle('display', 'inline');
			this.send({
				onComplete: function () {
					if (ps.img_spinner) ps.img_spinner
						.setStyle('display', 'none');
					var t = this.response.text;
					return ps.onComplete(Json.evaluate(t));
				},
				onFailure: function () {
					if (ps.img_spinner) ps.img_spinner
						.setStyle('display', 'none');
					msg = 'Failed to submit changes. '
					+ 'Check you Internet connection.';
					return ps.onComplete(msg);
				}
			});
			e.stop();
			return false;
		}.bindWithEvent(this.form));
	},

	onComplete: function (o) {
	try {
		if ($type(o) == 'string') {
			var d = { fullname: 'Full Name', email: 'Email',
				website: 'Your Blog or Website',
				birthdate: 'Date of Birth', gender: 'Gender',
				minibio: 'Mini Bio', country: 'Country' };
			this.displayValidation(d, o);
			return false;
		}
		f = this.updateField;
		this.form.getFormElements().each(function (el) {
			f(o, el);
		});
		$('gender_m').checked = (o['gender'] == 'M');
		$('gender_f').checked = (o['gender'] == 'F');
		this.displayValidation(null,
				'Done! Your profile was updated.');
		return true;
	} catch (e) {
		// alert(debug(e));
	}
	},

	updateField: function (o, el) {
		var name = el.getProperty('name');
		if (!$defined(name) || !$defined(o[name])) 
			return;

		switch (el.getTag()) {
		case 'select':
			$each(el.options, function (op) {
				op.selected = (op.value == o[name]);
			});
			break;
		case 'input':
		case 'textarea':
			el.value = o[name];
			break;
		default:
			break;
		}
	},
	
	displayValidation: function (d, msg) {
		if (!this.messages) {
			alert(msg);
			return false;
		}
		var ul = new Element(d ? 'ul' : 'p', {'class': 'error'});
		msg.split('\n').each(function (i) {
			var s = i;
			for (var j in d) {
				if (i.indexOf(j + ': ') == 0) {
					s = d[j] + ': ';
					s += i.substr(j.length + 2, i.length);
					break;
				}
			}
			var li = new Element(d ? 'li' : 'span');
			li.setText(s);
			li.injectInside(ul);
		}.bind(this));
		ul.injectInside(this.messages);
		if (!d) (function () {
			var fadeout = new Fx.Style(ul, 'opacity', {
				onComplete: function() { ul.empty(); },
				duration: 1000
			});
			fadeout.start(1, 0);
		}).delay(3000, this);
		return true;
	}

});

Popego.PasswordSettings = Popego.PersonalSettings.extend({
	
	onComplete: function (o) {
	try {
		this.form.getFormElements().each(function (el) {
			if (el.getProperty('type') == 'password')
				el.setProperty('value', '');
		});
		var d = o ? { current_password: 'Current Password',
			confirm_password: 'Confirm Password',
			new_password: 'New Password' } : null;
		if (!o) o = 'Done! Your password was changed.';
		this.displayValidation(d, o);
		return true;
	} catch (e) {
		// alert(debug(e));
	}
	}

});

function debug(o) {
	var s = '';
	for (i in o)
		s += i + ': ' + o[i] + '\n';
	return s;
}

window.addEvent('domready', function() {
	try {
	var avatarUploader = new Popego.AvatarUploader();
	// var themeSelector = new Popego.ThemeSelector();
	var personalSettings = new Popego.PersonalSettings(
		'personal_settings', 'profile_form_errors');
	var passwordSettings = new Popego.PasswordSettings(
		'password_settings', 'password_form_errors');
	} catch (e) {
		alert(debug(e));
	}
});

