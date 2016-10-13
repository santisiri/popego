/* POPEGO WIDGET CONTENT Javascript */
if (window.ActiveXObject) window.ie = true;

/**
 * FLASHING FACTS
 **/
 
// TODO: Refactorear con MOOTOOLS

// Sets HTML element opacity to a value ranging from 0 to 100
function setOpacity(obj, value) {
	if (!obj || !obj.style) return;
	obj.style.opacity = value / 100;
	obj.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + value + ')';
}
// Sets HTML element visibility to true/false (display block or none)
function setVisible(obj, bool) {
	if (!obj || !obj.style) return;
	obj.style.display = bool ? 'block' : 'none';
}
// FlashingList
function FlashingList(divs) {
	// Instance variables
	this.divs = new Array();
	this.currentIndex = 0;
	this.currentOpacity = 100;
	this.fadingStep = 100; // interval between opacity changes
	this.switchingStep = 5000; // interval in which each element is visible
	// Initialization
	for (var i = 0; i < divs.length; i++) {
		if (divs[i]) {
			setVisible(divs[i], (i < 1));
			setOpacity(divs[i], (i < 1) ? 100 : 0);
			this.divs.push(divs[i]);
		}
	}
	// Instance methods
	this.getElement = function (index) {
		if (index < 0) index += this.divs.length;
		var i = (this.currentIndex + index) % this.divs.length;
		return this.divs[i];
	}
	this.getCurrentElement = function () {
		return this.getElement(0);
	}
	this.getLastElement = function () {
		return this.getElement(-1);
	}
	this.nextElement = function () {
		this.currentIndex++;
		this.currentIndex %= this.divs.length;
		return this.getElement(0);
	}
	var fl = this;
	this.fadeInOut = function () {
		try {
			var p = fl.getLastElement();
			var o = fl.getCurrentElement();
			fl.currentOpacity += 10;
			if (fl.currentOpacity >= 100) {
				fl.currentOpacity = 100;
				setOpacity(p, 0);
				setOpacity(o, 100);
				setTimeout(fl.switcher, fl.switchingStep);
			} else {
				setOpacity(p, 100 - fl.currentOpacity);
				setOpacity(o, fl.currentOpacity);
				setTimeout(fl.fadeInOut, fl.fadingStep);
			}
		} catch (e) {
			alert(e.message); // TODO
		}
	}
	this.switcher = function () {
		try {
			var old = fl.getLastElement();
			setVisible(old, false);
			var p = fl.getCurrentElement();
			var o = fl.nextElement();
			fl.currentOpacity = 0;
			setOpacity(p, 100);
			setVisible(o, true);
			setOpacity(o, 0);
			setTimeout(fl.fadeInOut, fl.fadingStep);
		} catch (e) {
			alert(e.message); // TODO
		}
	}
	// Initialization
	setTimeout(this.switcher, this.switchingStep);
}

function getFlashingFactsDivs() {
	var ffParent = document.getElementById('facts');
	var re = new RegExp("\\bfact\\b", "g");
	var divs = new Array();
	for (var i = 0; i < ffParent.childNodes.length; i++) {
		var node = ffParent.childNodes[i];
		if (node.nodeType == 1
			&& node.nodeName.toLowerCase() == 'div'
			&& node.className.match(re)) {
			divs.push(node);
		}
	}
	return divs;
}

/**
 * WidgetContent
 **/
/*
if (typeof Popego == "undefined") Popego = {};
Popego.WidgetContent = new Class({
	//URLs
	URL_SIGNIN: '/signin?from=widget&parentUrl=' + Popego.Env.parentUrl + '&theme=' + Popego.Env.widgetTheme + '&instanceId=' + Popego.Env.instanceId,
	URL_SIGNOUT: '/signout?from=widget&owner=' + Popego.Env.username + '&parentUrl=' + Popego.Env.parentUrl + '&theme=' + Popego.Env.widgetTheme + '&instanceId=' + Popego.Env.instanceId,
	
	initialize: function(el) {
		this.contentDiv = el;
		this.wrapperDiv = this.contentDiv.getElement('.wrapper');
		this.avatarImg = this.contentDiv.getElement('.avatar');
		this.factsDiv = this.contentDiv.getElementById('facts');
		this.userEncounterDiv = this.contentDiv.getElement('.user_encounter'); //datapanel
		this.userLoginDiv = this.contentDiv.getElement('.user_login');		   //datapanel
		
		//Styles/Effects
		this.fadeFacts = new Fx.Style(this.factsDiv, 'opacity', {duration: 400, transition: Fx.Transitions.quartInOut});					
		this.fadeDataPanel = undefined
		
		this.isOverDataPanel = false;
		this.isDataPanelVisible = false;
		this.dataPanelInterval = undefined;
		this.activeDataPanel = undefined;
		this.setDataPanel(this.userEncounterDiv);
		
		this.setBehaviors();
	},
	
	openPopcard: function() {
		window.parent.location.replace(Popego.Env.parentUrl + '#OpenPopcard_' + Popego.Env.instanceId + '_' + (new Date()).getTime());
		window.parent.focus();
	},
	
	showLoginForm: function() {
		this.activeDataPanel.setStyle('display', 'none');
		this.userLoginDiv.setStyle('display', '');
		this.userLoginDiv.getElement('input[type=text]').focus();
		this.setDataPanel(this.userLoginDiv);
	},
	
	setDataPanel: function(el) {
		this.activeDataPanel = el;
		this.fadeDataPanel = new Fx.Style(this.activeDataPanel, 'opacity', {duration: 400, transition: Fx.Transitions.quartInOut});
		
		// Styles/Effects's Behavior
		var onCompleteFadeDataPanel = function() {
			if (!this.isDataPanelVisible) {// Se termino de esconder el datapanel
				if(this.activeDataPanel == this.userLoginDiv) {
					this.userLoginDiv.setStyle('display', 'none');
					this.userLoginDiv.setStyle('opacity', '1');
					this.userEncounterDiv.setStyle('opacity', '0');
					this.userEncounterDiv.setStyle('display', '');
					this.setDataPanel(this.userEncounterDiv);
				}
			}
		}
		this.fadeDataPanel.addEvent('onComplete', onCompleteFadeDataPanel.bind(this));
	},
	
	setBehaviors: function() {
		// Initialize view
		this.userEncounterDiv.setStyle('opacity', 0);
		this.userEncounterDiv.setStyle('display', '');
		
		// Open Popcard buttons
		this.contentDiv.getElement('.open').addEvent('mousedown', this.openPopcard.bind(this));
		this.wrapperDiv.addEvent('mousedown', this.openPopcard.bind(this));
		this.avatarImg.addEvent('mousedown', this.openPopcard.bind(this));
		
		// URL para login y logout
		this.userLoginDiv.getElementById('login').action = this.URL_SIGNIN;
		if (Popego.Env.remoteUserLoggedIn)
			this.userEncounterDiv.getElement('.logout').getElement('a').href = this.URL_SIGNOUT;
		else {
			this.userEncounterDiv.getElement('.logout').getElement('a').addEvent('click', this.showLoginForm.bind(this));
			var user = this.userLoginDiv.getElement('input[type=text]');
			var pwd = this.userLoginDiv.getElement('input[type=password]');
			user.addEvent('focus', function(){ this.select() });
			user.addEvent('blur', function(){ if (this.value.trim() == '') this.value = 'username';});
			pwd.addEvent('focus', function(){ this.select() });
			pwd.addEvent('blur', function(){ if (this.value.trim() == '') this.value = 'password';});
		}
		
		// Wrapper's Behavior
		var onWrapperOver = function() {
			$clear(this.dataPanelInterval);
			if (!this.isDataPanelVisible)
				this.showDataPanel();
		}
		var onWrapperOut = function() {
			if (this.isDataPanelVisible && !this.isOverDataPanel)
				this.dataPanelInterval = this.hideDataPanel.bind(this).delay(100);
		}
		this.wrapperDiv.addEvent('mouseenter', onWrapperOver.bind(this));
		this.wrapperDiv.addEvent('mouseleave', onWrapperOut.bind(this));
		
		// Si es IE5+ considero como wrapper tambien a la imagen (avatar)
		if (window.ie && !window.ie7) {
			this.avatarImg.addEvent('mouseenter', onWrapperOver.bind(this));
			this.avatarImg.addEvent('mouseleave', onWrapperOut.bind(this));
			this.factsDiv.addEvent('mouseenter', onWrapperOver.bind(this));
			this.factsDiv.addEvent('mouseleave', onWrapperOut.bind(this));
		}
		
		// DataPanel's Behavior
		var onDataPanelOver = function(e, panelDiv) {
			this.isOverDataPanel = true;
			this.activeDataPanel = panelDiv;
			$clear(this.dataPanelInterval);
		}
		var onDataPanelOut = function(e) {
			this.isOverDataPanel = false;
			this.dataPanelInterval = this.hideDataPanel.bind(this).delay(500);
		}
		this.userEncounterDiv.addEvent('mouseenter', onDataPanelOver.bindWithEvent(this, this.userEncounterDiv));
		this.userEncounterDiv.addEvent('mouseleave', onDataPanelOut.bindWithEvent(this));
		this.userLoginDiv.addEvent('mouseenter', onDataPanelOver.bindWithEvent(this, this.userLoginDiv));
		this.userLoginDiv.addEvent('mouseleave', onDataPanelOut.bindWithEvent(this));
	},
	
	fadeDiv: function(div, isFadeIn) {
		fade = new Fx.Style(div, 'opacity', {duration: 400, transition: Fx.Transitions.quartInOut});
		if (isFadeIn) fade.start(0,1);
		else fade.start(1,0);
	},
	
	showDataPanel: function() {
		this.isDataPanelVisible = true
		
		// Los paro por si estaban corriendo
		this.fadeFacts.stop();
		this.fadeDataPanel.stop();
		
		this.fadeFacts.start(1,0);
		this.fadeDataPanel.start(0,1);
	},
	
	hideDataPanel: function() {
		this.isDataPanelVisible = false;
		this.factsDiv.setStyle('display', '');
		
		// Lo paro por si estaba corriendo
		this.fadeFacts.stop();
		this.fadeDataPanel.stop();
		
		this.fadeFacts.start(0,1);
		this.fadeDataPanel.start(1,0);
	}
	
});
*/

window.addEvent('domready', function() {
	var ffdivs = getFlashingFactsDivs();
	var f = new FlashingList(ffdivs);
	//new Popego.WidgetContent($E('body'));
});

// For debugging only: Shows an alert dialog with all object properties
function debug(obj) {
	var s = '';
	for (i in obj) {
		s += i + ': ' + obj[i] + '\n';
	}
	alert(s);
}