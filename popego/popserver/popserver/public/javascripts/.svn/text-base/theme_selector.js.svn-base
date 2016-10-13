// theme_selector.js

if (typeof(Popego) == 'undefined') Popego = {};

Popego.ThemeSelector = new Class({
	
	// Se podrian pasar como parametros:
	// '.palette' (selector para ancestro de los Elements de tag 'li')
	// 'picked_color'/'' (classes de color seleccionado/sin seleccionar)
	
	// Se asume que todos los Elements de tag 'li' seleccionados
	// son los que forman la paleta y cada uno tiene dentro un anchor
	// con el URL en su href donde hacer el request por Json para el
	// cambio de theme.
	
	initialize: function () {
	try {
		var lis = $ES('li', '.palette');
		lis.each(function (li) {
			var anchor = li.getFirst();
			var f = this.onThemeSelected.bindWithEvent(anchor);
			anchor.addEvent('click', f);
			li.addEvent('click', f);
		}.bind(this));
	} catch (e) {
		// alert(debug(e));
	}
	},

	onThemeSelected: function (e) {
	try {
		var a = e.target;
		var li = a.getParent();
		if (li.getTag() != 'li') {
			li = a;
			a = li.getFirst();
		}
		var lis = $ES('li', li.getParent());
		lis.each(function (i) {
			i.setProperty('class', '');
		});
		var f = function (theme) {
			var link = $E('link', document.body);
			if (link) link.remove();
			var link = new Element('link', {
				href: '/css/themes/' + theme + '.css',
				rel: 'stylesheet',
				type: 'text/css'
			});
			link.injectTop(document.body);
			li.setProperty('class', 'picked_color');
		}
		var r = new Json.Remote(a.getProperty('href'));
		r.addEvent('onComplete', f);
		r.send();
		e.stop();
		return false;
	} catch (e) {
		// alert(debug(e));
	}
	}

});

