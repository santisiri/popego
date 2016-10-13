<%inherit file="/website/base.mako" />
<%
userpages = {'home': 'Home', 'socialfeed': 'Social Feed', \
	'stats': 'Stats', 'services': 'Web Services', \
	'widgets': 'Widgets', 'settings': 'Settings'}

# TODO: descablear esto del pageid usando url_for
# o sea, no deducir la seccion actual de la url sino segun el controller
pageid = request.environ['PATH_INFO'][len(c.user.username) + 2:]
if pageid.find('/') != -1: pageid = pageid[0:pageid.index('/')]
if pageid not in userpages: pageid = 'home'

%>
<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/website/default.css', '/css/website/updates.css', '/css/website/widgets.css', '/css/themes/deeppink.css']))}
</%def>
<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(h.asset_src('/javascripts/feedback.js'))}
</%def>
<%def name="title()">
<%
# FIXME: Este codigo no deberia duplicarse pero no encontre la forma
# de hacer la clausura de este def
userpages = {'home': 'Home', 'socialfeed': 'Social Feed', \
	'stats': 'Stats', 'services': 'Web Services', \
	'widgets': 'Widgets', 'settings': 'Settings'}

# TODO: descablear esto del pageid usando url_for
# o sea, no deducir la seccion actual de la url sino segun el controller
pageid = request.environ['PATH_INFO'][len(c.user.username) + 2:]
if pageid.find('/') != -1: pageid = pageid[0:pageid.index('/')]
if pageid not in userpages: pageid = 'home'
%>
${userpages.get(pageid, '')}
</%def>
<body>
<p></p>
<!-- Tool Tip Box -->
<!-- Displayed above the pictures of the previewer on each mouseover -->
<div class="tool_tip_box" style="display:none;">
	<!-- Here go long descriptions that popup when the mouse is over a help_box. -->
</div>
<!--End Tool Tip Box -->	
<!-- Header -->
<!--<div class="special_background">
</div>-->
<div class="header">
	<a href="/"><img src="${h.asset_src('/images/website/logo_cloud.png')}" title="Popego" class="official_logo pngfix" /></a>
	<div class="top"></div>
	
	<div class="tab_collection">
		
		<div class="tab_button_close"></div>
		<div class="tab_button">
			<a href="http://blog.popego.com/">Pop Blog</a>
		</div>		
		
		<div class="tab_button_close"></div>
		<div class="tab_button">
			<a href="/about/developers">Info for Developers</a>
		</div>
		<div class="tab_button_close"></div>
		<div class="tab_button">
			<a href="javascript:Popego.Feedback.showForm();">Give us your Feedback</a>
		</div>		
	</div>
	
</div>
<!-- End of Header -->

<!-- Body -->
<div class="body">
	
	<div class="title">
<%def name="heading_phrase()">Don't let the rain bother you.</%def>
<%

phrase = capture(self.heading_phrase).strip()
username = c.user.displayname or c.user.username
i = username.strip().find(' ')
if i >= 0: username = username[0:i]

%>
		<h1>Hello <strong>${username | h}</strong>. ${phrase |h}</h1>
		<h5>&nbsp;(not you? <a href="${h.url_for(controller='auth', action='signout', username=None)}">log out</a>)</h5>
	</div>
	
	<!--form action="#" id="search" class="search">
		<input type="text" id="search" value="search for popegos" />
		<input type="submit" value="go!" class="button"/>
	</form-->	
	
	<div class="separator"></div>
	
	<!-- Menu -->
	<div class="menu">
				
% for i in ['home', 'socialfeed', 'stats', 'services', 'widgets', 'settings']:
% if i != pageid:
		<div class="menu_button">
			<a href="/${c.user.username |h}/${i |h}">${userpages[i] |h}</a>
		</div>
		<div class="menu_closer"></div>			
% else:
		<div class="menu_button_active">
			${userpages[i] |h}
			<div class="menu_button_arrow"></div>
		</div>
		<div class="menu_closer_active"></div>
% endif
% endfor

	</div>
	<!-- End of Menu -->
	<!-- Content -->
	<div class="content">
		
		${next.body()}

		<div class="footer_separator"></div>
		
		<div class="website_menu">
			<img src="${h.asset_src('/images/website/logo_small_watermark.png')}" title="Created by The Popego Team." class="pngfix">
		</div>
		
		<div class="final_links">
			&copy; 2008 Popego Inc.
			<a href="/about/tos">Terms of Service</a>
			<a href="javascript:Popego.Feedback.showForm(2);">Contact Us</a>	
		</div>

	</div>
	<!-- End of Content -->



	
</div>
<!-- End of Body -->


<!-- Footer -->
<div class="footer">
</div>
<!-- End of Footer -->
