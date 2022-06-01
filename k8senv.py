from prometheus_api_client import PrometheusConnect
from kubernetes import client, config

def enviroment(cargaprevia=""):
    global dataloaded
    if (cargaprevia !=""):
        dataloaded=True
        print(dataloaded)

def normal(valor, min, max):
    """
    Función que normaliza numeros
    """
    return (valor - min) / (max - min )
  
def getstateloaded(action):
    global data
    
    return 

def step(initial_pods, serverprometheus, lapso,namespace):
    """
    Function that initialize enviroment
        Assign initial pods
    """
    global dataloaded
    print(dataloaded)
    if (dataloaded):
        print("proceso con archivo")
        # Normalization of the values
        number_pods= 10
        file_descriptors= 300
        receive_packets=3434044
        transmit_packets=234234
        dropped_packets= 212
        cpu_usage_seconds= 2
        cpu_throttled_seconds= 3
        memory_working_bytes=345345345
        memory_usage_bytes= 300
        score = (1  - (float(dropped_packets)/number_pods) - float(cpu_throttled_seconds)) / number_pods
        
        norm_number_pods = normal (number_pods,0,200)
        norm_file_descriptors = normal (float(file_descriptors),0,1000)
        norm_receive_packets = normal (float(receive_packets),0,100000)
        norm_transmit_packets = normal (float(transmit_packets),0,100000)
        norm_dropped_packets = normal (float(dropped_packets),0,1000)
        norm_cpu_usage_seconds = normal (float(cpu_usage_seconds),0,50)
        norm_cpu_throttled_seconds = normal (float(cpu_throttled_seconds),0,50)
        norm_memory_working_bytes = normal (float(memory_working_bytes),0,100000000)
        norm_memory_usage_bytes = normal (float(memory_usage_bytes),0,1000)
        info = {"vector_observations": [norm_number_pods,norm_file_descriptors,norm_receive_packets, norm_transmit_packets, 
            norm_dropped_packets, norm_cpu_usage_seconds, norm_cpu_throttled_seconds, norm_memory_working_bytes,
            norm_memory_usage_bytes] ,
            "rewards": [float(score)], "local_done" : [False]}
           
        return info
    config.load_kube_config()
    apps_api = client.AppsV1Api()
    deployment = client.V1Deployment()
    deployment.api_version = "apps/v1"
    deployment.kind = "Deployment"
    deployment.metadata = client.V1ObjectMeta(name="httpdia")
    name = "httpdia"
    spec = client.V1DeploymentSpec(
        selector=client.V1LabelSelector(match_labels={"app":"httpdia"}),
        template=client.V1PodTemplateSpec(),
    )
    container = client.V1Container(
        image="httpd",
        resources = {"limits": {"cpu":"500m"} , "requests": {"cpu":"200m"}},
        name=name, 
    )
    spec.template.metadata = client.V1ObjectMeta(
        name="httpdia",
        labels={"app":"httpdia"},
    )
    spec.template.spec = client.V1PodSpec(containers = [container])
    dep = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=spec,
    )
    dep.spec.replicas = initial_pods
    try:
        apps_api.create_namespaced_deployment(namespace="default", body=dep)
    except:
        error="Pod Existente"
    dep.spec.replicas = initial_pods
    changeddeploy= apps_api.replace_namespaced_deployment(name=name, namespace="default", body=dep)

    v1=client.CoreV1Api()

    prom = PrometheusConnect(url=serverprometheus, disable_ssl=True)
    strQuery='sum(rate(container_file_descriptors{pod=~"httpdia[^v]*", container!="POD", namespace="default", container ="httpdia"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    
    try:
        file_descriptors=resultado[0]["value"][1]
    except:
        print("Sin datos en file_descriptors")
        file_descriptors = "0"
    

    strQuery='sum(rate(container_network_receive_packets_total{pod=~"httpdia[^v]*", namespace="default",  interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    
    try:
        receive_packets=resultado[0]["value"][1]
    except:
        print("Sin datos en receive_packets")
        receive_packets = "0"
    
    strQuery='sum(rate(container_network_transmit_packets_total{pod=~"httpdia[^v]*", namespace="default" , interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    transmit_packets=resultado[0]["value"][1]

    strQuery='sum(rate(container_network_transmit_packets_dropped_total{namespace="default",pod="load-generator-jupyter",interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    dropped_packets=resultado[0]["value"][1]

    strQuery='sum(rate(container_cpu_usage_seconds_total{container_name!="POD",container!="POD" ,namespace="default" ,pod=~"httpdia[^v]*", }['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)

    try:
        cpu_usage_seconds=resultado[0]["value"][1]
    except:
        print("Sin datos en cpu_usage_seconds")
        cpu_usage_seconds = "0"
        
    

    strQuery='sum(rate(container_cpu_cfs_throttled_seconds_total{ namespace="default", pod=~"httpdia[^v]*" }['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    try:
        cpu_throttled_seconds=resultado[0]["value"][1]
    except:
        print("Sin datos en cpu_throttled_seconds")
        cpu_throttled_seconds = "0"

    
    
    

    strQuery='sum(rate(container_memory_working_set_bytes{ namespace="default", pod=~"httpdia[^v]*"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    memory_working_bytes=resultado[0]["value"][1]
    
    strQuery='count(container_memory_usage_bytes{container="httpdia", namespace="default"})'
    resultado = prom.custom_query(query=strQuery)

    try:
        memory_usage_bytes=resultado[0]["value"][1]
    except:
        print("Sin datos en memory_usage_bytes")
        memory_usage_bytes = "0"

        
    
    
    ret=v1.list_namespaced_pod(namespace,watch=False)
    pods=ret.items
    pods_names=[pod.metadata.name for pod in pods]
    number_pods= 0
    for pod in pods_names:
        if (pod.find("httpdia")>-1):
            number_pods = number_pods+1
    score = (1  - (float(dropped_packets)/number_pods) - float(cpu_throttled_seconds)) / number_pods
    
    # Normalization of the values
    norm_number_pods = normal (number_pods,0,200)
    norm_file_descriptors = normal (float(file_descriptors),0,1000)
    norm_receive_packets = normal (float(receive_packets),0,100000)
    norm_transmit_packets = normal (float(transmit_packets),0,100000)
    norm_dropped_packets = normal (float(dropped_packets),0,1000)
    norm_cpu_usage_seconds = normal (float(cpu_usage_seconds),0,50)
    norm_cpu_throttled_seconds = normal (float(cpu_throttled_seconds),0,50)
    norm_memory_working_bytes = normal (float(memory_working_bytes),0,100000000)
    norm_memory_usage_bytes = normal (float(memory_usage_bytes),0,1000)
    
    info = {"vector_observations": [norm_number_pods,norm_file_descriptors,norm_receive_packets, norm_transmit_packets, 
            norm_dropped_packets, norm_cpu_usage_seconds, norm_cpu_throttled_seconds, norm_memory_working_bytes,
            norm_memory_usage_bytes] ,
            "rewards": [float(score)], "local_done" : [False]}
           
    return info
    
def description():
    print("Este módulo tiene 3 funciones: ")
    print("\t- la que muestra la descripción del módulo")
    print("\t- la que suma los números que introduzcamos por parámetro")
    print("\t- la que multiplica los números que introduzcamos por parámetro")

def check_kuber_prometheus(lapso,namespace,serverprometheus):
    config.load_kube_config()
    v1=client.CoreV1Api()
    prom = PrometheusConnect(url=serverprometheus, disable_ssl=True)
    strQuery='sum(rate(container_file_descriptors{pod=~"httpdia[^v]*", container!="POD", namespace="default", container ="httpdia"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    file_descriptors=resultado[0]["value"][1]

    strQuery='sum(rate(container_network_receive_packets_total{pod=~"httpdia[^v]*", namespace="default",  interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    receive_packets=resultado[0]["value"][1]

    strQuery='sum(rate(container_network_transmit_packets_total{pod=~"httpdia[^v]*", namespace="default" , interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    transmit_packets=resultado[0]["value"][1]

    strQuery='sum(rate(container_network_transmit_packets_dropped_total{namespace="default",pod="load-generator-jupyter",interface="eth0"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    dropped_packets=resultado[0]["value"][1]

    strQuery='sum(rate(container_cpu_usage_seconds_total{container_name!="POD",container!="POD" ,namespace="default" ,pod=~"httpdia[^v]*", }['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    cpu_usage_seconds=resultado[0]["value"][1]

    strQuery='sum(rate(container_cpu_cfs_throttled_seconds_total{ namespace="default", pod=~"httpdia[^v]*" }['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    cpu_throttled_seconds=resultado[0]["value"][1]

    strQuery='sum(rate(container_memory_working_set_bytes{ namespace="default", pod=~"httpdia[^v]*"}['+lapso+']))'
    resultado = prom.custom_query(query=strQuery)
    memory_working_bytes=resultado[0]["value"][1]
    
    strQuery='count(container_memory_usage_bytes{container="httpdia", namespace="default"})'
    resultado = prom.custom_query(query=strQuery)
    memory_usage_bytes=resultado[0]["value"][1]
    
    ret=v1.list_namespaced_pod(namespace,watch=False)
    pods=ret.items
    pods_names=[pod.metadata.name for pod in pods]
    number_pods= 0
    for pod in pods_names:
        if (pod.find("httpdia")>-1):
            number_pods = number_pods+1

    score = (1  - (float(dropped_packets)/number_pods) - float(cpu_throttled_seconds)) / number_pods
    
    formatted_pods = "{:.2f}".format(float(number_pods))
    formatted_file_descriptors = "{:.2f}".format(float(file_descriptors))
    formatted_receive_packets = "{:.2f}".format(float(receive_packets))
    formatted_transmit_packets = "{:.2f}".format(float(transmit_packets))
    formatted_dropped_packets = "{:.2f}".format(float(dropped_packets))
    formatted_cpu_usage_seconds = "{:.2f}".format(float(cpu_usage_seconds))
    formatted_cpu_throttled_seconds = "{:.2f}".format(float(cpu_throttled_seconds))
    formatted_memory_working_bytes = "{:.2f}".format(float(memory_working_bytes))
    formatted_memory_usage_bytes = "{:.2f}".format(float(memory_usage_bytes))
    formatted_score = "{:.5f}".format(float(score))
    
    
    print("Pods:"+formatted_pods+" File:"+ formatted_file_descriptors+" Rece:"+ formatted_receive_packets+" Trans:"+ formatted_transmit_packets + 
     " Drop:"+ formatted_dropped_packets+" CPUSec:"+ formatted_cpu_usage_seconds+ " CPUThroSec:"+formatted_cpu_throttled_seconds
     + " Mem_Bytes:"+ formatted_memory_working_bytes +" Usage_Mem:"+formatted_memory_usage_bytes+"\n Score:" + formatted_score )
