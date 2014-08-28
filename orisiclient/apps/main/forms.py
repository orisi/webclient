from django import forms
from BTCAddressField import BCAddressField

class TimelockForm(forms.Form):
  # charter_url = forms.CharField()
  locktime = forms.IntegerField(
      min_value = 1,
      label="On how many minutes do you want to set a lock?")
  return_address = BCAddressField(
      label="Your Bitcoin return address")
