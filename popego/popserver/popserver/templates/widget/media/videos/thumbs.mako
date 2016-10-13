<!-- Sub Section: Videos -->
<div class="videos">
	<!-- GUI #2: Thumbnails -->
	<!-- This is the second instance, once he enters a group, the user browses through the thumbnails. -->
	<div id="thumbs">

		<!-- Index -->
		<div class="index" style="display:block;" id="Preview">		
			<div id="items_container" style="height:200px;">
			%for user_item in c.items:
				<div class="item" style="background:url(/images/widget/spinner_video_white.gif) no-repeat;width:96px;height:96px">
					<a href="#">
						<div class="image_strip" id="${user_item.id}" titl="${h.truncate(user_item.item.title, 40, '...')}" desc="${h.truncate(user_item.item.description, 200, '...')}">
							<img style="background:url(${user_item.item.thumbnails[0].url}) no-repeat;width:96px;height:96px;" src="/images/widget/blank.gif" />
							% for thumbnail in user_item.item.thumbnails[1:]:
								<!-- Agrego la imagen tambien en el src para que se cargue al principio y no en el rollover -->
								<img style="background:url(${thumbnail.url}) no-repeat;width:96px;height:96px;display:none;" src="${thumbnail.url}"/>
							% endfor
						</div>
					</a>
				</div>
			%endfor
			</div>
		  
			<div class="databox">
				<h1>${c.group.name}</h1>
				<span class="status_subtitle">Album created on ${c.group.import_date.strftime('%b %d')}, ${c.group.import_date.year}</span>
			</div>
		  
		</div>
		<!-- End of Index -->
    
		<!-- Footer -->
		<div class="footer">
			<div class="collection">
				<span class="btn_wayback"><a href="#">Back to Menu</a></span>
				<div class="pagination" style="display:inline" pageCount="${c.pageCount}">
					<div class="prev_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_back"><a href="#">Previous</a></span>
					</div>
					<div class="next_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_next"><a href="#">Next Page (${c.page}/${c.pageCount})</a></span>
					</div>
				</div>
			</div>
		</div>
		<!--End of Footer -->
	</div>	
	<!-- END OF GUI#2: Thumbnails -->
</div>
<!-- End of Sub Section -->	
