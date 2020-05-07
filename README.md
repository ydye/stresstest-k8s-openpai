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

```angular2

```

#### build

```bash
sudo docker build -t stress-openpai -f docker/dockerfile .
```

#### Prepare configurationfile and save as yml
```
target-url: x.x.x.x

master-url: x.x.x.x

stress-test-script: xxxxx
```

#### Generate kubernetes yaml file
```angular2

```

