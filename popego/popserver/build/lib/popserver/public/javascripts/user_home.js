/* Popegos of the World */
Popego.Poplist = new Class({
    initialize: function(el, itemDivs){
        this.container = el;
        this.items = new Array();
        
        // creo los items
        var idx = 0;
        itemDivs.each(function(div){
            this.items[idx++] = new Popego.Poplist.Item(div)
        }.bind(this));
    }
});

Popego.Poplist.Item = new Class({
    options: {
    },
    
    initialize: function(el, options){
        this.setOptions(options);
        this.container = el;
        
        this.popCardLink = undefined;
        this.popCardUser = undefined;
		this.popCardTheme = undefined;
		this.popCardKey = undefined;
		this.websiteLink = undefined;
        
		this._setElements();
		this._setBehaviors();
    },
	
	_setElements: function(){
		/* La estructura del item es la siguiente:
            
            <div class="popego_minicard">
                <a href="#" title="Visit website" target="_blank"><img src="${h.asset_src('/images/website/samples/avatar_sample_002.png')}" class="avatar_130"></a>
                <div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}"></div>
                <p>
                    <img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
                    <a href="#">${popego['user'].displayname}</a>					
                </p>
                <p>
                    <img src="${h.asset_src('/images/website/urllink_idle.png')}" class="poplink">
                    <a href="#" title="Website hosting this Popego." target="_blank">wikidada.org</a>								
                </p>					
                <p>
                    <h2><strong>${popego['compatibility']}%</strong></h2>
                    interest match
                </p>
            </div>
        */
		this.popCardLink = this.container.getElements('a')[1];
        this.popCardTheme = this.popCardLink.getAttribute('theme');
		this.popCardUser = this.popCardLink.getAttribute('username');
        //this.websiteLink = this.container.getElements('a')[2];
		
		//creo la popcard
		this.popCardKey = this.popCardUser + "_" + (new Date()).getTime(); //esto podria ser el id del widget
		Popego.popcards[this.popCardKey] = Popego.PopcardManager.create(this.popCardKey, this.popCardUser, "t"+this.popCardTheme, "default");
	},
    
    _setBehaviors: function(){
        var onPopCardClick = function(e) {
            e.stop();
            Popego.popcards[this.popCardKey].open();
        }
        this.popCardLink.addEvent('click', onPopCardClick.bindWithEvent(this));
    }
    
});
Popego.Poplist.Item.implement(new Options)

Popego.PopegosOfTheWorld = Popego.Poplist.extend({
    initialize: function(el){
        this.parent(el, el.getElements('.popego_minicard'));
    }
    
});

/* Seguro habra que extender de Website */
if ( typeof Popego.Website == 'undefined' ) Popego.Website = {};

Popego.Website.Home = new Class({
    initialize: function(el){
        this.container = el;
        
        this.container.getElement('.coming_soon_wrapper').setStyle('opacity', 0.3);
        this.popegosOfTheWorld = new Popego.PopegosOfTheWorld($('popegos_otw'));
    }
});

window.addEvent('domready', function() {
    var userHome = new Popego.Website.Home($ES('.content'));
});