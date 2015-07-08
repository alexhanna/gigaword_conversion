#!/usr/bin/env python
import re
import sys
import json

def tokensToSentence(tokens):
	""" Operations to clean up the parsed tokens and turn them into more human-readable text. """
	sent   = ""
	postQt = False
	for i, token in enumerate(tokens):
		sep = " "
		if i == 0:
			sep = ""

		## replace special characters
		token = re.sub(r"\-LRB\-", "(", token)
		token = re.sub(r"\-RRB\-", ")", token)
		token = re.sub(r"^dlrs$", "$", token)
				
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

def processDocument(line):
	""" Process an individual newswire item """
	data      = {}
	row       = line.split('\t')
	docid     = row[0]
	coreinfo  = json.loads(row[1])
	senttexts = json.loads(row[2])

	headline  = coreinfo.get("headline", None)
	dateline  = coreinfo.get("dateline", None)
	art_type  = coreinfo.get("type", None)
	date      = docid.split(".")[0].split("_")[-1]

	data['DOCID'] = docid
	if headline:
		hl = tokensToSentence(coreinfo['headline']['tokens'])
		data['TITLE'] = hl
	if dateline:
		dl = tokensToSentence(dateline["tokens"])
		data['DATELINE'] = dl
	if art_type:
		data['ARTICLE TYPE'] = art_type
	data['DATE'] = date

	body = ""
	for senttext in senttexts["sentences"]:
		sent = tokensToSentence(senttext["tokens"])
		body += sent + "\n\n"

	data['TEXT'] = body

	return data

def processJDocFile(filename):
	""" Process files which have been preprocessed into the JDoc format """
	fh  = open(filename, 'r')

	## write to file
	out_fn = filename.replace("jdoc", "sent")
	out    = open(out_fn, "w")
	for line in fh:
		data = processDocument(line)

		for field in ['DOCID', 'TITLE', 'DATELINE', 'ARTICLE TYPE', 'DATE']:
			if data.get(field, None):
				out.write(field + ": " + data[field].encode("utf-8") + "\n")

		out.write(data['TEXT'].encode("utf-8") + "\n")

	## but also return data to be inserted into Solr
	return data

def main():
	filename = sys.argv[1]
	processJDocFile(filename)

if __name__ == '__main__':
	main()

