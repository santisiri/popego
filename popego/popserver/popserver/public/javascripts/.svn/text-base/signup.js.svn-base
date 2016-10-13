// signup.js

if (typeof(Popego) == undefined) var Popego = {};

Popego.AbstractValidator = new Class({
	msg: undefined,
	initialize: function (msg) {
		this.msg = msg;
	},
	validate: function (s) {
		return true;
	},
	getValidationMessage: function () {
		return this.msg ? this.msg : 'Invalid value';
	}
});
Popego.RegExpValidator = Popego.AbstractValidator.extend({
	re: undefined,
	initialize: function (msg, re) {
		this.parent(msg);
		this.re = new RegExp(re, 'g');
	},
	validate: function (s) {
		return this.re.test(s);
	}
});
Popego.NotEmptyValidator = Popego.AbstractValidator.extend({
	initialize: function (msg, re) {
		this.parent(msg);
	},
	validate: function (s) {
		return (s.length > 0);
	}
});
Popego.FieldMatchValidator = Popego.AbstractValidator.extend({
	id: undefined,
	initialize: function (msg, other_field_id) {
		this.parent(msg);
		this.id = other_field_id;
	},
	validate: function (s) {
		var o = $(this.id);
		//alert(o ? o + ' == ' + o.getValue() : this.id);
		return (o && s == o.getValue());
	}
});
Popego.EmailValidator = Popego.RegExpValidator.extend({
	initialize: function(msg) {
		this.parent(msg, '^([a-zA-Z0-9_\\.\\-\\+])+\\@' 
			+ '(([a-zA-Z0-9\\-])+\\.)+([a-zA-Z0-9]{2,4})+$');
	}
});
Popego.UsernameValidator = Popego.RegExpValidator.extend({
	initialize: function(msg) {
		this.parent(msg, '^([a-zA-Z0-9_\\.\\-\\+])+$');
	}
});

Popego.AbstractSignupFormController = new Class({

	form: undefined,

	relatedForm: undefined,

	validators: undefined,

	initialize: function(form, relatedForm, validators) {
		this.form = $(form);
		this.relatedForm = $(relatedForm);
		this.validators = validators;
		var c = this;
		this.form.addEvent('submit', function (e) {
			try {
				var inputs = $ES('input', c.form);
				var s = '';
				for (var i = 0; i < inputs.length; i++)
					s += c.validate(inputs[i]);
				var el = $E('.error', c.form.getParent());
				if (el) el.empty();
				if (s || !c.onSubmit(e)) {
					c.displayValidationMessages(s);
					e.stop();
					return false;
				}
				return true;
			} catch (err) {
				alert(debug(err));
				e.stop();
				return false;
			}
		}.bindWithEvent(this.form));
	},

	validate: function (el) {
		var msg = '';
		var type = el.getProperty('type');
		if (type == 'text' || type == 'password') {
			msg = this.validateTextInput(el);
		} else if (type == 'checkbox') {
			var m = 'Cannot continue until you agree to the '
				+ 'Terms of Use and Privacy Policy.';
			msg = el.checked ? '' : m;
		}
		return msg;
	},

	validateTextInput: function(el) {
		var s = '';
		var name = $pick(el.getProperty('name') == '' ? undefined : el.getProperty('name'), el.getProperty('id').trim());
		var vs = this.validators[name];
		if (!vs) return s;
		var val = el.getValue();
		for (var i = 0; i < vs.length; i++) {
			if (!vs[i].validate(val)) {
				s = vs[i].getValidationMessage() + '\n';
				break;
			}
		}
		return s;
	},
	
	displayValidationMessages: function (s) {
	try {
		if (!s) return false;
		var el = $E('.error', this.form.getParent());
		if (!el) {
			alert(s);
			return false;
		}
		//el.empty();
		var ul = new Element('ul');
		s.split('\n').each(function (i) {
			if (i.trim() != '') {
				var li = new Element('li');
				li.setText(i);
				li.injectInside(ul);
			}
		});
		ul.injectInside(el);
		return true;
	} catch (e) {
		// alert(debug(e));
	}
	},

	onSubmit: function (e) {
		return true;
	}
});

Popego.SignupFormController = Popego.AbstractSignupFormController.extend({
	
	initialize: function (form, relatedForm) {
		var email_nev = new Popego.NotEmptyValidator(
				'Please enter your e-mail');
		var email_ev = new Popego.EmailValidator(
				'Please enter a valid e-mail');
		var username_nev = new Popego.NotEmptyValidator(
				'Please enter your username');
		var username_unv = new Popego.UsernameValidator('Username is '
				+ 'not valid (try with letters and numbers)');
		var v = {
			email: [email_nev, email_ev],
			username: [username_nev, username_unv]
		};
		this.parent(form, relatedForm, v);
	},

	onSubmit: function (e) {
		// TODO: en este recorrido del DOM se asumen algunas cosas...
		var t = this.form.getParent().getParent();
		t.setStyle('display', 'none');
		var t = t.getParent().getPrevious().getPrevious();
		t.setStyle('display', 'none');
		var t = this.relatedForm.getParent().getParent().getParent();
		t.setStyle('display', 'block');
		var username = '';
		var inputs = $ES('input', this.form);
		inputs.each(function(i) {
			if (i.getProperty('type') != 'text') return;
			var id = i.getProperty('id');
			if (id == 'username')
				username = i.getValue();
			var j = $E('input[name="' + id + '"]', 
				this.relatedForm);
			if (j) j.setProperty('value', i.getValue());
		});
		var w = $('welcome')
		if (w) w.setText('Welcome ' + username + '!');
		var input = $E('input[name="displayname"]', this.relatedForm);
		if (input) input.focus();
		return false;
	}
});

Popego.ExtendedSignupFormController = Popego.AbstractSignupFormController.extend({
	
	initialize: function (form, relatedForm) {
		var displayname_nev = new Popego.NotEmptyValidator(
				'Please enter your full name');
		var password_nev = new Popego.NotEmptyValidator(
				'Please enter your password');
		var passconfirm_nev = new Popego.NotEmptyValidator(
				'Please enter your password confirmation');
		var passconfirm_fmv = new Popego.FieldMatchValidator(
				'Passwords don\'t match; check for typos',
				'password');
		var v = {
			displayname: [displayname_nev],
			password: [password_nev],
			password_confirm: [passconfirm_nev, passconfirm_fmv]
		}
		this.parent(form, relatedForm, v);
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
		if (!$('signup')) return;
		new Popego.SignupFormController('signup', 'profile');
		new Popego.ExtendedSignupFormController('profile', 'signup');
		new Popego.TextInputCleaner();
	} catch (e) {
		// alert(debug(e));
	}
});

