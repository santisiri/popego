<%inherit file="base.mako" />

<%def name="title()">Alpha Signup</%def>

<%def name="display_box()">
<% return False %>
</%def>

<% field_dict = {'activation_code': 'Activation code', 'username': 'Username', 'password': 'Password', 'password_confirm': 'Password confirmation', 'terms_of_use': 'Terms of Service and Privacy Policy'} %>

<!-- SIGN UP EXTENDED Form -->
<div class="signup_extended_form">
	<div class="dialog"><div class="bubble"><div class="t"></div>		
		<p><strong id="welcome">Welcome ${c.fullName | h}!</strong></p> 
		<p>Please, complete your new account details and you'll be done.</p>
		<div class="error">
% if c.form_errors:
			<ul>
				% for i in c.form_errors:
				<li>${field_dict[i] if i in field_dict else i}: ${c.form_errors[i]}</li>
				% endfor
			</ul>
% endif
		</div>
		<form action="${h.url_for(controller='website/users')}" method="post" id="alpha_signup" class="signup">
			<input type="hidden" name="activation_code" value="${c.activationCode if c.activationCode else ''}" />
			<ul>
				<li><label>Choose a username you commonly use:</label><input type="text" name="username" value="" /></li>
			</ul>
			<ul>	
				<li><label>Password:</label><input type="password" id="password" name="password" class="short" value="" /><li>
				<li><label>Password again please:</label><input type="password" id="password_confirm" name="password_confirm" value="" class="short" /><li>
			</ul>
			<ul>
				<li><input type="checkbox" class="checkbox" name="terms_of_use" value="agree" id="terms_of_use" /><label class="side_label" for="terms_of_use">I have read and agree to the <a href="/about/tos" target="_blank">Terms of Use</a><%doc> and <a href="/about/">Privacy Policy</a></%doc>.</label> </li>
			</ul>
			<input type="submit" value="pop your ego" class="signup_button_small"/>
			<br style="clear: both;"/>
		</form>
	</div><div class="b"><div></div></div></div>
</div>
<!-- End of SIGN UP EXTENDED Form -->
<script src="${h.asset_src('/javascripts/signup.js')}"></script>
