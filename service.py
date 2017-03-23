# -*- coding: utf-8 -*-

import sys, json
import urllib, urllib2

from bottle import route, run, template, request, response, post
import ipfinder

import os, subprocess, string, random

host_ip = ipfinder.get_ip_address('eth0')
port = '7403'

def service(i_json, conf):
	o_json = None

	# Service routine -------------------------------------
	documents = i_json['documents']

	# data2rdf
	rdf_files = []
	for x in documents:
		data2rdf_input = {'input': x, 'conf': conf}

		data2rdf_output = send_postrequest(conf['address']['data2rdf'], json.dumps(data2rdf_input))
		data2rdf_output = json.loads(data2rdf_output)

		rdf_file = data2rdf_output['output']
		log = data2rdf_output['log']

		rdf_files.append(rdf_file)

	# triple upload
	for x in rdf_files:
		# making a rdf file
		dir_path = os.path.dirname(os.path.realpath(__file__)) + '/temp/'
		file_path = dir_path + id_generator() + '.ttl'

		i_file = open(file_path, 'w+')
		i_file.write(x.encode('utf-8'))
		i_file.close()

		# inserting triples into a triplestore
		db_id = conf['auth_info']['triplestore']['id']
		db_pw = conf['auth_info']['triplestore']['pw']

		graph_iri = 'http://qamel.kaist.ac.kr'

		command = 'curl --digest --user %s:%s --verbose --url "%s/sparql-graph-crud-auth?graph-uri=%s" -X POST -T "%s"' % (db_id, db_pw, conf['address']['triplestore'], graph_iri, file_path)
		subprocess.call(command, shell=True)

		# removing a rdf file
		subprocess.call('rm %s' % file_path, shell=True)

	o_json = {'rdf_files': rdf_files}
	# /Service routine -------------------------------------

	return o_json

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		# set CORS headers
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if request.method != 'OPTIONS':
			# actual request; reply with the actual response
			return fn(*args, **kwargs)
		
	return _enable_cors

def send_postrequest(url, input_string):
	opener = urllib2.build_opener()
	request = urllib2.Request(url, data=input_string, headers={'Content-Type':'application/json'})
	return opener.open(request).read()

def set_conf(new_conf):
	# default configuration
	i_file = open('conf.json', 'r')
	sInput = i_file.read()
	i_file.close()
	conf = json.loads(sInput)

	# updated configuration
	conf.update(new_conf)
	
	return conf

@route(path='/service', method=['OPTIONS', 'POST'])
@enable_cors
def do_request():
	if not request.content_type.startswith('application/json'):
		return 'Content-type:application/json is required.'

	# input reading
	i_text = request.body.read()
	try:
		i_text = i_text.decode('utf-8')
	except:
		pass
	i_json = json.loads(i_text)

	# configuration setting
	try:
		conf = set_conf(i_json['conf'])
	except:
		conf = set_conf({})

	# request processing
	o_json = service(i_json, conf)
	o_text = json.dumps(o_json, indent=5, separators=(',', ': '), sort_keys=True)	

	return o_text

run(server='cherrypy', host=host_ip, port=port)