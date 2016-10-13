<%inherit file="base.mako" />

<%def name="heading_phrase()">These are the basics about yourself.</%def>

<%def name="javascripts()">
  ${parent.javascripts()}
  ${h.javascript_include_tag(h.asset_src('/javascripts/avatar_uploader.js'))}
  ${h.javascript_include_tag(h.asset_src('/javascripts/user_settings.js'))}
</%def>

<script type="text/javascript">
		if (typeof(Popego) == 'undefined') Popego = {};	if (typeof(Popego.Env) == 'undefined') Popego.Env = {}; 
		Popego.Env.username = "${c.user.username if hasattr(c, 'user') else ''}";
</script>

<!-- Column 3 -->
		<div class="column_1" style="width:240px; line-height:22px;">
			
			<!-- Avatar Upload -->
			<div style="_padding-top:10px;margin-top:3px;">
				<h3><strong>Your Avatar</strong></h3>
                                We like <strong>BIG</strong> avatar pictures!
                                <div style="background-image: url(/images/website/avatar_nopic_200.png); width: 200px; height: 200px;">
				<p>
					<img src="${c.myAvatar}" width="200" height="200" alt="" title="${c.user.displayname |h}'s avatar" id="avatar_img" />
					<div class="frame_200"><img src="${h.asset_src('/images/website/avatar_frame_200_white.png')}" class="pngfix"></div>
				</p>
				</div>
				<form id="upload_avatar" action="/${c.user.username}/settings/avatar/upload" enctype="multipart/form-data" method="post">
					<p>
						Select a file to upload:
						<div class="uploader" style="padding-bottom: 12px;">
							<input name="my_avatar" type="file" style="" value="change picture" class="button"/>
						</div>
					</p>
					<img src="${h.asset_src('/images/website/spinner_white.gif')}" alt="Sending..." width="16" height="16" style="display: none;" />
					<span id="upload_message"></span>
					<iframe name="upload_iframe" id="upload_iframe" src="about:blank" style="display: none;"></iframe>
				</form>
				<p>
					<h5>
						It's recommended a 200x200 pixels picture.
						<br>JPG, PNG or GIF formats are supported.
					</h5>
				</p>
				
				<%doc>
				<p>
					<h3><strong>Color Theme</strong></h3>
					A color for the website and widgets.
					<div class="palette">
						<ol>
<% themes = ['red', 'teal', 'olive', 'orangered', 'darkslategray', 'lightgrey', 'deeppink', 'dodgerblue', 'yellowgreen', 'gold'] %>
% for t in themes:
							<li${' class="picked_color"' if t == c.myTheme else ''}><a href="/${c.user.username}/settings/theme/${t}" class="${t}"></a></li>
% endfor
						</ol>
					</div>
				</p>				
				</%doc>
			</div>
			<!-- End of Avatar Upload -->			

			<div style="clear:both;"></div>							
			
		</div>
		<!-- End of Column 3 -->

		<!-- Column 2 -->
		<div class="column_2">
			<!-- Services -->
			<div class="services">
				<h3><strong>Your Profile</strong></h3>
				Just the basic info about yourself.
				
				<form action="/${c.user.username}/settings/personal" method="post" id="personal_settings">
					<div style="float:left; margin-right:15px;">				
						<p>	
							<label for="name">Full Name:</label> <input type="text" class="long_input" id="name" name="fullname" value="${c.user.displayname or '' |h}" />
							<!--<label class="label_tooltip" style="display:block;">Real names help to identify real people.</label>-->
						</p>
						<p>
							<label for="blog">Your Blog or Website:</label> <input type="text" id="blog" name="website" value="${c.user.website or ''|h}" class="long_input" />
							<!--<label class="label_tooltip" style="display:block;">This is your digital home. Your Popego will promote it.</label>-->
						</p>
						<p>
							<label for="email">Email:</label> <input type="text" id="email" name="email" value="${c.user.email or '' |h}" class="long_input" />
							<!--<label class="label_tooltip" style="display:block;">It will be kept always private, unless you give your explicit permission.</label>-->
						</p>
					</div>
					<div style="float:left">
						<p>
							<label for="country">Country:</label>
							<select id="country" name="country">
								<option value=""${'' if c.user.country else ' selected="selected"'}></option>
								% for i in c.countries:
								<option value="${i[0] |h}"${' selected="selected"' if c.user.country and c.user.country.id == i[0] else ''}>${i[1] |h}</option>
								% endfor
							</select>
							<!--<label class="label_tooltip" style="display:block;">Your geographical place in the world.</label>-->
						</p>						
						<p>
							<div class="birthday_div">
								<div class="align_left">
									<label for="birthmonth">Date of Birth:</label> 
									<select size="0" class="birthday" id="birthmonth" name="birthmonth">
<%
from datetime import date
(birthyear, birthmonth, birthday) = c.user.birthdate.utctimetuple()[:3] \
		if c.user.birthdate else (0, 0, 0)
%>
										<option value=""${' selected="selected"' if birthmonth == 0 else ''}>&nbsp;</option>
% for i in range(1, 13):
										<option value="${i}"${' selected="selected"' if i == birthmonth else ''}>${date(2008, i, 1).strftime('%B')}</option>
% endfor
									</select>
								</div>								
								<div class="align_left">
									<label>&nbsp;</label> 
									<select size="0" class="birthday" id="birthdate" name="birthday">
										<option value=""${' selected="selected"' if birthday == 0 else ''}>&nbsp;</option>
% for i in range(1, 32):
										<option value="${i}"${' selected="selected"' if i == birthday else ''}>${i}</option>
% endfor
									</select>
								</div>
								<label>&nbsp;</label> 
								<select size="0" class="birthday" id="birthyear" name="birthyear">
										<option value=""${' selected="selected"' if birthyear == 0 else ''}>&nbsp;</option>
% for i in reversed(range(1899, date.today().year + 1)):
										<option value="${i}"${' selected="selected"' if i == birthyear else ''}>${i}</option>
% endfor
								</select>
								<!--<label class="label_tooltip" style="display:block;">You're not bad for someone your age.</label>-->
								<!-- NOTA: Textos por si es muy pendex: "Kid, it seems like you're too young to even read this words.." -->
							</div>
						</p>
						<p style="_padding-top:6px;">
							<label>Gender:</label>
							<input type="radio" id="gender_m" name="gender" value="M"${' checked="checked"' if c.user.gender == 'M' else ''} class="radio_button" /> Male 
							<input type="radio" id="gender_f" name="gender" value="F"${' checked="checked"' if c.user.gender == 'F' else ''} class="radio_button" /> Female
							<!--<label class="label_tooltip" style="display:block;">If you're not sure about this, a psychiatrist will help.</label>-->
						</p>
						
					</div>
					<div style="clear:both;">
						<p>
							<label for="minibio">Mini Bio:</label><textarea name="minibio" id="minibio" cols="70" rows="4" >${c.user.shortBio or '' |h}</textarea>
							<!--<label class="label_tooltip" style="display:block;">Introduce yourself to the world in 140 characters.</label>-->
						</p>
						<p id="profile_form_errors"></p>
						<p><input type="submit" value="submit changes" class="button"/><%doc><input type="reset" value="cancel" class="button"/></%doc><img src="${h.asset_src('/images/website/spinner_white.gif')}" alt="Sending..." width="16" height="16" style="display: none; padding: 0 12px;" /></p>					
					</div>
				</form>
				
				<div class="separator"></div>		

				<h3><strong>Change Password</strong></h3>
				<p>
				<form action="/${c.user.username}/settings/password" method="post" id="password_settings">
						<label>Current Password:</label> <input type="password" id="current_password" name="current_password" value="" />
						<p></p>
						<div class="align_left"><label>New Password:</label> <input type="password" id="new_password" name="new_password" value="" /></div>
						<label>Confirm Password:</label> <input type="password" id="confirm_password" name="confirm_password" value="" />							
						<p id="password_form_errors"></p>
						<p><input type="submit" value="change password" class="button"/><%doc><input type="reset" value="cancel" class="button"/></%doc><img src="${h.asset_src('/images/website/spinner_white.gif')}" alt="Sending..." width="16" height="16" style="display: none; padding: 0 12px;" /></p>
					</form>												
				</p>					
			</div>
			<!-- End of Services -->
		
		</div>
		<!-- End of Column 2 -->
