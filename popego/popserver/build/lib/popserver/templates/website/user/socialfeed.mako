<%inherit file="base.mako" />

<%def name="heading_phrase()">Last updates on the Popegos you follow.</%def>

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/card_bubble_default.css', '/css/widget/card_content_bubble.css']))}
</%def>

<script type="text/javascript">
		if (typeof(Popego) == 'undefined') Popego = {};	if (typeof(Popego.Env) == 'undefined') Popego.Env = {}; 
		Popego.Env.username = "${c.user.username if hasattr(c, 'user') else ''}";

		window.addEvent('domready', function() {
			$ES('.coming_soon_wrapper').setStyle('opacity', 0.3);
		});
</script>

<div class="super_column">
	<div style="text-align:center; width:100%; margin:40px 0px; line-height:26px;">
	<a href="javascript:Popego.Feedback.showForm();">
		<img src="${h.asset_src('/images/website/coming_soon.png')}" title="Give us your feedback!">
	</a>
	</div>		
</div>			
<!--Coming Soon Wrapper Begins here -->
<div class="coming_soon_wrapper" title="We are developing many new features. Stay tuned!">
	
	
		<!-- Column 1 -->
		<div class="column_1_bis" style="float:left;">
			
			<!-- Services -->
			<div class="popego_feed">
				
				<!-- CSS for Updates -->
				<link href="/css/website/updates.css" rel="stylesheet" type="text/css" />
				
				<h3><strong>Popego Updates</strong></h3>
				
				<p>
					<div class="databox">
						<div class="category_selected"><strong>all media</strong>,</div>
						<div class="category"><strong>videos</strong>,</div>
						<div class="category"><strong>pictures</strong>,</div>
						<div class="category"><strong>blog posts</strong>,</div>
						<div class="category"><strong>quotes</strong>,</div>
						<div class="category"><strong>music</strong>,</div>
						<div class="category"><strong>other</strong>.</div>
					</div>					
				</p>
				
				
				<!-- List of Updates -->
				<ul class="popego_updates">
					
					<div class="date_separator">
						<div style="float:left;">
							Today
						</div>
						<div style="float:right">
							<a href="#" style="font-size:11px;"><img src="${h.asset_src('/images/website/collapse_button_idle.png')}" class="poplink" title="collapse"></a>
						</div>
						<div style="clear:both"></div>
					</div>
					
					<li class="photo">
						<!--<img src="/images/icons/flickr_favicon.png" class="icon">-->
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Manuel Aristaran</a>
						has published 25 new <strong>photos</strong>.
						<p>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/website/samples/avatar_180_000.png')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/website/samples/avatar_180_001.png')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/website/sample_avatar.jpg')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/website/sample_thumbnail_01.png')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/widget/samples/sample_thumb_003.jpg')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/widget/samples/sample_thumb_002.jpg')}" class="thumbnail"></a>														
						</p>
						<h5>17 minutes ago, from <img src="${h.asset_src('/images/icons/flickr_favicon.png')}" class="icon"> <a href="#">Flickr</a> and <img src="${h.asset_src('/images/icons/facebook_favicon.png')}" class="icon">  <a href="#">Facebook</a>.</h5>
					</li>

					<li class="quote">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Fernando Zunino</a>
						was <strong>quoted</strong> saying:
						<p>
							<h2><img src="${h.asset_src('/images/website/quote_left.png')}" class="quotepic">Increible.. despues de haberlo visto en TN defendiendo la valija, me lo encuentro a Rossi, lider del bloque Kirchnerista, en el Che Bs. As..<img src="${h.asset_src('/images/website/quote_right.png')}" class="quotepic"></h2>
						</p>
						<h5>7 hours ago from <img src="${h.asset_src('/images/icons/twitter_favicon.png')}" class="icon"> <a href="#">Twitter</a>.</h5>
					</li>
					

					<li class="video">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Santiago Coffey</a>
						has favorited 2 new <strong>videos</strong>.
						<p>
							<a href="#" target="_blank" title="The title of the video"><img src="${h.asset_src('/images/widget/samples/sample_thumb_008.jpg')}" class="thumbnail"><%doc><div class="thumb_icon"><img src="${h.asset_src('/images/website/thumb_icon_play.png')}"></div></%doc></a>
							<a href="#" target="_blank" title="The title of the video"><img src="${h.asset_src('/images/widget/samples/sample_thumb_009.jpg')}" class="thumbnail"><%doc><div class="thumb_icon"><img src="${h.asset_src('/images/website/thumb_icon_play.png')}"></div></%doc></a>
						</p>
						<h5>3 days ago from <img src="${h.asset_src('/images/icons/youtube_favicon.png')}" class="icon"> <a href="#">YouTube</a>.</h5>
					</li>
					
					<li class="feed">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Fernando Zunino</a>
						wrote a new <strong>blog post</strong>.
						<p>

							<a href="#" class="postlink">An Update About Playdreamer</a>

						</p>
						<h5>on September 27, 2007 from <img src="${h.asset_src('/images/icons/rss_favicon.png')}" class="icon"> <a href="#">Blog Feed</a>.</h5>
					</li>
					
					<li class="music">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Victor Calvello</a>
						has been listening <strong>music</strong>.
						<p>
							<a href="#" target="_blank" title="Artist Name"><img src="${h.asset_src('/images/widget/samples/sample_artist_000.png')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="Artist Name"><img src="${h.asset_src('/images/widget/samples/sample_artist_001.png')}" class="thumbnail"></a>																					
							<a href="#" target="_blank" title="Artist Name"><img src="${h.asset_src('/images/widget/samples/sample_artist_002.png')}" class="thumbnail"></a>
						</p>
						<h5>on September 27, 2007 from <img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon"> <a href="#">Last.FM</a>.</h5>
					</li>											
					
					<li class="link">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Mariano Cortesi</a>
						has bookmarked a new <strong>link</strong>.
						<p>

							<a href="#" class="postlink">How to develop on Haskell while standing on one foot</a>
							<p class="link_comment"><img src="${h.asset_src('/images/website/quote_left.png')}" class="quotepic">It's a nice article on how I've learned to stop hating and start loving the bomb.<img src="${h.asset_src('/images/website/quote_right.png')}" class="quotepic"></p>

						</p>
						<h5>on September 27, 2007 from <img src="${h.asset_src('/images/icons/del.icio.us_favicon.png')}" class="icon"> <a href="#">Delicious</a>.</h5>
					</li>		
					
					<div class="date_separator">
						<div style="float:left;">
							Yesterday
						</div>
						<div style="float:right">
							<a href="#" style="font-size:11px;"><img src="${h.asset_src('/images/website/collapse_button_idle.png')}" class="poplink" title="collapse"></a>
						</div>
						<div style="clear:both"></div>
					</div>
											
					<li class="photo">
						<!--<img src="/images/icons/flickr_favicon.png" class="icon">-->
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Manuel Aristaran</a>
						has published 25 new <strong>photos</strong>.
						<p>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/widget/samples/sample_thumb_007.jpg')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/widget/samples/sample_thumb_006.jpg')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="The title of the photo"><img src="${h.asset_src('/images/widget/samples/sample_thumb_010.jpg')}" class="thumbnail"></a>
						</p>
						<h5>17 minutes ago, from <img src="${h.asset_src('/images/icons/flickr_favicon.png')}" class="icon"> <a href="#">Flickr</a> and <img src="${h.asset_src('/images/icons/facebook_favicon.png')}" class="icon">  <a href="#">Facebook</a>.</h5>
					</li>

					<li class="quote">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Fernando Zunino</a>
						was <strong>quoted</strong> saying:
						<p>
							<h2><img src="${h.asset_src('/images/website/quote_left.png')}" class="quotepic">Increible.. despues de haberlo visto en TN defendiendo la valija, me lo encuentro a Rossi, lider del bloque Kirchnerista, en el Che Bs. As..<img src="${h.asset_src('/images/website/quote_right.png')}" class="quotepic"></h2>
						</p>
						<h5>7 hours ago from <img src="${h.asset_src('/images/icons/twitter_favicon.png')}" class="icon"> <a href="#">Twitter</a>.</h5>
					</li>
					

					<li class="video">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Santiago Coffey</a>
						has favorited 2 new <strong>videos</strong>.
						<p>
							<a href="#" target="_blank" title="The title of the video"><img src="${h.asset_src('/images/widget/samples/sample_thumb_012.jpg')}" class="thumbnail"><%doc><div class="thumb_icon"><img src="${h.asset_src('/images/website/thumb_icon_play.png')}"></div></%doc></a>
							<a href="#" target="_blank" title="The title of the video"><img src="${h.asset_src('/images/widget/samples/sample_thumb_013.jpg')}" class="thumbnail"><%doc><div class="thumb_icon"><img src="${h.asset_src('/images/website/thumb_icon_play.png')}"></div></%doc></a>																					
						</p>
						<h5>3 days ago from <img src="${h.asset_src('/images/icons/youtube_favicon.png')}" class="icon"> <a href="#">YouTube</a>.</h5>
					</li>
					
					<div class="date_separator">
						<div style="float:left;">
							Last Week
						</div>
						<div style="float:right">
							<a href="#" style="font-size:11px;"><img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink" title="expand"></a>
						</div>
						<div style="clear:both"></div>
					</div>

					<div class="date_separator">
						<div style="float:left;">
							2 Weeks Ago
						</div>
						<div style="float:right">
							<a href="#" style="font-size:11px;"><img src="${h.asset_src('/images/website/collapse_button_idle.png')}" class="poplink" title="collapse"></a>
						</div>
						<div style="clear:both"></div>
					</div>											
					
					<li class="feed">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Fernando Zunino</a>
						wrote a new <strong>blog post</strong>.
						<p>

							<a href="#" class="postlink">An Update About Playdreamer</a>

						</p>
						<h5>on September 27, 2007 from <img src="${h.asset_src('/images/icons/rss_favicon.png')}" class="icon"> <a href="#">Blog Feed</a>.</h5>
					</li>
					
					<li class="music">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Victor Calvello</a>
						has been listening <strong>music</strong>.
						<p>
							<a href="#" target="_blank" title="Artist Name"><img src="${h.asset_src('/images/widget/samples/sample_artist_003.png')}" class="thumbnail"></a>
							<a href="#" target="_blank" title="Artist Name"><img src="${h.asset_src('/images/widget/samples/sample_artist_004.png')}" class="thumbnail"></a>																					
							<a href="#" target="_blank" title="Artist Name"><img src="${h.asset_src('/images/widget/samples/sample_artist_006.png')}" class="thumbnail"></a>
						</p>
						<h5>on September 27, 2007 from <img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon"> <a href="#">Last.FM</a>.</h5>
					</li>											
					
					<li class="link">
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Mariano Cortesi</a>
						has bookmarked a new <strong>link</strong>.
						<p>

							<a href="#" class="postlink">How to develop on Haskell while standing on one foot</a>
							<p class="link_comment"><img src="${h.asset_src('/images/website/quote_left.png')}" class="quotepic">It's a nice article on how I've learned to stop hating and start loving the bomb.<img src="${h.asset_src('/images/website/quote_right.png')}" class="quotepic"></p>

						</p>
						<h5>on September 27, 2007 from <img src="${h.asset_src('/images/icons/del.icio.us_favicon.png')}" class="icon"> <a href="#">Delicious</a>.</h5>
					</li>														
					
				</ul>
				<!-- End of List of Updates -->
				
				<p>
					<div class="show_more_updates"><a href="#">Show 10 more updates.</a></div>
				</p>							
			</div>
			<!-- End of Services -->
		
		</div>
		<!-- End of Column 1 -->
		
		<!-- Column 3 -->
		<div class="column_3">

			<h3><strong>Poplist</strong></h3>
			<%doc>
			<p>
				<div class="dialog"><div class="bubble"><div class="t"></div>
					
					<form style="text-align:center; padding:0px; margin:0px;">
						Show:
						<select size="1" id="embed" name="embed">
							<option value="0">All Popegos</option>
							<option value="1">Updated Popegos</option>
							<option value="2">My Followers</option>
						</select>
					</form>						
					
					<p></p>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_000.png')}" class="thumbnail">
							Fernando Zunino
						</a>
					</div>

					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_001.png')}" class="thumbnail">
							Victor Calvello
						</a>
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_002.png')}" class="thumbnail">
							Manuel Aristaran
						</a>
					</div>			
					
					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_003.png')}" class="thumbnail">
							Stevie Wonder
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>
					</div>

					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_004.png')}" class="thumbnail">
							Mariano Cortesi
						</a>
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_005.png')}" class="thumbnail">
							Enjuto Mojamuto
						</a>
					</div>			
									
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_006.png')}" class="thumbnail">
							Santiago Coffey
						</a>
					</div>
					
					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_007.png')}" class="thumbnail">
							Santiago Siri
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>						
					</div>
					
					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_023.png')}" class="thumbnail">
							Fernando Zunino
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>						
					</div>

					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_009.png')}" class="thumbnail">
							Victor Calvello
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>						
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_010.png')}" class="thumbnail">
							Manuel Aristaran
						</a>
					</div>			
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_011.png')}" class="thumbnail">
							Stevie Wonder
						</a>
					</div>

					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_012.png')}" class="thumbnail">
							Mariano Cortesi
						</a>
					</div>
					
					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_013.png')}" class="thumbnail">
							Enjuto Mojamuto
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>						
					</div>			
									
					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_014.png')}" class="thumbnail">
							Santiago Coffey
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>						
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_015.png')}" class="thumbnail">
							Santiago Siri
						</a>
					</div>	

					<div class="popego_avatar_thumbnail" title="Updated">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_016.png')}" class="thumbnail">
							Victor Calvello
						</a>
						<div class="updated_popego_thumb">
							<img src="${h.asset_src('/images/website/updated_popego.png')}">
						</div>						
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_017.png')}" class="thumbnail">
							Manuel Aristaran
						</a>
					</div>			
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_018.png')}" class="thumbnail">
							Stevie Wonder
						</a>
					</div>

					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_019.png')}" class="thumbnail">
							Mariano Cortesi
						</a>
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_020.png')}" class="thumbnail">
							Enjuto Mojamuto
						</a>
					</div>			
									
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_021.png')}" class="thumbnail">
							Santiago Coffey
						</a>
					</div>
					
					<div class="popego_avatar_thumbnail">
						<a href="#">
							<img src="${h.asset_src('/images/website/samples/pop_avatar_022.png')}" class="thumbnail">
							Santiago Siri
						</a>
					</div>								
																
					<div style="clear:both"></div>	
													
					
				</div><div class="b"><div></div></div></div>							
			</p>
		</%doc>
		<img src="/images/website/poplist.gif" />
			
		<div class="separator"></div>									
		
		<p>
			<h3><strong>Poplist Facts</strong></h3>
		</p>
		<%doc>
			<p>
				<div class="dialog"><div class="bubble"><div class="t"></div>
					
					<ul class="pop_stats">
						<li>
							Popego with most updates.
						</li>
						
						<li>
							Popego with more friends in common.
						</li>
						
						<li>
							Popego with more popularity
						</li>
						
						<li>
							Popego with most compatibility
						</li>
					</ul>		
													
					
				</div><div class="b"><div></div></div></div>						
					
			</p>			
		</%doc>
		<img src="/images/website/popego_facts.gif" />
		</div>
		<!-- End of Column 3 -->
</div>
