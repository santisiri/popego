<%inherit file="base.mako" />

<%def name="title()">Login</%def>

<!--

<%doc>
FIXME: Si se saca el form con el action como esta abajo, fallan los tests.
Tiene que ver con AuthKit y la herencia de este mako en signin.mako.
</%doc>

<form action="FORM_ACTION" method="post">
  <dl>
    <dt>Username:</dt>
    <dd><input type="text" name="username"></dd>
    <dt>Password:</dt>
    <dd><input type="password" name="password"></dd>
  </dl>
  <input type="submit" name="authform" value="Login" />
</form>

-->

<!-- LOGIN Form -->
<div class="login_form" style="display:block;margin-top:-10px;">
	<div class="dialog"><div class="bubble"><div class="t"></div>
		<strong>Welcome back!</strong>
		% if hasattr(c, 'error') and c.error:
		<div class="error">
			<ul>
				<li>Uh-oh! Login failed. Check your username and password and try again...</li>
			</ul>
		</div>
		% else:
			<p></p>
		% endif
		<form action="${h.url_for(controller='auth', action='signin')}" method="post" class="signup">
			<input type="text" name="username" value="your email or username" />
			<p><input type="password" name="password" value="a password" /></p>
			<input type="submit" value="log in!" class="signup_button"/>
		</form>	
		<%doc>
		<p>Not a user? <a href="${h.url_for(controller='website/users')}">Sign up here.</a> It's easy.</p>
		</%doc>
	</div><div class="b"><div></div></div></div>	
</div>		
<!-- End of LOGIN Form -->
