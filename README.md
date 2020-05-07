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

### K8S

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

#### Start stresstest on 

```angular2

```

