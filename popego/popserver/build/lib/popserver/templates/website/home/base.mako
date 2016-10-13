<%inherit file="/website/base.mako" />
<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(h.asset_src('/css/website/teaser.css'))}
</%def>
<div class="background">
	<div class="content">
		<!-- Teaser Widget -->
		<div class="teaser_widget">
			<img src="${h.asset_src('/images/website/teaser_widget.png')}" width="266px" height="385px" class="pngfix"/>
			<div class="final_links_alt">
			<%doc>
        	    <img src="${h.asset_src('images/website/question_green.png')}" class="pngfix" style="margin-top:-2px;margin-right:2px;">
				<%
					if h.current_url() == '/signup':
						quest = 'Already a user?'
						link = h.url_for(controller='website/home')
						text = 'Login here'
					else:
						quest = 'Not a user?'
						link = h.url_for(controller='website/users')
						text = 'Sign up here'
				%>
				${quest} <a href="${link}">${text}</a>.
			</%doc>
				<p><strong>We're hiring!</strong> Contact us at <a href="mailto:jobs@popego.com">jobs@popego.com</a></p>
			</div>
			

		</div>
		<!-- End of Teaser Widget -->
		
		<!-- Teaser Popcard -->
		<!--<div class="teaser_popcard_background">
			<img src="${h.asset_src('/images/website/teaser_popcard.png')}" width="554px" height="487px" />
		</div>-->
		<div class="teaser_popcard">
			<img src="${h.asset_src('/images/website/teaser_popcard.png')}" width="554px" height="487px" class="pngfix_scale" style="position:absolute; top:0px; left:0px; z-index:0;" />
			<!--<div class="hello_box">-->
			<img src="${h.asset_src('/images/website/alpha_slogan.png')}" title="Click to learn more." style="position:relative;margin:17px;"/>
			<!--</div>-->
<%
try:
	display = self.display_box()
except:
	display = True 
%>
% if display:
			<!-- NOTA: En Explanation Box, el link que dice "Learn More" y tambein el link de arriba ("Gather everything..") 
					   le pone el display:none al DIV de abajo y muestra el DIV de mas abajo (Explanation Box FULL SIZE) -->
			
			<!-- Explanation Box -->
			<div class="explanation_box" style="display:block">
				<!--<p>The web is beautiful. You can share videos at <a href="#">youtube</a>, pictures at <a href="#">flickr</a>, links at <a href="#">delicious</a> or contacts at <a href="#">facebook</a>. These and other services do a terrific job at their task. But as a user, you end up having your identity fragmented with many profiles: one for each service you want to use.</p>-->
				<p style="*margin-top:5px;_margin-top:12px;">Popego is a universal widget that feeds from all the web services you love to use. It can easily be embedded on any blog, forum or website. And when you find a Popego anywhere online, you'll discover the real people behind the username. <a href="javascript:void(0);" id="learn_more">Learn more.</a></p>
			</div>
			<!-- End of Explanation Box -->
			
			<!-- Explanation Box FULL SIZE -->
			<div class="explanation_box" id="full_explanation_box" style="display:none">
				<p style="*margin-top:5px;_margin-top:12px">Popego is a universal widget that feeds from all the web services you love to use. It can easily be embedded on any blog, forum or website. And when you find a Popego anywhere online, you'll discover the real people behind the username.</p><p><strong>Find out your reputation on your favorite topics or even how compatible you are with other people.</strong> Right now we support these great services (and many more to come):</p>
				<ul>
					<li><img src="${h.asset_src('/images/icons/flickr_favicon.png')}" class="pngfix"> <a href="http://www.flickr.com" target="_blank">flickr</a>,</li> 
					<li><img src="${h.asset_src('/images/icons/youtube_favicon.png')}"> <a href="http://www.youtube.com" target="_blank">youtube</a>,</li>
					<li><img src="${h.asset_src('/images/icons/del.icio.us_favicon.png')}"> <a href="http://del.icio.us" target="_blank">delicious</a>,</li>
					<li><img src="${h.asset_src('/images/icons/twitter_favicon.png')}"> <a href="http://www.twitter.com" target="_blank">twitter</a>,</li>
					<li><img src="${h.asset_src('/images/icons/lastfm_favicon.png')}"> <a href="http://www.last.fm" target="_blank">last.fm</a>.</li> 
				</ul>
				<p>There are many cool features waiting to be discovered. <a href="javascript:void(0);" id="give_it_a_try">Give it a try.</a></p>			
			</div>
			<!-- End of Explanation Box FULL SIZE -->
% endif					

			${next.body()}
					
		</div>
		<!-- End Teaser Popcard -->
		
		<div class="final_links">
			&copy; 2008 Popego Inc.
			<a href="http://blog.popego.com" target="_blank">Pop Blog</a>
			<a href="mailto:contact@popego.com">Contact Us</a>
		</div>
	</div>

</div>
	<script type="text/javascript">
	//<![CDATA[
		// links
		var explanationBox = $E('.explanation_box');
		var fullExplanationBox = $('full_explanation_box');
		var loginForm = $E('.login_form');
		
		function openFullExplanationBox() {
			explanationBox.setStyle('display', 'none');
			fullExplanationBox.setStyle('display', 'block');
			loginForm.setStyle('display', 'none');
			return false;
		}

		function closeFullExplanationBox() {
			explanationBox.setStyle('display', 'block');
			fullExplanationBox.setStyle('display', 'none');
			loginForm.setStyle('display', 'block');
			return false;
		}
		try {	
			$('learn_more').addEvent('click', openFullExplanationBox);
			//$('yet_another_learn_more').addEvent('click', openFullExplanationBox);
			$('give_it_a_try').addEvent('click', closeFullExplanationBox);
			$('learn_more').focus();
		} catch (e) {
		}
	//]]>
	</script>
