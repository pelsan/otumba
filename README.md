# Otumba

# Project: AI on Cloud Distributed Systems

### Introduction

This project, we train agents diferents scenarios in order to detect anomalies.
Scenario 1 Http Server
Scenario 2 Microservice + Database 


### Getting Started

The instructions are for to configurate the best scenario that i tested and needs less tricks that is on Ubuntu 20.04.2 LTS Linux , i tested it on windows 10 too and i will give the tricks needed in order to work  this project.

We have two parts
Core Instructions: The principal configuration that we need to have kubernetes, prometheus, jupyter notebook (machine learning with pytorch) and Instruction Scenarios: we configure the diferents scenarios ( simple web server,  web/mobile application, payments application)

### Core Instructions

Install and validate Anaconda, Jupyter, pytorch, otumba packages and other packages needed  [here](https://github.com/pelsan/otumba/blob/main/anaconda_otumba_install.txt)

Download the github project (git clone https://github.com/pelsan/otumba.git) 


Install and validate Docker [here](https://github.com/pelsan/otumba/blob/main/docker_install.txt)

Install and validate Kubernetes and minikube [here](https://github.com/pelsan/otumba/blob/main/kubernetes_install.txt)

Install and validate Prometheus [here](https://github.com/pelsan/otumba/blob/main/prometheus_install.txt)



Use the notebooks on "validate" folder to check installation and validate connection (check that otumba kernel is configured on your notebook files that are you using)

Linux: To open Jupyter Notebook:
	jupyter notebook

Windows: To open Jupyter Notebook:
	Menu - Anaconda - Jupyter


test_pytorch_packages.ipynb:  	validate Cuda/Pytorch/Otumba and others installed packages

test_kubernetes.ipynb			validate Kubernetes and Minikube from python

test_prometheus.ipynb			validate Prometheus from python
