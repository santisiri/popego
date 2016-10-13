var bgsleight	= function() {
/**
 * addLoadEvent guarentees that window onload events don't get overwritten and all events are called.
 * placing it inside the bgsleight function keeps it from conflicting with any other addLoadEvent functions 
 * that may be available.
 * @method addLoadEvent
 * @param func {Function}
 **/
	function addLoadEvent(func) {
		var oldonload = window.onload;
		if (typeof window.onload != 'function') {
			window.onload = func;
		} else {
			window.onload = function() {
				if (oldonload) {
					oldonload();
				}
				func();
			}
		}
	}

/**
 * 
 * @method fnLoadPngs
 **/
	function fnLoadPngs() {
		var rslt = navigator.appVersion.match(/MSIE (\d+\.\d+)/, '');
		var itsAllGood = (rslt != null && Number(rslt[1]) >= 5.5);
		for (var i = document.all.length - 1, obj = null; (obj = document.all[i]); i--) {
			if (itsAllGood && obj.currentStyle.backgroundImage.match(/\.png/i) != null) {
				fnFixPng(obj);
				obj.attachEvent("onpropertychange", fnPropertyChanged);
			}
		}
	}

/**
 * 
 * @method fnPropertyChanged
 **/
	function fnPropertyChanged() {
		if (window.event.propertyName == "style.backgroundImage") {
			var el = window.event.srcElement;
			if (!el.currentStyle.backgroundImage.match(/transparent\.gif/i)) {
				var bg	= el.currentStyle.backgroundImage;
				var src = bg.substring(5,bg.length-2);
				el.filters.item(0).src = src;
				el.style.backgroundImage = "url(/images/website/blank.gif)";
			}
		}
	}

/**
 * 
 * @method fnFixPng
 * @param obj {Object}
 **/
	function fnFixPng(obj) {
		var bg	= obj.currentStyle.backgroundImage;
		var src = bg.substring(5,bg.length-2);
		var sizingMethod = (obj.currentStyle.backgroundRepeat == "no-repeat") ? "crop" : "scale";
		obj.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + src + "', sizingMethod='" + sizingMethod + "')";
		obj.style.backgroundImage = "url(/images/website/blank.gif)";
	}
	return {
		init: function() {
				if (navigator.platform == "Win32" && navigator.appName == "Microsoft Internet Explorer" && window.attachEvent) {
				addLoadEvent(fnLoadPngs);
			}
		}
	}
}();

bgsleight.init();