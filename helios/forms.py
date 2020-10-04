#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Forms for Helios
"""

from django import forms
from .models import Election
from .widgets import SplitSelectDateTimeWidget
from .fields import SplitDateTimeField
from django.conf import settings


class ElectionForm(forms.Form):
  short_name = forms.SlugField(max_length=40, label='Kurzbezeichnung', help_text='keine Leerzeichen, wird Teil der URL f&uuml;r die Wahl, z.B. landesversammlung-2020')
  name = forms.CharField(max_length=100, label='Öffentliche Bezeichnung', widget=forms.TextInput(attrs={'size':60}), help_text='der offizielle Name deiner Wahl, z.B. Landesversammlung 2020')
  description = forms.CharField(max_length=4000, label='Beschreibung', widget=forms.Textarea(attrs={'cols': 70, 'wrap': 'soft'}), required=False)
  election_type = forms.ChoiceField(label="Typ", choices = Election.ELECTION_TYPES)
  use_voter_aliases = forms.BooleanField(required=False, initial=True, label='Aliase verwenden', help_text='Wenn angehakt, werden die W&auml;hler*innen-Namen im Tracking-Center durch Aliases (wie "V42") ersetzt')
  #use_advanced_audit_features = forms.BooleanField(required=False, initial=True, help_text='disable this only if you want a simple election with reduced security but a simpler user interface')
  randomize_answer_order = forms.BooleanField(required=False, label='Antworten in zufälliger Reihenfolge', initial=False, help_text='Wenn angehakt, werden die Wahlm&ouml;glichkeiten den W&auml;hler*innen in zuf&auml;lliger Reihenfolge angezeigt')
  private_p = forms.BooleanField(required=False, initial=True, label="Private Wahl", help_text='Eine private Wahl ist nur f&uuml;r registrierte W&auml;hler*innen sichtbar.')
  help_email = forms.CharField(required=False, initial="", label="Kontaktadresse", help_text='Eine Email-Adresse, an die sich W&auml;hler*innen wenden k&ouml;nnen, wenn sie Hilfe brauchen.')
  
  if settings.ALLOW_ELECTION_INFO_URL:
    election_info_url = forms.CharField(required=False, initial="", label="URL mit Wahlinformationen", help_text="Die URL eines Dokuments mit weiterf&uuml;hrenden Informationen zur Wahl, z.B. Biographien der Kandidat*innen, ...")
  
  # times
  voting_starts_at = SplitDateTimeField(label='Wahl startet um', help_text = 'Startdatum/-zeit der Wahl (UTC!)',
                                   widget=SplitSelectDateTimeWidget, required=False)
  voting_ends_at = SplitDateTimeField(label='Wahl endet um', help_text = 'Enddatum/-zeit der Wahl (UTC!)',
                                   widget=SplitSelectDateTimeWidget, required=False)

class ElectionTimeExtensionForm(forms.Form):
  voting_extended_until = SplitDateTimeField(label='Verschobenes Ende', help_text = 'Verl&auml;ngertes Enddatum der Wahl (UTC!)',
                                   widget=SplitSelectDateTimeWidget, required=False)
  
class EmailVotersForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=4000, widget=forms.Textarea)
  send_to = forms.ChoiceField(label="Senden an", initial="all", choices= [('all', 'alle W&auml;hler*innen'), ('voted', 'W&auml;hler*innen, die schon abgestimmt haben'), ('not-voted', 'W&aum;hler*innen, die noch nicht abgestimmt haben')])

class TallyNotificationEmailForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=2000, widget=forms.Textarea, required=False)
  send_to = forms.ChoiceField(label="Senden an", choices= [('all', 'alle W&auml;hler*innen'), ('voted', 'W&auml;hler*innen, die abgestimmt haben'), ('none', 'niemanden - bist du sicher?')])

class VoterPasswordForm(forms.Form):
  voter_id = forms.CharField(max_length=50, label="W&auml;hler*innen-ID")
  password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

