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

