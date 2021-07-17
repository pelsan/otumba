import time

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

class Pod:

	def __init__(self, namepod ,dockerimage ,namespace = "default", shell = "/bin/sh"):
	
		"""Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		"""
			
		self.namepod = namepod
		self.apiversion = "v1"
		self.kind = "Pod"
		self.dockerimage = dockerimage
		self.namespace = namespace        
		self.resp = None
		self.shell = shell

	def create(self):
	
		"""Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		"""
		config.load_kube_config()
		try:
			c = Configuration().get_default_copy()
		except AttributeError:
			c = Configuration()
			c.assert_hostname = False
		Configuration.set_default(c)
		core_v1 = core_v1_api.CoreV1Api()
		api_instance = core_v1
		try:
			self.resp = api_instance.read_namespaced_pod(name=self.namepod, namespace=self.namespace)
		except ApiException as e:
			if e.status != 404:
				print("Unknown error: %s" % e)
				exit(1)
		if not self.resp:
			print("Pod %s does not exist. Creating it..." + self.namepod)
			pod_manifest = {
				'apiVersion': 'v1',
				'kind': self.kind,
				'metadata': {
					'name': self.namepod
				},
				'spec': {
					'containers': [{
						'image': self.dockerimage,
						'name': 'sleep',
						"args": [
							"/bin/sh",
							"-c",
							"while true;do date;sleep 5; done"
						]
					}]
				}
			}
			self.resp = api_instance.create_namespaced_pod(body=pod_manifest, namespace=self.namespace)
			while True:
				self.resp = api_instance.read_namespaced_pod(name=self.namepod, namespace=self.namespace)
				if self.resp.status.phase != 'Pending':
					break
				time.sleep(1)
			print("Done.")

	def exec_command(self, strexec):

		core_v1 = core_v1_api.CoreV1Api()
		api_instance = core_v1
		print(strexec)
		self.resp = stream(api_instance.connect_get_namespaced_pod_exec, 
			self.namepod,
			self.namespace,
			command = self.shell,
			stderr=True, stdin=True,
			stdout=True, tty=False,
			_preload_content=False)
		self.resp.write_stdin(strexec + "\n")


