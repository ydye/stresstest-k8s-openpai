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

#### Build

```bash
sudo docker build -t stress-openpai -f Docker/dockerfile .
```