<%inherit file="base.mako" />

<%def name="heading_phrase()">Add the services you want.</%def>

<script type="text/javascript">
		if (typeof(Popego) == 'undefined') Popego = {};	if (typeof(Popego.Env) == 'undefined') Popego.Env = {}; 
		Popego.Env.username = "${c.user.username if hasattr(c, 'user') else ''}"; Popego.Env.baseUrl= "${c.baseUrl if hasattr(c, 'baseUrl') else ''}";
		Popego.Env.remoteUser = "${c.remoteUser if hasattr(c, 'remoteUser') else ''}"; 
		Popego.Env.remoteUserLoggedIn = Boolean("${c.remoteUserLoggedIn if hasattr(c, 'remoteUserLoggedIn') else 'False'}" == "True");
		Popego.Env.parentUrl = (document.referrer.split('?')[0] == location.href.split('?')[0]) ? "${c.parentUrl if hasattr(c, 'parentUrl') else '/'}" : document.referrer;
</script>

<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(h.asset_src('/javascripts/user_services.js'))}
</%def>

	<!-- Column 1/2 -->
    <div class="column_1bis">
      
      <!-- Services -->
      <div class="services">
	<h3><strong>List of Web Services</strong></h3>
	<span>Integrate all your web services in your Popego.</span>
	<img src="${h.asset_src('/images/website/tutorial_icon.png')}" class="help_box pngfix" title="List of Web Services::<strong>Popego</strong> integrates your fragmented digital identity (the many profiles you have on the web) in one single place. <br/><br/>This permits that each time someone finds you on a blog, forum or website, if he clicks on your <strong>Popego</strong>, he'll be able to get a glimpse of your interests, the media you like and how to reach you, all in one single place.">	
	<p>
	  <div class="databox">
	    <div class="service_type_tab">
	      <div class="category_selected"><strong>all</strong>,</div>
	      % for a in c.serviceTypes:
	      <div class="category">
		%if a==c.serviceTypes[-1]:
		and <strong>${a.type}</strong>.
		%else:
		<strong>${a.type}</strong>,
		%endif
	      </div>
	      % endfor
	    </div>
	  </div>		
	  
	  <div class="services_error_box" style="display:none">Mensaje de error</div>
	  
	  <!-- List of Services -->
	  <ul class="service_list">
	    <%
	       servicesAdded = [a.service.id for a in c.accounts]
	       def getAccount(sid):
	         for a in c.accounts:
	           if a.service.id == sid:
	             return a
	     %>
	    % for service in c.services:
	    <li id="srv${service.id}" class=${service.type.type}>
	      <div>
			<img src=${service.faviconURL()} class="pngfix"/>
			<span class="service_name">${service.name}</span>
		  </div>
	      <form class="search">
		%if service.id in servicesAdded:
		<% account = getAccount(service.id) %>
		<span class="prompt_text" style="display:none">${service.prompt_text}</span>
		<span class="added_text">${service.added_text}</span>
		  %if account.home_url is not None:
		  <span class="user_text"><a href="${account.home_url}">${account.username}</a>.</span>
		  %else:
		  <span class="user_text"><strong>${account.username}</strong><span>.</span></span>
		  %endif
		<span class="error_text" style="display:none"></span>
		<img src="${h.asset_src('/images/website/spinner_white.gif')}" style="display:none" class="spinner"/>
		<input type="text" name="username" value="" style="display:none"/>
		<input type="button" value="modify" class="button" style="display:none"/>
		<input type="button" value="remove" class="button" style="display:none"/>
		<input type="button" value="add" class="button"/>

		%else:

		<span class="prompt_text">${service.prompt_text}</span>
		<span class="added_text" style="display:none">${service.added_text}</span>
		<span class="user_text" style="display:none"><a href="#"></a>.</span>
		<span class="error_text" style="display:none"></span>
		<img src="${h.asset_src('/images/website/spinner_white.gif')}" style="display:none" class="spinner"/>
		<input type="text" name="username" value="" />
		<input type="button" value="modify" class="button" style="display:none"/>
		<input type="button" value="remove" class="button" style="display:none"/>
		<input type="button" value="add" class="button"/>
		%endif
	      </form>
	    </li>
	    % endfor
	  </ul>
	  <!-- End of List of Services -->
	</p>
	
	<p>					
	  <div class="show_more_updates"><p><a href="javascript:Popego.Feedback.showForm(1);">Suggest a web service.</a></p></div>
	</p>
	<p>
		<div style="text-align:center; width:100%; margin:40px 0px; line-height:26px;">
			<a href="javascript:Popego.Feedback.showForm();">
				<img src="${h.asset_src('/images/website/coming_soon.png')}" title="Give us your feedback!">
			</a>
		</div>		
	</p>
		<!--Coming Soon Wrapper Begins here -->
		<div class="coming_soon_wrapper" title="We are developing many new features. Stay tuned!">

			  <h3><strong>Your Interests</strong></h3>
			  Based on your tags, media and connections these are the interests we have detected.	
			<br>Help us get more accurate results by removing irrelevant tags.		
	
			<p>
			  <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" width="600" height="350" id="charts_mockup" align="middle">
				<param name="allowScriptAccess" value="sameDomain" />
				<param name="allowFullScreen" value="false" />
				<param name="wmode" value="transparent" />
				<param name="movie" value="/flash/website/interest_chart.swf" /><param name="quality" value="high" /><param name="bgcolor" value="#ffffff" />	<embed src="/flash/website/interest_chart.swf" wmode="transparent" quality="high" bgcolor="#ffffff" width="600" height="350" name="/flash/interest_chart.swf" align="middle" allowScriptAccess="sameDomain" allowFullScreen="false" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />
			  </object>
			</p>	
		</div>
	<p>&nbsp;</p>
      </div>
    </div>
    <!-- End of Column 1 -->
    
    <!-- Column 3 -->
    <div class="column_3">
		<!-- Tags -->
		<div class="tag_list">
			<h3><strong>Your Top Tags</strong></h3>
			<span>Based on all your Services.</span>
			<img src="${h.asset_src('/images/website/tutorial_icon.png')}" class="help_box pngfix" title="Your Top Tags::These tags are the words that define your identity and skills. They are obtained from the content of your web services.<br/><br/>Each time you browse the web and find a <strong>Popego</strong>, the system will be able to measure your compatibility with that user based on this Tags.<br/><br/>Also, brands and companies may sponsor <br/>your knowledge on the areas you consider you're best at.">
			<p>
				<div class="dialog"><div class="bubble"><div class="t"></div>
					<!-- List of Tags -->			
					<div class="tag_cloud" id="tag_cloud">
						% for tagCount in c.myTopTags:
						<span class="tag_hits_${tagCount['className']}">${tagCount['tagName'] |h}</span>
						% endfor
					</div>
					<!-- End List of Tags -->
					<p>
						<div class="trash_panel" id="trash_panel" style="display:${ 'none' if len(c.myTopTags) == 0 else ''}">
							<img src="${h.asset_src('/images/website/trash_icon.png')}" class="pngfix">
							<p>
								Drag here tags that don't describe your interests 
								or words that aren't topics (like "cool", "interesting").
							</p>
							<!-- NOTA: Una vez que se hizo el "drop" del item, pregunta para confirmar! -->
							<!--
							<img src="${h.asset_src('images/website/trash_icon_hover.png')}">
							<p>
								Do you confirm you want to delete the tag <strong>Supercanciones</strong>?
							</p>
							<a href="#">Yes, delete it</a> or <a href="#">No, cancel!</a>
							-->
						</div>
					</p>
					<div class="message" id="toptags_message" style="display:${ '' if len(c.myTopTags) == 0 else 'none'};">
						You have no tags yet. Start feeding your Popego with the services you commonly use so it can know you better.
					</div>
					<br id="clear_trick" style="clear:both;display:${ '' if len(c.myTopTags) == 0 else 'none'};"/>
				</div><div class="b iefix"><div></div></div></div>
			</p>
      </div>
      <!-- End of Tags -->
      <div style="clear:both;"></div>
     <%doc> <p>
	<div class="arrow_up"></div>
	<div class="dialog"><div class="bubble"><div class="t"></div>	
	    Add a missing or removed tag
	    <p>
	      <form action="#" id="add" class="">
		<input type="text" id="tag" value="" style="width:160px" />
		<input type="submit" value="add" class="button"/>
	      </form>	
	    </p>
	  </div><div class="b"><div></div></div></div>
      </p>
	</%doc>
    </div>
    <!-- End of Column 3 -->
    
