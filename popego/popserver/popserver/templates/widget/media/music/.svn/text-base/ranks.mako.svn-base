<!-- Sub Section: Music -->	
<div class="culture">
	<!-- GUI #3: Rankings -->
	<!-- This is the third GUI to show the Rankings -->
	<div id="ranking">
		<!-- Index -->
		<div class="index" id="Preview">
			<% counter = 0 %>
			%if c.rank == 'TopArtists':
				%for userItem in c.userItems:
				<% counter += 1 %>
				<div class="index_item_post">
					<div class="artist spinner_box_small">
						<a href="http://www.lastfm.com/artist/${userItem.item.title}" target="_blank"><img src="${h.gimme_first_valid([userItem.item.photo_url, c.defaultArtistImage])}" title="${userItem.item.title}" /></a>
					</div>
					
					<div class="index_item_detail">
						<a href="http://www.lastfm.com/artist/${userItem.item.title}" target="_blank">${userItem.item.title}</a></strong></a>
						<p><span class="ranking_score">Listened ${userItem.play_count} times.</span></p>
					</div>
					
					<div class="ranking_position">
						<% rank = (c.currentPage-1) * c.pageSize + counter %>
						#${rank} 
					</div>					
				</div>
				%endfor
			%else:
				%for userItem in c.userItems:
				<% counter += 1 %>
				<div class="index_item_post">
					<div class="artist spinner_box_small">
						<a href="http://www.lastfm.com/artist/${userItem.item.artist.title}" target="_blank"><img src="${h.gimme_first_valid([userItem.item.artist.photo_url, c.defaultArtistImage])}" title="${userItem.item.artist.title}" /></a>
					</div>
					
					<div class="index_item_detail">
						<!-- Nota: Randomizar la palabra 'interpreted by' ademas por 'sung by',  'in the voice of' -->
						<a href="${userItem.item.external_id}" target="_blank">${userItem.item.title}</a> by <a href="http://www.lastfm.com/artist/${userItem.item.artist.title}" target="_blank"><strong>${userItem.item.artist.title}</strong></a>
						<p><span class="ranking_score">Listened
						%if c.rank == 'TopSongs':
							${userItem.play_count} times.
						%else:
							${h.time_ago_in_words(userItem.creation_date)} ago.
						%endif
						</span></p>
					</div>
					
					<div class="ranking_position">
						<% rank = (c.currentPage-1) * c.pageSize + counter %>
						#${rank} 
					</div>					
				</div>
				%endfor
			%endif
		</div>
		<!-- End of Index -->			
			
		<!-- Footer -->
		<div class="footer">
			<div class="collection">
				<span class="btn_wayback"><a href="#">Back to Favorites</a></span>
				<!--<div class="service_filter">
					<span class="btn_none"><img src="/images/icons/lastfm_favicon.png" class="icon pngfix_scale" > <a href="#">last.FM</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>					
				</div>-->
				<div class="pagination" pageCount="${c.pageCount}">
					<div class="prev_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_back"><a href="#">Previous</a></span>
					</div>
					<div class="next_holder" style="display:none">
						<span class="vertical_separator"></span>
						<span class="btn_next"><a href="#">Next</a></span>
					</div>
				</div>
			</div>
		</div>
		<!--End of Footer -->
	</div>
	<!-- End of GUI #3 Rankings -->	
</div>
<!-- End of Sub Section -->	