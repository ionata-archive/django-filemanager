from filemanager import fields
from django.db.models import FileField


class FileBrowserField(FileField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': fields.FileBrowserField,
        }
        defaults.update(kwargs)
        return super(FileBrowserField, self).formfield(**defaults)

    def pre_save(self, model_instance, add):
        # Skip the pre_save of the FileField, as that tries to save the file
        # again, resulting in duplicates
        f = super(FileField, self).pre_save(model_instance, add)
        return f


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^filemanager\.models\.FileBrowserField"])
except ImportError:
    pass
