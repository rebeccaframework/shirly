<h1>${project_name}</h1>
<div>
${description|n}
</div>
<div>
<ul>
%for m in members:
<li>${m['user_name']}</li>
%endfor
</ul>
</div>
