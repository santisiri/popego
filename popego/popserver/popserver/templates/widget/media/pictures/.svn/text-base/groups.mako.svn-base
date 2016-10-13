<!-- Sub Section: Pictures -->
<div class="pictures">
	<!-- GUI #1: Groups -->
	<!-- This is the first thing that appears to the user, it display the sets of albums he might want to browse-->
	<div id="groups">
		<!-- Index -->
		<div class="index" id="Preview">		
		% for album in c.groups:
			% if len(album.items) > 0:
				<div class="index_item" id=${album.id}>
					<div class="group_thumb" style="background:url(/images/widget/spinner_group_white.gif) no-repeat;">
						<img src="${h.asset_src('/images/widget/blank.gif')}" style="background-image:url(${album.items[0].item.thumbnail_url});"/>
					</div>
					<div class="index_item_detail">
						<h3>${album.name}</h3>
						<img src=${album.account.service.faviconURL()} class="icon pngfix_scale" />
						<span class="index_item_date">${album.import_date.strftime('%b %d')}, ${album.import_date.year}</span>
					</div>
				</div>
			% endif
		% endfor
		</div>
		<!-- End of Index -->
			
		<!-- Footer -->
		<div class="footer">
			<div class="collection">
				<!--<div class="service_filter">
					<span class="btn_none"><img src="/images/icons/flickr_favicon.png" class="icon pngfix_scale" > <a href="#">Flickr</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>
					<span class="vertical_separator"></span>
					<span class="btn_none"><img src="/images/icons/picasa_favicon.png" class="icon pngfix_scale" > <a href="#">Picasa</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="picasa" checked="true" /></span>
				</div>-->
				<div class="pagination" pageCount="${c.pageCount}">
					<div class="prev_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_back"><a href="#">Previous</a></span>
					</div>
					<div class="next_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_next"><a href="#">More Albums</a></span>
					</div>
				</div>
			</div>
		</div>
		<!--End of Footer -->
	</div>
	<!-- END OF GUI #1: Groups -->
</div>
<!-- End of Sub Section -->	
