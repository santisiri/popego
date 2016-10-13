// flashing_facts.js
if (window.ActiveXObject) window.ie = true;

// For debugging only: Shows an alert dialog with all object properties
function debug(obj) {
	var s = '';
	for (i in obj) {
		s += i + ': ' + obj[i] + '\n';
	}
	alert(s);
}
// Sets HTML element opacity to a value ranging from 0 to 100
function setOpacity(obj, value) {
	if (!obj || !obj.style) return;
	obj.style.background = "#FF3366"; //otherwise ie adds an annoying shadow on text
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
// Traditional event registering
window.onload = function () {
	try {
		var ffdivs = getFlashingFactsDivs();
		var f = new FlashingList(ffdivs);
	} catch (e) {
		alert(e.message); // TODO
	}
}
