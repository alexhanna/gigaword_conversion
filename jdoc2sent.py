#!/usr/bin/env python
import re
import sys
import json

def tokensToSentence(tokens):
	sent   = ""
	postQt = False
	for i, token in enumerate(tokens):
		sep = " "
		if i == 0:
			sep = ""

		## replace special characters
		token = re.sub(r"\-LRB\-", "(", token)
		token = re.sub(r"\-RRB\-", ")", token)
				
		if False:
			pass
		elif postQt:
			sep = ""
			postQt = False	
		elif token in ["``", "`", "(", "["]: ## open, set flag
			postQt = True
			if False:
				pass
			elif token == "``":
				token = "\""
			elif token == "`":
				token = "'"
		elif token ==  "''": ## close quote, sep = ""
			token = '"'
			sep   = ""
		elif re.search(r"^([.,:;'\"?!)])|(\'s)|(\'ve)|(n\'t)$", token):
			sep   = ""
		sent += sep + token
	return sent

for line in sys.stdin:
	row       = line.split('\t')
	docid     = row[0]
	coreinfo  = json.loads(row[1])
	senttexts = json.loads(row[2])

	headline = coreinfo.get("headline", None)
	dateline = coreinfo.get("dateline", None)
	art_type = coreinfo.get("type", None)
	date     = docid.split(".")[0].split("_")[-1]

	print(docid)
	if headline:
		hl = tokensToSentence(coreinfo['headline']['tokens'])
		print(hl.encode("utf-8"))
	if dateline:
		dl = tokensToSentence(dateline["tokens"])
		print(dl.encode("utf-8"))
	if art_type:
		print(art_type)
	print(date)

	for senttext in senttexts["sentences"]:
		sent = tokensToSentence(senttext["tokens"])

		print(sent.encode("utf-8") + "\n")