<%inherit file="/website/base.mako" />
<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/website/default.css', '/css/website/widgets.css', '/css/websites/updates.css']))}
</%def>
<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(h.asset_src('/javascripts/feedback.js'))}
</%def>
<body>
<!-- Dynamic CSS -->
<style type="text/css">
	a,
	.button,
	.popego_avatar_thumbnail:hover a,
	.date_separator,
	.category strong,
	.label_tooltip {
		color:#FF3366;
	}
	
	input:focus,
	textarea:focus,
	.date_separator,
	.popego_avatar_thumbnail:hover img {
		border-color:#FF3366;
		
	}
	
	.menu_button_active,
	.menu_closer_active,
	.menu_button_arrow,
	.poplink,
	.category_selected {
		background-color:#FF3366;
	}
	
	.help_box {
		background-color:#FF900A;
	}
</style>
<!-- End of Dynamic CSS -->

<p></p>


<!-- Header -->
<!--<div class="special_background">
</div>-->

<div class="header">
	<!--<img src="/images/website/header_background_000.png" width="950px" height="100px" style="position:absolute; top:0px; left:0px; z-index:0;" />-->

	<!--<div class="release_logo" title="This means that Popego is still under development. Give us your feedback to improve the service."></div>-->
	<a href="/"><img src="${h.asset_src('/images/website/logo_cloud.png')}" title="Popego" class="official_logo" /></a>
	
	<div class="tab_collection">
		
		<div class="tab_button_close"></div>
		<div class="tab_button">
			<a href="http://blog.popego.com">Pop Blog</a>
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

	<!-- Content -->
	<div class="content">

		<!-- Column 2 -->
		<div class="column_2">

			${next.body()}

			<p>
				<div class="show_more_updates"><a href="javascript:history.go(-1)">Return to previous page.</a></div>
			</p>		
		
		</div>
		<!-- End of Column 2 -->
		
		
		<div class="footer_separator"></div>
		
		<div class="website_menu">
			<img src="${h.asset_src('/images/website/logo_small_watermark.png')}" title="Created by The Popego Team.">
		</div>
		
		<div class="final_links">
			&copy; 2008 Popego Inc.
			<%doc><a href="/about/">Your Privacy</a></%doc>
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
