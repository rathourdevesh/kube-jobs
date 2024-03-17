from flask import Flask, jsonify, request
from kubernetes import client, config

app = Flask(__name__)

def create_kubernetes_job():
    # Load Kubernetes configuration
    config.load_incluster_config()

    # Create Kubernetes API client
    api_instance = client.BatchV1Api()

    # Define the Job spec
    job_spec = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="flask-job"),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "flask-job"}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="flask-job",
                            image="flask-job-app1:latest",
                            image_pull_policy="Never",
                            # ports=[client.V1ContainerPort(container_port=5000)]
                        )
                    ],
                    restart_policy="Never",
                )
            ),
            # Ensure that the Job runs to completion before being terminated
            backoff_limit=0,
            completions=1,
            # Uncomment the line below if you want to specify parallelism
            # parallelism=1,
            # Uncomment the line below if you want to specify a deadline for the Job
            # active_deadline_seconds=600,
            # Uncomment the line below if you want to specify a TTL for the Job
            # ttl_seconds_after_finished=600
        )
    )

    try:
        # Create the Job
        api_instance.create_namespaced_job(namespace="default", body=job_spec)
        print("Job created successfully.")
    except Exception as e:
        print(f"Error creating Job: {e}")


# Sample endpoint to trigger the Job
@app.route('/trigger-job', methods=['POST'])
def trigger_job():
    payload = request.json  # Assuming payload is sent as JSON in the request body
    create_kubernetes_job()
    return jsonify({"message": "Job triggered successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
