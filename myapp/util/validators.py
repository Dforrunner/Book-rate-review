from wtforms.validators import ValidationError
from flask_login import current_user


class Unique(object):

    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class ValidUser(object):

    def __init__(self, model, field, message=u"This element doesn't exists."):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if not check:
            raise ValidationError(self.message)


class ValidateCurrentPass(object):
    def __init__(self, message=u"The current password is incorrect."):
        self.message = message

    def __call__(self, form, field):
        u = current_user
        if not u.check_password(form.current_password.data):
            raise ValidationError(self.message)
