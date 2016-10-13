<%def name="stylesheets()">
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/card_content_default.css', '/css/widget/card_content_bubble.css', '/css/widget/themes/card_content_' + c.theme + '.css']))}
</%def>

<%def name="javascripts()">
  ${h.javascript_include_tag(*map(h.asset_src, ['/javascripts/mootools.js', '/javascripts/utils.js']))}
</%def>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>Popego | The Internet meets You.</title>
	
	<link rel="Shortcut Icon" href="/favicon.ico">
	
	<!--[if lt IE 7.]>
	<link href="/css/widget/ie6.css" rel="stylesheet" type="text/css" />
	<link href="/css/ie6.css" rel="stylesheet" type="text/css" />
	<![endif]-->
	<%doc>TODO : El getattr no es para nada correcto, pero hay casos en los que g (globals) no esta definido. Investigar por que</%doc>
	%if getattr(g, 'stylesheet_bundle_path', None) is not None:
	${h.stylesheet_link_tag(h.asset_src(g.stylesheet_bundle_path))}
	%else:
	${self.stylesheets()}
	%endif
	
	<script type="text/javascript">
	//<![CDATA[
		//TODO: Mover esto, al Config o ver que onda
		if (typeof(Popego) == "undefined") var Popego= {};
		if (typeof(Popego.Env) == "undefined") {
			Popego.Env = {};
			Popego.Env.baseUrl = "${c.baseUrl}";
			Popego.Env.username = "${c.username}";
		}
	//]]>
	</script>
	
	%if getattr(g, 'javascript_bundle_path', None) is not None:
	${h.javascript_include_tag(h.asset_src(g.javascript_bundle_path))}
	%else:
        ${self.javascripts()}
	%endif
</head>
<body>
	<div class="menu">
	<ul>
<%
# TODO: no es muy prolijo detectar la seccion de esta forma:
# (depende de un mapping particular del routing)
import re
m = re.search('/api/widget/\w+/(\w+)', request.environ['PATH_INFO'])
currentSection = m.group(1) if m else ''
%>
% for i in ['home', 'media', 'about']:
		<li class="${'selected' if currentSection == i else ''}"><a href="${c.baseUrl}/${c.username}/api/widget/1/${i}${'?theme=' + c.theme if c.addThemeInReq else ''}"><span>${i.title()}</span></a></li>
% endfor
		<%doc><li class="disabled"><a href="#"><span>Interests</span></a></li></%doc>
		<%doc><li class="disabled"><a href="#"><span>Contact</span></a></li></%doc>
	</ul>
	<br style="clear:both;">
	</div>
	${next.body()}

</body>
</html>
