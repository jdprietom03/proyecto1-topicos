# Proyecto No 1: Name Node

# 1. Objetivo

Diseñar e implementar un sistema de archivos distribuido minimalista.

---

# 2. Aspectos solucionados y no solucionados

- [x]  Operación ‘list’ funcional.
- [x]  Operación ‘search’ funcional.
- [x]  Operación ‘get’ funcional.
- [x]  Operación ‘put’ funcional.
- [x]  Al solicitar un archivo el Name Node deberá de realizar un acercamiento de round robin hacia los Data Nodes.
- [x]  Puesta en marcha de Name Node Replica.
- [ ]  Implementación de método GETBATCH para poder descargar mas de un archivo.

---

# 3. Información general del diseño

## Sobre los servicios

En esta sección, se explican los servicios implementados para dar solución al reto propuesto, explicado en la sección: 1. Objetivo.

| Nombre del servicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| Name Node | Recibe y resuelve las solicitudes de los clientes, busca en el índice de archivos de los Data Nodes el archivo solicitado por el cliente y le redirige al Data Node que lo almacena; administra el índice de archivos de los Data Nodes.     | 3.234.34.168: 8080 & 80 |

---

# 4. Ambiente de desarrollo

En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto. Además, se exploran aspectos clave de la "Configuración de Parámetros del Proyecto", destacando cómo ajustar y personalizar los elementos esenciales que guiarán el desarrollo y funcionamiento del software.

## Estructura del código

A continuación, exploraremos la disposición de archivos y carpetas en nuestro proyecto. A continuación, se muestra una visión general de cómo se organizan los archivos y las subcarpetas en relación con el directorio principal del proyecto.

```
nameNode
├── client
│   ├── grpc
│   │   ├── contracts
│   │   │   ├── nameNode_pb2.py
│   │   │   ├── nameNode_pb2.pyi
│   │   │   └── nameNode_pb2_grpc.py
│   │   └── grpc_client.py
│   └── http
│       ├── list_client.py
│       ├── put_client.py
│       └── search_client.py
├── deploy
│   └── init.sh
├── requirements.txt
└── src
    ├── creds
    │   └── gs_creds.json
    ├── data
    │   └── index.csv
    ├── main.py
    ├── services
    │   ├── configs
    │   │   ├── contracts
    │   │   │   ├── nameNode_pb2.py
    │   │   │   ├── nameNode_pb2.pyi
    │   │   │   └── nameNode_pb2_grpc.py
    │   │   └── proto
    │   │       └── nameNode.proto
    │   ├── grpc_service.py
    │   ├── http_api.py
    │   └── name_node.py
    └── utils
        ├── env_vars.py
        └── index_table.py
```

## Configuración de parámetros del proyecto

Para la configuración de los parámetros del proyecto utilizamos un enfoque basado en variables de entorno. Esto nos brinda la flexibilidad necesaria para adaptar nuestro proyecto a diferentes entornos.

A continuación se muestra el contenido del archivo de configuraciones: ‘env_vars.py’. Este archivo actúa como un mapa que controla los aspectos esenciales de la aplicación.

```python
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Admin\\Desktop\\nameNode\\src\\creds\\gs_creds.json"
os.environ["PATH_2_GS_INDEX"] = "gs://data-nodes-index/index.csv" 
os.environ["OK-status"] = "200" #int
os.environ["ERROR-status"] = "400" #int

### SERVICES

os.environ["HTTP_HOST"] = "0.0.0.0"
os.environ["HTTP_PORT"] = "80" #int
os.environ["GRPC_PORT"] = "[::]:50000"
```

## Paquetes y dependencias

Las dependencias requeridas para la correcta ejecución del software desarrollado son las siguientes:

```
aiohttp==3.8.5
aiosignal==1.3.1
async-timeout==4.0.3
attrs==23.1.0
blinker==1.6.2
cachetools==5.3.1
certifi==2023.7.22
charset-normalizer==3.3.0
click==8.1.7
colorama==0.4.6
decorator==5.1.1
Flask==3.0.0
frozenlist==1.4.0
fsspec==2023.9.2
gcsfs==2023.9.2
google-api-core==2.12.0
google-auth==2.23.2
google-auth-oauthlib==1.1.0
google-cloud-core==2.3.3
google-cloud-storage==2.11.0
google-crc32c==1.5.0
google-resumable-media==2.6.0
googleapis-common-protos==1.60.0
grpcio==1.59.0
grpcio-tools==1.59.0
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
multidict==6.0.4
numpy==1.26.0
oauthlib==3.2.2
pandas==2.1.1
protobuf==4.24.4
pyasn1==0.5.0
pyasn1-modules==0.3.0
python-dateutil==2.8.2
pytz==2023.3.post1
requests==2.31.0
requests-oauthlib==1.3.1
rsa==4.9
six==1.16.0
tzdata==2023.3
urllib3==2.0.6
Werkzeug==3.0.0
yarl==1.9.2
```

---

# 5. Ambiente de ejecución

## Arquitectura general

En la presente sección se mostrara la arquitectura de referencia recomendada para el proyecto, un primer planteamiento de esta arquitectura, y finalmente, la arquitectura final y los servicios de Amazon Web Services (AWS) y Google Cloud Platform (GCP) empleados para el despliegue eficiente y escalable.

![Arquitectura de referencia recomendad para el proyecto.](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/arquiReferencia.png)

Arquitectura de referencia recomendad para el proyecto.

![Primer planteamiento de la arquitectura para el proyecto.](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/arquiPrimerPlanteo.jpg)

Primer planteamiento de la arquitectura para el proyecto.

![Arquitectura final; servicios de AWS y GCP usados.](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/31db7090940f74446dd0fad36da786631e342f19/docs/arquiFinal.svg)

Arquitectura final; servicios de AWS y GCP usados.

## Guía de uso

La siguiente guía brindará los pasos a seguir para un correcto funcionamiento y ejecución del software.

### Instalando requisitos previos

Primeramente deberemos de instalar los programas necesarios para la ejecución del proyecto; se instalarán Git y Python y se clonará el repositorio que contiene el código correspondiente.

```bash
#instalando git
sudo apt-get install git
echo "[x] Git instalado"

#instalando python
sudo apt install python3
echo "[x] Python instalado"

#clonando repositorio del codigo
git clone https://github.com/spuertaf/spuertaf-st0263.git
echo "[x] Repositorio de codigo clonado"
```

### Instalación de dependencias

Nos dirigiremos a la carpeta con el código correspondiente y crearemos un entorno virtual, accederemos a el e instalaremos las librerías y dependencias correspondientes.

```bash
#dirigiendome al directorio de codigo
cd spuertaf-st0263 (!) #actualizar ruta

#instalando librerias necesarias
sudo pip install -r requirements.txt
echo "[x] Librerias necesarias instaladas"
```

### Ejecución del programa

Finalmente podremos ejecutar el programa.

```bash
sudo python3 -m src.main
```

## Acciones

Los siguientes son los endpoints disponibilizados por el Name Node y las acciones permitidas por los mismos.  

### [GET] Get (endpoint)

Copia un archivo del Data Node al cliente.

<aside>
🌐 [GET] http://3.234.34.168:8080/get

</aside>

```python
import requests

url = "http://3.234.34.168:8080/get"

body = {
    "payload" : "123.*"
}

response = requests.get(url, json=body)

print(response.text)
```

![Untitled](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/nameNode/postmanGet.png)

Nombre

**payload**

Descripción

Expresión regular para la búsqueda del archivo.

Tipo de dato

*string*

### [GET]  Search (endpoint)

Buscar un archivo en todos los data nodes bajo una expresión regular (regex).

<aside>
🌐 [GET] http://3.234.34.168:8080/search

</aside>

```python
import requests

url = "http://3.234.34.168:8080/search"

body = {
    "payload" : "123.*"
}

response = requests.get(url, json=body)

print(response.text)
```

![Untitled](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/nameNode/postmanSearch.png)

Nombre

**payload**

Descripción

Expresión regular para la búsqueda del archivo.

Tipo de dato

*string*

### [GET] List (endpoint)

Listar todos los archivos presentes en los data nodes.

<aside>
🌐 [GET] http://3.234.34.168:8080/list

</aside>

```python
import requests

url = "http://3.234.34.168:8080/list"

body = {
    "payload" : "."
}

response = requests.get(url, json=body)

print(response.text)
```

![Untitled](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/nameNode/postmanList.png)

Nombre

**payload**

Descripción

N/A

Tipo de dato

*string*

### [PUT] Put (endpoint)

Agregar un archivo a un data node.

<aside>
🌐 [PUT] http://3.234.34.168:8080/put

</aside>

```python
import requests

url = "http://3.234.34.168:8080/put"

body = {
    "payload" : "/data/customer.txt"
}

response = requests.get(url, json=body)

print(response.text)
```

![Untitled](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/nameNode/postmanPut.png)

Nombre

**payload**

Descripción

Dirección local donde se encuentra el archivo a agregar al data node.  

Tipo de dato

*string*

### [gRPC] add_2_index (service)

Agregar al índice de archivos del name node una nueva ruta a un archivo creado en un data node.

<aside>
🌐 [gRPC] 3.234.34.168:80

</aside>

```python
from .contracts import nameNode_pb2_grpc, nameNode_pb2

import grpc

grpc_connection = grpc.insecure_channel("3.234.34.168:80")
grpc_channel = nameNode_pb2_grpc.Add2IndexStub(grpc_connection) 
request = nameNode_pb2.add2IndexRequest(dataNodeIP="DataNode1", path2Add="path/to/txt/file.txt")
response = grpc_channel.add_2_index(request)
print(response)
```

Nombre

**dataNodeIP**

**path2Add**

Descripción

IP del data node al cual se le añadió un nuevo archivo.

Ruta de ubicación del archivo añadido dentro del data node.

Tipo de dato

*string*

*string*