//La hago class y no abstract para poder implementar options
Popego.URLManager = new Class({
	options: {
		album: "0",
		page: 1,
		offset: 0,
		qty: 1,
		jsonified: false
	},
	
	initialize: function(){
		this.defaultOptions = this.options;
	},
	
	getPictures: function(user, options) {
		this.setOptions(options);
		var url = Popego.Env.baseUrl + "/" + user + "/api"
		if (this.options.jsonified) {
			if (this.options.album != "0") {
				url += "/items/pictures/" + this.options.album + "?offset=" + this.options.offset + "&count=30";
			} else {
				url += "/items/pictures?offset=" + this.options.offset;
			}
		} else {
			url += "/pictures/" + this.options.album + "/" + this.options.page;
		}
		this.resetOptions();
		return url;
	
	},
	
	getPictureAlbumList: function(user, options) {
		return Popego.Env.baseUrl + "/" + user + "/api/groups/pictures";
	},
    
    getAlbumList: function(user, item, options) {
		return Popego.Env.baseUrl + "/" + user + "/api/groups/" + item;
	},
	
	toQueryString: function(obj) {
		var result = "?";
		for (var prop in obj)
			result += prop + "=" + escape(obj[prop]) + "&";
		return result.substring(0, result.length-1);
	},
	
	resetOptions: function(){
		this.options = this.defaultOptions;
	}
	
});
Popego.URLManager.implement(new Options);
Popego.URLManager = new Popego.URLManager();