if (typeof Popego == "undefined") Popego = {};

//TODO: REFACTOREAR ESTOOOOOOOOOOOOOO!
/* Popego Environment */
if (typeof Popego.Env == 'undefined') {
	Popego.Env = {}; 
	Popego.Env.baseUrl = '';
}

Popego.Env.getUsername = function() {
  var pattern = /http:\/\/.*\/(\w+)\/api\/.*/; 
  var url = window.location.toString();
  var result = url.match(pattern); 
  if (result != null) { 
    return result[1];
  } else {
    throw new Error("Invalid Url");
  }
}

Popego.util = {}
Popego.util.upUntil = function(predicate, element) {
  while (element != null && !predicate(element)) {
    element = element.parentNode;
  }
  return element;
}

Popego.Env.username = Popego.Env.getUsername();


/*****************************************************************************/
/*
*/
Popego.Media = new Class({
	
	initialize: function(container){
		this.container = container;
		this.content = $E(".content", this.container);
		this.buttonbar = new Popego.UI.Buttonbar($E(".buttonbar"));
		this.panelbar = new Popego.UI.Panelbar($E(".bottompanels"));
		
        var components = {buttonbar:this.buttonbar, panelbar:this.panelbar};
		this.viewFactory = new Popego.Media.ViewFactory(this.content, components);
        
		//TODO: Se puede hacer un section manager
		this.sections = {};
		this.currentSection = null;
		this._initializeSections();
		
		this._setBehaviors();
		this.showSection(this.buttonbar.selectedButton.label);
		
	},
	
	_initializeSections: function(){
		//TODO: Ver detection dinamica
		this.sections = {};
		this.sections["pictures"] = new Popego.Media.PicturesSection(this.content, this);
		this.sections["videos"] = new Popego.Media.VideosSection(this.content, this);
		this.sections["bookmarks"] = new Popego.Media.BookmarksSection(this.content, this);
		this.sections["blogs"] = new Popego.Media.BlogsSection(this.content, this);
		this.sections["quotes"] = new Popego.Media.QuotesSection(this.content, this);
		this.sections["music"] = new Popego.Media.MusicSection(this.content, this);
	},
	
	_setBehaviors: function() {
		var onButtonbarClick = function(e) {
			this.showSection(e.target.selectedButton.label);
		}.bind(this);
		this.buttonbar.addEvent("buttonclick", onButtonbarClick);
        
        
        this.buttonbar.addEvent(Popego.UI.Buttonbar.Events.SHOW, this.refreshLayout.bind(this));
        this.buttonbar.addEvent(Popego.UI.Buttonbar.Events.HIDE, this.refreshLayout.bind(this));
        this.panelbar.addEvent(Popego.UI.Panelbar.Events.SHOW, this.refreshLayout.bind(this));
        this.panelbar.addEvent(Popego.UI.Panelbar.Events.HIDE, this.refreshLayout.bind(this));
        
	},
	
	showSection: function(sectionId){
		if (this.currentSection) this.currentSection.unload(true);
		this.currentSection = this.sections[sectionId];
		this.currentSection.show();
        this.refreshLayout();
	},
    
    refreshLayout: function() {
        var height;
        if (this.panelbar.visible)
            if (this.buttonbar.visible)
                height = 320;
            else
                height = 370
        else
            if (this.buttonbar.visible)
                height = 370
            else
                height = 400
        
        this.content.setStyle("height", height);
    }
	
});

window.addEvent('load', function() {
	mediaController = new Popego.Media($ES('.media'));
});

Popego.Media.ViewFactory = new Class({
    components: {},
    templates: {},
    views: [],
    
    initialize: function(container, components) {
        this.container = container;
        if($defined(components)) this.components = components;
        
        this._loadTemplates();
        this._setComponentListeners();
	},
    
    _loadTemplates: function() {
        //levanto los templates de las vistas del DOM y los remuevo
		$ES(".view").each(function(viewDiv) {
			this.templates[viewDiv.getAttribute("id")] = viewDiv.clone();
		}.bind(this));
        
        this.container.empty();
    },
    
    _setComponentListeners: function() {
        //yo solo escucho a los componentes y luego les aviso a las vistas
        var onEvent = function(e) {
            this.views.each(function(v){
                //le aviso a la vista solo si esta visible
                //y como en ppio solo una puede estarlo me voy
                if (v.attached && v.visible) {
                    v.listen(e);                    
                    return;
                }
            });
        }.bind(this);
        $each(this.components, function(comp, key){
            comp.getEventList().each( function(evt) {
                comp.addEvent(evt, onEvent);
            }.bind(this))
        }, this);
    },
    
    createView: function(id, renderer, section, options) {
        var view;
        if (id=="list")
            view = new Popego.Media.ListView(this.templates[id].clone(), renderer, section, options);
        else if (id=="detail")
            view = new Popego.Media.DetailView(this.templates[id].clone(), renderer, section, options);
        
        view.id = id;
        view.setComponents(this.components);
        this.views.include(view);
        
        return view;
    }
});


Popego.Media.View = new Class({
	
    options: {
        panelbar: null,
        buttonbar: "show",
        tooltips: null,
	navbuttons: "block",
        viewportSize: 20 //en items que entran por pantalla
    },
    
    
	initialize: function(container, renderer, section, options) {
		this.container = container;
		this.itemRenderer = renderer;
        this.section = section;
		this.setOptions(options);
		
        this.container.addClass(this.section.getItemName());
        this.content = this.container;
        this.id = "view";
        this.attached = false;
        this.visible = false;
        
        this.components = {};
        this.listeners = {};
        this.elements = {};
        
        // El comportamiendo se agrega cuando se attacha
        /*this.elements = {};
		this._setElements();
		this._setBehaviors();*/
	},
    
    _initializeLayout: function() {
        var panel = this.options.panelbar
        if (!panel) this.components.panelbar.hide();
        else this.components.panelbar.showPanel(panel);
	if (this.options.navbuttons != 'block') {
		this.components.panelbar.panels.navigation.setButtonsVisibility(true, false, false);
	 } else {
		this.components.panelbar.panels.navigation.setButtonsVisibility(true, true, true);
	 }
        if (!this.options.buttonbar || this.options.buttonbar != "show") this.components.buttonbar.hide();
        else this.components.buttonbar.show();
    },
	
	_setElements: function() {
		//se setean los elementos particulares de la vista
	},
	
	_setBehaviors: function() {
		//se setean los comportamientos propios de la vista
	},
    
    /****/
    setRenderer: function(itemRenderer) {
		this.itemRenderer = itemRenderer;
	},
	
	setSection: function(section) {
		this.section = section;
	},
    
    setComponents: function(components) {
        this.components = components;
    },
    /****/
    
    /****/
    addListener: function(eventName, listener) {
		var listeners = this.listeners[eventName];
		if (!$defined(listeners)) {
            listeners = this.listeners[eventName] = [];
        }
			
		listeners.include(listener);
	},
	
	removeListener: function(eventName, listener) {
		var listeners = this.listeners[eventName];
		listeners.remove(listener);
	},
    
    listen: function(e) {
        if (!$defined(e)) return;

        if (listeners = this.listeners[e.type]) {
            listeners.each(function(listener) {
                listener(e);
            }.bind(this))
        }
    },
    /****/
    
    attach: function(parentEl) {
        //TODO: ver que onda con los eventos y en todo caso hacer show y hide
        parentEl.adopt(this.container);
        if (!this.loaded) this.load();
        this.attached = true;
        
    },
    
    detach: function() {
        if (this.loaded) this.unload();
        
		var el = this.container.clone();
        if (this.container.parentNode) this.container.remove();
        this.container = el;
        this.attached = false;
    },
	
	draw: function(items) {
		// important efficiency issue: insert items HTML
		// after concatenated, not in every iteration
		var html = '';
		var n = items.length;
		for (var i = 0; i < n; i++)
			html += this.itemRenderer.draw(items[i], i);
		this.content.innerHTML += html;
		if (this.options.tooltips) this.setTooltips();
		this.update();
	},

	setTooltips: function () {
	},
    
	empty: function() {
		this.content.empty();
		this.update();
	},
	
	update: function() {
	},

	show: function() {
		if (!this.loaded) this.load();
		this._initializeLayout();
		this.container.setStyle("display", "");
		this.visible = true;
	},
	
	hide: function() {
        this.container.setStyle("display", "none");
		this.visible = false;
	},
    
    load: function() {
        this.elements = {};
		this._setElements();
        this._setBehaviors();
        this._initializeLayout();
        this.loaded = true;
    },
    
    unload: function() {
        //TODO: remover eventos
        this.loaded = false;
    },
    
    getItemDivs: function() {
        return $ES(".item", this.content);
    }
        
});
Popego.Media.View.implement(new Events, new Options);

Popego.Media.ListView = Popego.Media.View.extend({
	
	initialize: function(container, renderer, section, options) {
		this.parent(container, renderer, section, options);
        
        this.tooltips = []; //Tips objects. Se van sumando en el 'show more'
	},
    
    _initializeLayout: function() {
        this.parent();
        this.elements.showMore.setStyle("display", "none");
        $E('a', this.elements.showMore).setText("Show "+this.section.itemRequestDefaults.count+" more " + this.section.getItemName() + ".");
    },
	
	_setElements: function() {
        this.content = $E(".content", this.container);
		this.elements.boxShadows = $ES(".box_shadow", this.container);
		this.elements.showMore = $E(".show_more", this.container); 
	},
	
	_setBehaviors: function() {
        var onShowMoreClick = function(e) {
            new Event(e).stop();
			this.fireEvent("showmore", e);
		}.bind(this);
		$E("a", this.elements.showMore).addEvent("click", onShowMoreClick);
        
		var onItemClick = function(e) {
			//TODO: se esta disparando si apreto fuera del content tambien
			this.fireEvent("itemclick", e);
		};
		this.content.addEvent("click", onItemClick.bindWithEvent(this));
	},
    
	setTooltips: function(items) {
		var itemNodes = $ES(".item", this.content);
		$each(itemNodes, function (node, index) {
			if (!node.getProperty('title')) {
				node.setProperty('title', this.itemRenderer.generateTitle(this.section.items[index]));
			}
		}, this);
		this.tooltips = new Tips(itemNodes, {
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
    
    update: function() {
		this.parent();
        
		var n = this.section.items.length;
		var boxStyle = "none";
		var showStyle = "none";
		
		if (n>this.options.viewportSize) boxStyle = "";
		if (this.section.thereAreMoreItems) showStyle = "";
		
		this.elements.boxShadows.setStyle("display", boxStyle);
		this.elements.showMore.setStyle("display", showStyle);
        
	},
    
    setGroupFilter: function(values, title) {
        //TODO: Crear metodos genericos y estos usarlos de wrappers
        this.components.panelbar.panels.filters.setGroupFilter(values, title);
    }
});

Popego.Media.DetailView = Popego.Media.View.extend({
	
	initialize: function(container, renderer, section, options) {
		this.parent(container, renderer, section, options);
	},
    
    _setElements: function() {
        this.content = $E(".content", this.container);
    },
    
    draw: function(item) {
		var html = this.itemRenderer.draw(item);
		this.content.setHTML(html);
		this.update();
	}
});
Popego.Media.Section = new Class({
	
	initialize: function(container, mediaObj){
		this.container = container;
		this.media = mediaObj;
		
        this.items = [];
	this.itemRequestDefaults = {count: 30, tags: 0};
	this.thereAreMoreItems = true;
        
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
	
	getAlbumList: function() {
		var eventHandlers = {};
		eventHandlers.onComplete = this.onDataSuccess.bind(this);
		
		//TODO: timeout y error handling
		var url = Popego.URLManager.getAlbumList(Popego.Env.username, this.getItemName());
		var onComplete = function(obj) {
			var groups = obj.groups;
			var n = groups.length;
			var comboValues = [];
			comboValues[0] = {value:0, name:"All Albums"};
			for (var i=0; i<n; i++) {
				var name = groups[i].name;
				comboValues[i+1] = {value:name, name:name};
			}
            this.currentView.setGroupFilter(comboValues, "Select Album:");
		}.bind(this);
		var jxhr = new Json.Remote(url, {onComplete:onComplete}).send();
	},
	
	onAlbumFilterChange: function(e) {
        var combo = e.nativeObject.target;
		var value = combo.options[combo.selectedIndex].value;
		this.currentAlbum = value==0 ? undefined : value;
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
Popego.Media.ItemRenderer = new Class({
	
	initialize: function(){
		this.itemHTML = "<div>Item default</div>";
		this.titleHTML = "this is the <strong>title</strong>"
		this.data = {};		
	},
	
	draw: function(data) {
		var s = '';
		for (var i in data) {
			s += i + ': ' + data[i] + '<br/>';
		}
		return '<div>' + s + '</div>';
	},
	
	formatDate: function(s) {
		var a = s.split(" ").join(",").split("-").join(",").split(":").join(",").split(",");
		var d = new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]);
		return d.format('mediumDate');
	},
	
	formatDateAsIntervalInWords: function(s) {
		var a = s.split(" ").join(",").split("-").join(",").split(":").join(",").split(",");
		var d = new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]);
		return this.intervalInWords(d);
	},

	intervalInWords: function (from, to) {
		if (!to) to = new Date();
		var millisec_per_minute = 1000 * 60;
		var millisec_interval = Math.abs(to.getTime() - from.getTime());
		var i = Math.ceil(millisec_interval / millisec_per_minute); // interval in minutes
		if (i < 1) return ('less than a minute');
		if (i < 50) return (i + ' minute' + (i == 1 ? '' : 's'));
		if (i < 90) return ('about one hour');
		if (i < 1080) return (Math.round(i / 60) + ' hours');
		if (i < 1440) return ('one day');
		if (i < 2100) return ('about one day');
		if (i < 2880) return ('almost two days');
		else return (Math.round(i / 1440) + ' days');
	},

	truncate: function(s, maxlen) {
		return s.length > maxlen ? s.substr(0, maxlen - 3) + '...' : s;
	},
	
	escapeHTML: function(s) {
		var div = new Element('div').setText(s);
		return div.innerHTML.replace(/"/g, '&quot;');
	},
	
	generateTitle: function(data) {
		var title = this.titleHTML.replace("${ASSET:FAVICON_SERVICE}", "/images/icons/" + data.service.toLowerCase() + "_favicon.png"); //TODO: Usar Popego.Config
		title = title.replace("${TITLE}", data.title);
		title = title.replace("${DATE}", this.formatDate(data.date));
		return this.escapeHTML(title);
	}

});

Popego.Media.PictureThumbsRenderer = Popego.Media.ItemRenderer.extend({
	initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}';
		
		var n = 0, itemHTML = [];
		//TODO: Ver performance por el tema replace!!
		itemHTML[n++] = '<div class="item" title="' + this.titleHTML + '" style="background:url(/images/widget/spinner_box_medium.gif) no-repeat;">';
		itemHTML[n++] = '<a href="#">';
		itemHTML[n++] = '<img style="background-image:url(${THUMBNAIL});" id="${ID}" src="/images/widget/blank.gif"/>';
		itemHTML[n++] = '</a>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${ID}", data.url);
		html = html.replace("${TITLE}", this.escapeHTML(data.title));
		html = html.replace("${DESCRIPTION}", data.description);
		html = html.replace("${DATE}", this.formatDate(data.date));
		html = html.replace("${THUMBNAIL}", data.thumbnail);
		html = html.replace("${URL}", data.url);
		html = html.replace("${EXTERNAL_URL}", data.external_url);
		html = html.replace("${ASSET:FAVICON_SERVICE}", "/images/icons/" + data.service.toLowerCase() + "_favicon.png"); //TODO: Usar Popego.Config
		html = html.replace("${SERVICE}", data.service);
		
		this.data = data;
		return html;
	}
});

Popego.Media.PictureDetailRenderer = Popego.Media.ItemRenderer.extend({
    initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}';
		
		var n = 0, itemHTML = [];
		itemHTML[n++] = '<div class="item" style=" #position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">';
		itemHTML[n++] = '<a href="${EXTERNAL_URL}" target="_blank">';
		itemHTML[n++] = '<img src="${URL}"  style=" #position: relative; #top: -50%">';
		itemHTML[n++] = '</a>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${EXTERNAL_URL}", data.external_url);
		html = html.replace("${URL}", data.url);
		
		this.data = data;
		return html;
	}
});


Popego.Media.VideoThumbsRenderer = Popego.Media.ItemRenderer.extend({
	initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}"';
		
		var n = 0, itemHTML = [];
		itemHTML[n++] = '<div class="item" title="<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}" style="background:url(/images/widget/spinner_box_large.gif) no-repeat;">';
		itemHTML[n++] = '<a href="#">';
		itemHTML[n++] = '<div class="image_strip">';
		itemHTML[n++] = '<img id="${ID}" style="background:url(${THUMBNAILS[0]}) no-repeat;" src="/images/widget/blank.gif" />';
		itemHTML[n++] = '<img id="${ID}" style="background:url(${THUMBNAILS[1]}) no-repeat; display:none;"/>';
		itemHTML[n++] = '<img id="${ID}" style="background:url(${THUMBNAILS[2]}) no-repeat; display:none;"/>';
		itemHTML[n++] = '</div>';
		itemHTML[n++] = '</a>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${ID}", data.url);
		html = html.replace("${ID}", data.url);
		html = html.replace("${ID}", data.url);
		html = html.replace("${TITLE}", this.escapeHTML(data.title));
		html = html.replace("${DESCRIPTION}", data.description);
		html = html.replace("${DATE}", this.formatDate(data.date));
		html = html.replace("${THUMBNAILS[0]}", data.thumbnails[0]);
		html = html.replace("${THUMBNAILS[1]}", data.thumbnails[0]);
		html = html.replace("${THUMBNAILS[2]}", data.thumbnails[0]);
		html = html.replace("${URL}", data.url);
		html = html.replace("${ASSET:FAVICON_SERVICE}", "/images/icons/" + data.service.toLowerCase() + "_favicon.png"); //TODO: Usar Popego.Config
		
		this.data = data;
		return html;
	}
});


Popego.Media.VideoDetailRenderer = Popego.Media.ItemRenderer.extend({
    initialize: function() {
		this.parent();
		
		this.titleHTML = '<img src=\'${ASSET:FAVICON_SERVICE}\'><h1>${TITLE}</h1>${DATE}"';
		
		var n = 0, itemHTML = [];
		itemHTML[n++] = '<div class="item" style="#position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">';
		itemHTML[n++] = '<object width="400" height="336px">';
		itemHTML[n++] = '<param name="movie" value="${URL}"></param>';
		itemHTML[n++] = '<param name="wmode" value="transparent"></param>';
        itemHTML[n++] = '<embed width="400" height="336" src="${URL}" type="application/x-shockwave-flash" wmode="transparent"></embed>';
        itemHTML[n++] = '</object>';
		itemHTML[n++] = '</div>';
		this.itemHTML = itemHTML.join("");
	},
	
	draw: function(data) {
		var html = this.itemHTML.replace("${URL}", data.url);
        html = html.replace("${URL}", data.url); //reemplaza la primer aparicion
        
		this.data = data;
		return html;
	}
});

Popego.Media.BookmarksRenderer = Popego.Media.ItemRenderer.extend({

	initialize: function() {
		this.parent();
		this.itemHTML = this.getItemHTMLTemplate();
		this.tagHTML = '<li class="hits_lowest"><a href="javascript:void(0);">${TAG}</a></li>';
	},

	getItemHTMLTemplate: function() {
		var t = [], i = 0;
		// TODO: revisar css y estilos inline
		//<!--style="width: 95%; height: 37px;"-->
		t[i++] = '<div id="bookmark-${ID}" class="item">';
		t[i++] = '<div class="link_delicious" style="float: left;">';
		t[i++] = '<a href="${EXTERNAL_URL}" target="_blank">';
		t[i++] = '<h3>${POPULARITY}</h3> people</a></div>';
		t[i++] = '<div class="detail" style="width: 330px;">';
		t[i++] = '<img src="/images/icons/${SERVICE}_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">${DATE}</span>';
		t[i++] = '<h3><a href="${URL}" title="${TITLE}" target="_blank">${TRUNCATED_TITLE}</a></h3>';
		t[i++] = '<div class="tag_cloud"><ul>${TAGS}</ul></div></div></div>';
		return t.join('');
	},

	draw: function(data) {
		// gathering data attributes in r
		var r = {};
		['id', 'external_url', 'popularity', 'service', 'date', 'url',
				'title', 'tags'].each(function (i) {
			r[i] = data[i];
		});
		// attribute conversions
		r.service = r.service.toLowerCase();
		r.date = this.formatDate(r.date);
		r.tags = this.formatTags(r.tags);
		r.truncated_title = this.truncate($pick(r.title, ''), 36);
		// replacing in template
		var html = this.itemHTML;
		for (var i in r) {
			var s = '${' + i.toUpperCase() +'}';
			html = html.replace(s, r[i]);
		}
		return html;
	},

	formatTags: function(tags) {
		var s = '';
		if (tags.length > 6) {
			tags = Array.copy(tags, 0, 5);
			tags.push('...');
		}
		if ($type(tags) == $type([])) {
			tags.each(function (i) {
				if (s) s += ' + ';
				s += this.tagHTML.replace('${TAG}', i);
			}.bind(this));
		}
		return s;
	}
});

Popego.Media.BlogsRenderer = Popego.Media.ItemRenderer.extend({

	initialize: function() {
		this.parent();
		this.itemHTML = this.getItemHTMLTemplate();
		this.tagHTML = '<li class="hits_lowest"><a href="javascript:void(0);">${TAG}</a></li>';
		
		this.tempDescription = "Aca tiene que haber una descripcion pero aparentemente no se esta persistiendo. Aunque el agente si trae la data. Aca tiene que haber una descripcion pero aparentemente no se esta persistiendo. Aunque el agente si trae la data.";
	},

	getItemHTMLTemplate: function() {
		var t = [], i = 0;
		t[i++] = '<div id="article-${ID}" class="item">';
		//t[i++] = '<div class="index_item_detail">';
		t[i++] = '<img class="icon" src="/images/icons/blog_favicon.png"/>';
		t[i++] = '<span class="date">${DATE}</span>';
		t[i++] = '<h3><a title="Read entire post." href="${EXTERNAL_URL}" target="_blank">${TITLE}</a></h3>';
		t[i++] = '<span class="fulldesc" style="display: none;">${DESCRIPTION}</span>';
		t[i++] = '<span class="shortdesc">${TRUNCATED_DESCRIPTION}';
		// TODO: este javascript inline es horrible
		t[i++] = ' (<a href="javascript:void(0);" onclick="javascript: var fulldesc = $E(\'span.fulldesc\', this.getParent()); ';
		t[i++] = 'var shortdesc = $E(\'span.shortdesc\', this.getParent()); ';
		t[i++] = 'if (shortdesc) shortdesc.setStyle(\'display\', \'none\'); if (fulldesc) fulldesc.setStyle(\'display\', \'block\');';
		t[i++] = 'return false;">more</a>)</span>';
		//TODO: se necesitaria la account
		//t[i++] = '<div style="margin-top: 6px;">';
		//t[i++] = '<strong>Source:</strong>';
		//t[i++] = '<a href="#">www.gamesareart.com</a>';
		//t[i++] = '</div>';
		t[i++] = '<div class="tag_cloud"><ul>';
		t[i++] = '<li class="hits_lowest"><strong>Tags:</strong></li> ';
		t[i++] = '${TAGS}</ul></div></div>';
		return t.join('');
	},

	draw: function(data) {
		// gathering data attributes in r
		var r = {};
		['id', 'external_url', 'description', 'date', 'title', 'tags']
			.each(function (i) {
			r[i] = data[i];
		});
		// attribute conversions
		r.date = this.formatDate(r.date);
		r.tags = this.formatTags(r.tags);
		r.description = this.tempDescription;
		r.truncated_description = this.truncate(this.tempDescription, 128);
		// replacing in template
		var html = this.itemHTML;
		for (var i in r) {
			var s = '${' + i.toUpperCase() +'}';
			html = html.replace(s, r[i]);
		}

		return html;

	},

	formatTags: function(tags) {
		var s = '';
		if (tags.length > 6) {
			tags = Array.copy(tags, 0, 5);
			tags.push('...');
		}
		if ($type(tags) == $type([])) {
			tags.each(function (i) {
				if (s) s += ' + ';
				s += this.tagHTML.replace('${TAG}', i);
			}.bind(this));

		}
		return s;
	}

});

Popego.Media.QuotesRenderer = Popego.Media.ItemRenderer.extend({

	initialize: function() {
		this.parent();
		this.itemHTML = this.getItemHTMLTemplate();
	},

	getItemHTMLTemplate: function() {
		// TODO: en el ${TITLE} se podrian detectar los links
		// (http://...) y los replies (@username)
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post">';
		t[i++] = '<div class="index_item_detail">';
		t[i++] = '<a title="Read this quote at ${SERVICE}" href="${EXTERNAL_URL}" target="_blank">';
		t[i++] = '<img class="icon" src="/images/icons/${SERVICE_LOWERCASE}_favicon.png"/></a>';
		t[i++] = '<span class="date">${DATE}</span>';
		t[i++] = '<p>${TITLE}</p>';
		t[i++] = '</div></div>';
		return t.join('');
	},

	draw: function(data) {
 		r = {}
 		r.external_url = data.getExternalURL();
 		r.service = 'Twitter'; // TODO: un-hard-code
 		r.title = data.getText();
 		r.date = data.getTimeInWords();
 		r.service_lowercase = $pick(r.service).toLowerCase();

		// replacing in template
		var html = this.itemHTML;
		for (var i in r) {
			var s = '${' + i.toUpperCase() +'}';
			html = html.replace(s, r[i]);
		}

		return html;
	}

});

Popego.Media.MusicRankingRenderer = Popego.Media.ItemRenderer.extend({

	drawRankedMusic: function(data, index) {
		var t = [], i = 0;
		t[i++] = '<div class="item">';
		t[i++] = '<div class="artist spinner_box_small">';
		t[i++] = '<a href="'+data.external_url+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.title+'"></a>';
		t[i++] = '</div>';
		t[i++] = '<div class="detail">';
		// Nota: Randomizar la palabra 'interpreted by' ademas por 'sung by',  'in the voice of'
		t[i++] = '<a href="'+data.external_url+'" target="_blank">'+data.title+'</a> ';
		t[i++] = 'by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank"><strong>'+data.artist.name+'</strong></a>';
		t[i++] = '<p><span class="ranking_score">Listened '+this.formatDateAsIntervalInWords(data.date)+' ago.</span></p>';
		t[i++] = '</div>';
		t[i++] = '<div class="ranking_position">#'+(index+1)+'</div>';
		t[i++] = '</div>';
		return t.join('');
	},

	drawRankedSong: function(data, index) {
		var t = [], i = 0;
		t[i++] = '<div class="item">';
		t[i++] = '<div class="artist spinner_box_small">';
		t[i++] = '<a href="'+data.external_url+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.title+'"></a>';
		t[i++] = '</div>';
		t[i++] = '<div class="detail">';
		t[i++] = '<a href="'+data.external_url+'" target="_blank">'+data.title+'</a> ';
		t[i++] = 'by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank"><strong>'+data.artist.name+'</strong></a>';
		t[i++] = '<p><span class="ranking_score">Listened '+this.formatDateAsIntervalInWords(data.date)+' ago.</span></p>';
		t[i++] = '</div>';
		t[i++] = '<div class="ranking_position">#'+(index+1)+'</div>';
		t[i++] = '</div>';
		return t.join('');
	},

	drawRankedArtist: function (data, index) {
		var t = [], i = 0;
		t[i++] = '<div class="item">';
		t[i++] = '<div class="artist spinner_box_small">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank">';
		t[i++] = '<img src="'+data.thumbnail+'" title="'+data.title+'"></a></div>';
		t[i++] = '<div class="detail">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank">'+data.title+'</a>';
		t[i++] = '<p><span class="ranking_score">Listened '+data.playcount+' times.</span></p></div>';
		t[i++] = '<div class="ranking_position">#'+(index+1)+'</div></div>';
		return t.join('');
	},

	draw: function (data, index) {
		if (data.type == 'artist') {
			return this.drawRankedArtist(data, index);
		} else if (data.type == 'song') {
			return data.playcount ? this.drawRankedSong(data, index) : this.drawRankedMusic(data, index);
		}
		return '<div>No music information available</div>';
	}
});

Popego.Media.MusicRenderer = Popego.Media.ItemRenderer.extend({

	// TODO: descablear lastfm...
	drawArtist: function(data, data2) {
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post" style="width:390px">';
		t[i++] = '<div class="artist spinner_box">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank"><img src="'+data.thumbnail+'" title="'+data.title+'"></a>';
		t[i++] = '</div><div class="index_item_detail">';
		t[i++] = '<img src="http://assets1.popego.com/images/icons/lastfm_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">'+this.formatDate(data.date)+'</span>';
		t[i++] = '<h3>Favorite Artists</h3>';
		t[i++] = '<p style="margin-bottom:0px;margin-top:5px"><a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.title)+'" target="_blank"><strong>'+data.title+'</strong></a> ';
		if (data2) t[i++] = 'and <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data2.title)+'" target="_blank"><strong>'+data2.title+'</strong></a> ';
		t[i++] = (data2 ? 'are among': 'is one of') + ' the favorites.';
		t[i++] = '</p><p style="margin-top:0px"><span class="see_more btn_next">';
		t[i++] = '<a id="show_artists" href="javascript:void(0);">See Top 10 Artists</a></span></p>';
		t[i++] = '</div></div>';
		return t.join('');
	},

	drawSong: function(data) { // Favorite Songs
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post" style="width:390px">';
		t[i++] = '<div class="artist spinner_box">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.artist.name+'"></a></div>';
		t[i++] = '<div class="index_item_detail">';
		t[i++] = '<img src="http://assets1.popego.com/images/icons/lastfm_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">'+this.formatDate(data.date)+'</span>';
		t[i++] = '<h3>Favorite Songs </h3>';
		t[i++] = '<p style="margin-bottom:0px;margin-top:5px"><a href="'+data.external_url+'" target="_blank">'+data.title+'</a>, ';
		t[i++] = 'interpreted by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<strong>'+data.artist.name+'</strong></a>';
		t[i++] = ' has been listened <strong>'+data.playcount+'</strong> times.</p>'; // TODO:  "by ' + Popego.Env.username + ' " ??
		t[i++] = '<p style="margin-top:0px"><span class="see_more btn_next">';
		t[i++] = '<a id="show_songs" href="javascript:void(0);">See Top 10 Songs</a></span></p>';
		t[i++] = '</div>';
		t[i++] = '</div>';
		return t.join('');
	},

	drawMusic: function(data) { // Recently Listened
		var t = [], i = 0;
		t[i++] = '<div class="index_item_post" style="width:390px">';
		t[i++] = '<div class="artist spinner_box">';
		t[i++] = '<a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<img src="'+data.artist.thumbnail+'" title="'+data.artist.name+'"></a>';
		t[i++] = '</div><div class="index_item_detail">';
		t[i++] = '<img src="http://assets1.popego.com/images/icons/lastfm_favicon.png" class="icon pngfix_scale">';
		t[i++] = '<span class="date">'+this.formatDate(data.date)+'</span>';
		t[i++] = '<h3>Last Songs Listened</h3>';
		t[i++] = '<p style="margin-bottom:0px;margin-top:5px"><a href="'+data.external_url+'" target="_blank">'+data.title+'</a>, ';
		t[i++] = 'interpreted by <a href="http://www.lastfm.com/artist/'+encodeURIComponent(data.artist.name)+'" target="_blank">';
		t[i++] = '<strong>'+data.artist.name+'</strong></a> just about '+this.formatDateAsIntervalInWords(data.date)+' ago.</p>';
		t[i++] = '<p style="margin-top:0px"><span class="see_more btn_next"><a id="show_music" href="javascript:void(0);">Last 10 tracks played</a></span></p>';
		t[i++] = '</div></div>';
		return t.join('');
	},

	draw: function(data) {
		var html = '<div>No music available</div>';
		var item = data[0];
		if (!item)
			return html;
		if (item.type == 'artist') {
			html = this.drawArtist(data[0], data[1]);
		} else if (item.type == 'song') {
			html = item.playcount ? this.drawSong(item)
				: this.drawMusic(item);
		}
		return html;
	}

});
