import os
import json

from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.forms.fields import CharField
from django.forms.widgets import Input
from django.utils.html import mark_safe, format_html
from django.utils.translation import ugettext_lazy as _

FILE_UPLOAD_SCRIPT_TEMPLATE = '''
<script>
(function(widgetId, buttonId, selectedId, mediaUrl) {{
    "use strict";
    var button = document.getElementById(buttonId);
    var widget = document.getElementById(widgetId);
    var selected = document.getElementById(selectedId);

    button.addEventListener('click', function(e) {{
        e.preventDefault();

        window.SetUrl = function(path) {{
            if (path.substring(0, mediaUrl.length) !== mediaUrl) {{
                throw {{'message': 'Invalid file selected'}};
            }}
            path = path.substring(mediaUrl.length);
            widget.value = path;
            selected.innerHTML = '';

            var link = document.createElement('a');
            link.appendChild(document.createTextNode(mediaUrl + path));
            link.href = mediaUrl + path;
            link.target = '_blank';
            selected.appendChild(link);
        }};

        open(e.target.getAttribute('href'), 'filemanager',
            'height=600,width=800,resizable,scrollbars,status');
    }}, false);

}})({widget_id}, {button_id}, {selected_id}, {media_url});
</script>
'''

class FileBrowserWidget(Input):

    input_type = 'hidden'
    is_hidden = False

    def render(self, name, value, attrs=None):
        hidden_input = super(FileBrowserWidget, self).render(
            name, value, attrs)

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if 'id' not in final_attrs:
            return hidden_input
        widget_id = final_attrs['id']
        selected_id = widget_id + '__selected'
        button_id = widget_id + '__button'

        if value is None:
            file_link =  '<em>No file selected</em>'
        else:
            if isinstance(value, basestring):
                file_url = value
            else:
                file_url = value.url

            file_link = format_html('<a href="{0}" target="_blank">{0}</a>',
                                    file_url)

        selected = '<span id="{selected_id}">{file_link}</span>'.format(
            selected_id=selected_id,
            file_link=file_link)

        browse_button = '<button id="{button_id}" type="button" href="{href}">{text}</button>'.format(
            button_id=button_id,
            href=reverse('filemanager') + '?CKEditor=',
            text='Select a file')

        script = FILE_UPLOAD_SCRIPT_TEMPLATE.format(
            widget_id=json.dumps(widget_id),
            selected_id=json.dumps(selected_id),
            button_id=json.dumps(button_id),
            media_url=json.dumps(settings.FILEMANAGER_UPLOAD_URL))

        return mark_safe('{input}{browse} {selected}{script}'.format(
            input=hidden_input,
            selected=selected,
            browse=browse_button,
            script=script))

    def value_from_datadict(self, data, files, name):
        file_path = super(FileBrowserWidget, self).value_from_datadict(
            data, files, name)
        full_path = os.path.join(settings.FILEMANAGER_UPLOAD_ROOT, file_path)
        return File(open(full_path, 'rw+'), name=file_path)


class FileBrowserField(CharField):
    default_error_messages = {
        'invalid': _('That file does not exist'),
        'max_length': _('Ensure this filename has at most %(max)d characters (it has %(length)d).'),
    }

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', None)
        kwargs.update({
            'widget': FileBrowserWidget(),
        })
        super(FileBrowserField, self).__init__(*args, **kwargs)

    def clean(self, value):
        file_name = value.name
        super(FileBrowserField, self).clean(file_name)

        full_path = os.path.join(settings.FILEMANAGER_UPLOAD_ROOT, file_name)

        if self.max_length is not None and len(file_name) > self.max_length:
            error_values =  {'max': self.max_length, 'length': len(file_name)}
            raise ValidationError(self.error_messages['max_length'] % error_values)

        if not os.path.exists(full_path):
            raise ValidationError(self.error_messages['invalid'])

        return value

