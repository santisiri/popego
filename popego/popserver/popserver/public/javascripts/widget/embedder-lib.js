/*
Script: popego-context.js
	Contains <Popego.Context>
*/

/*
Class: Popego.Context
	Contiene:
	- datos de donde esta corriendo el widget (Ej. tipo de browser, browser mode)
	- funciones para obtener dimensiones del document (width, height, scroll)
	- funciones para escuchar y remover listeners de eventos
	- agrega un prototype a Function para manipular el this (bind)

Notes:
	Requiere de <Popego>
	
Properties:
	- browser ('opera', 'ie6', 'ie7', 'webkit420', 'webkit419', 'gecko')
	- browserMode ('strict', 'quirks')
	
Functions:
	- getWidth()
	- getHeight()
	- getScrollWidth()
	- getScrollHeight()
	- getScrollLeft()
	- getScrollTop()
	- addEvent()
	- removeEvent()
	
*/
if (typeof(Popego.Context) == "undefined") {
	Popego.Context = {};
	
	//Browser detection basado en Mootools
	if (window.opera) Popego.Context.browser = "opera"
	else if (window.ActiveXObject) Popego.Context.browser = window.XMLHttpRequest ? "ie7" : "ie6";
	else if (document.childNodes && !document.all && !navigator.taintEnabled) Popego.Context.browser = window.xpath ? "webkit420" : "webkit419";
	else if (document.getBoxObjectFor != null) Popego.Context.browser = "gecko";
	
	Popego.Context.browserMode = document.compatMode && document.compatMode == "CSS1Compat" ? "strict" : "quirks";
	
	//Window size basado en Mootools
	Popego.Context.getWidth = function(){
		if (Popego.Context.browser == "webkit419") return window.innerWidth;
		if (Popego.Context.browser == "opera") return document.body.clientWidth;
		return document.documentElement.clientWidth;
	};
	Popego.Context.getHeight = function(){
		if (Popego.Context.browser == "webkit419") return this.innerHeight;
		if (Popego.Context.browser == "opera") return document.body.clientHeight;
		return document.documentElement.clientHeight;
	};
	Popego.Context.getScrollWidth = function(){
		if ((/ie6|ie7/).test(Popego.Context.browser)) return Math.max(document.documentElement.offsetWidth, document.documentElement.scrollWidth);
		if ((/webkit419|webkit420/).test(Popego.Context.browser)) return document.body.scrollWidth;
		return document.documentElement.scrollWidth;
	};
	Popego.Context.getScrollHeight = function(){
		if ((/ie6|ie7/).test(Popego.Context.browser)) return Math.max(document.documentElement.offsetHeight, document.documentElement.scrollHeight);
		if ((/webkit419|webkit420/).test(Popego.Context.browser)) return document.body.scrollHeight;
		return document.documentElement.scrollHeight;
	};
	Popego.Context.getScrollLeft = function(){
		return this.pageXOffset || document.documentElement.scrollLeft;
	};
	Popego.Context.getScrollTop = function(){
		return this.pageYOffset || document.documentElement.scrollTop;
	};
	
	//Event listening functions
	Popego.Context.addEvent = function ( obj, type, fn ) {
		if (obj.addEventListener) {
			obj.addEventListener(type, fn, false);
		} else if (obj.attachEvent)	{
			obj["e"+type+fn] = fn;
			obj[type+fn] = function() {
				obj["e"+type+fn]( window.event );
			}
			obj.attachEvent("on"+type, obj[type+fn]);
		}
	};

	Popego.Context.removeEvent = function(obj, type, fn) {
		if (obj.removeEventListener) {
			obj.removeEventListener(type, fn, false);
		} else if (obj.detachEvent) {
			obj.detachEvent( "on"+type, obj[type+fn] );
			obj[type+fn] = null;
			obj["e"+type+fn] = null;
		}
	};
	
	// bind basado en Prototype framework
	Function.prototype.bind = function(obj) {
		var method = this, temp = function() {
			return method.apply(obj, arguments);
		 };
		return temp;
	}
}/*
Script: popego-utilsext.js
	Contains <Popego.UtilsExt>
*/

/*
Class: Popego.UtilsExt
	Contiene:
	- funciones para aplicar estilos inline pudiendo distinguir por browser
	- remplazo de keywords (ej. ${ASSET:widget_background} a http://xxx/images/w_bkg.png)

Notes:
	Requiere de <Popego>, <Popego.Context>, <Popego.Config>
	
Functions:
	- applyStyles()
	- applyIEStyles()
	- styleToInline()
	- keywordReplace()
	
*/
if (typeof(Popego.UtilsExt) == "undefined") {
	Popego.UtilsExt = {};
	
	/*
	Function: applyStyles
		Aplica estilos al elemento o html text suministrado segun el className.
		- Si h es un elemento setea los attr de style,
		- sino agrega "style='...'" al html text.
	
	Arguments:
		h - el htmlText o un DOM element
		styles - dict de estilos > {className1:{prop1:value, prop2:value, ...}
		theme - si se aplica algun theme (para aplicarlo el dict de estilos debe tenes un theme de estilos en la prop 'themes')
		
	Example:
		>Popego.UtilsExt.applyStyles('<div class=""/>', {className1:{prop1:value, prop2:value, ...}, className2:...}, "t993366")
	*/
	Popego.UtilsExt.applyStyles = function(h, styles, theme) {
		//Si me pasan el 'innerHTML' parseo el texto y le agrego style=''
		if (typeof(h) == "string") {
			var i; //index of 'class'
			var t = ''; //temp html
			
			while ((i = h.indexOf("class='")) != -1) {
				t += h.substring(0,i);
				h = h.substr(i+7);
				var x = h.indexOf("'");
				var c = h.substring(0,x); //class names
				h = h.substr(x+1);
				
				c = c.split(' ');
				var n = c.length;
				for (var i=0; i<n; i++) {
					t+= "style='" + Popego.UtilsExt.styleToInline(styles[c[i]], theme);
					if (styles.themes[theme])
						t+= Popego.UtilsExt.styleToInline(styles.themes[theme][c[i]], theme);
				}
				// ie styles
				if ((/ie6|ie7/).test(Popego.Context.browser)) {
					t += Popego.UtilsExt.applyIEStyles(null, styles, theme, c);
				}
				
				t += "'";
			};
			return t+h;
		}
		//Sino, me pasaron un elemento y se lo agrego al el.style.[prop]
		else if (typeof(h) == "object") {
			var c = h.className.split(' ');
			var n = c.length;
			for (var i=0; i<n; i++) {
				var style = styles[c[i]];
				for (var prop in style) {
					h.style[prop] = Popego.UtilsExt.keywordReplace(style[prop], {"theme":theme});
				}
				
				//agrego style del theme (si tiene)
				if (styles.themes[theme]) {
					style = styles.themes[theme][c[i]];
					for (var prop in style) {
						h.style[prop] = Popego.UtilsExt.keywordReplace(style[prop], {"theme":theme});
					}
				}
			}
			
			// styles para ie
			if ((/ie6|ie7/).test(Popego.Context.browser)) {
				Popego.UtilsExt.applyIEStyles(h, styles, theme, c);
			}
		}
		return h;
	};
	
	/*
	Function: applyIEStyles
		Aplica estilos para IE
			- Si h es un elemento setea los attr de style,
			- Si h es un string (html text) agrega "style='...'" al html text.
			- Sino devuelve un string con los attr. Ej: "border:none;width:20px"
	
	Notes:
		Requiere de <Popego.Context>
		Lo que hace es al className le agrega '_ie' e '_i6' o '_ie7' y busca esos estilos dentro de styles
		
		
	Arguments:
		h - el htmlText, un DOM element o null
		styles - dict de estilos > {className1:{prop1:value, prop2:value, ...}
		theme - si se aplica algun theme (para aplicarlo el dict de estilos debe tenes un theme de estilos en la prop 'themes')
		classes - array, con el name de las classes css a aplicar
		
	Example:
		>style = Popego.UtilsExt.applyIEStyles(null, {className1:{prop1:value, prop2:value, ...}, className2:...}, "t993366", ["widget", "iframe"])
	*/
	Popego.UtilsExt.applyIEStyles = function(h, styles, theme, classes) {
		//TODO: No esta armado para cuando h es un html text
		
		if ((/ie6|ie7/).test(Popego.Context.browser)) {
			//styles para 6 y 7 :: className_ie
			//styles para 6 :: className_ie6
			//styles para 7 :: className_ie7
			var version = ["_ie", "_" + Popego.Context.browser]; 
			
			var n = classes.length;
			var l = version.length;
			if (!h) {
				var result = "";
				for (var i=0; i<n; i++) {
					for (var j=0; j<l; j++) {
						if ((style = styles[classes[i] + version[j]])) {
							result += Popego.UtilsExt.styleToInline(style, theme);
						}
						if ((style = (styles.themes[theme]) ? styles.themes[theme][classes[i] + version[j]] : undefined)) {
							result += Popego.UtilsExt.styleToInline(style, theme);
						}
					}
				}
				return result;
			} else if (typeof(h) == "object") {
				for (var i=0; i<n; i++) {
					for (var j=0; j<l; j++) {
						if ((style = styles[classes[i] + version[j]])) {
							for (var prop in style) {
								h.style[prop] = Popego.UtilsExt.keywordReplace(style[prop], {"theme":theme});
							}
						}
							
						if ((style = (styles.themes[theme]) ? styles.themes[theme][classes[i] + version[j]] : undefined)) {
							for (var prop in style) {
								h.style[prop] = Popego.UtilsExt.keywordReplace(style[prop], {"theme":theme});
							}
						}
					}
				}
			}
		}
	};
	
	/*
	Function: styleToInline
		Devuelve un string con las propeidades del estilo separadas por ;
		Si el valor de la propiedad es un keyword lo reemplaza por el valor apropiado.
			
	Arguments:
		style - dict {prop1:value, prop2:value, ... }, el estilo
		theme - si se aplica, algun theme
		
	Example:
		>styleText = Popego.UtilsExt.styleToInline({prop1:value, prop2:value, ... }, "t993366")
	*/
	Popego.UtilsExt.styleToInline = function(style, theme) {
		var result = "";
		for (prop in style) {
			result += prop + ":" + Popego.UtilsExt.keywordReplace(style[prop], {"theme":theme}) + ";"
		}
		return result;
	};
	
	/*
	Function: keywordReplace
		Reemplaza por el recurso indicado dentro de ${} y devuelve el nuevo string
		Si no hay nada para reemplazar devuelve lo mismo que se paso

	Notes:
		Requiere de <Popego.Config>
		
	Arguments:
		str - el string que contiene lo que se quiere reemplazar
		options - dict
		
	Example:
		>replacedText = Popego.UtilsExt.keywordReplace("${ASSET:widget_background}, {theme:"t993366"})
	*/
	Popego.UtilsExt.keywordReplace = function(str, options) {
		var result = str;
		if ((i = str.indexOf("${")) != -1) {
			//por ahora solo espero ASSET:value
			var j = str.indexOf("}");
			var asset = str.substring(i+2, j);
			asset = asset.split(":");
			result = str.substring(0, i) + Popego.Config.getAsset(asset[1], options.theme) + str.substr(j+1);
		}
		return result;
	};
}/*
Script: popego-widgetmanager.js
	Contains <Popego.WidgetManager>
*/

/*
Class: Popego.WidgetManager
	Es un widget manager. (cuack:)
	Contiene el html del widget y los estilos.
	
	//TODO: habria que ver cuando tengo diferentes tipos de widget

Notes:
	Requiere de <Popego>, <Popego.Config>, <Popego.PopcardManager>
	
Properties:
	- htmlText, el html del widget
	- styles, dict de estilos (a su vez este tiene en la prop 'themes' un dict de themes)
	
Functions:
	- create()
	
*/
if (typeof(Popego.WidgetManager) == "undefined") {
	Popego.WidgetManager = {
		htmlText: "<div id='popego' class='widget'><iframe class='widget_iframe' src='" + Popego.Config.baseURL + "/${USERNAME}/api/widget/${ID}/content' scrolling='no' frameborder='0'></iframe></div>",
		styles: {
			widget: {
				"background":"url(${ASSET:widget_background}) 50% 50% no-repeat",
				"font-size":"13px",
				"font-family":"Arial, Tahoma, sans-serif",
				"text-align":"left",
				"color":"#fff",
				"width":"150px",
				"height":"240px",
				"padding":"9px",
				"zIndex":"9998"
			},
			widget_ie: {
				"width":"162px",
				"height":"250px",
				"padding": "6px",
				"padding-top": "4px"
			},
			widget_ie6: {
				"margin": "4px",
				"padding": "0px",
				"background": "none",
				"filter": "progid:DXImageTransform.Microsoft.AlphaImageLoader(src=\"${ASSET:widget_background}\",sizingMethod=\"scale\")"
			},
			widget_iframe: {
				"position":"absolute",
                "border":"0",
				"width":"150px",
				"height":"240px",
				"zIndex":"9995",
				"clear":"both"
			},
			widget_iframe_ie6: {
				"margin":"5px"
			},
			widget_iframe_ie7: {
				"margin":"7px"
			},
			wrapper: {
				"position":"absolute",
				"width":"159px",
				"height":"248px",
				"margin":"4px",
				"zIndex":"9999",
				"cursor":"pointer"
			},
			wrapper_ie6: {
				"background": "white",
				"filter": "alpha(opacity=1)"
			},
			wrapper_ie7: {
				"margin-left": "7px"
			},
			themes: {
				//theme: {cssClass:{properties}, cssClass2:{properties}, etc}
				"tff3366": {},
				"tff900a": {}
			}
		},
		create: function(key, user, theme, type, id, displayname){
			return {
				key: key,
				user: user,
				displayname: displayname,
				theme: theme,
				type: type,
                id: id,
				wr: undefined,
				
				initialize: function() {
					//levanto el container
					this.container = document.getElementById("pe_container_" + this.key);
					
					//creo la popcard para este widget
					Popego.popcards[this.key] = Popego.PopcardManager.create(this.key, this.user, this.theme, this.type, this.id, this.displayname);
					
					//wrapper para el click
					this.wr = document.createElement("div");
					this.wr.id = "pe_wr_" + this.key;
					this.wr.className = "wrapper";
					Popego.UtilsExt.applyStyles(this.wr, Popego.WidgetManager.styles, this.theme);
					
					var key = this.key;
					this.wr.onclick = function(e) {
						Popego.popcards[key].open();
					}
					
					this.container.appendChild(this.wr);
					
					
					//imprimo el widget
					this.container.appendChild(this._createWidgetDiv());
				},
				
				_createWidgetDiv: function(theme) {
					var tmpDiv = document.createElement("div");
					var html = Popego.WidgetManager.htmlText.replace("${USERNAME}", this.user).replace("${ID}", this.id);
					if (theme) html = html.replace("/content", "/content?theme=" + theme.substr(1));
					tmpDiv.innerHTML = Popego.UtilsExt.applyStyles(html, Popego.WidgetManager.styles, this.theme);
					
					return tmpDiv.childNodes[0];
				},
				
				setTheme: function(theme, persist) {
					//TODO: hacer que se persista
					this.theme = theme;
					this.container.removeChild(this.container.childNodes[1]);
					this.container.appendChild(this._createWidgetDiv(this.theme));
					Popego.popcards[this.key].setTheme(this.theme);
				}
			}
		}
	};
}
/*
Script: popego-popcardmanager.js
	Contains <Popego.PopcardManager>
*/

/*
Class: Popego.PopcardManager
	Es un popcard manager (cuack:)
	Contiene el html del widget y los estilos.
	
	//TODO: habria que ver cuando tengo diferentes tipos de widget

Notes:
	Requiere de <Popego>, <Popego.Config>, <Popego.UtilsExt>
	
Properties:
	- htmlText, el html del contenido de la popcard no el frame (este ultimo se hace con createElement)
	- initDepth, el z-index en donde se empiezan a ubicar las popcards
	- maxDepth, el maximo z-index de una popcard
	- styles, dict de estilos (a su vez este tiene en la prop 'themes' un dict de themes)
	
Functions:
	- getNextHighestDepth()
	- sendToFront()
	- create()
*/
if (typeof(Popego.PopcardManager) == "undefined") {
	Popego.PopcardManager = {
		htmlText: "<iframe scrolling='no' frameborder='no' src='" + Popego.Config.baseURL + "/${USERNAME}/api/widget/1/home' class='popcard_iframe'></iframe>",
		initDepth: 15000, //el z-index de donde arrancan las popcards
		maxDepth: 16000,  //el z-index maximo
		
		/*
		Function: getNextHighestDepth
			Devuelve el proximo z-index disponible
		*/
		getNextHighestDepth: function() {
			//me recuerda a actionscript :P
			var len = 0;
			for (var p in Popego.popcards)
				len++;
			return this.initDepth + len + 1
		},
		
		/*
		Function: sendToFront
			Asigna el z-index mas alto a la popcard que le pasan.
				
		Arguments:
			popcard - la instancia de la popcard
			
		Example:
			>Popego.PopcardManager.sendToFront(Popego.popcards["132690421"])
		*/
		sendToFront: function(popcard) {
			popcard.setDepth(this.maxDepth++);
		},
		
		styles: {
			popcard: {
				"position": "absolute",
				"background":"url(${ASSET:popcard_background}) 50% 50% no-repeat",
				"width":"460px",
				"height":"510px",
				"color":"#fff",
				"padding":"0",
				"margin":"0",
				"display":"block"
			},
			popcard_ie6: {
				"background": "none",
				"filter": "progid:DXImageTransform.Microsoft.AlphaImageLoader(src=\"${ASSET:popcard_background}\",sizingMethod=\"scale\")"
			},
			popcard_iframe: {
				"border":"1px solid red",
				"position":"absolute",
				"border":"0",
				"width":"415px",
				"height":"440px",
				"top":"53px",
				"left":"22px",
				"zIndex":"9999",
				"clear":"both"
			},
			
			themes: {
				//theme: {cssClass:{properties}, cssClass2:{properties}, etc}
				"tff3366": {},
				"tff900a": {}
			}
		},
			
		create: function(key, user, theme, type, id, displayname) {
			return {
				key: key,
				user: user,
				displayname: displayname,
				theme: theme,
				type: type,
				id: id,
				
				container: undefined,
				
				depth: Popego.PopcardManager.getNextHighestDepth(), //el z-index de la popcard
				
				isHidden: true,
				isFreezed: false,
				isDragging: false,
				
				freezeCoords: {
					beforeTop: 0,	//el top relativo al documento justo antes de freezarlo
					beforeLeft: 0,  //el left relativo al documento justo antes de freezarlo 
					scrollTop: 0,	//el top del scroll justo antes de freezarlo 
					scrollLeft: 0   //el left del scroll justo antes de freezarlo 
				},
				
				open: function() {
					if (typeof(this.container) == "undefined") {
						var popId = "popcard_" + this.key;
						this.container = document.createElement("div");
						this.container.setAttribute("id", popId);
						this.container.className = "popcard";
						Popego.UtilsExt.applyStyles(this.container, Popego.PopcardManager.styles, this.theme);
						
						this.container.style.visibility = "hidden";
						this.container.style.zIndex = this.depth;
						
						var html = Popego.PopcardManager.htmlText.replace("${USERNAME}", this.user);
						this.container.innerHTML = Popego.UtilsExt.applyStyles(html, Popego.PopcardManager.styles, this.theme);
						document.getElementsByTagName("body")[0].appendChild(this.container);

 						//
 						var div = document.createElement('div');
 						var idle = '/images/widget/button_close_idle.png';
 						idle = Popego.Config.getAssetsURL(idle) + idle;
 						var over = '/images/widget/button_close_over.png';
 						over = Popego.Config.getAssetsURL(over) + over;
 						var s = {
 							backgroundImage: 'url('+idle+')',
 							backgroundRepeat: 'no-repeat',
 							cssFloat:'right',
 							height:'24px',
 							margin:'10px 15px 0 0',
 							position:'relative',
 							width:'24px',
 							cursor:'pointer',
 							zIndex:'9999'
 						};
 						div.setAttribute('title', 'Close');
 						div.className = 'popcard_close cmd_close';
 						Popego.UtilsExt.applyStyles(div, {popcard_close: s, themes:{}}, this.theme);
 						div.setAttribute('onmouseout', 'this.style.backgroundImage = \'url('+idle+')\';');
 						div.setAttribute('onmouseover', 'this.style.backgroundImage = \'url('+over+')\';');
 						div._popcard = this; // TODO: preguntar a vic si hay mejor forma de acceder al hide de la popcard en en onclick
 						div.setAttribute('onclick', 'if (this._popcard) this._popcard.hide();');
 						this.container.appendChild(div);
 
 						//
 						var div = document.createElement('div');
 						var icon = '/images/widget/encounter_open_idle.png';
 						icon = Popego.Config.getAssetsURL(icon) + icon;
 						var s = {
 							background: 'transparent no-repeat url('+icon+') 0 3px',
 							cssFloat:'left',
 							//width:'300px',
 							height:'24px',
 							margin:'13px 0 0 18px',
 							paddingLeft: '20px',
 							position:'relative',
 							zIndex:'9998'
 						};
 						div.className = 'popcard_title';
 						div.innerHTML = '<strong style="color: white; font-weight: bold; font-family: Arial, Tahoma, FreeSans, sans-serif; font-size: 10pt;">' + this.displayname + '\'s Popego</strong>';
 						Popego.UtilsExt.applyStyles(div, {popcard_title: s, themes:{}}, this.theme);
 						this.container.appendChild(div);
 

						//dragging
						Popego.Context.addEvent(this.container, "mousedown", this.startDrag.bind(this));
						Popego.Context.addEvent(document, "mouseup", this.stopDrag.bind(this));
						
						//freeeeezing
						if (Popego.Context.browser != 'ie6')
							Popego.Context.addEvent(this.container, "dblclick", this.toggleFreezing.bind(this));
						
						//la mando al frente, la centro y la muestro
						Popego.PopcardManager.sendToFront(this);
						this.setPosition();
						this.show();
					} else if (this.isHidden) {
						Popego.PopcardManager.sendToFront(this);
						this.show();
					} else {
						this.close();
					}
				},
				close: function() {
					this.hide();
				},
				show: function() {
					this.isHidden = false;
					this.container.style.visibility = "visible";
				},
				hide: function() {
					this.isHidden = true;
					this.container.style.visibility = "hidden";
				},
				toggleFreezing: function(e) {
					if (this.isFreezed) {
						this.unfreeze(e);
					} else {
						this.freeze(e);
					}
				},
				freeze: function(e) {
					this.isFreezed = true;
					
					this.freezeCoords = {
						beforeTop: parseInt(this.container.style.top.split("px")[0]), 
						beforeLeft: parseInt(this.container.style.left.split("px")[0]),
						scrollTop: Popego.Context.getScrollTop(),
						scrollLeft: Popego.Context.getScrollLeft()
					};
					
					//calculo la diferencia entre donde aprete el mouse en la popcard y la posicion inicial de esta ultima
					var offsetX = (e.pageX || e.clientX) - parseInt(this.container.style.left.split("px")[0]);
					var operaDelOrto = parseInt(this.container.style.top.split("px")[0]); //increible, pero Opera me falla si pongo esto directo abajo
					var offsetY = (e.pageY || e.clientY) - operaDelOrto;
					
					this.container.style.position = "fixed";
					this.setPosition(e.clientY-offsetY, e.clientX-offsetX);
				},
				unfreeze: function(e) {
					this.isFreezed = false;
					var top = this.freezeCoords.beforeTop + Popego.Context.getScrollTop() - this.freezeCoords.scrollTop;
					var left = this.freezeCoords.beforeLeft + Popego.Context.getScrollLeft() - this.freezeCoords.scrollLeft;
					
					this.container.style.position = "absolute";
					this.setPosition(top, left);
				},
				
				/*
					Setea la posicion de la Popcard en la pantalla
					Si no recibe coordenadas la ubica centrada
				*/
				setPosition: function(top, left) {
					if (this.container) {
						this.container.style.top = (top || (Popego.Context.getHeight() - this.container.style.height.split('px')[0]) / 2 + Popego.Context.getScrollTop()) + "px";
						this.container.style.left = (left || (Popego.Context.getWidth() - this.container.style.width.split('px')[0]) / 2 + Popego.Context.getScrollLeft()) + "px";
					}
				},
				
				setDepth: function(n) {
					this.container.style.zIndex = n || this.depth;
				},
				
				startDrag: function(e) {
					if (this.isFreezed) return;
					
					//por las dudas
					this.stopDrag();
					this.isDragging = true;
					
					//traigo la popcard encima de todo
					Popego.PopcardManager.sendToFront(this);
					
					//calculo la diferencia entre donde aprete el mouse en la popcard y la posicion inicial de esta ultima
					var offsetX = (e.pageX || e.clientX) - parseInt(this.container.style.left.split("px")[0]);
					var operaDelOrto = parseInt(this.container.style.top.split("px")[0]); //increible, pero Opera me falla si pongo esto directo abajo
					var offsetY = (e.pageY || e.clientY) - operaDelOrto;
					
					//Lo hago asi para no meter el if adentro y que se compare en cada mousemove
					if ((/ie6|ie7/).test(Popego.Context.browser)) {
						//acomodo el offset considerando el scroll
						offsetX += Popego.Context.getScrollLeft();
						offsetY += Popego.Context.getScrollTop();
						this.onDragging = function(e){
							this.container.style.left = (e.clientX - offsetX + Popego.Context.getScrollLeft()) + "px";
							this.container.style.top = (e.clientY - offsetY + Popego.Context.getScrollTop()) + "px";
						}.bind(this);
					} else {
						this.onDragging = function(e){
							this.container.style.left = (e.pageX - offsetX) + "px";
							this.container.style.top = (e.pageY - offsetY) + "px";
						}.bind(this);
					}
					Popego.Context.addEvent(document, "mousemove", this.onDragging);
				},
				
				stopDrag: function() {
					if (this.isDragging) {
						this.isDragging = false;
						Popego.Context.removeEvent(document, "mousemove", this.onDragging);
					}
				},
				
				setTheme: function(theme, persist) {
					//TODO: hacer que se persista
					this.theme = theme;
					if (this.container) {
						var iframe = this.container.childNodes[0];
						var i = iframe.src.indexOf("?theme=");
						var url = iframe.src.substring(0, i==-1 ? iframe.src.length : i);
						iframe.src = url + "?theme=" + this.theme.substr(1);
						this.container.className = "popcard";
						Popego.UtilsExt.applyStyles(this.container, Popego.PopcardManager.styles, this.theme);
					}
				}
				
			}
		}		
	}
}
