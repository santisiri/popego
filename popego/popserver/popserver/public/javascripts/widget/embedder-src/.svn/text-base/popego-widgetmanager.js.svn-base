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
