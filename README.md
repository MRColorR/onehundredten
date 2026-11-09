# onehundredten

<!-- Project README scaffold: https://github.com/MRColorR/project-template -->

**Explore a cloud-bursting proof of concept built with K3s and two OpenStack clouds.**

[**🚀 Explore the proof of concept**](#getting-started) · [📚 Documentation](#documentation) · [🫶 Support](#support)

**Leave a star ⭐ if you like this project 🙂 Thank you!**

## Overview

In this project we produce a working PoC of a vendor-agnostic multi-cloud bursting solution using two openstack clouds (devstack) and a multi cloud kubernetes cluster (K3s).

The example services we run are a simple website and an API used to compute the factorial of the number entered on the website by the user. The computation is executed by the cluster and both services have their horizontal auto scaler and thanks to the labels defined on the nodes the services will be executed on the first cloud (on-prem) until no more resources are available. Then the autoscaler proceeds to burst the workload also on the second cloud (public/secondary cloud) realizing the cloud bursting function. Additionnaly in the blueprint we defined several policies for supporting auto backups/rollback of the services and rolling updates.

---

## Getting started

<a name="prerequisites"></a>

### Prerequisites

- To run the project locally you need an hypervisor and two VMs with nested virtualization capabilities and network connectivity with one or more NIC possibly with static IP adresses.
- Recomended VMs resources: 6 vCores, 12 GB RAM, 128 GB VHDD | Minimum VMs resources: 4 vCores, 8 GB RAM, 32 GB VHDD

---

<a name="how-to-run"></a>

### How to run

- Get the latest code from this repo
- Then setup all the components: 
  - Configure and deploy the Openstack clouds (one per VM)
    - Use the setupStackUser script to setup a user with paswordless sudo running: 
      
      ```curl https://raw.githubusercontent.com/MRColorR/onehundredten/master/openstack/setupStackUser.sh > setupStackUser.sh && sudo chmod +x setupStackUser.sh && ./setupStackUser.sh```
    - Now impersonate the stack user using: 
      
      ```sudo -u stack -i``` 
    - Run the devstack guided setup provided using: 
      
      ```sudo apt install git -y && git clone https://github.com/MRColorR/onehundredten && sudo chmod +x $PWD/onehundredten/openstack/setupAIO.sh && ./onehundredten/openstack/setupAIO.sh```
      - Notice: during these steps to make the cloud instances and cluster instances pingable on the local network you should use the same IP addresses space of your undelying network.
    - Repeat the steps on the other VM, now you have two clouds with two instances runing inside the cloud. You can check their assigned floating IPs using: 
      
      ``` source /devstack/openrc admin admin``` and then ```openstack server list```.
    - It's time to install the K3s cluter on the master node. and join the worker nodes: 
      - SSH into the master node using
        
        ```ssh -i kubekey debian@<masterNodeFloatingIP>``` 
      - Now inside the master node issue the following command: 
        
        ```sudo apt install curl -y && curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--node-external-ip <masterFloatingIP> --flannel-external-ip" sh -```
      - Retrieve from the master the cluster token that will allow us to add the worker nodes: 
        
        ```sudo cat /var/lib/rancher/k3s/server/node-token```
      - Now SSH into the workers node and make them join the cluster running the following command: 
        
        ```sudo apt install curl -y && curl -sfL https://get.k3s.io | K3S_URL=<masterFloatingIP>:6443 K3S_TOKEN="token" INSTALL_K3S_EXEC="--node-external-ip <workerFloatingIP>" sh -```
    - You can check on the master node if all is connected and running using: ```sudo kubectl get nodes``` and ```sudo kubectl top nodes```
    - Add labels to each node runing:
      
      ```sudo kubectl label nodes master1a worker1a node-type=on-prem ``` and ```sudo kubectl label nodes worker2b worker2b1 node-type=burst ```
    - To complete the project deploy the website and the factorial API using:
        
      ``` curl https://raw.githubusercontent.com/MRColorR/onehundredten/master/k8s-www-api-blueprint.yaml > k8s-www-api-blueprint.yaml && sudo kubectl apply -f k8s-www-api-blueprint.yaml ``` 
    - You should be able to reach the website from each node on port :30080 and ask for the factorial of a number you can also contatc directly the APi on port 30500

---

## Documentation

<a name="testing-and-getting-metrics"></a>

### Testing and getting metrics

You can get metrics about the deployment using the K8s_stats.py script in the K8s-metrics folder and while the scripts is getting and recording the metrics you can run the load test using Jmeter.

#### K8s Python Client
  - Start the metrics recording using 

    ```python k8s_stats.py --deployment_name=factorial-api --observation_time=480 --append``` 
    (check the code for optional flags you can use to customize its behaviour)
  - While the K8s Python Client is running , start the load test using Jmeter
#### JMeter load testing
  - Jmeter here is used for load tests, see the jmeter file. After downloading jmeter latest release you can run it using: 
    
    ```.\<apache-jmeter-x.yFolder>\bin\jmeter.bat -f -n -t '.\HTTP Request www and api 2.jmx' -l .\Report_HTML<hpa_tresh>\results.csv -e -o .\Report_HTML<hpa_tresh>\```

#### Boxplot and images genetation
  - Just run the draw_metrics.py to generate an SVG file containing the graphical rappresentation of the metrics recorded by the k8s_stats.py:

    ```python .\draw_metrics.py``` 
    (check the code for optional flags you can use to customize its behaviour)

## Contributing

Ideas, bug reports, documentation fixes and focused changes are welcome through this repository's collaboration channels.

Please include enough context to reproduce a problem or review a change.

## Support

**🫶 Support the project**

Your contributions are vital in helping to sustain the development of open-source projects and tools made freely available to everyone. If you find value in my work and wish to show your support, kindly consider making a donation.

☕ [Support me on Ko-fi](https://ko-fi.com/mrcolorrain) · 💛 [Donate with cryptocurrency](https://github.com/MRColorR/MRColorR/blob/main/SUPPORTERS.md#cryptocurrency-wallets)

Thank you for helping me keep building and sharing! 🙏 See the [supporter directory](https://github.com/MRColorR/MRColorR/blob/main/SUPPORTERS.md).

## License

A project license has not been declared in this repository. Contact the maintainer about reuse permissions.
