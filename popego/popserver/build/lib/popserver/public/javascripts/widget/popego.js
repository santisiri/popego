/*
Script: popego-ext.js
	Contains <Popego>
*/

/*
Class: Popego
	La verdad de la milanesa. A partir de aca cuelga lo demas.
	Lo unico que tiene es una funcion que se encarga de crear los widgets,
	Ademas tambien almacena los widgets y las popcards creadas.

Properties:
	- widgetDescriptor (lo setea el mako que devuelve el widget al usuario)
	- widgets (array)
	- popcards (dict)

Functions:
	- createWidget

*/
if (typeof(Popego) == "undefined") {
	Popego = {};
	
	/*
	 Property: widgets (array)
		Almacena los widgets creados (Popego.WidgetManager.create())
	*/
	Popego.widgets = [];
	
	/*
	 Property: popcards (dict)
		Almacena los popcards creadas (Popego.PopcardManager.create())
		La clave del dict es el id (key) del widget.
	*/
	Popego.popcards = {};
	
	
	/*
	  Function: createWidget
		Crea el widget con los attributos del widget descriptor
		Popego.widgetDescriptor = {key:"", user:"", theme:"", type:""}
	*/
	Popego.createWidget = function() {
		var n = Popego.widgets.length;
		var wd = Popego.widgetDescriptor;
		//var wd = gWidgetDescriptor;
		Popego.widgets[n] = Popego.WidgetManager.create(wd.key, wd.user, wd.theme, wd.type);
		Popego.widgets[n].initialize();
	};
}
/*
Property: widgetDescriptor
	Esta propiedad contiene los datos necesarios para instanciar un widget.
	Se setea desde el mako que responde al "embed code".
	
	Es un dict con:
		key - id del widget
		user - el usuario del que se muestra el widget
		theme - el theme del widget
		type - el tipo de widget, por ahora solo "default"

Notes:
	Si hay mas de un widget en la pagina, se va a ir pisando con los datos de cada widget
	y al final mantendra los datos del ultimo.
	Debido al sincronismo de la ejecucion (javascript), no deberia generar problemas.
*/
//Popego.widgetDescriptor = {key:(new Date().getTime()), user:"manuel", theme:"tff900a", type:"default"};


/*
Script: popego-config.js
	Contains <Popego.Config>
*/

/*
Class: Popego.Config
	Contiene:
	- datos de configuracion de Popego (ej. version del script corriendo, la URL base, URL de assets (cdn))
	- funciones para aplicar estilos inline pudiendo distinguir por browser
	- assets para los themes
	- remplazo de keywords (ej. ${ASSET:widget_background} a http://xxx/images/w_bkg.png)

Notes:
	Requiere de <Popego>, <Popego.Context>
	
Properties:
	- version
	- baseURL
	- assetsURLs (dict)
	- assets (dict)
	
Functions:
	- getAssetsURL()
	- getAsset()
	- applyStyles()
	- applyIEStyles()
	- styleToInline()
	- keywordReplace()
	
*/
if (typeof(Popego.Config) == "undefined") {
	//TODO: Reemplazar dinamicamente: version, baseURL, assetsURL
	Popego.Config = {};
	Popego.Config.version = "1.0";
	Popego.Config.baseURL = "http://localhost:5000";
	Popego.Config.assetsURLs = {
		"/images/widget": "http://localhost:5000",
		"default": "http://localhost:5000"
	};
	Popego.Config.assets = {
		//name : {path:common path, theme1:value, theme2:value, etc, default:value}
		widget_background: {
			"path": "/images/widget",
			"tff3366": "widget_background_ff3366.png",
			"tff900a": "widget_background_ff900a.png",
			"t0d6d6d": "widget_background_0d6d6d.png",
			"t3d3d3d": "widget_background_3d3d3d.png",
			"t4d8000": "widget_background_4d8000.png",
			"t6aac28": "widget_background_6aac28.png",
			"t9e9e9e": "widget_background_9e9e9e.png",
			"t013c76": "widget_background_013c76.png",
			"t129fc2": "widget_background_129fc2.png",
			"t0159b1": "widget_background_0159b1.png",
			"t666666": "widget_background_666666.png",
			"t993300": "widget_background_993300.png",
			"ta9d103": "widget_background_a9d103.png",
			"taa0000": "widget_background_aa0000.png",
			"tac20ac": "widget_background_ac20ac.png",
			"tc01258": "widget_background_c01258.png",
			"tdddddd": "widget_background_dddddd.png",
			"te4e40a": "widget_background_e4e40a.png",
			"te23d14": "widget_background_e23d14.png",
			"te72510": "widget_background_e72510.png",
			"tff900a": "widget_background_ff900a.png",
			"default": "widget_background_ff3366.png"
		},
		popcard_background: {
			"path": "/images/widget",
			"tff3366": "card_background_ff3366.png",
			"tff900a": "card_background_ff900a.png",
			"t0d6d6d": "card_background_0d6d6d.png",
			"t3d3d3d": "card_background_3d3d3d.png",
			"t4d8000": "card_background_4d8000.png",
			"t6aac28": "card_background_6aac28.png",
			"t9e9e9e": "card_background_9e9e9e.png",
			"t013c76": "card_background_013c76.png",
			"t129fc2": "card_background_129fc2.png",
			"t0159b1": "card_background_0159b1.png",
			"t666666": "card_background_666666.png",
			"t993300": "card_background_993300.png",
			"ta9d103": "card_background_a9d103.png",
			"taa0000": "card_background_aa0000.png",
			"tac20ac": "card_background_ac20ac.png",
			"tc01258": "card_background_c01258.png",
			"tdddddd": "card_background_dddddd.png",
			"te4e40a": "card_background_e4e40a.png",
			"te23d14": "card_background_e23d14.png",
			"te72510": "card_background_e72510.png",
			"tff900a": "card_background_ff900a.png",
			"default": "card_background_ff3366.png"
		}
	};
	
	/*
	Function: getAssetsURL
		Devuelve la URL del cdn para la key suministrada.
		Si no paso el key devuelve el cdn por default.

	Arguments:
		key - la clave del cdn (por lo general un path. Ej:'/images/widget/')

	Example:
		>Popego.Config.getAssetsURL('/images/widget')
	*/
	Popego.Config.getAssetsURL = function(key) {
		return Popego.Config.assetsURLs[key] || Popego.Config.assetsURLs["default"];
	};
	
	/*
	Function: getAsset
		Devuelve un recurso segun los parametros indicados.
		Si no hay theme utiliza los valores por default de estos.

	Arguments:
		name - el nombre del recurso.
		theme - optional, el theme que quiero del recurso.

	Example:
		>Popego.Config.getAsset('widget_background', 'tff3366')
	*/
	Popego.Config.getAsset = function(name, theme) {
		var path = Popego.Config.assets[name].path //es igual al key para el cdn
		var host = Popego.Config.getAssetsURL(path) + path;
		return host + "/" + (Popego.Config.assets[name][theme || "default"] || Popego.Config.assets[name]["default"]);
	};
}

/*
Script: popego-config.js
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
}

/*
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
	Popego.Config.applyStyles = function(h, styles, theme) {
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
	Popego.Config.applyIEStyles = function(h, styles, theme, classes) {
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
						if ((style = styles.themes[theme][classes[i] + version[j]])) {
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
							
						if ((style = styles.themes[theme][classes[i] + version[j]])) {
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
}

/*
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
		htmlText: "<div id='popego' class='widget'><iframe class='widget_iframe' src='" + Popego.Config.baseURL + "/${USERNAME}/api/widget/content?theme=${THEME}' scrolling='no' frameborder='0'></iframe></div>",
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
				"z-index":"9998"
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
				"z-index":"9995",
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
				"z-index":"9999",
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
		create: function(id, user, theme, type){
			return {
				key: id,
				user: user,
				theme: theme,
				type: type,
				wr: undefined,
				
				initialize: function() {
					//creo la popcard para este widget
					Popego.popcards[this.key] = Popego.PopcardManager.create(this.key, this.user, this.theme, this.type);
					
					//wrapper para el click
					document.write(Popego.Config.applyStyles("<div id='pe_wr_" + this.key + "' class='wrapper'></div>", Popego.WidgetManager.styles, this.theme));
					this.wr = document.getElementById("pe_wr_" + this.key)
					
					var key = this.key;
					this.wr.onclick = function(e) {
						Popego.popcards[key].open();
					}
					
					//imprimo el widget
					var html = Popego.WidgetManager.htmlText.replace("${USERNAME}", this.user).replace("${THEME}", this.theme.substr(1));
					document.write(Popego.Config.applyStyles(html, Popego.WidgetManager.styles, this.theme));
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
	Requiere de <Popego>, <Popego.Config>
	
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
		htmlText: "<iframe scrolling='no' frameborder='no' src='" + Popego.Config.baseURL + "/${USERNAME}/api/home/?nocache' class='popcard_iframe'></iframe>",
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
				"position":"absolute",
				"border":"0",
				"width":"415px",
				"height":"430px",
				"top":"65px",
				"left":"25px",
				"z-index":"9999",
				"clear":"both"
			},
			
			themes: {
				//theme: {cssClass:{properties}, cssClass2:{properties}, etc}
				"tff3366": {},
				"tff900a": {}
			}
		},
			
		create: function(wid, user, theme, type) {
			return {
				key: wid,
				user: user,
				theme: theme,
				type: type,
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
						Popego.Config.applyStyles(this.container, Popego.PopcardManager.styles, this.theme);
						
						this.container.style.visibility = "hidden";
						this.container.style.zIndex = this.depth;
						
						var html = Popego.PopcardManager.htmlText.replace("${USERNAME}", this.user);
						this.container.innerHTML = Popego.Config.applyStyles(html, Popego.PopcardManager.styles, this.theme);
						document.getElementsByTagName("body")[0].appendChild(this.container);
						
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
				}
				
			}
		}		
	}
}
//////////////////////////////////////////////////////////////////////////
// Creo un nuevo widget
/////////////////////////////////////////////////////////////////////////
Popego.createWidget();