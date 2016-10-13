// feedback.js

if (typeof(Popego) == 'undefined') Popego = {};

Popego.Feedback = new Class({

	showForm: function(selectedOptionIndex) {
		i = selectedOptionIndex ? selectedOptionIndex : 0;
		u = (Popego && Popego.Env && Popego.Env.username)
			? Popego.Env.username : 'about';
		html = '<div class="closer_white" title="Close"></div>';
		html += '<iframe src="/' + u + '/feedback?option=' + i;
		html += '" name="feedback" width="100%" height="265" ';
		html += 'style="border: none; clear: both;"></iframe>';
		Popego.Utils.showDialog(html, true, 'feedback_form');
		
		//this.setBehaviors();
		var closeBtn = $E('.closer_white', 'dialog_feedback_form');
		closeBtn.addEvent('click', this.hideForm);
	},
	
	hideForm: function() {
		Popego.Utils.hideDialog('feedback_form'); 
	}
	
});

Popego.FeedbackForm = new Class({
	
	initialize: function() {
		// initialize selected option
		this.initializeOptions();
		// initial focus on textarea
		var desc = $('desc');
		if (desc) desc.focus();
		// cancel button hides dialog
		var cancel = $E('input[type=reset]');
		if (cancel) cancel.addEvent('click', this.hideForm);
	},
		
	initializeOptions: function () {
		// parse GET parameter "option"
		var regex = new RegExp("[\\?&]option=(\\d+)");
		var results = regex.exec(location.search);
		var option = results ? parseInt(results[1]) : 0;
		var report = $('report');
		if (report) report.selectedIndex = option;
	},
		
	hideForm: function () {
		parent.Popego.Utils.hideDialog('feedback_form');
	}
	
});

Popego.Feedback = new Popego.Feedback();

window.addEvent('domready', function () {
	var feedback = $('feedback');
	if (feedback == document.forms[0]) {
		Popego.FeedbackForm = new Popego.FeedbackForm();
	}
});

