<!-- Sub Section: Pictures -->
<div class="pictures">
	<div id="thumbs">
		<div style="height:315px;" id="Preview">
			<!-- ATENCION: Si no hay suficientes imagenes como para justificar un Scroller, estos DIVs NO VAN, son las sombras -->
			<div class="box_shadow" style="background:url(${h.asset_src('/images/widget/shadow_top.png')}) top repeat-x; z-index:9999; position:absolute; height:10px; width:100%;"></div>
			<div class="box_shadow" style="background:url(${h.asset_src('/images/widget/shadow_bottom.png')}) bottom repeat-x; z-index:9999; bottom:35px; position:absolute; height:10px; width:100%;"></div>
			<div class="box_shadow" style="background:url(${h.asset_src('/images/widget/shadow_left.png')}) left repeat-y; z-index:9999; position:absolute; width:10px; height:317px;"></div>
			<div class="index" id="Preview"  style="padding:6px; padding-left:8px; height:303px;" >
				<div class="content">
					%for user_item in c.items:
					<div class="item" title="<img src='${h.asset_src(user_item.item.service.faviconURL())}'><h1>${user_item.item.title}</h1>${user_item.creation_date.strftime('%b %d')}, ${user_item.creation_date.year}" style="background:url(${h.asset_src('/images/widget/spinner_thumb_white.gif')}) no-repeat;">
						<a href="#"><img style="background-image:url(${h.asset_src(user_item.item.thumbnail_url)});" id="${user_item.item.url}" src="${h.asset_src('/images/widget/blank.gif')}"></a>
						<!-- para levantar la data en el js, despues lo elimina -->						
						<span style="display:none;" id="${user_item.id}" title="${user_item.item.title}" description="${user_item.item.description}" date="${user_item.creation_date}" thumbnail="${user_item.item.thumbnail_url}" url="${user_item.item.url}" externalUrl="${user_item.item.external_url}" service="${user_item.item.service.name}"/>
					</div>
					%endfor
				</div>
				<div class="show_more" style="clear:both;height:72px;">
					<br/>
					<h2 style="font-weight:normal;"><a href="#">Show 30 more pictures.</a></h2>
				</div>
			</div>
		</div>
		<div id="pictures_thumbs" class="bottompanel" style="padding:0px; margin:10px 0px;" pageCount="${c.pageCount}">
			<div style="float:left;">
				Selected Album:
				<select size="1" id="filter_by_album" name="filter_dropwdown">
					<option value="0">All Pictures</option>
				%for a in c.albums:
					<option value="${a.name | h}" title="${a.name}">${h.truncate(a.name, 30, '...')}</option>
				%endfor
				</select>
			</div>
			
			<%doc>
			<!--ESTO DE ACA ABAJO VA CUANDO HAYA "Advanced Filters"-->
			<div style="float:right; display:none;">
				<div class="next_holder" style="display:inline">
					<span class="btn_next"><a href="#">Advanced Filters</a></span>
				</div>
			</div>
			</%doc>
		</div>
	</div>
	<div id="fullsize" style="display:none;">
		<div class="viewer" style="background:url(${h.asset_src('/images/widget/spinner_white.gif')}) 50% 50% no-repeat; display: table; #position: relative; overflow: hidden;">
			<div title="<img src=\'{ASSET:FAVICON_SERVICE}\'><h1>{TITLE}</h1>{DATE}" style="#position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">
				<a href="" target="_blank">
					<img src="" style=" #position: relative; #top: -50%">
				</a>
			</div>
		</div>
		<div id="pictures_fullsize" class="bottompanel">
			<div style="float:right; width:190px;">
				<div id="next" class="bigbutton gonext"  title="foto anterior">
					Next
				</div>
				<div id="prev" class="bigbutton goback" title="foto siguiente">
					Previous
				</div>
			</div>
			
			<div style="width 220px; margin-top:3px;">
				<div id="return" class="bigbutton goback" style="float:left; background-image:url(${h.asset_src('/images/widget/bigbutton_rewind.png')})" title="Go back to menu.">
					Return
				</div>			
			</div>
		</div>
	</div>
</div>
<!-- End of Sub Section -->	
