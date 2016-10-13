/**
  * Realiza un call y lanza los siguientes eventos:
  *  - onSuccess
  *  - onFailure
  */
Popego.ServiceRequest = new Class({
	REQ_TIMEOUT: 15000, //timeout for XHR requests in milliseconds

	
	initialize: function(username, serviceId) {
	    this.username = username;
	    this.serviceId = serviceId;
	},

	call: function() {
	    this.xhr = new XHR({method: 'get'});
	    this.xhr.addEvent('onRequest', this._onDataRequest.bind(this));
	    this.xhr.addEvent('onFailure', this._onDataFailure.bind(this));
	    this.xhr.addEvent('onSuccess', this._onDataSuccess.bind(this));

	    this.xhr.send(this.getUrl());
	},

	getUrl: function() {
	},

	_onDataRequest: function() {
	    this.timeoutChecking = function() {
		if(this.xhr.running) {
		    this.xhr.cancel();
		    this._onDataFailure();
		} else { 
		    $clear(this.timeoutChecking);
		}
	    }.bind(this).delay(this.REQ_TIMEOUT);
	},
	
	_onDataFailure: function(t) {
	    $clear(this.timeoutChecking);
	    this.fireEvent('onFailure');
	},
	
	_onDataSuccess: function(t) {
	    $clear(this.timeoutChecking);
	    response = Json.evaluate(t)
	    this.fireEvent('onSuccess', response);
	}

    });
Popego.ServiceRequest.implement(new Events);
	
Popego.ServiceAddRequest = Popego.ServiceRequest.extend({
	getUrl: function() {
	    return '/' + Popego.Env.username + '/services/new/' + this.serviceId + '?username=' + this.username;
	}
    });

Popego.ServiceRemoveRequest = Popego.ServiceRequest.extend({
	getUrl: function() {
	    return '/' + Popego.Env.username + '/services/cancel/' + this.serviceId + '?username=' + this.username;
	}
    });


Popego.ServiceManager = new Class({


	Status: { OK: "ok", ERROR: "error" },

	initialize: function(srvContainer) {
	    this.container = srvContainer;
	    this.srvId = this.container.id.substring(3, this.container.id.length);

	    var promptText = this.container.getElement('.prompt_text');
	    
	    if (promptText.getStyle('display') == 'none') {
		this.state = Popego.ServiceManager.State.WithAccount;
	    } else {
		this.state = Popego.ServiceManager.State.WithoutAccount;
	    }

	    this._refreshButtonsStyle();
	},

	_addAccount: function(username) {
	    var addRequest = new Popego.ServiceAddRequest(username, this.srvId);
	    addRequest.addEvent('onSuccess', this._addRequestCallback.bind(this));
	    addRequest.addEvent('onFailure', this._onCommunicationFailure.bind(this));
	    addRequest.call()
	},


	_onCommunicationFailure: function() {
	    this._refreshStyle();
	    this.fireEvent('onCommunicationFailure');
	},

	_addRequestCallback: function(response) {
	    if (response.status == this.Status.OK) {
		this._onAddSuccess();
	    } else {
		this._onError(response);
	    }
	},

	_onAddSuccess: function() {
	    var input = this.container.getElement('input[type=text]');
	    var userText = this.container.getElement('.user_text');
	    userText.setHTML("<strong>" + input.value + "</strong><span>.</span>");

	    this.state = Popego.ServiceManager.State.WithAccount;
	    this._refreshStyle();

	    this.fireEvent('onAccountAdded', this);
	},

	_onError: function(response) {
	    if (response) {
		this._hideSpinner();
		this._showError(response.description);
		this.state = Popego.ServiceManager.State.WithErrors;
		this._refreshStyle();
	    }
	},


	_removeAccount: function(username) {
	    var removeRequest = new Popego.ServiceRemoveRequest(username, this.srvId);
	    removeRequest.addEvent('onSuccess', this._removeRequestCallback.bind(this));
	    removeRequest.addEvent('onFailure', this._onCommunicationFailure.bind(this));
	    removeRequest.call()

	},

	_removeRequestCallback: function(response) {
	    if (response.status == this.Status.OK) {
		this._onRemoveSuccess();
	    } else {
		this._onError(response);
	    }
	},

	_onRemoveSuccess: function() {
	    this.state = Popego.ServiceManager.State.WithoutAccount;
	    this._refreshStyle();
	    this.fireEvent('onAccountRemoved', this);
	},

	_showSpinner: function() {
	    this.container.getElement('.spinner').setStyle('display', '');
	    this.container.getElement('.prompt_text').setStyle('display', 'none');
	    this.container.getElement('.added_text').setStyle('display', 'none');
	    this.container.getElement('.user_text').setStyle('display', 'none');
	    this.container.getElement('input[type=text]').className = 'uploading';
	},
	
	_hideSpinner: function() {
	    this.container.getElement('.spinner').setStyle('display', 'none');
	    this.container.getElement('input[type=text]').className = '';
	},

	_showError: function(msg) {
	    var errorText = this.container.getElement('.error_text');
	    errorText.setText(msg);
	    errorText.setStyle('display', '');
	},

	addButtonClicked: function(form) {
	    var input = form.getElement('input[type=text]');
	    var username = input.value;
	    var button = form.getElements('input[type=button]')[2];

	    if (button.value == 'try again') {
		this.state = Popego.ServiceManager.State.WithoutAccount;
		this._refreshStyle();
		var input = this.container.getElement('input[type=text]');
		input.select();		
	    } else if (button.value == 'add more') {
		//TODO: Algo
	    } else { // Add
		//TODO: Avisar si no pone username y algo por el estilo
		if (username.trim() == '' || username == 'username') {
		    input.select();
		    return;
		}

		this._showSpinner();
		this._addAccount(username);
	    }
	},

	removeButtonClicked: function(form) {
	    var username = this._getUsernameFromUserText();
	    this._showSpinner();
	    this._removeAccount(username);
	},

	_getUsernameFromUserText: function() {
	    var userText = this.container.getElement('.user_text');
	    var anchor = userText.getElement('a');
	    if (anchor) {
		return anchor.getText();
	    } else {
		return userText.getElement('strong').getText();
	    }
	},

	_refreshStyle: function() {

	    var promptText = this.container.getElement('.prompt_text');
	    var addedText = this.container.getElement('.added_text');
	    var userText = this.container.getElement('.user_text');
	    var errorText = this.container.getElement('.error_text');
	    var input = this.container.getElement('input[type=text]');
		
	    this._hideSpinner();
		
	    switch(this.state) {
	    case Popego.ServiceManager.State.WithoutAccount:
		addedText.setStyle('display', 'none');
		userText.setStyle('display', 'none');
		errorText.setStyle('display', 'none');
		promptText.setStyle('display', '');
		input.setStyle('display', '');
		input.value = this._getUsernameFromUserText();
		break;
				
	    case Popego.ServiceManager.State.WithAccount:
		input.setStyle('display', 'none');
		promptText.setStyle('display', 'none');
		errorText.setStyle('display', 'none');
		addedText.setStyle('display', '');
		userText.setStyle('display', '');
		break;
		
	    case Popego.ServiceManager.State.WithErrors:
		input.setStyle('display', 'none');
		promptText.setStyle('display', 'none');
		addedText.setStyle('display', 'none');
		userText.setStyle('display', 'none');
		errorText.setStyle('display', '');
		break;
	    }
	    this._refreshButtonsStyle();
	},

	_refreshButtonsStyle: function() {
	    var buttons = this.container.getElements('input[type=button]'); 
	    switch(this.state) {
	    case Popego.ServiceManager.State.WithoutAccount:
		buttons[0].setStyle('display', 'none'); //modify
		buttons[1].setStyle('display', 'none'); //remove
		buttons[2].setStyle('display', ''); //add
		buttons[2].value = 'add';
		break;
		
	    case Popego.ServiceManager.State.WithAccount:
		buttons[0].setStyle('display', 'none'); //modify
		buttons[1].setStyle('display', ''); //remove
		buttons[2].setStyle('display', 'none'); //add
		break;
				
	    case Popego.ServiceManager.State.WithErrors:
		buttons[0].setStyle('display', 'none'); //modify
		buttons[1].setStyle('display', 'none'); //remove
		buttons[2].setStyle('display', ''); //add
		buttons[2].value = 'try again';
		break;
	    }
	}
});
Popego.ServiceManager.implement(new Events);
Popego.ServiceManager.State =  {
    WithAccount: 1,
    WithoutAccount: 2,
    WithErrors: 3
};


Popego.Services = new Class({
	
	initialize: function(el) {
	    this.contentDiv = el;
		this.toolTips = undefined;
	    this.serviceTypeTabDiv = undefined;
	    this.servicesDiv = undefined; 
	    this.servicesAddedDiv = undefined;
	    
	    this.serviceTypeSelected = '';
	    this.serviceTypeSelectedDiv = undefined;

	    this.srvManagers = {};
	    
		this.createTooltips();
	    this.createServiceList();
	    this.createTagCloud();
	    
	    this.setServiceFocus();
	},
	
	/*********************************** Create functions *******************************************/
	createTooltips: function() {
		this.toolTips = new Tips(this.contentDiv.getElements('.help_box')[0], {
			initialize:function(){
				this.fx = new Fx.Style(this.toolTip, 'opacity', {duration: 500, wait: false}).set(0);
			},
			onShow: function(toolTip) {
				this.fx.start(1);
			},
			onHide: function(toolTip) {
				this.fx.start(0);
			}
		});
	},
	
	createTagCloud: function() {
	    this.sortableTagCloud = new Popego.TagCloud('tag_cloud');
	    this.draggableTags = new Popego.DraggableTags($$('div#tag_cloud span'), $('trash_panel'), {setInterestURL: '/' + Popego.Env.username + '/tag_interest'});
	    this.sortableTagCloud.addEvent('refresh', function(e) {
		    this.makeDraggables($$('div#tag_cloud span'));
		}.bind(this.draggableTags));
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
	
	
	/*********************************** Service Manager Listeners ***********************************/
	
	onCommunicationFailure: function() {
	    var contentHolder = this.contentDiv.getElement('.services_error_box')[0];
	    contentHolder.setHTML('We\'re sorry, but the data is unavailable right now. <br/>Please try again later.');
	    contentHolder.style.display = '';
	},

	onAccountAdded: function(srvManager) {
	    this.setServiceFocus(srvManager.container);
	    // Lanzar refreshing de la lista de top tags
	    this.sortableTagCloud.triggerRefreshing();
	},
	
	onAccountRemoved: function(srvManager) {
	    this.setServiceFocus(srvManager.container)
	    // Lanzar refreshing de la lista de top tags
	    this.sortableTagCloud.triggerRefreshing();
	},
	
	/************************************************************************************************/
	
	/************************************ Style Functions *******************************************/

	showServicesByType: function(type) {
	    type = type || 'all';
	    var services = this.servicesDiv.getElements('li');
	    services.each(function(service) {
		    if ((type=='all' && service.className.split('_')[1]!='added')|| type==service.className) service.style.display = '';
		    else service.style.display = 'none';
		});
	},
	
	setServiceFocus: function(workingService) {
	    var currentService = workingService || this.contentDiv.getElement('.service_list').getFirst()[0];
	    var input = currentService.getElement('input[type=text]');
	    if (input.getStyle('display') != 'none') {
		input.select();
		return;
	    } else {
		var focused = false;
		var nextSrv = currentService.getNext();
		if (!nextSrv || nextSrv.tagName.toLowerCase() != 'li') nextSrv = currentService.getParent().getFirst();
		
		while (!focused && nextSrv != currentService) {
		    input = nextSrv.getElement('input[type=text]');
		    if (input.getStyle('display') != 'none') {
			input.select();
			focused = true;
		    } else {
			nextSrv = nextSrv.getNext();
			if (!nextSrv || nextSrv.tagName.toLowerCase() != 'li') nextSrv = currentService.getParent().getFirst();
		    }
		}
	    }
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
		    container = service;
		    this.srvManagers[container.id] = new Popego.ServiceManager(container);
		    this.srvManagers[container.id].addEvent('onCommunicationFailure', this.onCommunicationFailure.bind(this));
		    this.srvManagers[container.id].addEvent('onAccountAdded', this.onAccountAdded.bind(this));
		    this.srvManagers[container.id].addEvent('onAccountRemoved', this.onAccountRemoved.bind(this));

		    var txtUsername = container.getElement('input[type=text]');
		    txtUsername.addEvent('keydown', this.onUsernameInputKeyDown.bindWithEvent(this));

		    var buttons = container.getElements('input[type=button]');
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
	    var form = e.target.getParent();
	    var container = form.getParent();
	    this.srvManagers[container.id].addButtonClicked(form);
	},
	
	onServiceRemoveClick: function(e) {
	    var form = e.target.getParent();
	    var container = form.getParent();
	    this.srvManagers[container.id].removeButtonClicked(form);
	}
	/************************************************************************************************/
});

Popego.TagCloud = new Class({

	// Constants
	INITIAL_REFRESH_INTERVAL: 1000, // 1 sec
	INTERVAL_GROW_FACTOR: 2, // interval duplicates with each refresh
	MAX_REFRESH_INTERVAL: 120000, // 2 min

	/* URLs */
	//URL_TOPTAGS: '/' + Popego.Env.username + '/services/toptags',
	
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
			this.tagsXHR.send('/' + Popego.Env.username + '/services/toptags?n=40');
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
		this.fireEvent('refresh');
	},

	triggerRefreshing: function() {
		this.interval = this.INITIAL_REFRESH_INTERVAL;
		$clear(this.timeout);
		this.refresh();
	}

});
Popego.TagCloud.implement(new Events);

Popego.DraggableTags = new Class({
	options: {
	    'setInterestURL': ''
	},
	initialize: function(draggables, droppable, options) {
	    this.setOptions(options);

	    this.draggables = draggables;
	    this.droppable = droppable;
	    
		this.makeDraggables();
		
	    this._tagOrigPos = [];
	    
	    this.droppable.addEvents({
		    'over': function(el, obj) {
			this.droppable.setStyle('color', 'white');
		    }.bind(this),
		    'leave': function(el, obj) {
			this.droppable.setStyle('color', '#ddd');
		    }.bind(this),
		    'drop': function(el, obj) {
			var tag = el.getText();
			el.remove();
			this.droppable.setStyle('color', '#ddd');
			this.setInterest(tag, 'down');
		    }.bind(this)
	    });
	},

        setInterest: function(tag, direction) {
	    var xhr = new Ajax(this.options.setInterestURL + '/' + tag, {data: { direction: direction }, method: 'post'}).request()
	},
	
	makeDraggables: function(draggables) {
		if (draggables) this.draggables = draggables;
		this.draggables.each(this.makeTagDraggable.bind(this));
	},

	makeTagDraggable: function(tag) {
		var startDrag = function(el) {
			this._tagOrigPos = [el.getStyle('top'), el.getStyle('left')];
	    }

	    new Drag.Move(tag, { onStart: startDrag.bind(this), droppables: [this.droppable] });
	    tag.addEvent('emptydrop', function(e) {
		                         new Fx.Styles(e.element, {duration:300, wait:false, transition: Fx.Transitions.Elastic.easeOut}).start({
						 'top' : this._tagOrigPos[0],
						 'left': this._tagOrigPos[1]
					        });
		                      }.bind(this));
	}

});

Popego.DraggableTags.implement(new Options);

window.addEvent('domready', function() {
	var w = new Popego.Services($ES('.content'));
	$ES('.coming_soon_wrapper').setStyle('opacity', 0.3);
});
