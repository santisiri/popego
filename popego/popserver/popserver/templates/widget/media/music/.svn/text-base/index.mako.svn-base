<!-- Sub Section: Music -->	
<div class="culture">
	<!-- GUI #2: Favorites -->
	<!-- This is the second GUI of Culture showing the art-specific type of favorites -->
	<div id="favorites">
		
		<!-- Index -->
		<div class="index" id="Preview">		
			
			<!-- Last Songs Listened -->
			<div class="index_item_post">
			  %if c.lastSong is None:
				<div class="artist spinner_box">
					<a href="#" target="_blank"><img src="${c.defaultArtistImage}" title="No Song" /></a>
				</div>
				
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon pngfix_scale" />
					<span class="date">Unknown</span>
					<h3>Last Songs Listened</h3>
					<p>No recent songs</p>						 
				</div>

			  %else:
				<div class="artist spinner_box">
					<a href="http://www.lastfm.com/artist/${c.lastSong.item.artist.title}" target="_blank"><img src="${h.gimme_first_valid([c.lastSong.item.artist.photo_url, c.defaultArtistImage])}" title="${c.lastSong.item.artist.title}" /></a>
				</div>
				
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon pngfix_scale" />
					<span class="date">${c.lastSong.creation_date.strftime('%b %d')}</span>
					<h3>Last Songs Listened</h3>
					<p><a href="${c.lastSong.item.external_id}" target="_blank">${c.lastSong.item.title}</a>, ${h.gimme_anyone(['interpreted by','sung by','in the voice of'])} <a href="http://www.lastfm.com/artist/${c.lastSong.item.artist.title}" target="_blank"><strong>${c.lastSong.item.artist.title}</strong></a> just ${h.time_ago_in_words(c.lastSong.creation_date)} ago.</p>						 

					<p><span class="see_more btn_next"><a id="LastTracks" href="#">Last 10 tracks played</a></span></p>
				</div>
			   %endif
			</div>
			
			<!-- Favorite Artists -->
			<div class="index_item_post">	
			  %if len(c.favoriteArtists) > 0:
				<div class="artist spinner_box">
					<a href="http://www.lastfm.com/artist/${c.favoriteArtists[0].title}" target="_blank"><img src="${h.gimme_first_valid([c.favoriteArtists[0].photo_url, c.defaultArtistImage])}" title="${c.favoriteArtists[0].title}" /></a>
				</div>
				
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon pngfix_scale" />
					<span class="date">${c.favoriteArtistsDate.strftime('%b %d')}</span>
					<h3>Favorite Artists</h3>
					<p><a href="http://www.lastfm.com/artist/${c.favoriteArtists[0].title}" target="_blank"><strong>${c.favoriteArtists[0].title}</strong></a>
					% if len(c.favoriteArtists) > 1:
					and <a href="http://www.lastfm.com/artist/${c.favoriteArtists[1].title}" target="_blank"><strong>${c.favoriteArtists[1].title}</strong></a>
					% endif
					are among the favorites. 
					<!--<img src="/images/icons/compatibility.png" title="Match" class="pngfix" />Both of you ${h.gimme_anyone(['seem to like', 'also love', 'have in common', 'dig the sound of'])} <a href="#"><strong>The Beatles</strong></a>.</p>-->
					<p><span class="see_more btn_next"><a id="TopArtists" href="#">See the Top 10 artists</a></span></p>
				</div>
			   %else:
				<div class="artist spinner_box">
					<a href="#" target="_blank"><img src="${c.defaultArtistImage}" title="No Artists" /></a>
				</div>
				
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon pngfix_scale" />
					<span class="date">${c.favoriteArtistsDate.strftime('%b %d')}</span>
					<h3>Favorite Artists</h3>
					<p>No artists statistics.</p>
				</div>

			   %endif
			</div>
			
			<!-- Favorite Songs -->
			<div class="index_item_post">
			  %if c.favoriteSong is None:
				<div class="artist spinner_box">
					<a href="#" target="_blank"><img src="${c.defaultArtistImage}" title="No Songs" /></a>
				</div>
				
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon pngfix_scale" />
					<span class="date">Unknown</span>
					<h3>Favorite Songs </h3>
					<p>No songs statistics.</p>						 
				</div>

			  %else:
				<div class="artist spinner_box">
					<a href="http://www.lastfm.com/artist/${c.favoriteSong.artist.title}" target="_blank"><img src="${h.gimme_first_valid([c.favoriteSong.artist.photo_url, c.defaultArtistImage])}" title="${c.favoriteSong.artist.title}" /></a>
				</div>
				
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/icons/lastfm_favicon.png')}" class="icon pngfix_scale" />
					<span class="date">${c.favoriteSongDate.strftime('%b %d')}</span>
					<h3>Favorite Songs </h3>
					<p><a href="${c.favoriteSong.external_id}" target="_blank">${c.favoriteSong.title}</a>, interpreted by <a href="http://www.lastfm.com/artist/${c.favoriteSong.artist.title}" target="_blank"><strong>${c.favoriteSong.artist.title}</strong></a> has been ${h.gimme_anyone(['enjoyed','listened','felt'])} by ${c.user.username} <strong>${c.favoriteSongPlays}</strong> times.</p>						 
					<p><span class="see_more btn_next"><a id="TopSongs" href="#">See the Top 10 songs</a></span></p>
				</div>
			   %endif
			</div>								
		</div>
		<!-- End of Index -->

		<!-- Footer -->
		<div class="footer">
			<div class="collection">
				<!--<div class="service_filter">
					<span class="btn_none"><img src="/images/icons/lastfm_favicon.png" class="icon" > <a href="#">last.FM</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>					
					<span class="vertical_separator"></span>
					<span class="btn_none"><img src="/images/icons/apple_favicon.png" class="icon" > <a href="#">iTunes</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>					
					<span class="vertical_separator"></span>
					<span class="btn_none"><img src="/images/icons/ilike_favicon.png" class="icon" > <a href="#">iLike</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>					
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
	<!-- END OF GUI #1: Groups -->
</div>
<!-- End of Sub Section -->	
