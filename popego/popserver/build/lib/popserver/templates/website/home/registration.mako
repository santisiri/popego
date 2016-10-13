<%inherit file="base.mako" />
<%def name="title()">
  Signup
</%def>
<% field_dict = {'email': 'Email', 
                 'username': 'Username', 
                 'displayname': 'Full name', 
                 'password': 'Password', 
                 'password_confirm': 'Password confirmation'} %>
<!-- SIGN UP Form -->
<div class="signup_form" style="display:block;margin-top:-20px;">
	<div class="dialog"><div class="bubble"><div class="t"></div>		
		<p><strong>Give it a try.</strong> Signing up will just take a moment.</p>

		<div class="error">
% if c.form_errors:
			% for i in c.form_errors:
				<span>${field_dict[i] if i in field_dict else i}: ${c.form_errors[i]}</span>
			% endfor
% endif
		</div>
		<form id="signup" class="signup">
			<input type="text" id="email" value="${c.form_result['email'] if c.form_errors else 'your email'}" />
			<p><input type="text" id="username" value="${c.form_result['username'] if c.form_errors else 'a username you commonly use'}" /></p>
			<input type="submit" value="sign me up!" class="signup_button"/>
		</form>	
		<!--<p>If you're already a user, <a href="${h.url_for(controller='website/home')}">please log in here.</a></p>-->
	</div><div class="b"><div></div></div></div>
</div>
<!-- End of SIGN UP Form -->

<!-- SIGN UP EXTENDED Form -->
<div class="signup_extended_form" style="display:none;">
	<div class="dialog"><div class="bubble"><div class="t"></div>		
		<p><strong id="welcome">Welcome!</strong></p> 
		<p>Please, complete the basic details for your profile and you'll be done.</p>
		<div class="error">
% if c.form_errors:
			<ul>
				% for i in c.form_errors:
				<li>${field_dict[i] if i in field_dict else i}: ${c.form_errors[i]}</li>
				% endfor
			</ul>
% endif
		</div>
		<form action="${h.url_for(controller='website/users')}" method="post" id="profile" class="signup">
			<input type="hidden" name="email" value="${c.form_result['email'] if c.form_errors else ''}" />
			<input type="hidden" name="username" value="${c.form_result['username'] if c.form_errors else ''}" />
			<input type="hidden" name="shortBio" value="${c.form_result['shortBio'] if c.form_errors else ''}" />
			<ul>
				<li><label>Full name:</label><input type="text" name="displayname" id="name" value="${c.form_result['displayname'] if c.form_errors else ''}" /><li>
			</ul>
			<ul>	
				<li><label>Password:</label><input type="password" id="password" name="password" class="short" value="" /><li>
				<li><label>Password again please:</label><input type="password" id="password_confirm" name="password_confirm" value="" class="short" /><li>
			</ul>
			<ul>
				<li><input type="checkbox" class="checkbox" /><label class="side_label">I have read and agree to the <a href="/about/" target="_blank">Terms of Use</a><%doc> and <a href="/about/" target="_blank">Privacy Policy</a></%doc>.</label> </li>
			</ul>
			<ul>
				<input type="submit" value="pop your ego" class="signup_button_small"/>
			</ul>
		</form>
	</div><div class="b"><div></div></div></div>
</div>
<!-- End of SIGN UP EXTENDED Form -->
<script src="javascripts/signup.js"></script>
