#!/bin/bash

set -eu

if [ ! -f $SNAP_COMMON/config.yaml ]; then
	echo "configuration file $SNAP_COMMON/config.properties does not exist."
	exit 1
fi

export PATH=$SNAP/usr/lib/jvm/default-java/bin:$PATH
unset JAVA_HOME

$SNAP/opt/kafka/bin/kafka-server-start.sh $SNAP_COMMON/server.properties
