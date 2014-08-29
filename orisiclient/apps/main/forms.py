from django import forms
from BTCAddressField import BCAddressField

class TimelockForm(forms.Form):
  # charter_url = forms.CharField()
  locktime = forms.IntegerField(
      min_value = 1,
      label="How long should the money stay locked? In minutes")
  return_address = BCAddressField(
      label="Where should the money go after being unlocked? Your BTC return address")
