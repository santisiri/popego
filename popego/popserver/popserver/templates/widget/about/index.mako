<%inherit file="../base.mako" />

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/card_content_bubble.css', '/css/widget/card_content_default.css', '/css/widget/themes/card_content_'+c.widgetTheme+'.css']))}
	<!--[if lt IE 7.]>
	<link href="/css/ie6.css" rel="stylesheet" type="text/css" />
	<![endif]-->
</%def>
<%def name="javascripts()">
${h.javascript_include_tag(*map(h.asset_src, ['/javascripts/mootools.js', '/javascripts/zumup.js']))}
</%def>


<!-- Content -->
<div class="about">	
	<p><img src="${h.asset_src('/images/widget/veryalpha.png')}" title="Popego is under heavy development right now." style="float:right;" class="pngfix"><a href="http://www.popego.com" target="_blank"><img src="${h.asset_src('/images/widget/logo_name.png')}" class="pngfix"></a></p>
	<p><h1>The Internet Meets You.</h1></p>
	<!--<p>In a world of user generated content, eternal forum debates, wiki written articles and forum flame wars: <strong>usernames aren't enough</strong>.</p>-->
	<p>Popego is a universal widget that feeds from all the web services you love to use. It can easily be embedded on any blog, forum or website. And when you find a Popego anywhere online, you'll discover the real people behind the username.</p> 
	<p>With it you can <strong>find out your reputation on your favorite topics or even how compatible you are with other people.</strong> We support these great services (and many more to come):</p>	
	<p><ul>
		<li><img src="${h.asset_src('/images/icons/flickr_favicon.png')}" class="pngfix"> <a href="http://www.flickr.com" target="_blank">flickr</a>,</li> 
		<li><img src="${h.asset_src('/images/icons/youtube_favicon.png')}"> <a href="http://www.youtube.com" target="_blank">youtube</a>,</li>
		<li><img src="${h.asset_src('/images/icons/del.icio.us_favicon.png')}"> <a href="http://del.icio.us" target="_blank">delicious</a>,</li>
		<li><img src="${h.asset_src('/images/icons/lastfm_favicon.png')}"> <a href="http://www.lastfm.com" target="_blank">last.fm</a>,</li> 
		<li><img src="${h.asset_src('/images/icons/twitter_favicon.png')}"> <a href="http://www.twitter.com" target="_blank">twitter</a>,</li>
		<li><img src="${h.asset_src('/images/icons/wordpress_favicon.png')}"> <a href="http://www.wordpress.com" target="_blank">wordpress</a>,</li> 
		<li><img src="${h.asset_src('/images/icons/google_favicon.png')}"> <a href="http://reader.google.com" target="_blank">google reader</a>,</li>
		<li><img src="${h.asset_src('/images/icons/facebook_favicon.png')}"> <a href="http://www.facebook.com" target="_blank">facebook</a>,</li>
		<li><img src="${h.asset_src('/images/icons/blogger_favicon.png')}"> <a href="http://www.blogger.com" target="_blank">blogger</a>.</li>	
		<br style="clear:both;">		
	</ul></p>
	<p><a href="http://www.popego.com" target="_blank"><img src="${h.asset_src('/images/widget/popballs.png')}" style="float:right;"></a><strong>We are testing our alpha version right now</strong>. <br> <a href="http://www.popego.com" target="_blank">Visit our website to register</a>.</p>
</div>
<!--End of Content -->

</body>
</html>
