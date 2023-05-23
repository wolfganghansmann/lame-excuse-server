# lame-excuse-server

Lame Excuse Server is a demo application to show how to build a containerized Python application and how to run this application using the Google Kubernetes Engine (GKE).

## Step 1: Create a Kubernetes cluster

Log into Google Cloud Console.
- From menu select "Kubernetes Engine -> Clusters -> Create"
- Select name "autopilot-cluster-1"
- Select Region "europe-west3"

## Step 2: Build the lame-excuse-server container image

```
git clone https://github.com/wolfganghansmann/lame-excuse-server.git

cd lame-excuse-server

gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
```

## Step 2.1 (Optional) test the container in the Google Cloud Console

```
docker run -d -p 8000:8000 gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server

curl localhost:8000
```

## Step 3: Run the container image in Kubernetes

```
# Configure credentials for kebectl
gcloud container clusters get-credentials autopilot-cluster-1 --region europe-west3 --project $GOOGLE_CLOUD_PROJECT

kubectl version

# Create deployment with a single pod
kubectl create deployment lame-excuse-server --image=gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server

# Repeat until the pod is running
kubectl get pods

# Create service
kubectl expose deployment lame-excuse-server --port 80 --target-port 8000 --type LoadBalancer

# Retrieve external IP address of the service and test service in a web browser
kubectl get service
> NAME                 TYPE           CLUSTER-IP   EXTERNAL-IP      PORT(S)        AGE
> kubernetes           ClusterIP      10.22.0.1    <none>           443/TCP        7m11s
> lame-excuse-server   LoadBalancer   10.22.2.22   34.159.128.224   80:31320/TCP   44s

```

## Step 3.1 (Optional): Scale the deployment up and down

```
# Let application run in three pods
kubectl scale deployment lame-excuse-server --replicas 3

kubectl get pods
```

# Step 3.2 (Optional): Perform a rolling update of image in pods

```
# 
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2

kubectl set image deployments/lame-excuse-server lame-excuse-server=gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2

kubectl get pods
```

## Step 4: Remove lame-excuse-server container images in artifactory 

```
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2
```

## Step 5: Never forget to delete the cluster after the tests to prevent bill shock

