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
		var tooltip = $E('.tool-tip');
		if (tooltip) tooltip.setStyle('display', 'none');
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
    
    setGroupFilter: function(values, title, selectedIndex) {
        //TODO: Crear metodos genericos y estos usarlos de wrappers
        this.components.panelbar.panels.filters.setGroupFilter(values, title, selectedIndex);
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
