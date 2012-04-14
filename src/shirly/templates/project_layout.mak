<%inherit file="layout.mak" />
<div class="row">

<div class="span3">
${h.member_list(request)|n}
${h.ticket_list(request)|n}
<%block name="sidemenu">
</%block>
</div>

<div class="span9">
${next.body()}
</div>

</div>
