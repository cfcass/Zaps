import re, requests, json

email = input['email']

datacapture = r'\s*\n\s*((?:\w+\s*?)+)\s*\n'
phonecap = r'\s*\n\s*((?:\d+-?)+)\s*\n'
emcap = r'\s*\n\s*(\S+)\s*\n'

billsecre = re.search("BILLED TO:\s*\n((?:.*?\n)+)\s*Order Summary\s*\n", email)
billsection = billsecre.group(1) if billsecre else None
billnamere = re.search("\s*\n?\s*(\w.*?)\s*\n((?:.*?\n)+.+\,.+,.+\d{2,}.*?)\s*\n(?:.*?\n)+\s*(\S+@\S+)\s*\n\s*(\S.*?)\s*\n", billsection)
billname = billnamere.group(1) if billnamere else None
address = billnamere.group(2) if billnamere else None
billemail = billnamere.group(3) if billnamere else None
billphone = billnamere.group(4) if billnamere else None


namere = re.search("Name:" + datacapture, email)
childnamere = re.search("Childs Name:" + datacapture, email)
agere = re.search("Childs Age:" + datacapture, email)
phonere = re.search("Phone:" + phonecap, email)
emre = re.search("Email:" + emcap, email)
addaccre = re.search("Additional Accommodations:\s*\n\s*(\w(?:.+\w.+\n*)+)\nAdditional Comments:", email)
addcomre = re.search("Additional Comments:\s*\n\s*(\w(?:.+\w.+\n*)+)\n\n\d\n", email)
titlere = re.search("SUBTOTAL\s*\n\s*\n\s*(\S.+)\s*\n\s*(\S.*?)\s*\n", email)
moneyre = re.search("\sTOTAL\s*\n\s*\$(\S.*?)\s*\n", email)

name = namere.group(1) if namere else None
childname = childnamere.group(1) if childnamere else None
age = agere.group(1) if agere else None
phone = phonere.group(1) if phonere else None
em = emre.group(1) if emre else None
addacc = addaccre.group(1) if addaccre else None
addcom = addcomre.group(1) if addcomre else None
title = titlere.group(1) if titlere else None
code = titlere.group(2) if titlere else None
billname = billnamere.group(1) if billnamere else None
money = moneyre.group(1) if moneyre else None

url = r'https://us12.api.mailchimp.com/3.0/lists/<List ID goes here/members'
mergefields = {}
if billname:
    mergefields['NAME'] = billname
if childname:
    mergefields['CHILDNAME'] = childname
if address:
    mergefields['ADDRESS'] = address
if age:
    mergefields['CHILDAGE'] = age
if billphone:
    mergefields['PHONE'] = billphone
if billemail:
    mergefields['BILLINGEMA'] = billemail
if em:
    mergefields['EMAIL'] = em
if addacc:
    mergefields['ADDACC'] = addacc
if addcom:
    mergefields['ADDCOM'] = addcom
if title:
    mergefields['COURSE'] = title
if code:
    mergefields['CODE'] = code
if money:
    mergefields['PRICE'] = money

payload = {
           'email_address': em,
           'status': 'subscribed',
           'merge_fields': mergefields}

response = requests.post(url, json=payload,
    auth=requests.auth.HTTPBasicAuth('<MailChimp Username goes here', 'API Key goes here'))

output = [{'Response':response.text}]
