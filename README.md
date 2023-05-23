# Lame Excuse Server

Lame Excuse Server is a demo application to show how to build a containerized Python application and how to run this application using the Google Kubernetes Engine (GKE).

## Step 1: Create a Kubernetes cluster

Log into the Google Cloud Console (https://cloud.google.com)

Once logged in, create a Kubernetes cluster:
- From menu select "Kubernetes Engine -> Clusters -> Create"
- Select name (or leave default "autopilot-cluster-1")
- Select region (e.g. "europe-west3")
- Finally, select "CREATE"

This may take several minutes to complete.

## Step 2: Build the lame-excuse-server container image

Activate the Google Cloud Shell and enter the following commands:

```
# Fetch the repository from GitHub
git clone https://github.com/wolfganghansmann/lame-excuse-server.git

cd lame-excuse-server

# Create a Container image and store it in the Container Registry
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
```

## Step 2.1 (Optional): Test the container in the Google Cloud Console

```
# Run the container
docker run -d -p 8000:8000 gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server

# Test 
curl localhost:8000
```

## Step 3: Run the container image in Kubernetes

```
# Configure credentials for kebectl
gcloud container clusters get-credentials autopilot-cluster-1 --region europe-west3 --project $GOOGLE_CLOUD_PROJECT

# Make sure everything runs without any error messages
kubectl version
kubectl get nodes

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

## Step 3.2 (Optional): Perform a rolling update of image in pods

```
# Modify main.py first.
# Then rebuild the container image and give it a different version (e.g. v2)
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2

# Perform the rolling update by assigning the new container image to the deployment
kubectl set image deployments/lame-excuse-server lame-excuse-server=gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2

kubectl get pods
```

## Step 4: Remove lame-excuse-server container images in artifactory 

```
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2
```

## Step 5: Shutdown the Kubernetes cluster

Never forget to delete the cluster after the tests to prevent bill shock!
