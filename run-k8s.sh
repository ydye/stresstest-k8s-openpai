#!/bin/bash

while getopts "w:m:c:" opt; do
  case $opt in
    c)
      CLUSTER_CONFIG=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG"
      exit 1
      ;;
  esac
done

echo "config file path: ${CLUSTER_CONFIG}"


python3 stresstest-generator.py -c ${CLUSTER_CONFIG}

kubectl create configmap locust-script-configuration --from-file=kubernetes/ --dry-run -o yaml | kubectl apply --overwrite=true -f - || exit $?

kubectl create -f kubernetes/locust-master.yaml

kubectl create -f kubernetes/locust-slave.yaml