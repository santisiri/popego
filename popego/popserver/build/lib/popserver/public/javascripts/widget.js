/* POPEGO WIDGET JAVASCRIPT */
if (typeof Popego == "undefined") Popego = {};
if (typeof Popego.Env == "undefined") Popego.Env = {'username':'', 'baseUrl':'', 'instanceId':''};

/* Popego: Widget */
Popego.Widget = new Class({
	initialize: function(el) {
	    this.widgetDiv = el;
		this.lastMessageId = '';
		this.focusInvalidate = false; //Porque el foco salta varias veces
		
		//color theme del widget
		this.currentTheme = Popego.Env.widgetTheme;
		
		//Event handlers
		this.onWindowFocusHandler = undefined;
		this.setBehaviors();
		
	    // PopCard asociado
	    this.popCard = new Popego.PopCard(this);
	},
	// abrir el popcard - delega a PopCard.open();
	openPopCard: function() {
	    this.popCard.open();
	},
	
	parseMessage: function(msg) {
		if (msg == 'OpenPopcard') {
			this.clearLocation();
			this.openPopCard();
		}
	},
	
	clearLocation: function() {
		window.location.hash = '#Popego';
	},
	
	setBehaviors: function() {
		this.onWindowFocusHandler = function(e) {
			if (!this.focusInvalidate) {
				this.focusInvalidate = true;
				
				var hash = window.location.hash.split('#')[1]
				if (hash) {
					var msg = hash.split('_')[0]
					var id = hash.split('_')[1]
					if ((typeof Popego.Env.instanceId == "undefined" || id == Popego.Env.instanceId) && hash != undefined && hash != this.lastMessageId) {
						this.lastMessageId = hash;
						this.parseMessage(msg);
					}
				}
				this.focusInvalidate = false;
			}
		}.bind(this);
		this.onWindowFocusHandler.periodical(500);
		//window.addEvent('focus', this.onWindowFocusHandler);
	},
	
	setTheme: function(theme) {
		Popego.Env.widgetTheme = theme;
		this.currentTheme = Popego.Env.widgetTheme;
		this.popCard.currentTheme = Popego.Env.widgetTheme;
		this.popCard.reload();
	},
	
	clean: function() {
		window.removeEvent('focus', this.onWindowFocusHandler);
	}
});

Popego.PopCard = new Class({
	initialize: function(parentWidget) {
	    // el widget asociado
	    this.parentWidget = parentWidget;
	    // div contenedor del popcard
	    this.popCardDiv = new Element('div', { 'id': 'popcard', 'class': 'dialog', 'styles': { 'visibility': 'hidden', 'height': 0 } });
	    this.popCardDiv.injectInside($$('body')[0]);
	    // estado abierto/cerrado del popcard
	    this.isOpen = false;
	    // ya inserte el contenido del PopCardDiv?
	    this.isFilled = false;
		// el color actual del widget (si se cambia necesariamente tengo que hacer un reload de la popcard)
		this.currentTheme = parentWidget.currentTheme;
	},

	// abrir el popcard
	open: function() {
	    if (this.isOpen) return;
		
	    if (!this.isFilled) {
		    this.fillPopCardDiv();
			this.popCardDiv.getElement('.cmd_close').addEvent('click', this.close.bind(this));
			
			//sets button bar behavior
			var buttons = this.popCardDiv.getElement('.button_bar').getElements('span');
			buttons.each(function(button) {
				button.addEvent('click', this.onButtonBarClick.bindWithEvent(this, button));
				if (button.className == 'menu_button_selected')
					this.buttonSelected = button
			}.bind(this)); 
			this.iframe = this.popCardDiv.getElement('iframe');
			
			//hago el widget draggable
			new Drag.Move(this.popCardDiv);
			
	    }
		
	    // restore height
	    this.popCardDiv.setStyle('height', Popego.PopCard.Defaults.height)
		
	    var popCardCoord = this.popCardDiv.getCoordinates();
	    var popCardTop   = (Window.getHeight() - popCardCoord.height) / 2 + Window.getScrollTop();
	    var popCardLeft  = (Window.getWidth() - popCardCoord.width) / 2 + Window.getScrollLeft();
		
	    this.popCardDiv.setStyles({ 'top': popCardTop, 'left': popCardLeft - (window.ie?20:0) });
		this.popCardDiv.setStyle('visibility', 'visible');
	},
	// cerrar
	close: function() {
	    this.popCardDiv.setStyle('visibility', 'hidden');
	},
	
	// recarga el iframe
	reload: function() {
		if (this.isFilled)
			this.iframe.src = this.iframe.src.split('?')[0];
	},

	// 'llenar' el popcarddiv
	fillPopCardDiv: function() {
		var popCardHTML = []; var idx = 0;
		popCardHTML[idx++] = '<!--Card Content -->'
		popCardHTML[idx++] = '<div class="content">';
		popCardHTML[idx++] = '<!-- Card Top -->';
		popCardHTML[idx++] = '<div class="t"></div>';
		popCardHTML[idx++] = '<div class="wrapper_pink">';
		popCardHTML[idx++] = '<div class="menu">';
		popCardHTML[idx++] = '<!-- Dynamic Style: Modified according to user settings -->';
		popCardHTML[idx++] = '<img src="' + Popego.Env.baseUrl + '/images/widget/logo_mini.png" title="' + Popego.Env.username + '\'s Popego" class="pngfix"/>';
		popCardHTML[idx++] = '<span class="button_bar">';
		popCardHTML[idx++] = '<span class="menu_button_selected">home</span>';
		popCardHTML[idx++] = '<span><a href="#">media</a></span>';
		popCardHTML[idx++] = '<span><a href="#">popego</a></span>';
		popCardHTML[idx++] = '</span>';
		popCardHTML[idx++] = '</div>';
		popCardHTML[idx++] = '<div class="cmd_close" title="Close"></div>';
		popCardHTML[idx++] = '<!--Bubble-->';
		popCardHTML[idx++] = '<div class="dialog" id="popbubble">';
		popCardHTML[idx++] = '<!-- Content -->';
		popCardHTML[idx++] = '<div class="content">';
		popCardHTML[idx++] = '<!-- Bubble Top -->';
		popCardHTML[idx++] = '<div class="t"></div>';
		popCardHTML[idx++] = '<div class="wrapper_white">';
		popCardHTML[idx++] = '<iframe src="'+ Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/widget/1/home"  scrolling="no" frameborder="0"></iframe>';
		popCardHTML[idx++] = '</div>';
		popCardHTML[idx++] = '</div>';
		popCardHTML[idx++] = '<!--End of Content-->';
		popCardHTML[idx++] = '<!-- Bubble Bottom -->';
		popCardHTML[idx++] = '<div class="b"><div></div></div>';
		popCardHTML[idx++] = '</div>';
		popCardHTML[idx++] = '<!--End of Bubble-->';
		popCardHTML[idx++] = '</div>';
		popCardHTML[idx++] = '</div>';
		popCardHTML[idx++] = '<!--End of Card Content-->';
		popCardHTML[idx++] = '<!-- Card Bottom -->';
		popCardHTML[idx++] = '<div class="b"><div></div></div>';
		this.popCardDiv.setHTML(popCardHTML.join(''));
		this.isFilled = true;
	},
	
	//Button behavior
	onButtonBarClick: function(e, currentTarget) {
		var sectionsMap = {
			'home'  :'home',
			'media' :'media',
			'popego' :'about'
		};
		
		//var buttonClicked = e.target.tagName == 'A' ? e.target.parentElement : e.target;
		var buttonClicked = currentTarget;
		if (buttonClicked != this.buttonSelected) {
			this.buttonSelected.className = '';
			this.buttonSelected.setHTML('<a href="#">' + this.buttonSelected.getText() + '</a>');
			
			buttonClicked.className = 'menu_button_selected';
			buttonClicked.setText(buttonClicked.getElement('a').getText());
			this.buttonSelected = buttonClicked;
			this.iframe.src = Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/widget/1/' + sectionsMap[buttonClicked.getText()];
		}
		e.stop();
	}

});

Popego.PopCard.Defaults = {
    height: '485px'
}


/* wrapper para console.log : usar para debuggear */ 
var _d = function(msg) { 
    if (!("console" in window) || !("firebug" in console)) return;
    console.log(msg);
}

window.addEvent('domready', function() {
	Popego.widgetInstance = new Popego.Widget($('popego'));
});
