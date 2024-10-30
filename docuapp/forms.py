from django.forms import ModelForm
from django import forms
from .models import Expedient, ReceiveExpedient, DocType, Office, Condition
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit



# DOCTYPE FORM --------------------------------------------------------------------
class DocTypeForm(ModelForm):

    class Meta:     
        model = DocType
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

        # Verificamos si estamos en modo edición
        if hasattr(self.instance, 'name') and self.instance.name:
            submit_text = "Actualizar"
        else:
            submit_text = "Registrar"

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', submit_text, css_class='btn btn-primary')
        )



# OFFICE FORM --------------------------------------------------------------------
class OfficeForm(ModelForm):

    class Meta:     
        model = Office
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

        # Verificamos si estamos en modo edición
        if hasattr(self.instance, 'name') and self.instance.name:
            submit_text = "Actualizar"
        else:
            submit_text = "Registrar"

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', submit_text, css_class='btn btn-primary')
        )



# EXPEDIENT FORM --------------------------------------------------------------------
class ExpedientForm(ModelForm):

    class Meta:     
        model = Expedient
        fields = ['document','doc_number', 'subject', 'remitter', 'destination', 'condition', 'folio', 'phone', 'email', 'observation']

        widgets = {
            'subject': forms.Textarea(attrs={'rows': 1}),
            'observation': forms.Textarea(attrs={'rows': 1}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['document'].widget.attrs.update({'autofocus': 'autofocus'})

        if self.instance.subject:  
            self.fields['document'].widget.attrs.pop('autofocus', None)
        
        if not self.instance.pk:
            self.fields['condition'].initial = Condition.objects.get(name="ASIGNADO")
        
        self.fields['condition'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef; pointer-events: none;'  
        })

        if not self._should_show_contact_fields(user):
            del self.fields['phone']
            del self.fields['email']
        
        if hasattr(self.instance, 'doc_number') and self.instance.doc_number:
            submit_text = "Actualizar"
        else:
            submit_text = "Registrar"

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('document', css_class='form-group col-md-6 mb-0'),
                Column('doc_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-6 mb-0'),
                Column('remitter', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('destination', css_class='form-group col-md-6 mb-0'),
                Column('condition', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0') if 'phone' in self.fields else None,
                Column('email', css_class='form-group col-md-6 mb-0') if 'email' in self.fields else None,
                css_class='form-row'
            ),
            Row(
                Column('folio', css_class='form-group col-md-6 mb-0'),
                # Column('observation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', submit_text, css_class='btn btn-primary')
        )

        self.fields['document'].empty_label = 'Escoge documento...'
        self.fields['destination'].empty_label = 'Escoge destino...'

    def _should_show_contact_fields(self, user):
        """Verifica si se deben mostrar los campos 'phone' y 'email'."""
        return user.is_superuser or user.groups.filter(name='mpmtc').exists()



# RECEIVE EXPEDIENT FORM --------------------------------------------------------------------
class ReceiveExpedientForm(forms.ModelForm):
    expedient_code = forms.CharField(label='Código', disabled=True, required=False)
    expedient_doc_number = forms.CharField(label='N° Doc.', disabled=True, required=False)
    expedient_subject = forms.CharField(label='Asunto', disabled=True, required=False)

    class Meta:
        model = ReceiveExpedient
        fields = ['office', 'condition', 'destination' ,'observation']
        widgets = {
            'observation': forms.Textarea(attrs={'rows': 1, 'maxlength': 50}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        expedient = kwargs.pop('expedient', None)
        is_edit = kwargs.pop('is_edit', False)

        super().__init__(*args, **kwargs)

        if user:
            user_groups = user.groups.all()
            office = Office.objects.filter(groups__in=user_groups).first()

            if office:
                self.fields['office'].initial = office

        self.fields['condition'].queryset = Condition.objects.exclude(name='ASIGNADO')

        if expedient:
            self.fields['expedient_code'].initial = expedient.code
            self.fields['expedient_doc_number'].initial = expedient.doc_number
            self.fields['expedient_subject'].initial = expedient.subject
        
        if not is_edit:
            self.fields['destination'].widget = forms.HiddenInput()
        else:
            self.fields['destination'].widget.attrs.update({'class': 'form-control'})
            
        if self.instance.pk:
            self.fields['condition'].initial = Condition.objects.get(name="RECIBIDO")
        
            self.fields['condition'].widget.attrs.update({
            'readonly': 'readonly',
            'style': 'background-color: #e9ecef; pointer-events: none;'  
            })

            self.fields['office'].widget.attrs.update({
                    'readonly': 'readonly',
                    'style': 'background-color: #e9ecef; pointer-events: none;'
                })

        if hasattr(self.instance, 'office') and self.instance.office:
            self.fields['condition'].widget.attrs.pop('readonly', None)
            self.fields['condition'].widget.attrs.pop('style', None)
            

            submit_text = "Actualizar"
        else:
            submit_text = "Registrar"
            self.fields.pop('observation')

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('office', css_class='form-group col-md-6 mb-0'),
                Column('condition', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('destination', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('observation', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', submit_text, css_class='btn btn-primary')
        )

        self.fields['office'].empty_label = 'Escoge oficina...'
        self.fields['destination'].empty_label = 'Escoge destino...'
        self.fields['condition'].empty_label = 'Escoge estado...'
