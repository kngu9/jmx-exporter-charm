#!/bin/bash

set -eu

if [ ! -f $SNAP_COMMON/config.yaml ]; then
	echo "configuration file $SNAP_COMMON/config.yaml does not exist."
	exit 1
fi

java -jar $SNAP/jmx_prometheus_httpserver/jmx_prometheus_httpserver-0.11.0-jar-with-dependencies.jar 0.0.0.0:4081 $SNAP_COMMON/config.yaml
