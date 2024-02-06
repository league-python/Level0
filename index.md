Mon Feb  5 15:09:11 PST 2024



<ul>
{% for page in site.pages %}
    {{page.url}}
	{% if  page.url contains '/lessons/'%}
	<li><a href="{{ site.baseurl }}{{page.url}}">{{page.title}}</a></li>	
	{% endif %}

{% endfor %}   
</ul>