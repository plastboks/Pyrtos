from pyrtos.forms.meta import BaseForm, strip_filter

from pyrtos.models import AlertSetting

from wtforms import (
    validators,
    widgets,
    TextField,
    HiddenField,
    PasswordField,
    BooleanField,
    SelectField,
    SelectMultipleField,
)


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AlertSettingCreateForm(BaseForm):
    """
    Class constants representing form fields.

    title -- string, title
    hour -- selector, hour
    minutes -- selector, minute
    """
    title = TextField('Title',
                      [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    weekfilter = MultiCheckboxField('Days',
                                    coerce=unicode,
                                    choices=AlertSetting.days_list,
                                    )
    hour = SelectField('Hour',
                       coerce=int,
                       choices=[(n, "%02d" % n)
                                for n in AlertSetting.hour_list])
    minute = SelectField('Minute',
                         coerce=int,
                         choices=[(n, "%02d" % n)
                                  for n in AlertSetting.minute_list])
    days_in_advance = SelectField('Days in advance',
                                  coerce=int,
                                  choices=[(n, "%d" % n)
                                           for n in
                                           AlertSetting.days_advance_list])
    active = BooleanField('Active', default=True)


class AlertSettingEditForm(AlertSettingCreateForm):
    """
    Class constants representing form fields.

    id -- category id, used in edit forms.
    """
    id = HiddenField()
