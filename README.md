# Lame Excuse Server

The Lame Excuse Server is a demo application to show how to build a containerized Python application and how to run this application using the Google Kubernetes Engine (GKE). 

The server produces a random lame excuse in the Bastard Operator From Hell (BOFH) style (cf. https://bofh.d00t.org/).

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

Fetch the repository from GitHub:
```
git clone https://github.com/wolfganghansmann/lame-excuse-server.git
cd lame-excuse-server
```

Create a container image and store it in the Google Container Registry:
```
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
```

## Step 2.1 (Optional): Test the container in the Google Cloud Console

Run the container:
```
docker run -d -p 8000:8000 gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
```

Test if the container is working:
```
curl http://localhost:8000
> {"excuse":"magnetic interference from money/credit cards", ...}
```

## Step 3: Run the container image in Kubernetes

Configure credentials for kubectl:
```
gcloud container clusters get-credentials autopilot-cluster-1 --region europe-west3 --project $GOOGLE_CLOUD_PROJECT
```

Make sure everything runs without any error messages:
```
kubectl version
> [...]

kubectl get nodes
> NAME                                                 STATUS   ROLES    AGE     VERSION
> gk3-autopilot-cluster-1-default-pool-51e1048c-wp0g   Ready    <none>   6m21s   v1.25.8-gke.500
> gk3-autopilot-cluster-1-pool-1-a239f898-82ds         Ready    <none>   3m28s   v1.25.8-gke.500
```

Create deployment with a single pod:
```
kubectl create deployment lame-excuse-server --image=gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
> deployment.apps/lame-excuse-server created
```

Repeat until the pod is running:

```
kubectl get pods
> NAME                                 READY   STATUS    RESTARTS   AGE
> lame-excuse-server-9df795c6f-9zl9t   1/1     Running   0          63s
```

Create a Kubernetes service to expose the application to the world via a load balancer:
```
kubectl expose deployment lame-excuse-server --port 80 --target-port 8000 --type LoadBalancer
> service/lame-excuse-server exposed
```

Retrieve external IP address of the service and test service in a web browser:
```
kubectl get service
> NAME                 TYPE           CLUSTER-IP    EXTERNAL-IP      PORT(S)        AGE
> kubernetes           ClusterIP      10.22.0.1     <none>           443/TCP        12m
> lame-excuse-server   LoadBalancer   10.22.0.164   35.198.131.223   80:30610/TCP   41s

curl http://35.198.131.223
> {"excuse":"Recursivity.  Call back if it happens again.", "served_by":"lame-excuse-server-9df795c6f-9zl9t"}}
```

## Step 3.1 (Optional): Scale the deployment up and down

Let application run in three pods:
```
kubectl scale deployment lame-excuse-server --replicas 3
> deployment.apps/lame-excuse-server scaled
```

Wait until all pods have status "Running":
```
kubectl get pods
> NAME                                 READY   STATUS    RESTARTS   AGE
> lame-excuse-server-9df795c6f-9zl9t   1/1     Running   0          7m9s
> lame-excuse-server-9df795c6f-qtnv6   1/1     Running   0          2m44s
> lame-excuse-server-9df795c6f-txx6l   1/1     Running   0          2m44s
```

## Step 3.2 (Optional): Perform a rolling update of image in pods

Modify main.py first. Then rebuild the container image and give it a different version (e.g. v2):
```
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2
```

Perform the rolling update by assigning the new container image to the deployment
```
kubectl set image deployments/lame-excuse-server lame-excuse-server=gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2
```

Wait until all pods have status "Running" again:
```
kubectl get pods
> NAME                                  READY   STATUS    RESTARTS   AGE
> lame-excuse-server-78b7746f55-5mq96   1/1     Running   0          71s
> lame-excuse-server-78b7746f55-tgfz6   1/1     Running   0          80s
> lame-excuse-server-78b7746f55-wrs9c   1/1     Running   0          77s
```

## Step 4: Remove lame-excuse-server container images in artifactory 

```
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/lame-excuse-server:v2
```

## Step 5: Shutdown the Kubernetes cluster

Never forget to delete the cluster after the tests to prevent bill shock!
