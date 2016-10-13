<%def name="title()"></%def>
<%def name="stylesheets()">
  ${h.stylesheet_link_tag(h.asset_src('/css/website/dialog.css'))}
</%def>
<%def name="javascripts()">
  ${h.javascript_include_tag(*map(h.asset_src, ['/javascripts/mootools.js', '/javascripts/utils.js']))}
</%def>
<% page_title = capture(self.title).strip() + ' | ' if capture(self.title).strip() != '' else '' %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>${page_title}Popego | The Internet meets You</title>

	<link href="/css/website/default.css" rel="stylesheet" type="text/css" />
	<link href="/css/website/dialog.css" rel="stylesheet" type="text/css" />
	<link href="/css/website/updates.css" rel="stylesheet" type="text/css" />
	<link href="/css/website/widgets.css" rel="stylesheet" type="text/css" />
	<link href="/css/themes/deeppink.css" rel="stylesheet" type="text/css" />

	<script type="text/javascript" src="/javascripts/mootools.js"></script>
	<script type="text/javascript" src="/javascripts/utils.js"></script>
	<script type="text/javascript" src="/javascripts/feedback.js"></script>

</head>
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
	<!--<img src="/images/website/header_background_000.png" width="950px" height="100px" style="position:absolute; top:0px; left:0px; z-index:0;" />-->

	<!--<div class="release_logo" title="This means that Popego is still under development. Give us your feedback to improve the service."></div>-->
	<a href="/"><img src="/images/website/logo_cloud.png" title="Popego" class="official_logo pngfix" /></a>
	
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
		
		<%doc>
		<!--<div class="tab_button_close"></div>
		<div class="tab_button">
			You are logged in as <strong>verylongusername</strong>. <a href="#">Log out</a>.
		</div>
		
		<div class="tab_button_active_close"></div>
		<div class="tab_button_active">
			Log in: 
			<input type="text" id="blog" value="username" />
			<input type="password" id="blog" value="password" />
			<a href="#">OK</a>, or <a href="#">register</a>.
		</div>-->
		</%doc>
		
	</div>
	
</div>
<!-- End of Header -->

<!-- Body -->
<div class="body">
	
	<div class="title">

	<style type="text/css">
		p, li { margin:12px 0; }
		blockquote { margin-bottom:60px; }
	</style>

	<div class="title">
		<h1><strong>${self.title()}</strong></h1>
	</div>


	</div>
	
	<%doc>	
	<form action="#" id="search" class="search">
		<input type="text" id="search" value="search for popegos" />
		<input type="submit" value="go!" class="button"/>
	</form>
	</%doc>	
	
	<div class="separator"></div>
	
	<!-- Menu -->
	<div class="menu">
				
	</div>
	<!-- End of Menu -->
	
	

	<!-- Content -->
	<div class="content">
		
		${next.body()}

		<div class="footer_separator"></div>
		
		<div class="website_menu">
			<img src="/images/website/logo_small_watermark.png" title="Created by The Popego Team." class="pngfix">
		</div>
		
		<div class="final_links">
			&copy; 2008 Popego Inc.
			<%doc><a href="/about/">Your Privacy</a></%doc>
			<a href="/about/tos">Terms of Service</a>
			<a href="javascript:Popego.Feedback.showForm();">Contact Us</a>	
		</div>

	</div>
	<!-- End of Content -->



	
</div>
<!-- End of Body -->


<!-- Footer -->
<div class="footer">
</div>
<!-- End of Footer -->

</body>
</html>
