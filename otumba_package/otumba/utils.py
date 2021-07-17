from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from kubernetes import client,config
from prometheus_api_client import PrometheusConnect
config.load_kube_config()
v1=client.CoreV1Api()

def manage_pods(replicas, docker_image, name_pod, cpu_limits, cpu_request, namespace_pod):
    config.load_kube_config()
    apps_api = client.AppsV1Api()
    deployment = client.V1Deployment()
    deployment.api_version = "apps/v1"
    deployment.kind = "Deployment"
    deployment.metadata = client.V1ObjectMeta(name=name_pod)
    spec = client.V1DeploymentSpec(
        selector=client.V1LabelSelector(match_labels={"app":name_pod}),
        template=client.V1PodTemplateSpec(),
    )
    container = client.V1Container(
        image=docker_image,
        resources = {"limits": {"cpu":cpu_limits} , "requests": {"cpu":cpu_request}},
        name=name_pod, 
    )
    spec.template.metadata = client.V1ObjectMeta(
        name=name_pod,
        labels={"app":name_pod},
    )
    spec.template.spec = client.V1PodSpec(containers = [container])
    dep = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name_pod),
        spec=spec,
    )
    dep.spec.replicas = replicas
    try:
        apps_api.create_namespaced_deployment(namespace=namespace_pod, body=dep)
    except:
        print("Pod Exist, updating replicas")    
    dep.spec.replicas = replicas
    changeddeploy= apps_api.replace_namespaced_deployment(name=name_pod, namespace=namespace_pod, body=dep)


def get_pod_metrics_scenario_1(server, lapso, namespace, podname, requestpodname):

    prom = PrometheusConnect(url=server, disable_ssl=True)

    strQuery='sum(rate(container_file_descriptors{pod=~"' + podname +'[^v]*", container!="POD", namespace="' + namespace + '", container ="' + podname +'"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    try:
        file_descriptors=resultado[0]["value"][1]
    except:
        file_descriptors = "0"
    
    strQuery='sum(rate(container_network_receive_packets_total{pod=~"' + podname +'[^v]*", namespace="' + namespace + '",  interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    try:
        receive_packets=resultado[0]["value"][1]
    except:
        receive_packets = "0"

    strQuery='sum(rate(container_network_transmit_packets_total{pod=~"' + podname +'[^v]*", namespace="'+ namespace + '" , interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    try:
        transmit_packets=resultado[0]["value"][1]
    except:
        transmit_packets = "0"

    strQuery='sum(rate(container_network_transmit_packets_dropped_total{namespace="'+ namespace +'",pod="'+ requestpodname + '",interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    try:
        dropped_packets=resultado[0]["value"][1]
    except:
        dropped_packets = "0"
    

    strQuery='sum(rate(container_cpu_usage_seconds_total{container_name!="POD",container!="POD" ,namespace="'+ namespace +'" ,pod=~"' + podname +'[^v]*", }['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    try:
        cpu_usage_seconds=resultado[0]["value"][1]
    except:
        cpu_usage_seconds = "0"

    strQuery='sum(rate(container_cpu_cfs_throttled_seconds_total{ namespace="'+ namespace + '", pod=~"' + podname +'[^v]*" }['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    
    try:
        cpu_throttled_seconds=resultado[0]["value"][1]
    except:
        cpu_throttled_seconds = "0"    

    strQuery='sum(rate(container_memory_working_set_bytes{ namespace="' + namespace + '", pod=~"' + podname +'[^v]*"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    
    try:
        memory_working_bytes=resultado[0]["value"][1]
    except:
        memory_working_bytes = "0"    
    
    
    strQuery='count(container_memory_usage_bytes{container="' + podname +'", namespace="'+ namespace +'"})'
    resultado = prom.custom_query(query=strQuery)
    
    try:
        memory_usage_bytes=resultado[0]["value"][1]
    except:
        memory_usage_bytes = "0"    
    
    
    ret=v1.list_namespaced_pod(namespace,watch=False)
    pods=ret.items
    pods_names=[pod.metadata.name for pod in pods]
    number_pods= 0
    for pod in pods_names:
        if (pod.find(podname)>-1):
            number_pods = number_pods+1
    
    formatted_pods = "{:.1f}".format(float(number_pods))
    formatted_file_descriptors = "{:.1f}".format(float(file_descriptors))
    formatted_receive_packets = "{:.1f}".format(float(receive_packets))
    formatted_transmit_packets = "{:.1f}".format(float(transmit_packets))
    formatted_dropped_packets = "{:.1f}".format(float(dropped_packets))
    formatted_cpu_usage_seconds = "{:.10f}".format(float(cpu_usage_seconds))
    formatted_cpu_throttled_seconds = "{:.10f}".format(float(cpu_throttled_seconds))
    formatted_memory_working_bytes = "{:.1f}".format(float(memory_working_bytes))
    formatted_memory_usage_bytes = "{:.1f}".format(float(memory_usage_bytes))

    return{"pods": formatted_pods,"file_descriptors":formatted_file_descriptors,"receive_packets":formatted_receive_packets,
          "transmit_packets":formatted_transmit_packets, "dropped_packets":formatted_dropped_packets,
          "cpu_usage_seconds":formatted_cpu_usage_seconds, "cpu_throttled_seconds": formatted_cpu_throttled_seconds,
          "memory_working_bytes": formatted_memory_working_bytes, "memory_usage_bytes" :formatted_memory_usage_bytes}

