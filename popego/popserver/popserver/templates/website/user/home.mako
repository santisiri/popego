<%inherit file="base.mako" />

<%def name="heading_phrase()">Welcome!</%def>

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/card_bubble_default.css', '/css/widget/card_content_bubble.css']))}
</%def>


<script type="text/javascript">
		if (typeof(Popego) == 'undefined') Popego = {};	if (typeof(Popego.Env) == 'undefined') Popego.Env = {}; 
		Popego.Env.username = "${c.user.username if hasattr(c, 'user') else ''}";
</script>

<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(*map(h.asset_src, ['/javascripts/user_home.js', '/javascripts/widget/popego-ext.js', '/javascripts/widget/popego-config.js', '/javascripts/widget/embedder-lib.js']))}
</%def>

<!-- Tour -->
<div class="super_column">
	<div class="tutorial_fact">
		<img src="${h.asset_src('/images/website/tutorial_step_000.png')}">
		<a href="${h.url_for(controller='website/service')}">Start adding your web services here.</a>
		<div class="separator" style="margin:14px 0;"></div>
		<div style="font-size:12px; line-height:22px;">
			The web is full of great services that let you share media and keep in contact with friends. Popego will build a whole profile based on your favorite websites.
		</div>
	</div>
	
	<div class="tutorial_fact">
		<img src="${h.asset_src('/images/website/tutorial_step_001.png')}">
		<a href="${h.url_for(controller='website/widgets')}">Many widget designs available.</a>
		<div class="separator" style="margin:14px 0;"></div>
		<div style="font-size:12px; line-height:22px;">
			Anyone that visits your blog will get to discover all your favorite videos, pictures, blogs, links and more without having to leave your site.
		</div>
	</div>
	
	<div class="tutorial_fact" style="margin:0;">
		<img src="${h.asset_src('/images/website/tutorial_step_002.png')}">
		<a href="#">Discover other Popegos like you.</a>
		<div class="separator" style="margin:14px 0;"></div>
		<div style="font-size:12px; line-height:22px;">
			Each time you see a Popego Widget anywhere online, it will recognize your profile. You'll discover how many interests in common you have with other people and much more.
		</div>
	</div>		
</div>
<!-- End of Tour -->

<div class="column_3">			
	<div class="special_button">
		<img src="${h.asset_src('/images/website/video_icon.png')}" class="pngfix">
		<a href="#"><strong>Popego Video Tour</strong></a>
	</div>
	<div style="font-size:12px; line-height:22px; text-align:center;">
		Learn about Popego in just 3 minutes.
	</div>			
</div>		

<!-- Column 1 bis -->
<div id="popegos_otw" class="column_1_bis">
	<div class="home_item">
		<p>
			<div>
				<h3><strong>Popegos of the World</strong></h3>
				<span>These are the last popegos seen live. Go ahead and meet them!</span>
			</div>
		</p>
		
		% for popego in c.lastPopegos:
		<div class="popego_minicard">
			<a href="#" title="Visit website" target="_blank"><img src="${h.url_for_user_avatar(popego['user'], 200)}" class="avatar_130"></a>
			<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
			<p>
				<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
				<a href="#" theme="${popego['theme']}" username="${popego['user'].username}" title="Discover ${popego['user'].displayname}'s digital life.">${h.truncate(popego['user'].displayname, 16, '...') |h}</a>
			</p>
			<p>
				<img src="${h.asset_src('/images/website/urllink_idle.png')}" class="poplink">
				<a href="${popego['url']}" title="This Popego is hosted in ${popego['url']}" target="_blank">${h.truncate(popego['url'][7:], 15, '...') if popego['url'] else '' |h}</a>								
			</p>					
			<p>
				<h2><strong>${h.gimme_first_valid([popego['compatibility'], '?'],['None'])}% </strong></h2>
				interest match
			</p>
		</div>
		% endfor
		<div style="clear:both;"></div>
	</div>
</div>
<!-- End of Column 1bis-->

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
			<div class="home_item">
				<h3><strong>News &amp; Updates</strong></h3>			
				<div class="announcement">
					<h2>You have <strong>24 new items</strong> on your <a href="#">Social Feed</a>, <strong>6 new followers</strong> on the <a href="#">poplist</a> and <strong>12 users</strong> have <a href="#">checked your popego</a> since yesterday.</h2>
				</div>
				<div class="announcement">
					<h2>We have a <strong>new avatar uploader</strong>. It supports <a href="#">many pictures</a> and it even imports Second Life avatars.</h2>
				</div>				
			</div>
			
			<div class="home_item">				
				<p>
					<div>
					<h3><strong>Last Popegos Met</strong></h3>
					<span>Users that have been checking your popego lately.</span>
					</div>
				</p>
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_031.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Guillermo Gonz...</a>			
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>
				</div>
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_019.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Santiago Coffey</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>					
				</div>
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_022.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Mariano Cortesi</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/collapse_button_idle.png')}" class="poplink">
						<a href="#">Remove</a>						
					</p>					
				</div>				
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_007.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Manuel Aristaran</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>
				</div>
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_029.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Victor Calvello</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>					
				</div>
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_024.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Mariano Cortesi</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>					
				</div>
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_016.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Pranav Laftiti</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>					
				</div>	
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_027.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Bruce Wayne</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>					
				</div>
				<div style="clear:both;"></div>
				<p>
					<div class="show_more_updates"><a href="#">Show 4 more popegos.</a></div>
				</p>	
			</div>
			
			<div class="home_item" style="display:none;">					
				<p>
					<h3><strong>Reccommended Popegos</strong></h3>
					Based on common interests and our secret sauce, these are popegos you might want to meet.
				</p>	
			
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_006.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Guillermo Gonz...</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>
				</div>
				
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_009.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Victor Calvello</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>					
				</div>
				
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_028.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Mariano Cortesi</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/collapse_button_idle.png')}" class="poplink">
						<a href="#">Remove</a>						
					</p>					
				</div>				
				
				<div class="popego_minicard">
					<img src="${h.asset_src('/images/website/samples/avatar_sample_013.png')}" class="avatar_130">
					<div class="frame_130"><img src="${h.asset_src('/images/website/avatar_frame_130_white.png')}" class="pngfix"></div>
					<p>
						<img src="${h.asset_src('/images/website/poplink_idle.png')}" class="poplink">
						<a href="#">Manuel Aristaran</a>					
					</p>
					<p>
						<img src="${h.asset_src('/images/website/expand_button_idle.png')}" class="poplink">
						<a href="#">Follow</a>						
					</p>
				</div>						
				
				<div style="clear:both;"></div>
				You and them have these interests in common: 
				<p>
					<div class="tag_list">
						<ul>
							<li><strong>Boca Juniors</strong></strong> + </li> 
							<li><strong>Carmen San Diego</strong> + </li>  
							<li><strong>iPhone</strong> + </li>  
							<li><strong>Apple Computer Inc.</strong></li>
						</ul>
					</div>
				</p>
				<div style="clear:both;"></div>
				<p>					
					<div class="show_more_updates"><p><a href="#">Discover other popegos like you.</a></p></div>
				</p>		
			</div>	
		</div>
		<!-- End of Services -->		
	</div>
	<!-- End of Column 1 -->

	<!-- Column 3 -->
	<div class="column_3">
		<%doc>
		<div id="highlight">
			<div class="dialog"><div class="bubble"><div class="t"></div>
				<h3><strong>Popego Completeness</strong></h3>
				<div class="percentage_box_full"></div>
				<div class="percentage_box_full"></div>
				<div class="percentage_box_full"></div>
				<div class="percentage_box_full"></div>
				<div class="percentage_box_full"></div>		
				<div class="percentage_box"></div>
				<div class="percentage_box"></div>
				<div class="percentage_box"></div>
				<div class="percentage_box"></div>
				<div class="percentage_box"></div>
				<div class="percentage_number">
					<h2><strong>80%</strong></h2>
				</div>
				<div style="clear:both;"></div>
				<!-- <p style="text-align:center;">
					<a href="#">Your pending actions</a>
					<img src="images/website/arrow_down_white.png">
				</p>-->
				<!-- NOTA: Cuando se hace click en "Your Pending Actions", esto hace que se expanda el 
						   DIV y aparezca la lista de abajo. El link "your pending actions" desaparece
						   por el de "Collapse List". -->
				<ul class="completeness_list">
					<li>Upload an <strong>Avatar</strong></li>
					<li class="completeness_done">Add 5 web <strong>Services</strong></li>
					<li>Publish a <strong>Widget</strong></li>
					<li class="completeness_done">Complete your <strong>Profile</strong></li>						
					<li>Define your <strong>Interests</strong></li>
					<li>Include <strong>Social Networks</strong></li>
				</ul>
				<p style="text-align:center;">
					<a href="#">Collapse list</a>
					<img src="${h.asset_src('/images/website/arrow_up_white.png')}">
				</p>					
			</div><div class="b"><div></div></div></div>	
		</div>
		</%doc>
		<img src="${h.asset_src('/images/website/popego_completeness.gif')}" />
		<div class="separator"></div>						
		<p>
			<h3><strong>Quick Stats</strong></h3>
		</p>
		<%doc>
		<p>
			<div class="dialog"><div class="bubble"><div class="t"></div>
				<ul class="pop_stats">
					<li>
						You are following <strong>74 popegos</strong>.
					</li>
					<li>
						<strong>340 popegos</strong> are following you.
					</li>
					<li>
						Last week your popego was viewed <strong>203 times</strong>.
					</li>
					<li>
						Since October 2008, you've had <strong>33,029 views</strong>.
					</li>
				</ul>		
			</div><div class="b"><div></div></div></div>						
		</p>
		</%doc>
		<img src="${h.asset_src('/images/website/quick_stats.gif')}" />
	</div>
	<!-- End of Column 3 -->
</div>
