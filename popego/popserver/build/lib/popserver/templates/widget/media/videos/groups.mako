<!-- Sub Section: Videos -->
<div class="videos">
	<!-- GUI #1: Groups -->
	<!-- This is the first thing that appears to the user, it display the sets of albums he might want to browse-->
	<div id="groups">
		<!-- Index -->
		<div class="index" id="Preview">
		% for group in c.groups:
			% if len(group.items) > 0:
				<div class="index_item" id=${group.id}>
					<div class="group_thumb" style="background:url(/images/widget/spinner_group_white.gif) no-repeat;">
						<img src="${h.asset_src('/images/widget/blank.gif')}" style="background-image:url(${group.items[0].item.thumbnails[0].url});"/>
					</div>
					<div class="index_item_detail">
						<h3>${group.name}</h3>
						<img src=${group.account.service.faviconURL()} class="icon"/>
						<span class="index_item_date">${group.import_date.strftime('%b %d')}, ${group.import_date.year}</span>
					</div>
				</div>
			% endif
		% endfor
		</div>
		<!-- End of Index -->
    
    <!-- Footer -->
    <div class="footer">
      <div class="collection">
	<div class="pagination" style="display:inline" pageCount="${c.pageCount}">
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
