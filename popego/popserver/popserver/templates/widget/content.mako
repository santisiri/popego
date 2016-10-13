<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Popego</title>
    
	<link href="/css/widget/widget_content_default.css" rel="stylesheet" type="text/css" />
    <link href="/css/widget/themes/widget_content_${c.theme}.css" rel="stylesheet" type="text/css" />
	<!--[if lt IE 7.]>
	<link href="/css/ie6.css" rel="stylesheet" type="text/css" />
	<![endif]-->
	
	<script type="text/javascript" src="/javascripts/mootools.js"></script>
	<script type="text/javascript">
	//<![CDATA[
		var Popego= {}; 
		Popego.Env = {}; Popego.Env.username = "${c.user.username}"; Popego.Env.baseUrl= "${c.baseUrl}";
		Popego.Env.remoteUser = "${c.remoteUser.username if c.remoteUser is not None else ''}"; Popego.Env.remoteUserLoggedIn = Boolean("${c.remoteUserLoggedIn}" == "True");
		Popego.Env.parentUrl = (document.referrer.split('?')[0] == location.href.split('?')[0]) ? "${c.parentUrl if c.parentUrl else '/'}" : document.referrer;
		Popego.Env.theme = "${c.theme}"; 
		Popego.Env.cache = (Popego.Env.parentUrl.indexOf(Popego.Env.baseUrl) != 0);
	//]]>
	</script>
	<script type="text/javascript" src="/javascripts/widget_content.js"></script>
	
</head>
<body style="background-image:url(/images/widget/widget_background_${c.theme}.png);">
	<div class="wrapper"></div>
	
	<!-- Avatar and Name -->
	<a href="http://www.popego.com" target="_blank"><img src="${h.asset_src('/images/widget/logo_micro.png')}" title="Popego.com" class="logo pngfix" alt="Popego.com" /></a>
	<span class="username"><h3>${h.truncate(c.user.displayname, 20, '...') |h}</h3></span>
	<img src="${c.myAvatar}" width="150" height="150" class="avatar" alt="${(c.user.displayname) |h}'s avatar" title="" />
    <div class="frame"></div>
	<!-- End of Avatar and Name -->
    
	%if not c.error:
	<!-- GUI #1: Flashing Facts -->
    <div id="facts" class="fact">
    	<!-- Media Preview -->
		% if c.myLastMedia:
		<div class="fact media" style="display: none;">
			Last media
			<p>
			% for m in c.myLastMedia:
				<img style="background:url(${m['thumbnail'] |h}) 30% center no-repeat;" alt="${m['title'] |h}" src="/images/widget/blank.gif" title="${m['title'] |h}" longdesc="${m['description'] |h}" />
			% endfor
			</p>
		</div>
		% endif
		<!-- End of Media Preview -->
      
		<!-- Quotation -->
		% if c.myQuoteAccount:
		<div class="fact quotation" style="display: none;">
			<img src="${h.asset_src('/images/widget/quote_left_white.png')}" alt="&quot;" class="pngfix"/><span id="quote_text">&nbsp;</span><img src="${h.asset_src('/images/widget/quote_right_white.png')}" alt="&quot;" class="pngfix"/>
		</div>
		% endif
		<!-- End of Quotation -->
		
		<%doc>
		<!-- Real and Virtual Location -->
		<div class="fact location" style="display: none;">
			<img src="${h.asset_src('/images/widget/profile/status_online.png')}" title="Online" alt="" class="pngfix" /> <img src="${h.asset_src('/images/widget/profile/nation_cameroon.png')}" title="Connected from Yahounde, Cameroon." alt="" class="pngfix"/>
			<p style="margin-top:-10px;_margin-top:-7px;text-align:left;">
				<strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Online</strong>.
			</p>
			<p style="text-align:left;">
				Connected from Wichita, US.
			</p>
		</div>
		<!-- End of Real and Virtual Location -->
		<%/doc>
		<%doc>
		<!-- Sponsor -->
		<div class="fact sponsor" style="display:none">
			<img src="${h.asset_src('/images/widget/samples/sample_sponsor_000.png')}" alt="" class="pngfix"/>
			<p>
				Just Do It.
			</p>
		</div>
		<!-- End of Sponsor -->
		</%doc>
		<%doc>
		<!-- Blog Post -->
		<div class="fact post" style="display:none">
			<br />
			<img src="${h.asset_src('/images/widget/standard_rss.png')}" alt="" class="pngfix_scale" /> Last blog update
			<p>
				<strong>Oh yeah, so now what?</strong>
			</p>
			<h5>October 26, 2007</h5>
		</div>
		<!-- End of Blog Post -->
		</%doc>

		<!-- Tags -->
% if c.myTopTags:
		<div class="fact tags" style="display:none">
			<ul>
<%
from random import shuffle
tagIndexes = range(0, len(c.myTopTags) - 1)
shuffle(tagIndexes)
hitClasses = ['highest', 'top', 'top', 'middle', 'middle', 'low', 'low', 'lowest']
k = float(len(hitClasses) + 1) / float(len(c.myTopTags))
# TODO: Las anchor de los tags deben llevar a algun lado??
%>
% for i in tagIndexes:
				<li class="hits_${hitClasses[int(round(i * k))] |h}">${c.myTopTags[i] |h}</li>
% endfor
			</ul>
		</div>
% endif
		<!-- End of Tags -->
		
		% if c.compatibility is not None:
		<!-- Compatibility -->
		<div class="fact compatibility" style="display:none;">
			<h1>${c.compatibility}%</h1><!-- Nota: Estaria muy copado hacer una animacion javascript y que el numero este fuera incrementando de 0 hasta su valor como si fuera una balanza -->
			<p>
				compatible with you
			</p>
		</div>
		<!-- End of Compatibility -->
		% endif
    </div>
	<!-- End of GUI #1: Flashing Facts -->
		
	<!-- GUI #2 -->
	<!-- This appears when Popego has been Clicked: Follow + Compare Us -->
	<div class="user_encounter" style="display:none;">
		%if c.remoteUser is not None:
			<p><h5>Hi ${c.remoteUser.username},
			%if c.remoteUserLoggedIn:
			<div class="logout"><a href="#">sign out</a></div>
			%else:
			<div class="logout"><a href="#">sign in</a></div>
			%endif
			</h5></p>
		%else:
			<p><h5>Hello,<div class="logout"><a href="#">sign in</a></div></h5></p>
		%endif
			<p><div class="open icon_button" title="Discover ${c.user.displayname}'s digital life.">Open this Popego</div></p>
		<%doc>
		%if c.remoteUser is not None and c.remoteUserLoggedIn:
			<p><div class="follow icon_button" title="${c.user.displayname} will be added to your Pop List.">Follow on Poplist</div></p>
		%else:
			<div id="get_popego" class="open icon_button" title="See how interesting ${c.user.displayname} is for you."><a href="http://www.popego.com/" target="_blank">Get a Popego</a></div></p>
		%endif
	    </%doc>
			<div id="get_popego" class="open icon_button" title="See how interesting ${c.user.displayname} is for you."><a href="http://www.popego.com/" target="_blank">Get a Popego</a></div></p>
	</div>
	<!-- End of GUI #2 -->	
	%endif
	
	<!-- GUI #3 -->
	<!-- This appears when Popego has been Clicked: Follow + Compare Us -->
	<div class="user_login" style="display:none;">
		<script language="javascript" src="/javascripts/utils.js"></script>
		<p><h5>Sign in, or <a href="http://www.popego.com/" target="_blank">Get a Popego</a>.</h5></p>					  
		% if c.error:
		<div class="error">
			<ul>
				<li>Username or password doesn't exists</li>
			</ul>
		</div>
		% endif
		<form action="" method="post" id="login">
			<input type="hidden" id="widgetOwner" name="widgetOwner" value="${c.username}" />
			<div class="inputs">
				<input type="text" id="username" name="username" value="username" />
				<input type="password" id="password" name="password" value="password" />
			</div>
			<input type="submit" value="ok!" class="button"/>
		</form>			
	</div>
	<!-- End of GUI #3 -->

% if c.myQuoteAccount:
	<script type="text/javascript" src="${h.asset_src('/javascripts/widget/popego-twitter-lib.js')}"></script>
	<script src="http://twitter.com/statuses/user_timeline/${c.myQuoteAccount.username}.json?count=1&amp;callback=Popego.setTwitterQuote" defer="defer" type="text/javascript"></script>
% endif

</body>
</html>
