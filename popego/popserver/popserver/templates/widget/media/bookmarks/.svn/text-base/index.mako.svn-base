<!-- Sub Section: Links -->			
<div class="links" style="display:block;">
	<!-- GUI #1: Groups -->
	<!-- This is the first thing that appears to the user, it display the sets of albums he might want to browse-->
	<div id="groups" style="display:block;">
		<!-- Index -->
		<div class="index" style="display:block;" id="Preview">
		%for userItem in c.userItems:
			<div class="index_item_post" style="width: 95%;height:37px;"> <!--TODO Remover estilos de aca -->
				<div class="link_delicious" style="float:left">
					<a href="${userItem.item.serviceUrl}" target="_blank">
						<h3>${userItem.item.popularity}</h3> people
					</a>
				</div>
				<div class="index_item_detail" style="width: 330px;">
					<img src="${userItem.item.service.faviconURL()}" class="icon pngfix_scale" />
					<span class="date">${userItem.creation_date.strftime('%b %d')}, ${userItem.creation_date.year}</span>
					<h3><a href="${userItem.item.url}" title="${userItem.item.title}" target="_blank">${h.truncate(userItem.item.title, 37, '...')}</a></h3>
					<div class="tag_cloud">
					%if len(userItem.tags) > 0:
						<ul>
						<%
							letters = 0
							h.reset_counter()
						%>
						%for tag in userItem.tags[0:-1]:
							<% letters += len(tag.name) %>
							%if letters < 40 and len(userItem.tags[h.counter()].name) < 8:
								<li class="hits_lowest"><a href="javascript:void(0);">${tag.name}</a></li> + 
							%endif
						%endfor
							<li class="hits_lowest"><a href="javascript:void(0);">${userItem.tags[-1].name}</a></li>	    
						</ul>
					%else:
						No Tags
					%endif
					</div>		 
				</div>
			</div>
		%endfor
			<div class="index_item_post" style="display:none">
				<div class="link_digg">
					<h3>256</h3>
					diggs
				</div>
				<div class="index_item_detail">
					<img src="${h.asset_src('/images/website/digg_favicon.png')}" class="icon" />
					<span class="date">Nov 17</span>
					<h3><a href="#">Daft Punk Live Concert</a></h3>
					Websites from Digg do not have tags. Only Stupid descriptions...
				</div>
			</div>		
		</div>
		<!-- End of Index -->	
			
		<!-- Footer -->
		<div class="footer">
			<div class="collection">
				<!--<div class="service_filter">
					<span class="btn_none"><img src="${h.asset_src('/images/icons/del.icio.us_favicon.png')}" class="icon pngfix_scale" > <a href="#">delicious</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>					
					<span class="vertical_separator"></span>
					<span class="btn_none"><img src="${h.asset_src('/images/icons/digg_favicon.png')}" class="icon pngfix_scale" > <a href="#">digg</a> &nbsp;&nbsp;<input type="checkbox" name="source" value="true" checked="true" /></span>					
				</div>-->
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
	<!-- END OF GUI #1: Groups -->	
</div>
<!-- End Sub Section: Links -->
