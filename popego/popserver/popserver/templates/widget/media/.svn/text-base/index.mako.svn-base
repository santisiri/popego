<%inherit file="../base.mako" />

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/card_bubble_default.css', '/css/widget/card_content_bubble.css']))}
</%def>

<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(*map(h.asset_src,['/javascripts/popego-ui.js', '/javascripts/popego-urlmanager.js', '/javascripts/date.format.js', '/javascripts/widget/media-src/media.js', '/javascripts/widget/media-src/media-sections.js', '/javascripts/widget/media-src/media-views.js', '/javascripts/widget/media-src/media-renderers.js', '/javascripts/widget/popego-twitter-lib.js']))}
<script type="text/javascript">
<!--
if (!Popego.Env) Popego.Env = {};
% if c.myQuoteAccount:
Popego.Env.quoteAccount = {username: '${c.myQuoteAccount.username}', service: '${c.myQuoteAccount.service.name}'};
% else:
Popego.Env.quoteAccount = {username: null, service: null};
% endif
//-->
</script>
</%def>
</head>
  <body>
    <div class="media" style="height:407px">
	  <div class="buttonbar">
		<ul>
			<li class="selected"><span>${c.types[0].type}</span> (${c.typesCount[c.types[0].type]}),</li>
			%for type in c.types[1:]:
                %if type.type != "quotes":
                <li><span><a href="javascript:void(0);">${type.type}</a></span> (${c.typesCount[type.type]}),</li>
                %endif
			%endfor
			<!--<li>and <span><a href="javascript:void(0);">${c.types[-1].type}</a></span> (${c.typesCount[c.types[-1].type]}).</li>-->
			<li class="disabled"><span><a href="#">books</a></span> (0),</li>
			<li class="disabled"><span><a href="#">feeds</a></span> (0),</li>
			<li class="disabled">and <span><a href="#">profiles</a></span> (0).</li>
		</ul>
	  </div>

		<div class="content" style="height:320px;width:415px;">
		  <div class="view" id="list">
			<div style="height:315px;" id="Preview">
				<div class="box_shadow" style="background:url(${h.asset_src('/images/widget/shadow_top.png')}) top repeat-x; z-index:9999; position:absolute; height:10px; width:100%;"></div>
				<div class="box_shadow" style="background:url(${h.asset_src('/images/widget/shadow_bottom.png')}) bottom repeat-x; z-index:9999; bottom:35px; position:absolute; height:10px; width:100%;"></div>
				<div class="box_shadow" style="background:url(${h.asset_src('/images/widget/shadow_left.png')}) left repeat-y; z-index:9999; position:absolute; width:10px; height:317px;"></div>
				<div class="index" id="Preview"  style="padding:6px; padding-left:8px; height:303px;" >
					<div class="content"></div>
					<div class="show_more" style="clear:both;height:72px;display:none;">
						<br/>
						<h2 style="font-weight:normal;"><a href="javascript:void(0);">Show 30 more pictures.</a></h2>
					</div>
				</div>
			</div>
		  </div>
		  <div class="view" id="detail">
            <div class="content" style="background:url(${h.asset_src('/images/widget/spinner_white.gif')}) 50% 50% no-repeat; display: table; #position: relative; overflow: hidden;"></div>	
          </div>
		</div>
	
		<div class="bottompanels">
			<div id="filters" class="bottompanel" style="padding:0px; margin:10px 0px;display:none;">
			  <div style="float:left;">
				  <span>Selected Group:</span>
				  <select size="1" id="filter_by_group" name="filter_dropwdown" style="width: 300px; font-family: Arial, Tahoma, FreeSans, sans-serif;">
					  <option value="0">All Groups</option>
				  </select>
			  </div>
			</div>
			<div id="navigation" class="bottompanel" style="display:none">
				<div style="float:right; width:190px;">
					<div id="next" class="bigbutton gonext"  title="foto anterior">Next</div>
					<div id="prev" class="bigbutton goback" title="foto siguiente">Previous</div>
				</div>
				
				<div style="width 220px; margin-top:3px;">
					<div id="back" class="bigbutton goback" style="float:left; background-image:url(${h.asset_src('/images/widget/bigbutton_rewind.png')})" title="Go back to menu.">
						Return
					</div>			
				</div>
			</div>
		</div>
    </div>

% if c.myQuoteAccount:
<script src="http://twitter.com/statuses/user_timeline/${c.myQuoteAccount.username}.json?callback=Popego.setTwitterQuotes" defer="defer" type="text/javascript"></script>
% endif
    <!-- End of Section -->	
