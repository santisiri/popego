// alpha.js

if (typeof(Popego) == 'undefined') Popego = {};

Popego.AlphaTesterSignup = new Class({

	form: undefined,
	emailForm: undefined,
	extendedForm: undefined,
	explanationBox: undefined,
	fullExplanationbox: undefined,
	emailInput: undefined,
	firstButton: undefined,

	initialize: function (form, emailForm, extendedForm,
		explanationBox, fullExplanationBox) {
		this.form = $(form);
		this.emailForm = $(emailForm);
		this.extendedForm = $(extendedForm);
		this.explanationBox = $(explanationBox);
		this.fullExplanationBox = $(fullExplanationBox);
		var inputs = $ES('input', this.emailForm);
		this.emailInput = inputs[0];
		this.firstButton = inputs[1];
		this.setBehaviors();
	},

	setBehaviors: function () {
		this.form.addEvent('submit', 
			this.submitForm.bindWithEvent(this));
		this.firstButton.addEvent('click',
			this.submitEmail.bindWithEvent(this));
		this.emailInput.addEvent('blur', function (e) {
			var s = this.emailInput.getProperty('value').trim();
		       	if (s) this.checkEmail();
			return true;
		}.bindWithEvent(this));
	},

	submitEmail: function (e) {
		try{
			if (!this.checkEmail()) {
				this.emailInput.addEvent('keyup', function () {
					this.checkEmail();
					return true;
				}.bindWithEvent(this));
				this.emailInput.focus();
				e.stop();
				return false;
			}
			this.switchForm();
			return true;
		} catch (e) {
			// alert(debug(e));
		}
	},
	
	submitForm: function (e) {
		if (this.extendedForm.getStyle('display') == 'none') {
			this.submitEmail(e);
			e.stop();
			return false;
		}
		return true;
	},

	switchForm: function () {
		this.explanationBox.setStyle('display', 'none');
		this.fullExplanationBox.setStyle('display', 'none');
		this.emailForm.setStyle('display', 'none');
		this.extendedForm.setStyle('display', 'block');
		$E('input', this.extendedForm).focus();
	},
	
	openFullExplanationBox: function (e) {
		this.explanationBox.setStyle('display', 'none');
		this.fullExplanationBox.setStyle('display', 'block');
		this.emailForm.setStyle('display', 'none');
		this.extendedForm.setStyle('display', 'none');
		e.stop();
		return false;
	},

	closeFullExplanationBox: function (e) {
		this.explanationBox.setStyle('display', 'block');
		this.fullExplanationBox.setStyle('display', 'none');
		this.emailForm.setStyle('display', 'block');
		this.extendedForm.setStyle('display', 'none');
		e.stop();
		return false;
	},

	isValidEmail: function (email) {
		if (typeof(email) != 'string') return false;
		var r  = /^([\w\.%\-\+])+\@(([\w\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
		return r.test(email);
	},

	checkEmail: function() {
		var m = $('invalid_email_message');
		var s = this.emailInput.getProperty('value').trim();
		var emailIsOk = this.isValidEmail(s);
		if (emailIsOk) {
			if (m) m.setText('');
			this.emailInput.setProperty('value', s);
		} else {
			if (m) m.setText('Enter a valid e-mail first!');
			else alert('E-mail required!');
		}
		return emailIsOk;
	}
});

/*
function debug(o) {
	var s = '';
	for (i in o)
		s += i + ': ' + o[i] + '\n';
	return s;
}
*/

window.addEvent('domready', function() {
	try {
		var o = new Popego.AlphaTesterSignup('alpha_signup',
			'signup_form', 'signup_extended_form',
			'explanation_box', 'full_explanation_box');

		// links
		var open = o.openFullExplanationBox.bindWithEvent(o);
		var close = o.closeFullExplanationBox.bindWithEvent(o);
		$('learn_more').addEvent('click', open);
		$('yet_another_learn_more').addEvent('click', open);
		$('give_it_a_try').addEvent('click', close);
		$('learn_more').focus();

	} catch (e) {
		// alert(debug(e));
	}
});
