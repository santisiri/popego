if (typeof(Popego.UI) == "undefined") {
    
    Popego.UI = {};
    Popego.UI.Event = new Class({
        type: "event",
        target: null,
        nativeObject: null,
        
        initialize: function(type, target, e) {
            this.type = type,
            this.target = target,
            this.nativeObject = e
        }
    });
    Popego.UI.Component = new Class({
        className: "Popego.UI.Component",
        children: [],
        
        initialize: function(){
            //TODO: Por ahora nada, en el futuro se puede armar una arq de componentes copada
        },
        
        getEventList: function() {
            var events = [];
            $each(eval(this.className).Events, function(value, key){
                events.include(value);
            });
            //TODO: por ahora solo agarro un nivel mas abajo
            $each(this.children, function(child, key){
                child.getEventList().each( function(evt) {
                    events.include(evt);
                });
            });
            return events;
        }
    });
    Popego.UI.Component.Events = {};
    Popego.UI.Component.implement(new Events);
    
    Popego.UI.Button = Popego.UI.Component.extend({
        className: "Popego.UI.Button",
        
        selected: false,
        disabled: true,
        label: "",
        
        //<li class="selected"><span>button 1</span></li>
        initialize: function(container){
            this.container = container;
            this.label = this.container.getElement("span").getText();
            
            var className = this.container.className;
            if (className == "selected") this.select();
            else if (className == "disabled") this.disabled = true;
            else this.unselect();
        },
        
        select: function() {
            this.container.className = "selected";
            this.container.getElement('span').setHTML(this.label);
            this.selected = true;
        },
        
        unselect: function() {
            this.container.className = "";
            var span = new Element('span');
            var a = new Element('a');
            a.setText(this.label);
            var onClick = function(e) {
                var evtObj = new Popego.UI.Event(Popego.UI.Button.Events.BUTTON_CLICK, this, e);
                this.fireEvent(evtObj.type, evtObj);
            }
            a.addEvent('click', onClick.bind(this));
            span.adopt(a);
            this.container.getElement('span').replaceWith(span);
            this.selected = false;
        }
    });
    Popego.UI.Button.Events = {
        BUTTON_CLICK: "buttonclick"
    }
    
    Popego.UI.Buttonbar = Popego.UI.Component.extend({
        className: "Popego.UI.Buttonbar",
        /*
         <div>
            <ul>
                <li class="selected"><span>button 1</span></li>
                <li><span><a href="#">videos</a></span></li>
                <li class="disabled"><span><a href="#"></a><span></li>			
            </ul>
          </div>
        */
        initialize: function(container){
            this.container = container;
            
            this.children = [];
            this.selectedButton = null;
            
            var n = 0;
            $ES("li", this.container).each(function(li){
                var btn = new Popego.UI.Button(li);
                var onClick = function(e) {
                    this.selectedButton.unselect();
                    this.selectedButton = e.target;
                    e.target.select();
                    e.target = this;
                    this.fireEvent(e.type, e);
                }
                btn.addEvent(Popego.UI.Button.Events.BUTTON_CLICK, onClick.bindWithEvent(this));
                if (btn.selected) this.selectedButton = btn;
                this.children[n++] = btn;
            }.bind(this));
            
            if (!$defined(this.selectedButton))
                this.selectByIndex(1);
        },
        
        selectByIndex: function(idx) {
            //TODO: errors
            if ($defined(this.selectedButton))
                this.selectedButton.unselect();
            this.selectedButton = this.children[idx-1];
            this.selectedButton.select();
        },
        
        show: function() {
            this.container.setStyle("display", "");
            this.visible = true;
            var evtObj = new Popego.UI.Event(Popego.UI.Buttonbar.Events.SHOW, this);
            this.fireEvent(evtObj.type, evtObj);
        },
        
        hide: function() {
            this.container.setStyle("display", "none");
            this.visible = false;
            var evtObj = new Popego.UI.Event(Popego.UI.Buttonbar.Events.HIDE, this);
            this.fireEvent(evtObj.type, evtObj);
        }
    });
    
    Popego.UI.Buttonbar.Events = {
        SHOW: "showbuttonbar",
        HIDE: "hidebuttonbar"
    };
    
    
    Popego.UI.Panel = Popego.UI.Component.extend({
        className: "Popego.UI.Panel",
        id: "generic",
        
        initialize: function(container){
            this.container = container;
            
            this.visible = false;
            this.hide();
            
            this.elements = {};
            this._setElements();		
            this._setBehaviors();
        },
        
        _setElements: function() {
            //se setean los elementos particulares de la vista
        },
        
        _setBehaviors: function() {
            //se setean los comportamientos propios de la vista
        },
        
        show: function() {
            this.container.setStyle("display", "");
            this.visible = true;
        },
        
        hide: function() {
            this.container.setStyle("display", "none");
            this.visible = false;
        }
    });
    
    
    Popego.UI.NavigationPanel = Popego.UI.Panel.extend({
        className: "Popego.UI.NavigationPanel",
        id: "navigation",
        
        initialize: function(container){
            this.parent(container);
        },
        
        _setElements: function() {
            this.elements["next"] = $("next"); //ojo con el scope,
            this.elements["prev"] = $("prev"); //quizas mejor en vez de id
            this.elements["back"] = $("back"); //usar className
        },
        
        _setBehaviors: function() {
            //todo: podria haberlo generalizado cheee...
            var onBack = function(e) {
                var evtObj = new Popego.UI.Event(Popego.UI.NavigationPanel.Events.BACK_CLICK, this, e)
                this.fireEvent(evtObj.type, evtObj);
            };
            var onPrev = function(e) {
                var evtObj = new Popego.UI.Event(Popego.UI.NavigationPanel.Events.PREV_CLICK, this, e)
                this.fireEvent(evtObj.type, evtObj);
            };
            var onNext = function(e) {
                var evtObj = new Popego.UI.Event(Popego.UI.NavigationPanel.Events.NEXT_CLICK, this, e)
                this.fireEvent(evtObj.type, evtObj);
            };
            this.elements.back.addEvent("click", onBack.bindWithEvent(this));
            this.elements.prev.addEvent("click", onPrev.bindWithEvent(this));
            this.elements.next.addEvent("click", onNext.bindWithEvent(this));
        },
        
        setElementTitle: function(elId, title) {
            var el = this.elements[elId];
            el.setAttribute("title", title);
        },
        
        setNextButtonTitle: function(title){
            this.setElementTitle("next", title);
        },
        
        setPrevButtonTitle: function(title){
            this.setElementTitle("prev", title);
        },
        
        setButtonsVisibility: function(back, next, prev) {
            this.elements.back.setStyle("display", back ? "":"none");
            this.elements.prev.setStyle("display", next ? "":"none");
            this.elements.next.setStyle("display", prev ? "":"none");
        },
        
        getEventList: function() {
            var events = [];
            $each(eval("Popego.UI.NavigationPanel").Events, function(value, key){
                events.include(value);
            });
            return events;
        }
    });
    Popego.UI.NavigationPanel.Events = {
        BACK_CLICK: "backclick",
        PREV_CLICK: "prevclick",
        NEXT_CLICK: "nextclick"
    }
    
    Popego.UI.FilterPanel = Popego.UI.Panel.extend({
        className: "Popego.UI.FilterPanel",
        id: "filters",
        
        initialize: function(container){
            this.parent(container);
        },
        
        _setElements: function(){
            this.elements["filter_by_group"] = $("filter_by_group");
        },
        
        _setBehaviors: function(){
            var groupFilter = this.elements["filter_by_group"];
            var onGroupFilterChange = function(e) {
                var evtObj = new Popego.UI.Event(Popego.UI.FilterPanel.Events.GROUP_FILTER_CHANGE, this, e);
                this.fireEvent(evtObj.type, evtObj);
            };
            
            groupFilter.addEvent("change", onGroupFilterChange.bindWithEvent(this));
        },
        
        setComboFilter: function(id, name, data, selectedIndex) {
            var combo = this.elements[id];
            combo.empty();
            if($defined(name)) combo.getPrevious().setText(name);
            
            var n = data.length;
            for(var i=0; i<n; i++) {
                var op = new Element("option", {"value": data[i].value});
                op.setText(data[i].name);
                combo.adopt(op);
            }
	    if ($defined(selectedIndex)) combo.selectedIndex = selectedIndex;
        },
        
        setGroupFilter: function(data, text, selectedIndex) {
            this.setComboFilter("filter_by_group", $pick(text, "Select Album:"), data, selectedIndex);
        }
    });
    Popego.UI.FilterPanel.Events = {
        GROUP_FILTER_CHANGE: 'groupfilterchange'
    }
    
    Popego.UI.Panelbar = Popego.UI.Component.extend({
        className: "Popego.UI.Panelbar",
        
        initialize: function(container) {
            this.container = container;
            this.children = [];
            this.panels = {}
            this.currentPanel = null;
            this.visible = false;
            
            //cargo los paneles que ya tengo en el DOM
            this.container.getChildren().each(function(panelDiv){
                this._parsePanel(panelDiv);
            }.bind(this));
        },
        
        _parsePanel: function(panelDiv) {
            var id = panelDiv.getAttribute("id");
            var panel;
            
            if (id == "filters")
                panel = new Popego.UI.FilterPanel(panelDiv);
            else if (id == "navigation")
                panel = new Popego.UI.NavigationPanel(panelDiv);
            
            var onEvent = function(e) {
                this.fireEvent(e.type, e);
            }.bind(this);
            panel.getEventList().each( function(evt) {
                panel.addEvent(evt, onEvent);
            });
            
            this.children.include(panel);
            this.panels[id] = panel;
        },
        
        showPanel: function(id) {
            if(!this.visible) this.show();
            
            if($defined(this.currentPanel) && this.currentPanel.visible) {
                this.currentPanel.hide();
            }
                
            var panel = this.panels[id];
            this.currentPanel = panel;
            this.currentPanel.show();
        },
        
        hidePanel: function(id) {
            this.panels[id].hide();
        },
        
        show: function() {
            this.container.setStyle("display", "");
            this.visible = true;
            var evtObj = new Popego.UI.Event(Popego.UI.Panelbar.Events.SHOW, this);
            this.fireEvent(evtObj.type, evtObj);
        },
        
        hide: function() {
            this.container.setStyle("display", "none");
            this.visible = false;
            var evtObj = new Popego.UI.Event(Popego.UI.Panelbar.Events.HIDE, this);
            this.fireEvent(evtObj.type, evtObj);
        }
    });
    
    Popego.UI.Panelbar.Events = {
        PANEL_CHANGE: "panelchange",
        PANEL_CLICK: "panelclick",
        SHOW: "show",
        HIDE: "hide"
    };
}
