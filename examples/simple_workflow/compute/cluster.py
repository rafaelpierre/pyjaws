from pyjaws.api.base import Cluster, Runtime

cluster = Cluster(
    job_cluster_key = "ai_cluster",
    spark_version = Runtime.DBR_13_ML,
    num_workers = 2,
    node_type_id = "Standard_DS3_v2",
    cluster_log_conf = {
        "dbfs": {
            "destination": "dbfs:/home/cluster_log"
        }
    }
)