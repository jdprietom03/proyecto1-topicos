# Proyecto No 1: Data Nodes

# 1. Objetivo

Diseñar e implementar un sistema de archivos distribuido minimalista.

---

# 2. Aspectos solucionados y no solucionados

- [x]  Operación ‘list files’ funcional.
- [x]  Operación ‘find file’ funcional.
- [x]  Operación ‘get file’ funcional.
- [x]  Operación ‘put files’ funcional.
- [x]  Un archivo debe de estar en al menos dos (2) Data Nodes.
- [ ]  Puesta en marcha de Data Node Replica.
- [ ]  Aquel Data Node que reciba un archivo del cliente tendrá la responsabilidad de transferirlo al Data Node replica.

---

# 3. Información general del diseño

## Sobre los servicios

En esta sección, se explican los servicios implementados para dar solución al reto propuesto, explicado en la sección: 1. Objetivo.

| Nombre del servicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| Data Node 1 | Almacena los archivos subidos por los clientes; notifica al Name Node en caso de que un nuevo archivo haya sido creado.  | 3.223.88.22: 50051 & 80 |
| Data Node 2 | Almacena los archivos subidos por los clientes; notifica al Name Node en caso de que un nuevo archivo haya sido creado.  | 44.208.106.154: 50051 & 80 |

---

# 4. Ambiente de desarrollo

En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto. Además, se exploran aspectos clave de la "Configuración de Parámetros del Proyecto", destacando cómo ajustar y personalizar los elementos esenciales que guiarán el desarrollo y funcionamiento del software.

## Estructura del código

A continuación, exploraremos la disposición de archivos y carpetas en nuestro proyecto. A continuación, se muestra una visión general de cómo se organizan los archivos y las subcarpetas en relación con el directorio principal del proyecto.

```
DATANODE
├── README.md
├── assets
│   ├── 123.txt
│   ├── file1.txt
│   ├── file2.txt
│   └── test.txt
└── src
    ├── IndexClient.py
    ├── README.md
    ├── client.py
    ├── compile.py
    ├── config
    ├── main.py
    ├── protobufs
    │   ├── __init__.py
    │   ├── proto
    │   │   ├── Add2Index.proto
    │   │   └── FileServices.proto
    │   └── python
    │       ├── Add2Index_pb2.py
    │       ├── Add2Index_pb2.pyi
    │       ├── Add2Index_pb2_grpc.py
    │       ├── FileServices_pb2.py
    │       ├── FileServices_pb2.pyi
    │       ├── FileServices_pb2_grpc.py
    │       └── __init__.py
    ├── requirements.txt
    └── server
        ├── __init__.py
        ├── common
        │   ├── __init__.py
        │   └── services.py
        └── grpc
            └── server.py
```

## Configuración de parámetros del proyecto

Para la configuración de los parámetros del proyecto utilizamos un enfoque basado en variables de entorno. Esto nos brinda la flexibilidad necesaria para adaptar nuestro proyecto a diferentes entornos.

A continuación se muestra el contenido de los archivos de configuraciones: ‘.config’ y ‘.env’. Estos archivos controlan los aspectos esenciales de la aplicación.

```
[PATHS]
ASSETS_DIR=./../assets
PROTO_DIR = ./protobufs/proto
PROTO_FILE_DATA_NODE = ./protobufs/proto/FileServices.proto
PROTO_FILE_NAME_NODE = ./protobufs/proto/Add2Index.proto
OUTPUT_DIR = ./protobufs/python
[RETRY]
RETRIES_ADD_IP = 10
CHUNK_SIZE = 1024
```

```
GRPC_HOST=127.0.0.1:50051
```

## Paquetes y dependencias

Las dependencias requeridas para la correcta ejecución del software desarrollado son las siguientes:

```python
grpcio==1.57.0
grpcio-tools==1.57.0
protobuf==4.24.2
pika==1.2.0
flask==2.0.1
flask-restful==0.3.9
python-dotenv==0.17.1
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
git clone https://github.com/jdprietom03/proyecto1-topicos
echo "[x] Repositorio de codigo clonado"
```

### Instalación de dependencias

Nos dirigiremos a la carpeta con el código correspondiente y crearemos un entorno virtual, accederemos a el e instalaremos las librerías y dependencias correspondientes.

```bash
#dirigiendome al directorio de codigo
cd proyecto1-topicos/DATANODE/src

#instalando librerias necesarias
pip install -r requirements.txt
echo "[x] Librerias necesarias instaladas"
```

### Ejecución del programa

Finalmente podremos ejecutar el programa.

```bash
python3 main.py
```

## Sobre el Streaming de archivos
Originalmente, el sistema usaba Protocol Buffers sin streaming para la transferencia de archivos a través de gRPC. Esta implementación presentaba limitaciones significativas:

- Límite de tamaño: gRPC, en muchas implementaciones, tiene un límite predeterminado de 4MB por mensaje. Esto significa que, sin streaming, cualquier archivo que superara este tamaño no podría ser transferido sin ajustar este límite, lo que no es siempre deseable.
- Eficiencia y Uso de Memoria: Transferir archivos grandes en un solo bloque puede ser ineficiente y consumir una cantidad significativa de memoria, ya que todo el archivo debe cargarse en memoria antes de ser enviado.
- Tiempo de Respuesta: Enviar un archivo grande de una sola vez podría aumentar el tiempo de respuesta, ya que el receptor tendría que esperar a que se complete toda la transferencia antes de poder procesarla.

**Beneficios del Streaming**

Al adoptar streaming en gRPC, superamos estas limitaciones:
- Manejo de Archivos Grandes: Al dividir los archivos en chunks, podemos transferir archivos de cualquier tamaño, sin estar restringidos por el límite de 4MB.
- Eficiencia: El streaming permite una transferencia más eficiente, reduciendo el uso de memoria y permitiendo que el receptor procese los datos a medida que llegan.
- Resiliencia: El streaming mejora la capacidad de manejar interrupciones y reanudar transferencias.

## Acciones

Los siguientes son los endpoints disponibilizados por los Data Nodes y las acciones permitidas por los mismos.  

### [gRPC] ListFiles (service)

Listar todos los archivos presentes en un Data Node.

<aside>
🌐 [gRPC] 3.223.88.22:50051

</aside>

```python
import grpc
from google.protobuf.empty_pb2 import Empty
import FileService_pb2 as FileServiceStub
import FileService_pb2_grpc as FileServices_pb2_grpc

address = "3.223.88.22:50051"
channel = grpc.insecure_channel(address) 
stub = FileServices_pb2_grpc.FileServiceStub(channel)

request = Empty()
response = stub.ListFiles(request)
```

### [gRPC] FindFile (service)

Buscar un archivo en un Data Node.

<aside>
🌐 [gRPC] 3.223.88.22:50051

</aside>

```python
import grpc
import FileService_pb2 as FileServiceStub
import FileService_pb2_grpc as FileServices_pb2_grpc

address = "3.223.88.22:50051"
channel = grpc.insecure_channel(address) 
stub = FileServices_pb2_grpc.FileServiceStub(channel)

file_name = "123.txt"
request = FileServicesStub.FileRequest(file_name)
response = stub.FindFile(request)
```

Nombre

**file_name**

Descripción

Nombre del archivo a buscar.

Tipo de dato

*string*

### [gRPC] GetFile (service)

`Ahora soporta Streaming!`

Descargar un archivo remoto ubicado en un Data Node en local.

<aside>
🌐 [gRPC] 3.223.88.22:50051

</aside>

```python
import grpc
import FileService_pb2 as FileServiceStub
import FileService_pb2_grpc as FileServices_pb2_grpc

address = "3.223.88.22:50051"
channel = grpc.insecure_channel(address) 
stub = FileServices_pb2_grpc.FileServiceStub(channel)

file_path = "123.txt"
request = FileServicesStub.FileRequest(file_name)
try:
	response = {
		"data": stub.GetFile(request),
		"status": 200
	}
except:
	response = {
		"status":500
	}
```

Nombre

**file_path**

Descripción

Ruta al archivo remoto que se encuentra dentro del Data Node.

Tipo de dato

*string*

### [gRPC] PutFile (service)

`Ahora soporta Streaming!`

Subir un archivo local a un Data Node.

<aside>
🌐 [gRPC] 3.223.88.22:50051

</aside>

```python
import grpc
import FileService_pb2 as FileServiceStub
import FileService_pb2_grpc as FileServices_pb2_grpc

address = "3.223.88.22:50051"
channel = grpc.insecure_channel(address) 
stub = FileServices_pb2_grpc.FileServiceStub(channel)

file_path = "123.txt"
request = FileServicesStub.FileContent(file_name, data=bytes(data))
response = stub.PutFile(request)
```

Nombre

**file_path**

**data**

Descripción

Ruta al archivo local a enviar al Data Node.

Contenido del archivo local a enviar al Data Node en bytes.

Tipo de dato

*string*

*bytes*
