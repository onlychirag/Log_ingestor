from django import forms

class LogSearchForm(forms.Form):
    level = forms.CharField(required=False)
    message = forms.CharField(required=False)
    resource_id = forms.CharField(required=False)
    timestamp = forms.DateTimeField(required=False)
    trace_id = forms.CharField(required=False)
    span_id = forms.CharField(required=False)
    commit = forms.CharField(required=False)
    parent_resource_id = forms.CharField(required=False)  # Assuming it's a direct field
