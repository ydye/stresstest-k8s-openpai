#!/bin/bash

kubectl create configmap locust-script-configuration --from-file=kubernetes/ --dry-run -o yaml | kubectl apply --overwrite=true -f - || exit $?

kubectl create -f locust-master.yaml

kubectl create -f locust-slave.yaml