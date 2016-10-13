if (typeof(Popego) == 'undefined') Popego = {};

Popego.Utils = new Class({
	
	initialize: function () {
		// Dialog's Effects
		this.fadeDialog = undefined;
		this.fadeOverlay = undefined;
	},
	
	/*
		Crea una ventana de dialogo con el contenido que le pasan
	*/
	showDialog: function(html, isModal, id) {
		var body = $$('body')[0];
		
		this.hideSelectBoxes();
		this.hideFlash();
		
		var overlayDiv = $('overlay');
		if (!overlayDiv) {
			overlayDiv = new Element('div', {'id': 'overlay'});
			overlayDiv.addEvent('click', function(){ this.hideDialog(id)}.bind(this) );
			overlayDiv.setStyle('opacity', 0);
			overlayDiv.setStyle('height', this.getPageSize()[1]);
			this.fadeOverlay = new Fx.Style(overlayDiv, 'opacity', {duration: 400, transition: Fx.Transitions.quartInOut});
			body.appendChild(overlayDiv);
		} else {
			overlayDiv.setStyle('opacity', 0);
			overlayDiv.setStyle('display', '');
		}
		
		this.fadeOverlay.start(0, 0.6);
		
		var dialogId = 'dialog' + (id?'_'+id:'');
		var dialogDiv = $(dialogId);
		if (!dialogDiv) {
			dialogDiv = new Element('div', {'id': dialogId, 'styles':{'visibility':'hidden'}});
			dialogDiv.setHTML(html);
			dialogDiv.className = 'floating_form';
			dialogDiv.setStyle('opacity', 0);	
			this.fadeDialog = new Fx.Style(dialogDiv, 'opacity', {duration: 100, transition: Fx.Transitions.quartInOut});
			body.appendChild(dialogDiv);
		} else {
			dialogDiv.setStyle('opacity', 0);
			dialogDiv.setStyle('display', '');
		}
		
		var dialogSize = dialogDiv.getCoordinates();
		dialogDiv.setStyle('top', (Window.getHeight() - dialogSize.height) / 2 + Window.getScrollTop());
	    dialogDiv.setStyle('left', (Window.getWidth() - dialogSize.width) / 2 + Window.getScrollLeft());
		if (dialogDiv.getStyle('visibility') == 'hidden') dialogDiv.setStyle('visibility', 'visible');
		
		this.fadeDialog.start(0, 1);
	},
	hideDialog: function(id) {
		this.removeDialog(id);
		return;
		
		var dialogId = 'dialog' + (id?'_'+id:'');
		this.fadeDialog.start(1,0);
		this.fadeOverlay.start(0.6, 0);
		this.showSelectBoxes();
		this.showFlash();
	},
	removeDialog: function(id) {
		var dialogId = 'dialog' + (id?'_'+id:'');
		this.fadeOverlay.stop();
		this.fadeOverlay.start(0.6, 0);
		var d = $(dialogId);
		if (d) d.remove();
		this.showSelectBoxes();
		this.showFlash();
	},
	
	showSelectBoxes: function() {
		var selects = document.getElementsByTagName("select");
		for (i = 0; i != selects.length; i++)
			selects[i].style.visibility = "visible";
	},

	hideSelectBoxes: function() {
		var selects = document.getElementsByTagName("select");
		for (i = 0; i != selects.length; i++)
			selects[i].style.visibility = "hidden";
	},

	showFlash: function() {
		var flashObjects = document.getElementsByTagName("object");
		for (i = 0; i < flashObjects.length; i++)
			flashObjects[i].style.visibility = "visible";
			
		var flashEmbeds = document.getElementsByTagName("embed");
		for (i = 0; i < flashEmbeds.length; i++)
			flashEmbeds[i].style.visibility = "visible";
	},

	hideFlash: function() {
		var flashObjects = document.getElementsByTagName("object");
		for (i = 0; i < flashObjects.length; i++)
			flashObjects[i].style.visibility = "hidden";
			
		var flashEmbeds = document.getElementsByTagName("embed");
		for (i = 0; i < flashEmbeds.length; i++)
			flashEmbeds[i].style.visibility = "hidden";
	},
	
	/*
		TODO: Chequear esto y usar mootools
		Returns array with page width, height and window width, height
		Core code from - quirksmode.com
		Edit for Firefox by pHaez
	*/
	getPageSize: function() {
	
		var xScroll, yScroll;
		
		if (window.innerHeight && window.scrollMaxY) {	
			xScroll = window.innerWidth + window.scrollMaxX;
			yScroll = window.innerHeight + window.scrollMaxY;
		} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
			xScroll = document.body.scrollWidth;
			yScroll = document.body.scrollHeight;
		} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
			xScroll = document.body.offsetWidth;
			yScroll = document.body.offsetHeight;
		}
		
		var windowWidth, windowHeight;
		
		if (self.innerHeight) {	// all except Explorer
			if(document.documentElement.clientWidth){
				windowWidth = document.documentElement.clientWidth; 
			} else {
				windowWidth = self.innerWidth;
			}
			windowHeight = self.innerHeight;
		} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
			windowWidth = document.documentElement.clientWidth;
			windowHeight = document.documentElement.clientHeight;
		} else if (document.body) { // other Explorers
			windowWidth = document.body.clientWidth;
			windowHeight = document.body.clientHeight;
		}	
		
		// for small pages with total height less then height of the viewport
		if(yScroll < windowHeight){
			pageHeight = windowHeight;
		} else { 
			pageHeight = yScroll;
		}
		
		// for small pages with total width less then width of the viewport
		if(xScroll < windowWidth){	
			pageWidth = xScroll;		
		} else {
			pageWidth = windowWidth;
		}

		arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight) 
		return arrayPageSize;
	},

	
	/*
		Permite el uso de PNG con transparencias en IE 5.5+ usando un filtro propietario de MS
		Correctly handle PNG transparency in Win IE 5.5 & 6.
		http://homepage.ntlworld.com/bobosola. Updated 18-Jan-2006.
	*/
	fixPng: function() {
		var arVersion = navigator.appVersion.split("MSIE")
		var version = parseFloat(arVersion[1])
		
		if ((version >= 5.5) && (document.body.filters)) {
			for(var i=0; i<document.images.length; i++) {
				var img = document.images[i]
				var imgName = img.src.toUpperCase()
				if (imgName.substring(imgName.length-3, imgName.length) == "PNG") {
					var imgID = (img.id) ? "id='" + img.id + "' " : ""
					var imgClass = (img.className) ? "class='" + img.className + "' " : ""
					var imgTitle = (img.title) ? "title='" + img.title + "' " : "title='" + img.alt + "' "
					var imgStyle = "display:inline-block;" + img.style.cssText 
					if (img.align == "left") imgStyle = "float:left;" + imgStyle
					if (img.align == "right") imgStyle = "float:right;" + imgStyle
					if (img.parentElement.href) imgStyle = "cursor:hand;" + imgStyle
					var strNewHTML = "<span " + imgID + imgClass + imgTitle
					+ " style=\"" + "width:" + img.width + "px; height:" + img.height + "px;" + imgStyle + ";"
					+ "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader"
					+ "(src=\'" + img.src + "\', sizingMethod='scale');\"></span>" 
					img.outerHTML = strNewHTML
					i = i-1
				}
			}
		}
	}

});

Popego.TextInputCleaner = new Class({

	initialize: function () {
		var u = this;
		$$('input').each(function (el) {
			var type = el.getProperty('type');
			if (!(['text', 'password'].contains(type)))
				return;
			el.addEvent('focus', u.clearInputText.bindWithEvent(el));
			el.addEvent('blur', u.restoreInputText.bindWithEvent(el));
			// TODO: revisar por que falla fireEvent
			// TODO: el color podria ser un parametro
			if (el.value)
				el.setStyle('color', '#CCCCCC');
		});
	},

	clearInputText: function(e) {
		inputField = e.target;
		if(!inputField._hasChanged) {
			inputField._originalValue = inputField.value;
			inputField.value = '';
			inputField.setStyle('color', '');
		}
		inputField._hasChanged = true;
		e.stop();
		return false;
	},
	
	restoreInputText: function(e) {
		inputField = e.target;
		if (inputField._hasChanged && inputField.value == '') {
			inputField.value = $pick(inputField._originalValue, '');
			inputField._hasChanged = false;
			inputField.setStyle('color', '#CCCCCC');
		}
		e.stop();
		return false;
	}
});

// utils
Popego.Utils = new Popego.Utils();

// image preloading
new Asset.images([
		'/images/website/close_white_hover.png',
		'/images/website/signup_button_hover.png',
		'/images/website/signup_button_small.png'
	]);

// text input cleaner (for login and alpha signup only)
window.addEvent('domready', function () {
	if ($E('.login_form') || $('alpha_signup'))
		new Popego.TextInputCleaner();
});

