from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User, Client
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.generic.network import Firewall
from diagrams.programming.framework import Fastapi, Spring, Vue
from diagrams.onprem.container import Docker

with Diagram("Logical Architecture", direction="LR", filename="../images/logical_architecture"):
    practitioner = User("Practitioner") 

    with Cluster("On Premise"):
        browser = Client("Browser")
        konnektor = Server("Konnektor")
        practitioner >> browser >> konnektor
        iag = Firewall("Firewall")
    
    with Cluster("TI") as ti:
        spa1 = Server("Webserver")

    with Cluster("Internet"):
        spa2 = Server("Webserver")

    browser >> iag >> spa2
    konnektor >> iag >> spa1

with Diagram("Proof of Concept Architecture", filename="../images/poc_architecture"):
    browser = Client("Browser")
    with Cluster("Docker Compose"):
        cors_proxy = Fastapi("CORS Proxy")
        conlibre = Docker("Konnektor Emulator")
        cors_ui = Vue("CORS UI Demo")

        cors_proxy >> conlibre
        cors_ui

    konnektor = Server("Konnektor")

    cors_proxy >> Edge(style="dotted") >> konnektor

    browser >> Edge(label="http://localhost:8080") >> cors_ui
    browser >> Edge(label="http://localhost/8000") >> cors_proxy
