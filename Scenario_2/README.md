Scenario 2
Simple application Pod
docker pull pelsan/otumba-scn2:0.0.1

kubectl run podscen2 --image=pelsan/otumba-scn2:0.0.1 --port=5000
kubectl expose pod podscen2 --type=LoadBalancer --port=5000 --target-port=5000
minikube service podscen2


Configuring database

kubectl apply -f secret-dev.yaml
kubectl apply -f secret-pgadmin.yaml 
kubectl apply -f configmap-postgres-initbd.yaml
kubectl apply -f persistence-volume.yaml
kubectl apply -f persistence-volume-claim.yaml
kubectl apply -f deployment-postgres.yaml 
kubectl apply -f deployment-pgadmin.yaml
kubectl apply -f service-postgres.yaml
kubectl apply -f service-pgadmin.yaml 

obtain ip
minikube ip

for instance ip = 192.168.49.2
using web browser
http://192.168.49.2:30200 

user: admin@admin.com
pass: qwerty


add new server we can check port using
kubectl get svc postgres-service

the port is 30432 and ip is 192.168.49.2 

---Configuring database using service -------------
on pgadmin wepp application select "add new server"
general
name: postgresservice
connection 
host: 192.168.49.2
port: 30432
maintenance database: postgres
username: postgres
pass: qwerty

---Configuring database using pod -------------
--- user , database and pass is on configmap-postgres-initbd.yaml-----

for example
NAME               TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
postgres-service   NodePort   10.102.153.146   <none>        5432:30432/TCP   23m

general
name: postgrespod
connection
host: 10.102.153.146
port: 5432
maintenance database: billingapp_db
username: billingapp
pass: qwerty

can be exposed outside 
minikube service postgres-service