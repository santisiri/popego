<%inherit file="base.mako" />

<script type="text/javascript">
		if (typeof(Popego) == 'undefined') Popego = {};	if (typeof(Popego.Env) == 'undefined') Popego.Env = {}; 
		Popego.Env.username = "${c.user.username if hasattr(c, 'user') else ''}";
</script>

		<!-- Column 2 -->
		<div class="column_2">
			<!-- Services -->
			<div class="services">
				<h3><strong>Sorry, this section is not available yet.</strong></h3>
				This is an early alpha version of our product, and we still have many features being cooked.
				<br />Give us your <a href="javascript:Popego.Feedback.showForm();">feedback</a> and help us improve every aspect behind Popego.

				<div class="announcement" style="clear:both;">
					<blockquote>
						<h2>
							&#8220;Alpha children work much harder&#8221; 
						</h2>
						<br>Aldous Huxley, <strong><em>Brave New World</em></strong> (1932)
					</blockquote>
				</div>				

			</div>
			<!-- End of Services -->
		
		</div>
		<!-- End of Column 2 -->

