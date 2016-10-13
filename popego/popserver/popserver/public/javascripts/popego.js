/**
 *  Módulo utilizado por el site popego.com 
 */

if (typeof Popego == "undefined") Popego = {};

Popego.Services = new Class({
	
	/* CONSTANTS */
	REQ_TIMEOUT: 5000, //timeout for XHR requests in milliseconds
	
	/* STYLES */
	STYLE_SERVICE_NORMAL: 'style_srv_normal',
	STYLE_SERVICE_ADDED: 'style_srv_added',
	STYLE_SERVICE_ERROR: 'style_btn_srv_error',
	
	URL_REMOVE_SERVICE: '/user/' + Popego.Env.username + '/profile/service/cancel/',
	URL_ADD_SERVICE: '/user/' + Popego.Env.username + '/profile/service/new/',
	
	Status: { OK: "ok", ERROR: "error" },

	initialize: function(el) {
		this.contentDiv = el;
		this.serviceTypeTabDiv = undefined;
		this.servicesDiv = undefined; 
		this.servicesAddedDiv = undefined;
		
		this.serviceTypeSelected = '';
		this.serviceTypeSelectedDiv = undefined;
		this.workingService = undefined; //el Element del servicio que voy a remover o agregar
		
		// XHR to get subsections' data
		this.servicesXHR = new XHR({method: 'get'});
		this.servicesXHR.addEvent('onRequest', this.onDataRequest.bind(this));
		this.servicesXHR.addEvent('onFailure', this.onDataFailure.bind(this));
		this.servicesXHR.addEvent('onSuccess', this.onDataSuccess.bind(this));
		this.servicesXHR.errorRenderHash = new Hash();
		this.servicesXHR.currentRequestURL = '';
		this.timeoutChecking = undefined;	//checks for request timeouts
		
		this.createServiceList();
		this.createTagCloud();
	},
	
	/*********************************** Create functions *******************************************/
	createTagCloud: function() {
		this.sortableTagCloud = new Popego.TagCloud('tag_cloud');
		// TODO: Probablemente el dragging de tags no se haga, 
		// sino que se cambie por un rating (para personalizar 
		// lista por ponderacion ademas de hits) -- a definir
	},
	
	createServiceList: function() {
		this.serviceTypeTabDiv = this.contentDiv.getElement('.services').getElement('.service_type_tab')[0];
		this.servicesDiv = this.contentDiv.getElement('.services').getElement('.service_list')[0];
		this.setServiceListBehaviors();
	},
	/************************************************************************************************/
	
	/************************************ Services XHR Handlers *************************************/
	onDataRequest: function() {
		this.timeoutChecking = function() {
			if(this.servicesXHR.running) {
				this.servicesXHR.cancel();
				this.onDataFailure();
			}
			else $clear(this.timeoutChecking);
		}.bind(this).delay(this.REQ_TIMEOUT);
	},
	
	onDataFailure: function(t) {
		$clear(this.timeoutChecking);
		
		/* TODO: esta linea va a ser inconsistente si hay llamadas en paralelo */
		var contentHolder = this.servicesXHR.errorRenderHash.get(this.servicesXHR.currentRequestURL)
		contentHolder.setHTML('We\'re sorry, but the data is unavailable right now. <br/>Please try again later.');
		contentHolder.style.display = '';
		
		this.resetServiceItemStyle();
		this.workingService = undefined;
	},
	
	onDataSuccess: function(t) {
		$clear(this.timeoutChecking);
	},
	/************************************************************************************************/
	
	/********************************** Add and Remove Services functions **************************/
	addService: function(srvId, username) {
		var url = this.URL_ADD_SERVICE + srvId + '?username=' + username;
		this.serviceAddedHandler = this.onServiceAddedResponse.bind(this);	//hago esto para despues poder hacer un removeEvent
		this.servicesXHR.addEvent('onSuccess', this.serviceAddedHandler);
		this.servicesXHR.errorRenderHash.set(url, this.contentDiv.getElement('.services_error_box')[0]);
		this.servicesXHR.currentRequestURL = url;
		this.servicesXHR.send(url);
		// Lanzar refreshing de la lista de top tags
		this.sortableTagCloud.triggerRefreshing();
	},
	
	removeService: function(srvId, username) {
		var url = this.URL_REMOVE_SERVICE + srvId + '?username=' + username;
		this.serviceRemovedHandler = this.onServiceRemovedResponse.bind(this);	//hago esto para despues poder hacer un removeEvent
		this.servicesXHR.addEvent('onSuccess', this.serviceRemovedHandler);
		this.servicesXHR.errorRenderHash.set(url, this.contentDiv.getElement('.services_error_box')[0]);
		this.servicesXHR.currentRequestURL = url;
		this.servicesXHR.send(url);
	},
	/************************************************************************************************/
	
	/*********************************** Service Reponse Handlers ***********************************/
	onServiceAddedResponse: function(t) {
		this.servicesXHR.removeEvent('onSuccess', this.serviceAddedHandler);
		
		response = Json.evaluate(t)
		if (response.status == this.Status.OK) this.onServiceAddedSuccess();
		else this.onServiceError(response);
	},
	
	onServiceRemovedResponse: function(t) {
		this.servicesXHR.removeEvent('onSuccess', this.serviceAddedHandler);
		
		response = Json.evaluate(t)
		if (response.status == this.Status.OK) this.onServiceRemovedSuccess();
		else this.onServiceError(response);
	},
	
	onServiceAddedSuccess: function(t) {
		var input = this.workingService.getElement('input[type=text]');
		this.workingService.getElement('.user_text').getElement('a').setText(input.value);
		this.setServiceItemStyle(this.STYLE_SERVICE_ADDED);
	},
	
	onServiceRemovedSuccess: function(t) {
		this.servicesXHR.removeEvent('onSuccess', this.serviceRemovedHandler);
		this.setServiceItemStyle(this.STYLE_SERVICE_NORMAL);
	},
	
	onServiceError: function(response) {
		if (response) {
			this.hideServiceSpinner();
			this.showServiceError(response.description);
			this.setServiceItemStyle(this.STYLE_SERVICE_ERROR);
		}
		this.workingService = undefined;
	},
	/************************************************************************************************/
	
	/************************************ Style Functions *******************************************/
	setServiceItemStyle: function(style) {
		var promptText = this.workingService.getElement('.prompt_text');
		var addedText = this.workingService.getElement('.added_text');
		var userText = this.workingService.getElement('.user_text');
		var errorText = this.workingService.getElement('.error_text');
		var input = this.workingService.getElement('input[type=text]');
		
		this.hideServiceSpinner();
		
		switch(style) {
			case this.STYLE_SERVICE_NORMAL:
				input.setStyle('display', '');
				promptText.setStyle('display', '');
				addedText.setStyle('display', 'none');
				userText.setStyle('display', 'none');
				errorText.setStyle('display', 'none');
				break;
				
			case this.STYLE_SERVICE_ADDED:
				input.setStyle('display', 'none');
				promptText.setStyle('display', 'none');
				addedText.setStyle('display', '');
				userText.setStyle('display', '');
				errorText.setStyle('display', 'none');
				break;
				
			case this.STYLE_SERVICE_ERROR:
				input.setStyle('display', 'none');
				promptText.setStyle('display', 'none');
				addedText.setStyle('display', 'none');
				userText.setStyle('display', 'none');
				errorText.setStyle('display', '');
				break;
		}
		this.setButtonsStyle(style);
	},
	
	resetServiceItemStyle: function(setFocus) {
		this.hideServiceSpinner();
		
		var username = this.workingService.getElement('.user_text').getElement('a').getText();
		if (username.trim() == '') {
			this.setServiceItemStyle(this.STYLE_SERVICE_NORMAL);
			if (setFocus) {
				var input = this.workingService.getElement('input[type=text]');
				input.select();
			}
		} else
			this.setServiceItemStyle(this.STYLE_SERVICE_ADDED);
	},
	
	setButtonsStyle: function(style) {
		var buttons = this.workingService.getElements('input[type=button]'); 
		switch(style) {
			case this.STYLE_SERVICE_NORMAL:
				buttons[0].setStyle('display', 'none'); //modify
				buttons[1].setStyle('display', 'none'); //remove
				buttons[2].setStyle('display', ''); //add
				buttons[2].value = 'add';
				break;
				
			case this.STYLE_SERVICE_ADDED:
				buttons[0].setStyle('display', ''); //modify
				buttons[1].setStyle('display', ''); //remove
				buttons[2].setStyle('display', ''); //add
				buttons[2].value = 'add more';
				break;
				
			case this.STYLE_SERVICE_ERROR:
				buttons[0].setStyle('display', 'none'); //modify
				buttons[1].setStyle('display', 'none'); //remove
				buttons[2].setStyle('display', ''); //add
				buttons[2].value = 'try again';
				break;
		}
	},
	
	showServiceSpinner: function() {
		this.workingService.getElement('.spinner').setStyle('display', '');
		this.workingService.getElement('.prompt_text').setStyle('display', 'none');
		this.workingService.getElement('.added_text').setStyle('display', 'none');
		this.workingService.getElement('.user_text').setStyle('display', 'none');
		this.workingService.getElement('input[type=text]').className = 'uploading';
	},
	
	hideServiceSpinner: function() {
		this.workingService.getElement('.spinner').setStyle('display', 'none');
		this.workingService.getElement('input[type=text]').className = '';
	},
	
	showServiceError: function(msg) {
		var errorText = this.workingService.getElement('.error_text');
		errorText.setText(msg);
		errorText.setStyle('display', '');
	},
	
	showServicesByType: function(type) {
		type = type || 'all';
		var services = this.servicesDiv.getElements('li');
		services.each(function(service) {
			if ((type=='all' && service.className.split('_')[1]!='added')|| type==service.className) service.style.display = '';
			else service.style.display = 'none';
		});
	},
	/************************************************************************************************/
	
	/********************************** Service List Behaviors **************************************/
	setServiceListBehaviors: function() {
		var types = this.serviceTypeTabDiv.getElements('div').getElement('strong');
		types.each(function(type){
			if (type.getParent().className == 'category_selected') {
				this.serviceTypeSelected = type.getText();
				this.serviceTypeSelectedDiv = type.getParent();
			}
			type.addEvent('click', this.onServiceTypeTabClick.bindWithEvent(this));
		}.bind(this));
		
		var services = this.servicesDiv.getElements('li');
		services.each(function(service) {
			this.workingService = service;
			
			var txtUsername = service.getElement('input[type=text]');
			txtUsername.addEvent('focus', function(){ if (this.value == 'username') this.value = '';});
			txtUsername.addEvent('blur', function(){ if (this.value.trim() == '') this.value = 'username';});
			txtUsername.addEvent('keydown', this.onUsernameInputKeyDown.bindWithEvent(this));
			
			var promptText = service.getElement('.prompt_text');
			var buttons = service.getElements('input[type=button]'); 
			this.setButtonsStyle(promptText.getStyle('display') == 'none' ? this.STYLE_SERVICE_ADDED : this.STYLE_SERVICE_NORMAL );
			
			buttons[0].addEvent('click', function(){alert(this.value)}); //modify
			buttons[1].addEvent('click', this.onServiceRemoveClick.bindWithEvent(this)); //remove
			buttons[2].addEvent('click', this.onServiceAddClick.bindWithEvent(this)); //add
		}.bind(this));
	},
	
	setServicesAddedItemBehavior: function(el) {
		var removeDiv = el.getElement('.service_remove');
		removeDiv.addEvent('click', this.onServiceRemoveClick.bindWithEvent(this, removeDiv));
	},
	/************************************************************************************************/
	
	/******************************* Service List Behaviors Handlers ********************************/
	onServiceTypeTabClick: function(e) {
		this.serviceTypeSelectedDiv.className = 'category';
		this.serviceTypeSelectedDiv = e.target.getParent();
		this.serviceTypeSelectedDiv.className = 'category_selected';
		this.serviceTypeSelected = this.serviceTypeSelectedDiv.getElement('strong').getText();
		this.showServicesByType(this.serviceTypeSelected);
	},
	
	onUsernameInputKeyDown: function(e) {
		if (e.key == 'enter' && e.target.value != '') {
			this.onServiceAddClick(e);
			e.stopPropagation();
			e.stop();
		}
	},
	
	onServiceAddClick: function(e) {
		var form = e.target.getParent()
		var input = form.getElement('input[type=text]');
		var username = input.value;
		var button = form.getElements('input[type=button]')[2];
		this.workingService = form.getParent();
		
		if (button.value == 'try again') {
			this.resetServiceItemStyle(true);
		} else if (button.value == 'add more') {
			//TODO: Algo
		} else {
			//TODO: Avisar si no pone username y algo por el estilo
			if (username.trim() == '' || username == 'username') {
				input.select();
				return;
			}
			
			var srvId = this.workingService.id.substring(3, this.workingService.id.length);
			this.showServiceSpinner();
			this.addService(srvId, username);
		}
	},
	
	onServiceRemoveClick: function(e) {
		var form = e.target.getParent()
		var username = form.getElement('.user_text').getElement('a').getText();
		
		//TODO: requerir confirmacion
		this.workingService = form.getParent();
		var srvId = this.workingService.id.substring(3, this.workingService.id.length);
		
		this.showServiceSpinner();
		this.removeService(srvId, username);
	}
	/************************************************************************************************/
});

Popego.TagCloud = new Class({

	// Constants
	INITIAL_REFRESH_INTERVAL: 1000, // 1 sec
	INTERVAL_GROW_FACTOR: 2, // interval duplicates with each refresh
	MAX_REFRESH_INTERVAL: 120000, // 2 min

	// Instance variables
	tagCloud: undefined,
	tagsXHR: undefined, 
	interval: 1,
	timeout: null,
	
	// Constructor
	initialize: function (el) {
		//this.tagCloud = new Sortables($(el));
		// TODO: Eliminar la conversion a Sortables??
		this.tagCloud = $(el);
		this.interval = this.INITIAL_REFRESH_INTERVAL;
		// TODO: se podrian parametrizar algunos strings
		// cableados abajo entre los metodos
	},

	// Instance methods
	onFailure: function (e) {
		var m = $('toptags_message');
		if (!m) return;
		// El elemento m no existe si ya habia tags.
		// (Pero no importa. El unico caso a contemplar es:
		// No habia ni un tag y fallo el refresh de top tags)
		m.setText('Oops... There was a problem while refreshing '
			+ 'your list of top tags. Try reloading this page.');
		m.setStyle('display', 'block');
		this.timeout = this.refresh.delay(this.interval, this);
	},

	onSuccess: function (str) {
		try {
			var newTags = Json.evaluate(str);
			this.refreshWith(newTags);
			if (this.interval < this.MAX_REFRESH_INTERVAL) {
				this.timeout = this.refresh.delay(this.interval, this);
				this.interval *= this.INTERVAL_GROW_FACTOR;
			}
		} catch (e) {
		}
	},
	
	refresh: function() {
		try {
			this.tagsXHR = new XHR({method: 'get'});
			this.tagsXHR.addEvent('onFailure', this.onFailure.bind(this));
			this.tagsXHR.addEvent('onSuccess', this.onSuccess.bind(this));
			this.tagsXHR.send('/user/' + Popego.Env.username + '/profile/toptags?n=40');
		} catch (e) {
		}
	},
	
	refreshWith: function(newTags) {
		if (!this.tagCloud) return;
		
		var inner = '';
		var m = $('toptags_message');
		var trash = $('trash_panel');
		var br = $('clear_trick');
		if (newTags.length == 0) {
			m.setStyle('display', '');
			trash.setStyle('display', 'none');
			br.setStyle('display', '');
		} else {
			for (var i = 0; i < newTags.length; i++) {
				inner += '<span class="tag_hits_' + newTags[i].className + '">' + newTags[i].tagName + '</span>\n';
			}
			m.setStyle('display', 'none');
			trash.setStyle('display', '');
			br.setStyle('display', 'none');
			// this.tagCloud = new Sortables(this.tagCloud);
			// TODO: eliminar la conversion a Sortables??
		}
		this.tagCloud.setHTML(inner);
	},

	triggerRefreshing: function() {
		this.interval = this.INITIAL_REFRESH_INTERVAL;
		$clear(this.timeout);
		this.refresh();
	}

});

Popego.AjaxUploader = new Class({

	form: undefined,
	iframe: undefined,
	onSubmit: function () {},
	onComplete: function () {},

	initialize: function (form, iframe, onSubmit, onComplete) {
	try {
		// form and iframe elements setup
		this.form = $(form);
		this.iframe = $(iframe);
		if (!$defined(iframe))
			this.createIframe('ajax_uploader_iframe');
		else if (!this.iframe)
			this.createIframe(iframe.toString());

		// form-iframe targetting
		this.form.setProperty('target', this.iframe.id);
		// event setup
		if ($type(onSubmit) == 'function')
			this.onSubmit = onSubmit; 
		if ($type(onComplete) == 'function')
			this.onComplete = onComplete;
		this.form.addEvent('submit', this.onSubmit.bind(this));
		this.iframe.addEvent('load', this.onComplete.bind(this));
	} catch (e) {
		// alert(e.message);
	}
	},

	createIframe: function (id) {
		this.iframe = new Element('iframe');
		this.iframe.setStyle('display', 'none');
		this.iframe.setProperty('src', 'about:blank');
		this.iframe.setProperty('id', id);
		this.iframe.setProperty('name', id);
		this.iframe.injectInside(this.form);
	}

});

Popego.AvatarUploader = Popego.AjaxUploader.extend({
	
	message: undefined,

	initialize: function () {
		this.parent('upload_avatar', 'upload_iframe',
				this.onSubmit, this.onComplete);
		this.message = $('upload_message');
	},

	onSubmit: function () {
		this.message.setText('Uploading avatar...');
		return true;
	},
	
	onComplete: function () {
		try {
			var t = this.getIframeText();
			this.message.setText(t);
			var avatar = $ES('.avatar_box');
			this.refreshImage(avatar.getFirst());
		} catch (e) {
			// alert(e.message);
		}
		return true;
	},

	refreshImage: function (img) {
		if (!$defined(img)) return false;
		var src = img.getProperty('src').toString();
		var i = src.lastIndexOf('?');
		if (i >= 0) src = src.substr(0, i);
		src += '?' + new Date().getTime().toString();
		img.setProperty('src', src);
		return true;
	},

	getIframeText: function (iframe) {
		var f = $pick(iframe, this.iframe);
		var doc = undefined;
		if (f.contentDocument) { // For NS6
			doc = f.contentDocument; 
		} else if (f.contentWindow) { // For IE5.5 and IE6
			doc = f.contentWindow.document;
		} else if (f.document) { // For IE5
			doc = f.document;
		}
		return (doc && doc.body) ? doc.body.innerHTML : '';
	}

});

Popego.ThemeSelector = new Class({
	
	initialize: function () {
	try {
		var lis = $ES('li', '.palette');
		lis.each(function (li) {
			var anchor = li.getFirst();
			var f = this.onThemeSelected.bindWithEvent(anchor);
			anchor.addEvent('click', f);
			li.addEvent('click', f);
		}.bind(this));
	} catch (e) {
		// alert(debug(e));
	}
	},

	onThemeSelected: function (e) {
	try {
		var a = e.target;
		var li = a.getParent();
		if (li.getTag() != 'li') {
			li = a;
			a = li.getFirst();
		}
		var lis = $ES('li', li.getParent());
		lis.each(function (i) {
			i.setProperty('class', '');
		});
		var f = function (theme) {
			var link = $E('link', document.body);
			if (link) link.remove();
			var link = new Element('link', {
				href: '/css/themes/' + theme + '.css',
				rel: 'stylesheet',
				type: 'text/css'
			});
			link.injectTop(document.body);
			li.setProperty('class', 'picked_color');
		}
		var r = new Json.Remote(a.getProperty('href'));
		r.addEvent('onComplete', f);
		r.send();
		e.stop();
		return false;
	} catch (e) {
		// alert(debug(e));
	}
	}

});

function debug(o) {
	var s = '';
	for (i in o)
		s += i + ': ' + o[i] + '\n';
	return s;
}