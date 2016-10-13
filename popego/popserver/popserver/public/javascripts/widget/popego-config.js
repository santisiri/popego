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
	Requiere de <Popego>
	
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
			"t000000": "widget_background_000000.png",
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
			"t000000": "card_background_000000.png",
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
		return host + "/" + (Popego.Config.assets[name][theme || "default"] || Popego.Config.assets[name]["default"]) + (typeof(Popego.Config.revision) == 'undefined' || Popego.Config.revision == null ? '' : '?' + Popego.Config.revision);
	};
}
