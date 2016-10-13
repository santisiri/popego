<%inherit file="../../base.mako" />

<%def name="title()">Feedback</%def>

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag('/css/website/default.css', '/css/themes/deeppink.css')}
<style type="text/css">
body {
	background: white;
}
#screenshot {
	color:#666666;
	height:28px;
	padding:0pt 4px;
	width:auto;
	background:#F3F3F3 none repeat scroll 0%;
	border-color:#FFFFFF rgb(211, 211, 211) rgb(211, 211, 211) rgb(255, 255, 255);
	border-style:solid;
	border-width:2px;
	border:1px solid #CCCCCC;
	font-size:12px;
	vertical-align:middle;
	line-height:22px;
}
#feedback label {
	padding: 4px 0;
}
#feedback p {
	float: left;
	margin: 5px 0;
}
#feedback .clear {
	clear: both;
}
#feedback p {
	float: left;
}
#feedback textarea {
	width: 450px;
}
</style>
</%def>

<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(h.asset_src('/javascripts/feedback.js'))}
</%def>

<h3><strong>Feedback Form</strong></h3>
It's very important for us to get <strong>tons of feedback</strong> from you.

% if c.result is None:

	<form action="${request.environ['PATH_INFO']}" enctype="multipart/form-data" method="post" id="feedback">
	<div>
		<div>
			<p>
				<label for="report">I want to:</label>
				<select name="report" id="report">
					<option value="bug">Report a Bug (error)</option>
					<option value="suggest">Suggest an Idea</option>
					<option value="contact">Contact the Team</option>
				</select>
			</p>
			<p style="margin-left: 15px;">
				<label for="screenshot">Screenshot (optional):</label>
				<input type="file" name="screenshot" id="screenshot" />
			</p>
		</div>
		<div class="clear">
			<p>
				<label for="desc">Tell us about it:</label><textarea id="desc" name="desc" cols="70" rows="4"></textarea>
			</p>
			<p class="clear"><input type="submit" value="send message" class="button"/> <input type="reset" value="cancel" class="button" /></p>
		</div>
	</div>
</form>

% else:

<br/>
<br/>
<h3><strong>${c.result or 'Thanks for your message' |h}</strong></h3>

<%doc>
If c.result is an empty string, it means feedback was successfully submitted.
</%doc>
% if not c.result:
<script>
(function () {
	try {this.hideDialog('feedback_form');} catch (e) {}
}).delay(3000, parent.Popego.Utils);
</script>
% endif

% endif

% if c.result:
<a id="goback" href="javascript:window.history.go(-1);">Go back</a>
% endif
