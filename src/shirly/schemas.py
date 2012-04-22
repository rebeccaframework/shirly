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

class TicketSchema(formencode.Schema):
    ticket_name = v.UnicodeString(not_empty=True)
    description = v.UnicodeString(not_empty=True)
    estimated_time = v.Int()


    filter_extra_fields = True
    allow_extra_fields = True

class NewMilestoneSchema(formencode.Schema):
    milestone_name = v.UnicodeString(not_empty=True)
    due_date = v.DateConverter(not_empty=True)
    description = v.UnicodeString(not_empty=True)
    
    filter_extra_fields = True
    allow_extra_fields = True
