import gettext

""" localization support """
en = gettext.translation(
    'messages', 'translations/generated', languages=['en'])
pt_br = gettext.translation(
    'messages', 'translations/generated', languages=['pt_BR'])

en.install()
