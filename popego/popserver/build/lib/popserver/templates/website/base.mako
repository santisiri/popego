<%def name='title()'></%def>
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
	<title>${page_title}Popego | The Internet meets You.</title>
	
	<link rel="Shortcut Icon" href="/favicon.ico">
	<!--[if lt IE 7.]>
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
		var Popego= {}; Popego.Env = {}; Popego.Env.baseUrl = "";
	//]]>
	</script>
	%if getattr(g, 'javascript_bundle_path', None) is not None:
	${h.javascript_include_tag(h.asset_src(g.javascript_bundle_path))}
	%else:
        ${self.javascripts()}
	%endif
</head>
<body>
  ${next.body()}
</body>
</html>


