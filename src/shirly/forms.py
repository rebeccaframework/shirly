from pyramid_simpleform.renderers import FormRenderer as _FormRenderer
from webhelpers.html import HTML, escape, literal

class FormRenderer(_FormRenderer):
    def _render_bootstrap_control(self, name, control):
        return literal("".join(['<div class="control-group">',
            self.label(name, class_="control-label"),
            '<div class="controls">',
            control(name),
            '</div>',
            '</div>',]))

    def textfield(self, name):
        return self._render_bootstrap_control(name, self.text)

    def textareafield(self, name):
        return self._render_bootstrap_control(name, self.textarea)
