if (typeof(Popego) == 'undefined') Popego = {};

Popego.Widgets = new Class({
	
	URL_WIDGET: '/${USER}/api/onsitewidget/1',
	URL_EMBED: '${BASE_URL}/${USER}/api/widget/1',
	
	initialize: function(el) {
		this.contentDiv = el;
		this.canvas = this.contentDiv.getElement('.canvas')[0];
		this.paletteDiv = this.contentDiv.getElement('.palette')[0];
		this.embedTextArea = $$('textarea');
		this.selectedColorLi = this.paletteDiv.getElement('.picked_color');
		this.form = $('widget_settings');
		
		Popego.Env.widgetTheme = this.WIDGET_COLOR;
		
		//Refactorear cuando haya varias instancias
		this.widget = null;
		this.widgetKey = "preview";
		this.widgetUser = Popego.Env.username;
		this.widgetDisplayname = Popego.Env.displayname;
		this.widgetTheme = this.selectedColorLi.getFirst().className.split('x')[1];
		this.widgetType = "default";
		
		this.setBehaviors();
		this.showEmbedCode();
		this.previewWidget(this.canvas);
	},
	
	setBehaviors: function() {
		var colors = this.paletteDiv.getElements('a');
		var changeWidgetColor = function(e) {
			if(this.selectedColorLi)
				this.selectedColorLi.className = '';
			this.selectedColorLi = e.target.getParent();
			this.selectedColorLi.className = 'picked_color';
			this.widgetTheme = e.target.className.split('x')[1];
			this.form.getFirst().setProperty("value", this.widgetTheme);
			
			this.showEmbedCode();
			this.previewWidget();
			
			e.stop();
			return false;
		}
		colors.each(function(color) {
			color.addEvent('click', changeWidgetColor.bindWithEvent(this));
		}.bind(this));
		
		var embedCodeFocus = function(e) { e.target.select(); }
		this.embedTextArea.addEvent('focus', embedCodeFocus.bindWithEvent(this));
		this.embedTextArea.addEvent('click', embedCodeFocus.bindWithEvent(this));
		
		var embedCodeKeyDown = function(e) { e.stop();}
		this.embedTextArea.addEvent('keydown', embedCodeKeyDown.bindWithEvent(this));
		
		//TODO: No se esta considerando que haya muchos widgets en pantalla
		var spinner = $ES('img', this.form).getLast();
		var msgPanel = $E('.messages', this.form);
		this.form.addEvent('submit', function (e) {
			if (spinner)
				spinner.setStyle('display', 'inline');
			this.send({
				onComplete: function () {
					if (spinner) spinner.setStyle('display', 'none');
					var t = this.response.text;
					var r = Json.evaluate(t);
					msgPanel.setText(r.statusText);
				},
				onFailure: function () {
					if (spinner) spinner.setStyle('display', 'none');
					msg = 'Failed to submit changes. Check you Internet connection.';
					msgPanel.setText(msg);
				}
			});
			e.stop();
			return false;
		}.bindWithEvent(this.form));

	},
	
	showEmbedCode: function() {
		//TODO: Agregar parametros para tamanio y color
		var scriptTag = '<script type="text/javascript" src="' + this.URL_EMBED.replace("${USER}", 
                        Popego.Env.username).replace("${BASE_URL}", Popego.Env.baseUrl)  +'"></script>'
		this.embedTextArea.setText(scriptTag);
	},
	
	previewWidget: function(canvas) {
		canvas = canvas || this.canvas;
		
		if (!$defined(this.widget)) {
			var wAjax = new Ajax(this.URL_WIDGET.replace("${USER}", Popego.Env.username) + '?theme=' + this.widgetTheme, {update: canvas});
			var initWidget = function() {
				this.widget = Popego.createWidget({key: this.widgetKey, user:this.widgetUser, theme:"t"+this.widgetTheme,
												  type:this.type, id:1, displayname:this.widgetDisplayname});
			}
			wAjax.addEvent('onComplete', initWidget.bind(this));
			wAjax.request();
		} else {
			this.widget.setTheme("t" + this.widgetTheme);
		}
	}
	
});

window.addEvent('domready', function() {
	var w = new Popego.Widgets($ES('.content'));
});
