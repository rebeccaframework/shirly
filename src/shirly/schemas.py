import formencode
import formencode.validators as v

class NewProjectSchema(formencode.Schema):
    project_name = v.UnicodeString(not_empty=True)
    description = v.UnicodeString(not_empty=True)

    filter_extra_fields = True
    allow_extra_fields = True


class NewTicketSchema(formencode.Schema):
    ticket_name = v.UnicodeString(not_empty=True)
    description = v.UnicodeString(not_empty=True)
    estimated_time = v.Int()


    filter_extra_fields = True
    allow_extra_fields = True

