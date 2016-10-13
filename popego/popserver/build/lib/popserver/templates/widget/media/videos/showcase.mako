<!-- Sub Section: Videos -->
<div class="videos">
	<!-- GUI #3: Showcase -->
	<!-- Once a picture gets selected, goest straight into this viewer-->
	<div id="showcase">
		<div class="viewer" style="background:url(/images/widget/spinner_white.gif) 50% 50% no-repeat;height:225px;">
			<object width="100%" height="100%">
				<param name="movie" value="${c.userItem.item.embedURL}"></param>
				<param name="wmode" value="transparent"></param>
				<embed src="${c.userItem.item.embedURL}" type="application/x-shockwave-flash" wmode="transparent" width="100%" height="100%"></embed>
			</object>
		</div>	
		
		<div class="databox">
			<h1><span title="${c.userItem.item.title}">${h.truncate(c.userItem.item.title, 50, '...')}</span></h1>
			<span class="status_subtitle">${c.userItem.creation_date.strftime('%b %d')}, ${c.userItem.creation_date.year} by <a href="http://www.youtube.com/profile?user=${c.userItem.item.author}" target="_blank">${c.userItem.item.author}</a></span>
		</div>
		
		<!-- Footer -->
		<div class="footer">
			<div class="collection">
				<span class="btn_wayback"><a href="#">Back to Thumbnails</a></span>
				<div class="pagination" style="display:inline" pageCount="${c.pageCount}">
					<div class="prev_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_back"><a href="#">Previous</a></span>
					</div>
					<div class="next_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_next"><a href="#">Next Picture (26/102)</a></span>
					</div>
				</div>	
			</div>
		</div>
		<!--End of Footer -->
	</div>
	<!-- END OF GUI #3: Showcase -->
</div>
<!-- End of Sub Section -->	
