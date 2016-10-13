<!-- Sub Section: Pictures -->
<div class="pictures">
	<!-- GUI #3: Showcase -->
	<!-- Once a picture gets selected, goest straight into this viewer-->
	<div id="showcase">
		<div class="viewer" style="background:url(/images/widget/spinner_white.gif) 50% 50% no-repeat;">
		  <a href="${c.userItem.item.external_url}" target="_blank"><img src="${c.userItem.item.url}" title="Click to see in Full Size."></a>
		</div>	

		<div class="databox">
			<h1>${c.imgDesc}</h1>
			<span class="status_subtitle">${c.userItem.creation_date.strftime('%b %d')}, ${c.userItem.creation_date.year} by <a href="http://www.flickr.com/photos/${c.account.username}" target="_blank">${c.account.username}</a></span>
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
