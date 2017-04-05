# Server Controller

Description
-----
Server Controller is a workflow manager that is to link all of the modules (Data2RDF, Virtuoso - RDF triplestore) to construct a united information extraction framework as a service. It is a part of the information extraction framework for the EUROSTAR - QAMEL project.

Prerequisite
-----
The module is working on Python 2.7. It must be prepared to install Python 2.7 and PIP (Python Package Index) before the installation of the module.

How to install / execute
-----
Before executing the module, we need to install all of the dependencies.
To install dependencies, execute the following command.

```
sh dependency.sh
```

Configure a service address of the modules (Data2RDF, Virtuoso - RDF triplestore) by editing "conf.json" as follows.

```
{
	"address": {
		"data2rdf": "http://qamel.kaist.ac.kr:7401/service",
		"triplestore": "http://qamel.kaist.ac.kr:8890"
	},
	"auth_info": {
		"triplestore": {
			"id": "admin's ID for Virtuoso conductor",
			"pw": "admin's password for Virtuoso conductor"
		}
	}
}
```

To execute the module, run the service by the following command.

```
python service.py
```

The address of REST API is as follows.

```
http://(server-address):7403/service
```

The module accepts only a POST request which of content type must be "application/json".

AUTHOR(S)
---------
* Jiseong Kim, MachineReadingLab@KAIST

License
-------
Released under the MIT license (http://opensource.org/licenses/MIT).