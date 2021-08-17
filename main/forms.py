from django import forms

from .models import Schema, Column


class SchemaForm(forms.ModelForm):
    user_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    column_separator = forms.ChoiceField(
        label="Column separator",
        widget=forms.Select(
            attrs={
                'class': 'form-control custom-select'
            }
        ),
        choices=Schema.COLUMN_SEPARATOR
    )
    string_separator = forms.ChoiceField(
        label="String separator",
        widget=forms.Select(
            attrs={
                'class': 'form-control custom-select'
            }
        ),
        choices=Schema.STRING_SEPARATOR
    )

    class Meta:
        model = Schema
        fields = ('user_id', 'title', 'column_separator', 'string_separator')


class ColumnForm(forms.ModelForm):
    name = forms.CharField(
        label='Column name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    column_type = forms.ChoiceField(
        label='Type',
        widget=forms.Select(
            attrs={
                'class': 'form-control custom-select'
            }
        ),
        choices=Column.TYPES
    )
    range_from = forms.IntegerField(
        label='From',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control range range_from',
                'min': '0'
            }
        ),
        required=False

    )
    range_to = forms.IntegerField(
        label='To',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control range range_to',
                'min': '0'
            }
        ),
        required=False
    )
    order = forms.IntegerField(
        label='Order',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': '0'
            }
        )
    )

    class Meta:
        model = Column
        fields = ('name', 'column_type', 'range_from', 'range_to', 'order')

    def clean(self):
        column_type = self.cleaned_data['column_type']
        range_from = self.cleaned_data['range_from']
        range_to = self.cleaned_data['range_to']
        if column_type == 'I':
            if range_from is None:
                self.add_error('range_from', "This field is required")
            elif range_to is None:
                self.add_error('range_to', "This field is required")
            elif range_from >= range_to:
                self.add_error('range_from', "'From' should be less than 'To'")


ColumnSchemaFormSet = forms.inlineformset_factory(Schema, Column, form=ColumnForm, extra=1)
