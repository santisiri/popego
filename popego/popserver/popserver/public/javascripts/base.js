	
//Input tooltip text

function clearinputText(inputField,passwordStyle) {
	if(!inputField._haschanged){inputField.value=''};
	inputField._haschanged=true;
	if (passwordStyle == true) {
		inputField.type = "password";  	
	}
}

//MaxLength for TextAreas

function addEvent( obj, type, fn, tmp ) {
        if( obj.attachEvent ) {
                obj["e"+type+fn] = fn;
                obj[type+fn] = function(){obj["e"+type+fn]( window.event );}
                obj.attachEvent( "on"+type, obj[type+fn] );
        } else
                obj.addEventListener( type, fn, false );
}

function removeEvent( obj, type, fn ) {
        if( obj.detachEvent ) {
                obj.detachEvent( "on"+type, obj[type+fn] );
                obj[type+fn] = null;
        } else
                obj.removeEventListener( type, fn, false );
}


// Declare the namespace
var fdTextareaController;

(function() {
        function fdTextareaMaxlength(inp, maxlength) {
                this._inp       = inp;
                this._max       = Number(maxlength);
                var self        = this;

                self.maxlength = function() {
                        if(self._inp.disabled) return false;

                        if(self._inp.value.length > self._max) {
                                self._inp.value = self._inp.value.substring(0, self._max);
                                return false;
                        }

                        return true;
                }


                // Has Safari keypress foibles ? Needs tested...
                addEvent(self._inp, 'keypress', self.maxlength, false);

                // Sorry folks, but using the "onblur" event is the only way to cut the text down to size
                // after a users cut & paste action
                addEvent(self._inp, 'blur',     self.maxlength, false);

                // IE only event 'onpaste'

                // Conditional compilation used to load only in IE win.
                // As we don't need the onblur event for IE, we remove it at the same time.

                /*@cc_on @*/
                /*@if (@_win32)
                addEvent(self._inp, 'paste', function(){ setTimeout(self.maxlength, 50); }, true);
                removeEvent(self._inp, 'blur', self.maxlength, false);
                /*@end @*/

                // Call the maxlength function immediately to trim any text inserted server-side to the required length.
                self.maxlength();
        };

        // Construct the previously declared namespace
        fdTextareaController = {
                textareas: [],

                _construct: function( e ) {

                        var regExp_1 = /fd_max_([0-9]+){1}/ig;

                        var textareas = document.getElementsByTagName("textarea");

                        for(var i = 0, textarea; textarea = textareas[i]; i++) {
                                if(textarea.className && textarea.className.search(regExp_1) != -1) {
                                        max = parseInt(textarea.className.match(regExp_1)[0].replace(/fd_max_/ig, ''));
                                        if(max) fdTextareaController.textareas[fdTextareaController.textareas.length] = new fdTextareaMaxlength(textarea, max);
                                }
                        }

                },

                _deconstruct: function( e ) {

                }
        }
})();

// onload events
addEvent(window, 'load', fdTextareaController._construct, false);
addEvent(window, 'unload', fdTextareaController._deconstruct, false);
