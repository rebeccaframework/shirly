import formencode
import formencode.validators as v

class NewProjectSchema(formencode.Schema):
    project_name = v.UnicodeString(not_empty=True)
    description = v.UnicodeString(not_empty=True)

    filter_extra_fields = True
    allow_extra_fields = True
