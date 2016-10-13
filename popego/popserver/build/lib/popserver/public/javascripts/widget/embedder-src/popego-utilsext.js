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
}