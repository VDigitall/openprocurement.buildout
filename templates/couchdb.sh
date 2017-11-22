#!/bin/bash
export ERL_FLAGS="-couch_ini /opt/couchdb/etc/default.ini {{parts.buildout.directory}}/etc/couchdb.ini /opt/couchdb/etc/local.ini"
/opt/couchdb/bin/couchdb
