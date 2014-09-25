from django.views.generic import TemplateView, FormView, View
from django.templatetags.static import static
from forms import TimelockForm
from orisiclient.apps.fastcast.fastproto import generateKey, sendMessage, constructMessage, getMessages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from models import TimelockAddress

import json
import requests
import time
import datetime

from math import ceil
from random import randrange

# Create your views here.
class MainPageView(TemplateView):
  template_name = 'main/main.html'

class FAQView(TemplateView):
  template_name = 'main/faq.html'


##

MINERS_FEE = 4 * 4096

class GetTimelockForAddress(View):
  def get(self, request, *args, **kwargs):
    data = {}

    message_id = request.GET.get('message_id', False)
    if not message_id:
      data['result'] = 'failure'
    else:
      data['result'] = 'success'
      messages = getMessages()
      messages = messages['results']
      f1_messages = []

      for msg in messages:
        try:
          msg['body'] = json.loads(msg['body'])
        except:
          continue
        if 'operation' in msg['body'] and \
            msg['body']['operation'] == 'safe_timelock_created' and \
            msg['body']['in_reply_to'] == message_id:
          msg_data = {}
          msg_data['mark'] = msg['body']['mark']
          msg_data['addr'] = msg['body']['addr']
          msg_data['time'] = msg['body']['time']
          f1_messages.append(msg_data)

      if len(f1_messages) > 0:
        data['results'] = f1_messages
        data['created'] = 'yes'
      else:
        found_error = False
        for msg in messages:
          if 'operation' in msg['body'] and \
              msg['body']['operation'] == 'safe_timelock_error' and \
              msg['body']['in_reply_to'] == message_id:
            data['result'] = 'success'
            data['created'] = 'no'
            found_error = True
            break

        if not found_error:
          data['result'] = 'failure'


    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

class TimelockRetrieveView(TemplateView):
  template_name = 'main/timelock_retrieve.html'

  def get_context_data(self, **kwargs):
    context = super(TimelockRetrieveView, self).get_context_data(**kwargs)

    has_key = self.request.session.get('fastcast_address', False)

    data = json.loads(has_key)
    pub = data['pub']

    ta = TimelockAddress.objects.filter(pub=pub).order_by('-ts')[0]
    context['ta'] = ta

    context['locktime'] = ta.locktime

    return context

  def get(self, *args, **kwargs):
    has_key = self.request.session.get('fastcast_address', False)
    if not has_key:
      return HttpResponseRedirect('homepage')
    data = json.loads(has_key)
    pub = data["pub"]
    if TimelockAddress.objects.filter(pub=pub).order_by('-ts').count() == 0:
      return HttpResponseRedirect('homepage')

    return super(TimelockRetrieveView, self).get(*args, **kwargs)

class TimelockView(FormView):
  template_name = 'main/timelock.html'
  form_class = TimelockForm

  def get_success_url(self):
      return reverse_lazy('main:timelock-retrieve')

  def form_valid(self, form):
    has_key = self.request.session.get('fastcast_address', False)
    if not has_key:
      pub, priv = generateKey()
      self.request.session['fastcast_address'] = json.dumps({'pub':pub, 'priv':priv})
    else:
      data = json.loads(has_key)
      pub = data['pub']
      priv = data['priv']

    charter_json = requests.get('http://' + self.request.get_host() + static('charter.json')).content
    charter = json.loads(charter_json)

    oracle_pubkeys = []
    oracle_fees = {}
    for o in charter['nodes']:
      oracle_pubkeys.append(o['pubkey'])
      oracle_fees[o['address']] = o['fee']
    min_sigs = int(ceil(float(len(oracle_pubkeys))/2))

    oracle_fees[charter['org_address']] = charter['org_fee']

    key_list = oracle_pubkeys

    request = {}
    return_address = form.cleaned_data['return_address']


    msig_addr = return_address

    request['message_id'] = "%s-%s" % (msig_addr, str(randrange(1000000000,9000000000)))

    ta = TimelockAddress(
        address = return_address,
        pub = pub,
        message_id = request['message_id'],
        locktime = form.cleaned_data['locktime'])
    ta.save()

    request['pubkey_list'] = key_list
    request['miners_fee_satoshi'] = MINERS_FEE
    request['locktime'] = time.time() + int(form.cleaned_data['locktime'])*60
    request['return_address'] = return_address
    request['oracle_fees'] = oracle_fees
    request['req_sigs'] = min_sigs
    request['operation'] = 'safe_timelock_create'

    meta_request = {}
    meta_request['source'] = pub
    meta_request['channel'] = 0
    meta_request['epoch'] = time.mktime(datetime.datetime.utcnow().timetuple())
    meta_request['body'] = json.dumps(request)

    sendMessage(constructMessage(priv, **meta_request))

    return super(TimelockView, self).form_valid(form)
