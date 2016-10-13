Popego.Media.Section = new Class({
	
	initialize: function(container, mediaObj){
		this.container = container;
		this.media = mediaObj;
		
        this.items = [];
	this.itemRequestDefaults = {count: 30, tags: 0};
	this.thereAreMoreItems = true;
	this.groups = [];
        
        this.views = {};
        this.defaultViewId = "list";
        this.currentView = null;
		
		this.loaded = false;
		this.visible = false;
        
        this._initializeViews();
        this._setBehaviors();
	},
    
    _initializeViews: function() {
        
    },
    
    _setBehaviors: function() {

    },
    
    setView: function(id) {
        if($defined(this.currentView)) {
            if (this.currentView == this.views[id]) return;
            this.currentView.hide();
        }
         
        this.currentView = this.views[id];
        
        if (!this.currentView.attached)
            this.currentView.attach(this.container);
        
        this.currentView.show();
    },
	
	show: function() {
		//si no esta cargada (no hay items) lo voy a buscar primero
		//y despues los muestro (populate)
		this.loaded = true;
        this.container.setStyle("display", "");
		this.visible = true;
	},
	
	hide: function() {
		this.container.setStyle("display", "none");
        this.visible = false;
	},
    
    unload: function(keepItems) {
        for (var v in this.views) {
            var view = this.views[v];
            if (view.attached) view.detach();
        }
        this.currentView = null;
        if(!keepItems) this.clearItems();
        this.load = false;
    },
	
	refresh: function() {
		this.clearItems();
		this.currentView.empty();
		this.requestItems();
	},
	
	update: function(items) {
		this.currentView.draw(items);
	},
	
	populate: function() {
		this.update(this.items);
	},

	getItemName: function() {
		return "item";
	},
    
	getGroupName: function() {
		return "group";
	},
    
    getItemIndexById: function(id) {
        var items = this.items;
        var n = items.length;
        for(var i=0; i<n; i++)
            if(items[i].url == id)
                return i;
        return null;
    },
    
    clearItems: function() {
        this.items = [];
    },
	
	requestItems: function(count, offset, group, tags) {
		var url = this.getRequestURL();
		if (group) url += "/" + encodeURIComponent(group);
		
		var querystring = {};
		querystring.count = $pick(count, this.itemRequestDefaults.count);
		querystring.offset = $pick(offset, this.items.length);
		if (tags || this.itemRequestDefaults.tags)
			querystring.tags = (tags || this.itemRequestDefaults.tags);
		
		var eventHandlers = {};
		eventHandlers.onComplete = this.onDataSuccess.bind(this);
		
		//TODO: timeout y error handling
		var jxhr = new Json.Remote(url+Popego.URLManager.toQueryString(querystring), eventHandlers).send();
	},
	
	getRequestURL: function(){
		//TODO: Usar URLManager
		return Popego.Env.baseUrl + "/" + Popego.Env.username + "/api/items/" + this.getItemName();
	},
    
    onDataSuccess: function(obj) {
		//TODO: no se que onda si aparecen items duplicados (el merge los elimina)
        var items = obj.items;
	this.thereAreMoreItems = !(items.length < obj.count);
        if (items.length > 0) {
            this.items.merge(items);
        	this.update(items);
        } else {
		this.currentView.update(); // para ocultar "Show N more items"
	}
	},
	
	onShowMore: function() {
		this.requestItems();
	}
});


Popego.Media.PicturesSection = Popego.Media.Section.extend({
	
	initialize: function(container, mediaObj) {
		this.parent(container, mediaObj);
			
		this.currentAlbum = null;
		this.currentAlbumIndex = null;
		this.currentItemIndex = null;
	},
    
    _initializeViews: function() {
        //TODO:lo estoy haciendo cuando se crean las secciones, quizas sea mejor la primera vez que se muestran
       	//Renderers de las vistas
        this.views.list = this.media.viewFactory.createView("list", new Popego.Media.PictureThumbsRenderer(), this, {panelbar:"filters", tooltips:true});
        this.views.detail = this.media.viewFactory.createView("detail", new Popego.Media.PictureDetailRenderer(), this, {panelbar:"navigation", buttonbar:"none"});
    },
    
    _setBehaviors: function() {
        this.views.list.addEvent("showmore", this.onShowMore.bind(this));
        this.views.list.addEvent("itemclick", this.onItemClick.bind(this));
        this.views.list.addListener(Popego.UI.FilterPanel.Events.GROUP_FILTER_CHANGE, this.onAlbumFilterChange.bind(this));
        
        this.views.detail.addListener(Popego.UI.NavigationPanel.Events.BACK_CLICK, this.onBackToMenuClick.bind(this));
        this.views.detail.addListener(Popego.UI.NavigationPanel.Events.PREV_CLICK, this.onShowPrev.bind(this));
        this.views.detail.addListener(Popego.UI.NavigationPanel.Events.NEXT_CLICK, this.onShowNext.bind(this));
    },
	
	show: function() {
		if(!$defined(this.currentView)) this.setView(this.defaultViewId);
        
		//TODO: separar un poco mejor esto. quizas antes de que se muestre recalcular el layout
		this.getAlbumList();
           
		if(!this.loaded) {
			this.requestItems(60);
			this.loaded = true;
		} else {
		var itemDivs = this.currentView.getItemDivs();
		this.currentView.update();
		this.currentView.setTooltips();
        }
        this.container.setStyle("display", "");
        this.visible = true;
	},
	
	refresh: function() {
		this.clearItems();
		this.currentView.empty();
		this.requestItems(60, 0, this.currentAlbum);
	},
	
	getItemName: function() {
		return "pictures";
	},
	
	getGroupName: function() {
		return "album";
	},
	
	getAlbumList: function() {
		if (this.groups.length != 0) {
			this.refreshAlbumList();
			return;
		}

		var eventHandlers = {};
		eventHandlers.onComplete = this.onDataSuccess.bind(this);
		
		//TODO: timeout y error handling
		var url = Popego.URLManager.getAlbumList(Popego.Env.username, this.getItemName());
		var onComplete = function(obj) {
			this.groups = Array.copy(obj.groups);
			this.refreshAlbumList();
		}.bind(this);
		var jxhr = new Json.Remote(url, {onComplete:onComplete}).send();
	},

	refreshAlbumList: function() {
		var groupname = this.getGroupName();
		groupname = groupname.charAt(0).toUpperCase() + groupname.substr(1);
		var comboValues = [];
		comboValues[0] = {value:0, name:"All "+groupname+"s"};
		var n = this.groups.length;
		for (var i=0; i<n; i++) {
			var name = this.groups[i].name;
			var value = name;
			if (name.length > 48) name = name.substr(0, 44) + '...';
			comboValues[i+1] = {value:value, name:name};
		}
		this.currentView.setGroupFilter(comboValues, "Select "+groupname+":", this.currentAlbumIndex);
	},
	
	onAlbumFilterChange: function(e) {
        var combo = e.nativeObject.target;
		var value = combo.options[combo.selectedIndex].value;
		this.currentAlbum = (value == 0) ? undefined : value;
		this.currentAlbumIndex = combo.selectedIndex;
		this.refresh();
	},
	
	onShowMore: function(e) {
		this.requestItems(null, null, this.currentAlbum);
	},
    
    onShowNext: function(e) {
        this.showItemDetailByIndex(++this.currentItemIndex);
    },
    
    onShowPrev: function(e) {
        this.showItemDetailByIndex(--this.currentItemIndex);
    },
    
    onBackToMenuClick: function(e) {
      this.setView("list");
    },
    
    onItemClick: function(e) {
        this.setView("detail");
        this.showItemDetailByIndex(this.getItemIndexById(e.target.getAttribute("id")));
    },
    
    //TODO: esto lo tendria que hacer la vista??
    showItemDetailByIndex: function(i) {
	    this.currentItemIndex = i;
        var next = i == this.items.length-1 ? false : true;
        var prev = i == 0 ? false : true;
        var navPanel = this.media.panelbar.panels.navigation;
        
        navPanel.setButtonsVisibility(true, prev, next);
		//alert(i + " - " + this.items.length);
        if (next) navPanel.setNextButtonTitle(this.items[i+1].title);
        if (prev) navPanel.setPrevButtonTitle(this.items[i-1].title);
        this.currentView.draw(this.items[i]);
    }
});


Popego.Media.VideosSection = Popego.Media.PicturesSection.extend({
    
    initialize: function(container, mediaObj) {
		this.parent(container, mediaObj);
	},
    
    _initializeViews: function() {
        //TODO:lo estoy haciendo cuando se crean las secciones, quizas sea mejor la primera vez que se muestran
       	//Renderers de las vistas
        this.views.list = this.media.viewFactory.createView("list", new Popego.Media.VideoThumbsRenderer(), this, {panelbar:"filters", tooltips:true, viewportSize:16});
        this.views.detail = this.media.viewFactory.createView("detail", new Popego.Media.VideoDetailRenderer(), this, {panelbar:"navigation", buttonbar:"none"});
    },
    
    _setBehaviors: function() {
        this.views.list.addEvent("showmore", this.onShowMore.bind(this));
        this.views.list.addEvent("itemclick", this.onItemClick.bind(this));
        this.views.list.addListener(Popego.UI.FilterPanel.Events.GROUP_FILTER_CHANGE, this.onAlbumFilterChange.bind(this));
        
        this.views.detail.addListener(Popego.UI.NavigationPanel.Events.BACK_CLICK, this.onBackToMenuClick.bind(this));
        this.views.detail.addListener(Popego.UI.NavigationPanel.Events.PREV_CLICK, this.onShowPrev.bind(this));
        this.views.detail.addListener(Popego.UI.NavigationPanel.Events.NEXT_CLICK, this.onShowNext.bind(this));
    },
    
	getItemName: function() {
		return "videos";
	},
    
	getGroupName: function() {
		return "playlist";
	}
});


Popego.Media.BookmarksSection = Popego.Media.Section.extend({

	initialize: function(container, mediaObj) {
		this.parent(container, mediaObj);
		this.itemRequestDefaults.tags = 7;
		this.itemRequestDefaults.count = 15;
	},

	_initializeViews: function () {
		this.views.list = this.media.viewFactory.createView("list", new Popego.Media.BookmarksRenderer(), this, {viewportSize:7});
	},

	_setBehaviors: function() {
		this.views.list.addEvent("showmore", this.onShowMore.bindWithEvent(this));
	},

	onShowMore: function (e) {
		e.stop(); // TODO: ver por que scrollea mal a veces
		this.requestItems();
	},

	show: function() {
		if(!$defined(this.currentView)) this.setView(this.defaultViewId);
		if(!this.loaded) {
			this.requestItems(15);
			this.loaded = true;
		} else {
			this.populate();
		}
		this.container.setStyle("display", "");
		this.visible = true;
	},

	refresh: function() {
		this.clearItems();
		//this.media.viewManager.currentView.empty();
		this.requestItems(null, 0, null);
	},

	getItemName: function() {
		return "bookmarks";
	}
});

Popego.Media.BlogsSection = Popego.Media.Section.extend({

	initialize: function(container, mediaObj) {
		this.parent(container, mediaObj);
		this.itemRequestDefaults.tags = 7;
		this.itemRequestDefaults.count = 10;
	},

	_initializeViews: function () {
		this.views.list = this.media.viewFactory.createView("list", new Popego.Media.BlogsRenderer(), this, {viewportSize:4});
	},

	_setBehaviors: function() {
		this.views.list.addEvent("showmore", this.onShowMore.bindWithEvent(this));
	},

	onShowMore: function (e) {
		e.stop(); // TODO: ver por que scrollea mal a veces
		this.requestItems();
	},

	show: function() {
		if(!$defined(this.currentView))
			this.setView(this.defaultViewId);
        
		if(!this.loaded) {
			this.requestItems(10);
			this.loaded = true;
		}
		this.container.setStyle("display", "");
		this.visible = true;
	},

	refresh: function() {
		this.clearItems();
		this.currentView.empty();
		this.requestItems(null, 0, null);
	},

	getItemName: function() {
		return "blogs";
	}

});

Popego.Media.QuotesSection = Popego.Media.Section.extend({
  	initialize: function(container, mediaObj) {
 		this.parent(container, mediaObj);
 		this.thereAreMoreItems = false;
 		//this.itemRequestDefaults.count = 15;
 		this.items = Array.copy(Popego.userQuotes);
 	},
 
 	_initializeViews: function () {
 		this.views.list = this.media.viewFactory.createView("list", new Popego.Media.QuotesRenderer(), this, {});
 	},
 
 	//_setBehaviors: function() {
 	//	this.views.list.addEvent("showmore", this.onShowMore.bindWithEvent(this));
 	//},
 	
 	//onShowMore: function (e) {
 	//	e.stop(); // TODO: ver por que scrollea mal a veces
 	//	this.requestItems();
 	//},
 
 	show: function() {
 		if(!$defined(this.currentView))
 			this.setView(this.defaultViewId);
         
 		if(!this.loaded) {
 			this.update(this.items);
 			//this.requestItems(15);
  			this.loaded = true;
  		}
  		this.container.setStyle("display", "");
		this.visible = true;
	},

	refresh: function() {
		this.clearItems();
		this.currentView.empty();
        this.update(this.items);
		//this.requestItems(null, 0, null);
	},

    requestItems: function () {
       // overriding to ignore
    },


	getItemName: function() {
		return "quotes";
	}

});


Popego.Media.MusicSection = Popego.Media.Section.extend({

	initialize: function(container, mediaObj) {
		this.parent(container, mediaObj);
		this.thereAreMoreItems = false;
	},

	_initializeViews: function () {
		this.views.list = this.media.viewFactory.createView("list", new Popego.Media.MusicRenderer(), this, {});
		this.views.ranking = this.media.viewFactory.createView("list", new Popego.Media.MusicRankingRenderer(), this, {panelbar: 'navigation', navbuttons: 'none', viewportSize:1}); //TODO: viewportSize, los items que chequea son item groups
	},

	_setBehaviors: function () {
        	this.views.list.addEvent("itemclick", this.onItemClick.bind(this));
		this.views.ranking.addListener(Popego.UI.NavigationPanel.Events.BACK_CLICK, this.onBackToMenuClick.bind(this));
	},

	onItemClick: function (e) {
		ev = new Event(e);
		target = ev.target;
		if (target.getTag() == 'a') {
			var ids = ['show_music', 'show_artists', 'show_songs'];
			var i = ids.indexOf(target.getProperty('id'));
			if (i >= 0) {
				ev.stop();
				this.setView('ranking');
				this.currentView.empty();
				this.currentView.draw(this.items[i]);
			}
		}
	},

	onBackToMenuClick: function () {
		this.setView('list');
	},
	
	show: function() {
		if (!$defined(this.currentView)) this.setView(this.defaultViewId);
		if(!this.loaded) {
			this.items = new Array(3);
			this.requestItems(10, 0, 'Top Artists');
			this.requestItems(10, 0, 'Top Tracks');
			this.requestItems(10, 0, 'Recently Listened');
			this.loaded = true;
		} else {
			this.currentView.update();
		}
		this.container.setStyle("display", "");
		this.visible = true;
        },

        onDataSuccess: function(obj) {
		var i;
		switch (obj.group) {
		case 'Top Artists': i = 1; break;
		case 'Top Tracks': i = 2; break;
		case 'Recently Listened': i = 0; break;
		default: break;
		}
		this.items[i] = obj.items;
		if (this.items[0] && this.items[1] && this.items[2])
			this.update(this.items);
        },

	getItemName: function() {
		return "music";
	}
});
