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
