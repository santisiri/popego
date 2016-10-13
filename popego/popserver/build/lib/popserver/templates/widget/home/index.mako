<%inherit file="../base.mako" />

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${h.stylesheet_link_tag(*map(h.asset_src, ['/css/widget/card_bubble_default.css', '/css/widget/card_content_bubble.css']))}
</%def>
<%def name="javascripts()">
${h.javascript_include_tag(*map(h.asset_src, ['/javascripts/mootools.js', '/javascripts/zumup.js']))}
</%def>

<div class="home">
	<div class="header">
		<a href="#" style="float:left;margin-right:10px"><img src="${c.myAvatar}" width="100" height="100" alt="${c.user.displayname |h}'s avatar"/><div class="thumb_mask" title="Now, that's what I call a job well done!"></div></a>
		<a href="${c.user.website or 'http://www.popego.com'}" target="_blank"><div class="homesite_icon" title=""></div></a>
		<h1>${c.user.displayname |h}</h1>
		<blockquote style="text-align: left;">
		% if c.myQuoteAccount or c.user.shortBio:
			<img class="pngfix" src="/images/widget/quote_left.png" /><span id="quote_text">${c.user.shortBio or '' |h}</span><img class="pngfix" src="/images/widget/quote_right.png" />
		% endif
		% if c.myQuoteAccount:
			<img src="/images/icons/twitter_favicon.png" title="Twitter" style="display: none;" />
			<strong style="display: none;"><a href="http://twitter.com/${c.myQuoteAccount.username}" title="See ${c.user.displayname}'s Twitter." target="_blank" id="quote_date"></a></strong>
		% endif
<%doc>
		% if c.myQuote and c.myQuote['quote'].strip() != '':
			<img class="pngfix" src="/images/widget/quote_left.png" />${h.auto_link(c.myQuote['quote'], target='_blank')}<img class="pngfix" src="/images/widget/quote_right.png" />
			% if c.myQuote['service']:
			<strong><a href="${c.myQuote['url']}" title="See ${c.user.displayname}'s ${c.myQuote['service']}." target="_blank"><img src="/images/icons/${c.myQuote['service'].lower()}_favicon.png" title="${c.myQuote['service']}"></a>.</strong>
			% endif
</%doc>
      </blockquote>
    </div>
	
    <div class="separator"></div>
	
    <div class="databox" style="min-height:100px;">
		<div class="category_reduced">
		% if c.myServiceTypes:
			<strong>Some of his</strong>
		% else:
			No services available.
		% endif
		</div>
<%
import re
wordParser = re.compile('(\w+)')

def getListedServiceType(st):
        s = c.myServiceTypes
        if st == s[-1]:
                return (('' if len(s) == 1 else '& ') + '%s.') % st
        else:
                return ('%s, ') % st

%>
	
		% for st in c.myServiceTypes:
			<div id="toggle_${st}" class="category<% context.write('_selected' if st == c.myServiceTypes[0] else '') %>"><% context.write(wordParser.sub(r'<strong>\1</strong>', getListedServiceType(st))) %></div>
		% endfor
		
		<div id="zumup">
			<ul id="pictures" class="preview">
			% if len(c.myLastPhotos) == 0:
				<p>No pictures available.</p>
			% else:
				<div id="thumbs">
				% for m in c.myLastPhotos:
					<div class="item" style="background:url(/images/widget/spinner_white.gif) 50% 50% no-repeat; width:63px;height:63px;">
						<a href="${m['url'] |h}" target="_blank"><img style="background-image:url(${m['thumbnail'] |h});" alt="${m['title'] |h}" src="/images/widget/blank.gif" title="${m['title'] |h}" longdesc="${m['description'] |h}"></a>
					</div>
				% endfor
				</div>
			% endif
			</ul>

			<ul id="videos" class="preview">
				% if len(c.myLastVideos) == 0:
					<p>No videos available.</p>
				% else:
					<div id="thumbs">
					% for m in c.myLastVideos:
						<div class="item" style="background:url(/images/widget/spinner_white.gif) 50% 50% no-repeat; width:63px;height:63px;">
							<a href="${m['url'] |h}" target="_blank"><img style="background:url(${m['thumbnail'] |h}) 30% center no-repeat;" alt="${m['title'] |h}" src="/images/widget/blank.gif" title="${m['title'] |h}" longdesc="${m['description'] |h}"></a>
						</div>			
					% endfor
					</div>
				% endif
			</ul>
			
			<ul id="music" class="preview">
				<p>No music available.</p>
			</ul>
		</div>
		
		<p class="clear">

		</p>
	</div>

	<div class="separator"></div>

	<div class="databox" style="min-height:55px;">

		<div class="tag_cloud">
% if c.myTopTags:
			<ul>
<%
from random import shuffle
tagIndexes = range(0, len(c.myTopTags) - 1)
shuffle(tagIndexes)
hitClasses = ['highest', 'top', 'top', 'middle', 'middle', 'low', 'low', 'lowest']
k = float(len(hitClasses) + 1) / float(len(c.myTopTags))
# TODO: Las anchor de los tags deben llevar a algun lado??
%>
% for i in tagIndexes:
				<li class="hits_${hitClasses[int(round(i * k))] |h}"><a href="javascript:void(0);">${c.myTopTags[i] |h}</a></li>
% endfor
			</ul>
% else:
			<div class="category_reduced">${c.user.displayname |h}'s tag cloud is coming soon!</div>
% endif
		</div>

	</div>


	<div class="separator"></div>

	<br>
	<div class="databox" style="display:block;">	
		<div class="compatibility">
			<img src="${h.asset_src('/images/widget/compatibility_med.png')}" title="Popego Compatibility" class="pngfix" style="margin-top:0px">
			%if c.remoteUser is None:
				<a href="#">Get a popego</a> to discover <strong>how compatible</strong> you are with this user. Or you can <a href="#">sign in here</a>.
			%elif c.compatibility is None:
				<strong>Compatibility can't be measured.</strong> There isn't enough information on your popegos.			
			%else:
				<h2>${c.compatibility}%</h2>
				<span>
					You have a <strong>${h.gimme_value_level(c.compatibility)} compatibility</strong> with each other according to your interests.
				</span>
			%endif
			<br>
		</div>
	</div>

<%doc>		
	<div class="databox" style="display:block;">
		<img class="pngfix" src="/images/widget/profile/nation_cameroon.png" title="Connected from Yahounde, Cameroon." />
		<img class="pngfix" src="/images/widget/profile/status_online.png" title="Online" />
		<span class="tread">
			<strong>Seen 2 days ago at </strong>
			<img src="${h.asset_src('/images/icons/youtube_favicon.png')}" title="Youtube.com" class="pngfix"/>
			<a href="#">youtube.com</a>,
			<img src="${h.asset_src('/images/icons/blogger_favicon.png')}" title="Blogger.com" class="pngfix"/>
			<a href="#">blogspot.com</a>.
		</span>
	</div>
</%doc>

</div>

% if c.myQuoteAccount:
<script type="text/javascript" src="${h.asset_src('/javascripts/widget/popego-twitter-lib.js')}"></script>
<script src="http://twitter.com/statuses/user_timeline/${c.myQuoteAccount.username}.json?count=1&amp;callback=setTwitterQuote" defer="defer" type="text/javascript"></script>
%endif
