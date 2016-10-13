if (typeof Popego == "undefined") Popego = {};

/* Popego Environment */
/*if (typeof Popego.Env == 'undefined') {
	Popego.Env = {}; 
	Popego.Env.baseUrl = '';
}
*/
/*Popego.Env.getUsername = function() {
  var pattern = /http:\/\/.*\/(\w+)\/api\/.*/; 
  /*var url = window.location.toString();
  var result = url.match(pattern); 
  if (result != null) { 
    return result[1];
  } else {
    throw new Error("Invalid Url");
  }
}

/*Popego.Env.username = Popego.Env.getUsername();*/

Popego.util = {}
Popego.util.upUntil = function(predicate, element) {
  while (element != null && !predicate(element)) {
    element = element.parentNode;
  }
  return element;
}




/******************************************************************************
 ** MEDIA Controller
 ** @desc  
 ** @version 
 *****************************************************************************/  
Popego.Media = new Class({
	
	REQ_TIMEOUT: 5000, //timeout for XHR requests in milliseconds
	
	initialize: function(el) {
		this.sectionDiv = el;
		this.buttonSelected = undefined; //tab button selected
		
		// XHR to get subsections' data
		this.subSectionXHR = new XHR({method: 'get'});
		this.subSectionXHR.addEvent('onRequest', this.onDataRequest.bind(this));
		this.subSectionXHR.addEvent('onFailure', this.onDataFailure.bind(this));
		this.subSectionXHR.addEvent('onSuccess', this.onDataSuccess.bind(this));
		this.timeoutChecking = undefined;	//checks for request timeouts
		
		//function - Cuando falla aparece un link para volver y ejecuta esta funcion
		this.returnToPrevious = undefined;
		
		this.setBehaviors();
		
		if (this.buttonSelected)
			this.getSubSection(this.buttonSelected.getElement('strong').getText());
	},
	
	setBehaviors: function() {
		//sets button bar behavior
		var menuDiv = this.sectionDiv.getElement('.subsections_menu')[0];
		if (menuDiv) {
			var buttons = menuDiv.getElements('div');
			var bLength = buttons.length;
			buttons.each(function(button){
				button.addEvent('click', this.onButtonBarClick.bind(this));
				
				if (button.className == 'category_selected')
					this.buttonSelected = button;				
			}.bind(this));
		}
	},
	
	//ButtonBar's button behavior
	onButtonBarClick: function(e) {
		//var buttonClicked = e.currentTarget;
		e = new Event(e);
		
		var isCategory = function(e) {return (e.className.search('category') == 0)}
		var buttonClicked = Popego.util.upUntil(isCategory, e.target)
		
		if (buttonClicked != this.buttonSelected) {
			this.buttonSelected.className = 'category';
			
			buttonClicked.className = 'category_selected';
			this.buttonSelected = buttonClicked;
			this.getSubSection(this.buttonSelected.getElement('strong').getText());
		}
	},
	
	getSubSection: function(name) {
		//TODO: ver si conviene mas guardar o crear una instancia cada vez
		switch (name){
			case 'pictures':
				this.currentSubSection = new Popego.Media.Pictures();
				this.getData();
				break;
			case 'videos':
				this.currentSubSection = new Popego.Media.Videos();
				this.getData();
				break;
			case 'blog posts':
				break;
			case 'feeds':
				break;
			case 'music':
				this.currentSubSection = new Popego.Media.Music();
				this.getData();
				break;
			case 'bookmarks':
				this.currentSubSection = new Popego.Media.Bookmarks();
				this.getData();
				break;
		}
		//this.getData();
	},
	
	getData: function(showSpinner) {
		if (showSpinner || showSpinner == undefined) this.sectionDiv.getElement('.main').setHTML('<img src="/images/widget/spinner_white.gif" style="margin-top:10px;margin-left:8px;"/>');
		this.subSectionXHR.send(this.currentSubSection.getUrl());
	},
	
	// XHR Handlers
	onDataRequest: function() {
		this.timeoutChecking = function() {
			if(this.subSectionXHR.running) {
				this.subSectionXHR.cancel();
				this.onDataFailure();
			}
			else $clear(this.timeoutChecking);
		}.bind(this).delay(this.REQ_TIMEOUT);
	},
	
	onDataFailure: function() {
		$clear(this.timeoutChecking);
		var link = '';
		if(this.returnToPrevious) link = '<br/><br/><a href="javascript:mediaController.returnToPrevious();">Return to previous page.</a>';
		this.render('We\'re sorry, but the data is unavailable right now. <br/>Please try again later.' + link, true);
	},
	
	onDataSuccess: function(t) {
		$clear(this.timeoutChecking);
		this.render(t);
	},
	//---
	
	render: function(t, error) {
		this.sectionDiv.getElement('.main').setHTML(t);
		
		if (error == undefined || !error)
			this.currentSubSection.setBehaviors(this.sectionDiv);
	}
});

// Media SubSections ----------------------------------------------------------
Popego.Media.SubSection = new Class({
	
 	subSectionDiv: '',
	viewDiv: '',
	paginationDiv: '',
	
	initialize: function(id, name, view) {
		this.id = id;
		this.name = name;
		this.currentView = view;
		
		this.currentPage = 1;
		this.currentAlbumsPage = 1;
		this.currentThumbsPage = 1;
		this.pageCount = 0;
		
		this.btnBack = undefined;
		this.btnNext = undefined; 
	},
	
	getUrl: function(){ return this.getViewUrl(this.currentView); },
	
	setBehaviors: function(parentDiv) {
		this.subSectionDiv = parentDiv.getElement('.'+this.id);
		this.viewDiv = this.subSectionDiv.getElementById(this.currentView);
		this.paginationDiv = this.viewDiv.getElement('.footer').getElement('.collection').getElement('.pagination');
		this.pageCount = parseInt(this.paginationDiv.getProperty('pageCount'));
	
		this.btnBack = this.paginationDiv.getElement('.prev_holder')[0];
		this.btnNext = this.paginationDiv.getElement('.next_holder')[0];
		if(this.currentPage > 1) this.btnBack.style.display = 'inline';
		if(this.pageCount > this.currentPage) this.btnNext.style.display = 'inline';
	}
});


/******************************************************************************
** PICTURES SubSection 
******************************************************************************/ 
Popego.Media.Pictures = Popego.Media.SubSection.extend({
	
	initialize: function(id, name, initView){
		this.parent(id || 'pictures', name || 'pictures', initView || 'groups');
		
		this.currentAlbum = '';
		this.currentItem = '';
		this.statusMsgTimer = undefined;
	},
	
	getViewUrl: function(view){
		switch(view)
		{
			case 'groups':
				return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/pictures/albums/' + this.currentPage;
				break;
			case 'thumbs':
				return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/pictures/' + this.currentAlbum.id + '/' + this.currentPage;
				break;
			case 'showcase':
				return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/pictures/' + this.currentAlbum.id + '/pic/' + this.currentItem.id;
		}
	},
	
	setStatusMsg: function(title, subtitle) {
		var titleContainer = this.viewDiv.getElement('.index').getElement('.databox').getElement('h1');
		var stContainer = this.viewDiv.getElement('.index').getElement('.databox').getElement('.status_subtitle');
		titleContainer.setText(title);
		stContainer.setText(subtitle);
	},
	
	setBehaviors: function(parentDiv) {
		this.parent(parentDiv);
		
		switch (this.currentView){
			case 'groups':
				this.setGroupsBehavior();
				break;
			case 'thumbs':
				this.setThumbsBehavior();
				break;
			case 'showcase':
				this.setShowcaseBehavior();
		}
	},
	
	setGroupsBehavior: function() {
		var albums = this.viewDiv.getElements('.index_item')[0];
		albums.each(function(album){album.addEvent('click', this.onAlbumClick.bindWithEvent(this, album))}.bind(this));
		this.btnBack.addEvent('click', this.onPreviousAlbumsClick.bindWithEvent(this));
		this.btnNext.addEvent('click', this.onMoreAlbumsClick.bindWithEvent(this));
	},
	
	setThumbsBehavior: function() {
		var thumbs = this.viewDiv.getElementById('items_container').getElements('div')[0];
		thumbs.each(function(thumb) {
			var img = thumb.getElement('img');
			img.addEvent('click', this.onThumbClick.bindWithEvent(this, img));
			img.addEvent('mouseover', this.onThumbOver.bindWithEvent(this, img));
			img.addEvent('mouseout', this.onThumbOut.bindWithEvent(this, img));
		}.bind(this));
		
		//footer
		var btnBackToMenu = this.viewDiv.getElement('.footer').getElement('.collection').getElement('.btn_wayback')[0];
		btnBackToMenu.addEvent('click', this.onBackToMenuClick.bindWithEvent(this));
		this.btnBack.addEvent('click', this.onPreviousThumbsClick.bindWithEvent(this));
		this.btnNext.addEvent('click', this.onMoreThumbsClick.bindWithEvent(this));
	},
	
	setShowcaseBehavior: function() {
		//footer
		btnBackToThumbs = this.viewDiv.getElement('.footer').getElement('.collection').getElement('.btn_wayback')[0];
		btnBackToThumbs.addEvent('click', this.onBackToThumbsClick.bindWithEvent(this));
	},
	
	
	// Manejo de eventos de la vista 'GROUPS' ------------------------------------
	onAlbumClick: function(e, currentTarget) {
		var id, name, date;
		id = currentTarget.id;
		title = currentTarget.getElement('.index_item_detail').getElement('h3').getText();
		date = currentTarget.getElement('.index_item_date').getText();
		
		this.currentAlbum = new Popego.Media.Item(id, title, '', date);
		this.currentView = 'thumbs';
		this.currentAlbumsPage = this.currentPage;
		this.currentPage = 1;
		mediaController.returnToPrevious = this.onBackToMenuClick.bind(this);
		mediaController.getData();
	},
	
	onPreviousAlbumsClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage > 1 ? this.currentPage-1 : 1;
		mediaController.getData();
	},
	
	onMoreAlbumsClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage < this.pageCount ? this.currentPage+1 : this.pageCount;
		mediaController.getData();
	},
	
  // Manejo de eventos de la vista 'THUMBS' ------------------------------------
	onThumbClick: function(e, currentTarget) {
		var pic = currentTarget;
		this.currentItem = new Popego.Media.Item(pic.id, pic.getProperty('titl'), pic.getProperty('desc'), '');
		this.currentView = 'showcase';
		this.currentThumbsPage = this.currentPage;
		this.currentPage = 1;
		mediaController.returnToPrevious = this.onBackToThumbsClick.bind(this);
		mediaController.getData();
	},
	
	onThumbOver: function(e, currentTarget) {
		var pic = currentTarget;
		this.setStatusMsg(pic.getProperty('titl'), pic.getProperty('desc'));
		this.isThumbOver = true;
		this.statusMsgTimer = $clear(this.statusMsgTimer);
	},
	
	onThumbOut: function(e) {
		var tmpThis = this;
		this.isThumbOver = false;
		this.statusMsgTimer = function(){
			if(!tmpThis.isThumbOver)
				tmpThis.setStatusMsg(tmpThis.currentAlbum.title, 'Album created on ' + tmpThis.currentAlbum.date);
		}.delay(100);
	},
	
	onBackToMenuClick: function(e) {
		if(e) e.stop();
		
		this.currentPage = this.currentAlbumsPage;
		this.currentAlbum = '';
		this.currentView = 'groups';
		
		mediaController.returnToPrevious = undefined;
		mediaController.getData();
	},
	
	onPreviousThumbsClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage > 1 ? this.currentPage-1 : 1;
		mediaController.getData();
	},
	
	onMoreThumbsClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage < this.pageCount ? this.currentPage+1 : this.pageCount;
		mediaController.getData();
	},
	
	// Manejo de eventos de la vista 'SHOWCASE' ----------------------------------
	onBackToThumbsClick: function(e) {
		if(e) e.stop();
		
		this.currentPage = this.currentThumbsPage;
		this.currentItem = '';
		this.currentView = 'thumbs';
		
		mediaController.returnToPrevious = undefined;
		mediaController.getData();
	}
});

//could be album or picture
Popego.Media.Item = new Class({
	id: '',
	title: '',
	desc: '',
	date: '',
	
	initialize: function(id, title, desc, date){
		this.id = id;
		this.title = title;
		this.desc = desc;
		this.date = date;
	}
});

Popego.Media.Pictures.Views = new Abstract({
	GROUPS: 'g',
	THUMBS: 't',
	SHOWCASE: 's'
});

/******************************************************************************
** VIDEOS SubSection 
******************************************************************************/
Popego.Media.Videos = Popego.Media.Pictures.extend({
  	
  initialize: function(id, name, initView) {
		this.parent(id || 'videos', name || 'videos', initView || 'groups');
		
		this.currentAlbum = '';
		this.currentItem = '';
		this.statusMsgTimer = undefined;
		this.rollOverTimer = undefined;
		this.rollOverCounter = 0;
	},
	
	getViewUrl: function(view){
		switch(view)
		{
			case 'groups': 
				return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/videos/albums/' + this.currentPage;
				break;
			case 'thumbs': 
				return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/videos/' + this.currentAlbum.id + '/' + this.currentPage;
				break;
			case 'showcase': 
				return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/videos/' + this.currentAlbum.id + '/v/' + this.currentItem.id;
		}
	},
	
	
	setThumbsBehavior: function() {
		var thumbs = this.viewDiv.getElements('.image_strip')[0];
		thumbs.each(function(thumb){
			thumb.addEvent('click', this.onThumbClick.bindWithEvent(this, thumb));
			thumb.addEvent('mouseenter', this.onThumbOver.bindWithEvent(this, thumb));
			thumb.addEvent('mouseleave', this.onThumbOut.bindWithEvent(this, thumb));
		}.bind(this));
		
		//footer
		var btnBackToMenu = this.viewDiv.getElement('.footer').getElement('.collection').getElement('.btn_wayback')[0];
		btnBackToMenu.addEvent('click', this.onBackToMenuClick.bindWithEvent(this));
		this.btnBack.addEvent('click', this.onPreviousThumbsClick.bindWithEvent(this));
		this.btnNext.addEvent('click', this.onMoreThumbsClick.bindWithEvent(this));
	},
	
	stopThumbSwitching: function(thumbDiv) {
		this.rollOverCounter = 0;
		
		var thumbs = thumbDiv.getElements('img');
		thumbs[0].style.display = '';
		thumbs[1].style.display = 'none';
		thumbs[2].style.display = 'none';
		this.rollOverTimer = $clear(this.rollOverTimer);
	},
	
	// Manejo de eventos de la vista 'THUMBS' ------------------------------------
	onThumbOver: function(e, currentTarget) {
		var thumbs = currentTarget.getElements('img');
		var tLength = thumbs.length;
			
		thumbs[0].style.display = 'none';
		thumbs[1].style.display = '';
		thumbs[2].style.display = 'none';
		this.rollOverCounter++;
		
		var tmpThis = this;
		this.rollOverTimer = function() {
			thumbs[tmpThis.rollOverCounter++%3].style.display = 'none'
			thumbs[tmpThis.rollOverCounter%3].style.display = '';
			
		}.periodical(1000);
		
		this.parent(e.event, currentTarget);
	},
	
	onThumbOut: function(e, currentTarget) {
		this.stopThumbSwitching(currentTarget);
		this.parent(e.event, currentTarget);
	},
	
	onThumbClick: function(e, currentTarget) {
		this.stopThumbSwitching(currentTarget);
		this.parent(e, currentTarget);
	}
	
});

Popego.Media.Videos.Views = new Abstract({
	GROUPS: 'g',
	THUMBS: 't',
	SHOWCASE: 's'
});


/******************************************************************************
** BOOKMARKS SubSection 
******************************************************************************/
Popego.Media.Bookmarks = Popego.Media.SubSection.extend({
  	
	initialize: function(id, name, initView) {
		this.parent(id || 'links', name || 'links', initView || 'groups');
		
		this.currentAlbum = '';
		this.currentItem = '';
		this.statusMsgTimer = undefined;
		this.rollOverTimer = undefined;
		this.rollOverCounter = 0;
	},
	
	getViewUrl: function(view){
		return Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/bookmarks/' + this.currentPage;
	},
	
	setBehaviors: function(parentDiv){
		this.parent(parentDiv)
		this.btnBack.addEvent('click', this.onPreviousLinkClick.bindWithEvent(this));
		this.btnNext.addEvent('click', this.onMoreLinkClick.bindWithEvent(this));
	},


	onPreviousLinkClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage > 1 ? this.currentPage-1 : 1;
		mediaController.getData();
	},
	
	onMoreLinkClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage < this.pageCount ? this.currentPage+1 : this.pageCount;
		mediaController.getData();
	}

});


/******************************************************************************
** MUSIC SubSection 
******************************************************************************/
Popego.Media.Music = Popego.Media.SubSection.extend({
	
	initialize: function(id, name, initView) {
		this.parent(id || 'culture', name || 'culture', initView || 'favorites');
		
		this.currentRank = '';	// 'tracks', 'artists' or 'songs'
	},
	
	getViewUrl: function(view) {
		var url = Popego.Env.baseUrl + '/' + Popego.Env.username + '/api/music/'
		if (view == 'ranking') return url + 'ranks/' + this.currentRank + '/' + this.currentPage;	
		else return  url + this.currentPage;  //'favorites' view
	},
	
	setBehaviors: function(parentDiv) {
		this.parent(parentDiv);
		if(this.currentView=='favorites') {
			var rankLinks = this.viewDiv.getElements('.see_more')[0];
			rankLinks.each(function(link){
				link = link.getElement('a');
				link.addEvent('click', this.onRankLinkClick.bindWithEvent(this, link.getAttribute('id')));
			}.bind(this));
		}
		else { //ranking
			var btnBackToMenu = this.viewDiv.getElement('.footer').getElement('.collection').getElement('.btn_wayback')[0];
			btnBackToMenu.addEvent('click', this.onBackToFavoritesClick.bindWithEvent(this));
			this.btnBack.addEvent('click', this.onPreviousRankPageClick.bindWithEvent(this));
			this.btnNext.addEvent('click', this.onNextRankPageClick.bindWithEvent(this));
		}
	},
	
	onRankLinkClick: function(e, rank) {
		e.stop();
		
		this.currentView = 'ranking';
		this.currentRank = rank;
		mediaController.returnToPrevious = this.onBackToFavoritesClick.bind(this);
		mediaController.getData();
	},
	
	onBackToFavoritesClick: function(e) {
		if (e) e.stop();
		
		this.currentView = 'favorites'
		this.currentPage = 1;
		this.currentRank = '';
		
		mediaController.returnToPrevious = undefined;
		mediaController.getData();
	},
	
	onPreviousRankPageClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage > 1 ? this.currentPage-1 : 1;
		mediaController.getData();
	},
	
	onNextRankPageClick: function(e) {
		e.stop();
		
		this.currentPage = this.currentPage < this.pageCount ? this.currentPage+1 : this.pageCount;
		mediaController.getData();
	}
	
});

Popego.Media.Music.Views = new Abstract({
	FAVORITES: 'fav',
	RANKING: 'rank'
});

Popego.Media.Music.Ranks = new Abstract({
	TRACKS: 'fav',
	ARTISTS: 'rank',
	SONGS: 'songs'
});

window.addEvent('load', function() {
	mediaController = new Popego.Media($ES('.media'));
});
