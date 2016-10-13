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
}