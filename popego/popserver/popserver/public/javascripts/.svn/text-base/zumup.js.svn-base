// zumup.js

// Global variables
var toggles = new Array();
var previewers = new Array();

// Auxiliary functions
function toggle(current) {
	try {
		for (var i = 0; i < toggles.length; i++) {
			if (!toggles[i]) continue;
			toggles[i].className = (i == current) ?
				'category_selected' : 'category';
			if (previewers[i]) previewers[i].style.display =
				(i == current) ? 'block' : 'none';
		}
	} catch (e) {
		debug(e); // TODO
	}
}

function getOnClickHandler(i) {
	var f = function(e) {
		e = new Event(e);
		toggle(i);
		e.stop();
	};
	return f;
}

// Traditional event registration
window.onload = function () {
	try {
		toggles = new Array(
			$('toggle_pictures'),
			$('toggle_videos'),
			$('toggle_blogs'),
			$('toggle_music')
		);
		previewers = new Array(
			$('pictures'),
			$('videos'),
			$('blogs'),
			$('music')
		);
		first = -1;
		for (var i = 0; i < toggles.length; i++) {
			if (!toggles[i]) continue;
			if (first < 0) first = i;
			toggles[i].addEvent('click', getOnClickHandler(i));
		}
		if (first >= 0)
			toggle(first);
	} catch (e) {
		debug(e); // TODO
	}
}

// For debugging only
function debug(obj) {
	var s = '';
	for (var i in obj)
		s += i + ': ' + obj[i] + '\n';
	alert(s);
}

