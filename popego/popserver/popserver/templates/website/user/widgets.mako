<script type="text/javascript">
		if (typeof(Popego) == 'undefined') Popego = {};	if (typeof(Popego.Env) == 'undefined') Popego.Env = {}; 
		Popego.Env.username = "${c.user.username if hasattr(c, 'user') else ''}"; Popego.Env.displayname = "${c.user.displayname if hasattr(c, 'user') else ''}"; 
        Popego.Env.baseUrl= "${c.baseUrl if hasattr(c, 'baseUrl') else ''}";
		Popego.Env.remoteUser = "${c.remoteUser if hasattr(c, 'remoteUser') else ''}"; 
		Popego.Env.remoteUserLoggedIn = Boolean("${c.remoteUserLoggedIn if hasattr(c, 'remoteUserLoggedIn') else 'False'}" == "True");
		Popego.Env.parentUrl = (document.referrer.split('?')[0] == location.href.split('?')[0]) ? "${c.parentUrl if hasattr(c, 'parentUrl') else '/'}" : document.referrer;
</script>

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/theme_selector.css', '/css/widget/widget_default.css', '/css/widget/card_bubble_default.css', '/css/widget/card_content_bubble.css']))}
</%def>

<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(*map(h.asset_src, ['/javascripts/user_widgets.js', '/javascripts/widget/popego-ext.js', '/javascripts/widget/popego-config.js', '/javascripts/widget/embedder-lib.js']))}
</%def>

<%inherit file="base.mako" />

<%def name="heading_phrase()">Give style to your Widgets.</%def>

	<!-- Content -->
	<div class="content">
		<!-- Column 1 -->
		<div>
			
			<!-- Services -->
			<div class="popego_widgets">
								
				<h3><strong>Widget Designs</strong></h3>
				
				Embed a widget of your Popego on any site or online community so the world can meet you.
				
				<!-- List of Updates -->
				<ul class="popego_updates">
					<li>
						<div class="widget_settings">
							<p><strong>Color Theme</strong></p>
							<div class="palette">
								<ol>
								<% 
									themes = ['aa0000', 'e72510', 'e23d14', 'ff900a', '4d8000', '6aac28',\
									'a9d103', 'e4e40a', '0d6d6d', '013c76', '0159b1', '129fc2', 'ff3366',\
									'ac20ac', 'c01258', '993300', '3d3d3d', '666666', '9e9e9e', 'dddddd'] 
								%>
								% for t in themes:
									<li${' class="picked_color"' if t == c.theme else ''}><a href="#" class="x${t}"></a></li>
								% endfor
								</ol>
							</div>
                                                                        
							<p><strong>Embed Code</strong></p>
							<form style="padding:0px; margin:0px;">
								<textarea readonly="readonly" id="code" name="code"></textarea>
								<label class="label_tooltip" style="display:block;">Copy &amp; paste this code on your blog's HTML template.</label>
							</form>
                                    
                            <form action="/${c.user.username}/widgets/1/theme" method="post" id="widget_settings" style="float:right">
                                <input type="HIDDEN" name="theme" value="">                                   
                                <p><span class="messages"></span><img src="${h.asset_src('/images/website/spinner_white.gif')}" alt="Sending..." width="16" height="16" style="display: none; padding: 0 12px;" /><input type="submit" value="save" class="button"/></p>
                            </form>

                                    
						</div>
						<div class="widget_preview">
							<p><strong>Preview</strong></p>
							<p>
								<div class="canvas"></div>
							</p>
						</div>
						<div style="clear:both"></div>
					</li>
			</div>
		</div>
	</div>
	<!-- End of Content -->
