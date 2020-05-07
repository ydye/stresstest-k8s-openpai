# stresstest-k8s-openpai

### Local 

#### Setup env

```
sudo pip3 install locust
```

#### Test healthz stress test

```
locust -H https://x.x.x.x -f test/healthz.py
```

### Distributed mode in K8S

#### Setup env

```bash
sudo pip3 install -r requirements.txt
```

#### Prepare configurationfile and save as yml

```
target-url: x.x.x.x

master-url: x.x.x.x

stress-test-script: xxxxx
```

#### Label k8s node with master and slave

- master node

```
kubectl label nodes <node-name> locust-role=master 
```

- slave node

```
kubectl label nodes <node1-name> locust-role=slave

...

kubectl label nodes <nodeX-name> locust-role=slave
```

#### Start stresstest on kubernetes

```bash
./run-k8s.sh -c ${path-to-config}
```
