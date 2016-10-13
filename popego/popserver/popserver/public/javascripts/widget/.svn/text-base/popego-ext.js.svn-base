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
}


if (typeof(Popego.widgets) == "undefined") {	
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
		Crea el widget con los attributos del widget descriptor recibido
	  
	  Arguments:
		wd, widget descriptor. Ex: {key:"123ad159a", user:"vic", theme:"tff3366", type:"default", id:"1", displayname:"Victor Calvello"}
		
	  Returns:
		the created widget instance
	*/
	Popego.createWidget = function(wd) {
		var n = Popego.widgets.length;
		var widget = Popego.WidgetManager.create(wd.key, wd.user, wd.theme, wd.type, wd.id, wd.displayname);
		Popego.widgets[n] = widget;
		Popego.widgets[n].initialize();
		
		return widget;
	};
}
