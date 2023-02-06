# Dataproc Example 

A simple example of setting up Dataproc 

1. [Install and run a Jupyter notebook on a Dataproc cluster](https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook)

* bucket name: `da-bucket1`
* command: 

```
gcloud beta dataproc clusters create da-cluster1 \
    --optional-components=ANACONDA,JUPYTER \
    --image-version=1.3 \
    --enable-component-gateway \
    --bucket=da-bucket1 \
    --region=us-central1 \
    --project=alpine-guild-286019
```

2. [Dataproc on Google Kubernetes Engine  |  Dataproc Documentation](https://cloud.google.com/dataproc/docs/concepts/jobs/dataproc-gke#register-the-gke-cluster-with-cloud-dataproc)

* cluster name and region:

```
GKE_CLUSTER=da-cluster1 \
  GCE_REGION=us-central1
```

* create clusters

```
gcloud beta container clusters create "${GKE_CLUSTER}" \
    --scopes=cloud-platform \
    --workload-metadata-from-node=GCE_METADATA \
    --machine-type=n1-standard-4 \
    --region="${GCE_REGION}"
```

2. create dataproc-on-gke cluster
    * name:

```
DATAPROC_CLUSTER=da-cluster2 \
  VERSION=1.4.27-beta \
  BUCKET=da-bucket1
```

* command:

```
gcloud beta dataproc clusters create "${DATAPROC_CLUSTER}" \
    --gke-cluster="${GKE_CLUSTER}" \
    --region="${GCE_REGION}" \
    --image-version="${VERSION}" \
    --bucket="${BUCKET}"
```

3. Submit a Spark Job:

```
gcloud dataproc jobs submit spark-r \
    --cluster="${DATAPROC_CLUSTER}" file:/usr/lib/spark/examples/src/main/r/dataframe.R \
    --region="${GCE_REGION}"
```

4. Clean up


## References 

* <https://cloud.google.com/dataproc/docs/guides/submit-job>
* <https://cloud.google.com/dataproc/docs/guides/manage-spark-dependencies>
