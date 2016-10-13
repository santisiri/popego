<%
	import datetime

	content = '';
	
	#esto del key se va a reemplazar por un id de instancia cuando las estemos trackeando
	key = str(datetime.datetime.utcnow().microsecond)
	
	
	if c.display == 'preview':
		content += '<div id="pe_container_preview" style="margin-left:150px"></div>'
	else:
		#TODO: ver INTERVAL Y KEY que se pisan con varios popegos
		content += '<script type="text/javascript">\
						if (typeof(intervals) == "undefined") {\
							var intervals = [];\
						}\
						document.write("<div id=pe_container_' + key + '></div>");\
						function init_' + key +'() {\
							if (typeof(Popego) != "undefined" && typeof(Popego.WidgetManager) != "undefined") {\
								clearInterval(intervals["' + key + '"]);\
								var wDesc = {};\
								wDesc.key = "' + key + '";\
								wDesc.user = "' + c.username + '";\
								wDesc.displayname = "' + c.displayname + '";\
								wDesc.theme = "t' + c.theme +'";\
								wDesc.type = "default";\
								wDesc.id = ' + str(c.widgetId)  + ';\
								Popego.createWidget(wDesc);\
							}\
						}\
						intervals["' + key + '"] = setInterval(function(){init_' + key + '();}, 100);\
					</script>\
					<script type="text/javascript" src="' + h.asset_src('/javascripts/widget/popego-ext.js') + '"></script>\
					<script type="text/javascript" src="' + h.asset_src('/javascripts/widget/popego-config.js') +'"></script>\
					<script type="text/javascript" src="' + h.asset_src('/javascripts/widget/embedder-lib.js') +'"></script>'
%>
% if c.display == 'default':
	var content = '${content}';
	document.write(content);
% else:
	${content}
% endif

