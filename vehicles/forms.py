import datetime
from django import forms
from django.forms.util import flatatt
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy
from vehicles.models import CarMake, CarModel

class CarModelWidget(forms.Select):        
    class Media(object):
        js = ("https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js",'vehicles/selector.js')

    def __init__(self, attrs=None):
        forms.Select.__init__(self, attrs, [])

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<div%s><select class="car-year-selector">' % flatatt(final_attrs)]
        
        year_value = '2010'
        if not value == '':
            try:
                if type(value) == type(1):
                    value = CarModel.objects.get(pk=value)
                year_value = value.year
            except (ValueError, CarModel.objects.model.DoesNotExist):
                value = ''

        YEARS = []
        for year in range(2010, 1948, -1):
            YEARS.append((str(year), str(year)))
        options = self.render_options(YEARS, [year_value])
        if options:
            output.append(options)

        output.append(u'</select>')
        output.append(u'<select class="car-make-selector">')
        
        make_names = []
        makes = CarMake.objects.filter(carmodel__year__exact=year_value).distinct().order_by('name')
        for make in makes:
            make_names.append((make.name,make.name))
        make_value = make_names[0][0]
        if not value == '':
            make_value = value.make.name
        options = self.render_options(make_names, [make_value])
        if options:
                output.append(options)
                
        output.append(u'</select>')
        output.append(u'<select name="'+final_attrs['name']+'" class="car-model-selector">')
        
        model_choices = []
        models = CarModel.objects.filter(make__name__iexact=make_value, year=year_value).order_by('name')
        for model in models:
                model_choices.append((model.id, model.name))
        model_value = model_choices[0][0]
        if not value == '':
            model_value = value.id
        options = self.render_options(model_choices, [model_value])
        if options:
            output.append(options)
        output.append(u'</select>')
        
        return mark_safe(u'\n'.join(output))


class CarModelField(forms.Field):
    """A Field that lets you pick a model of car by year and make."""
    default_error_messages = {
        'invalid_choice': ugettext_lazy(u'Select a valid car model. That choice is not one of'
                            u' the available models.'),
    }

    def __init__(self, empty_label=u"---------",
                 required=True, label=None, initial=None,
                 help_text=None, to_field_name=None, *args, **kwargs):
        if required and (initial is not None):
            self.empty_label = None
        else:
            self.empty_label = empty_label
        widget = CarModelWidget
        forms.Field.__init__(self, required, widget, label, initial, help_text,
                       *args, **kwargs)

    def prepare_value(self, value):
        if hasattr(value, '_meta'):
            return value.pk
        return super(CarModelField, self).prepare_value(value)

    def to_python(self, value):
        try:
            value = CarModel.objects.get(**{'pk': value})
        except (ValueError, CarModel.objects.model.DoesNotExist):
            raise ValidationError(self.error_messages['invalid_choice'])
        return value

    def validate(self, value):
        return forms.Field.validate(self, value)
