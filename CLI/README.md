# Proyecto No 1: CLI Client

# 1. Objetivo

Diseñar e implementar un sistema de archivos distribuido minimalista.

---

# 2. Aspectos solucionados y no solucionados

- [x]  Comando ‘get file’ funcional.
- [x]  Comando ‘put file’ funcional.
- [x]  Comando ‘list files’ funcional.
- [x]  Comando ‘search file’ funcional.
- [x]  Comando ‘salir’ funcional.

---

# 3. Información general del diseño

## Sobre los servicios

En esta sección, se explican los servicios implementados para dar solución al reto propuesto, explicado en la sección: 1. Objetivo.

| Nombre del servicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| Command-line Interface (CLI) Client | Permite a los usuarios dar instrucciones e interactuar con el Name Node y los Data Nodes. | local |

---

# 4. Ambiente de desarrollo

En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto. Además, se exploran aspectos clave de la "Configuración de Parámetros del Proyecto", destacando cómo ajustar y personalizar los elementos esenciales que guiarán el desarrollo y funcionamiento del software.

## Estructura del código

A continuación, exploraremos la disposición de archivos y carpetas en nuestro proyecto. A continuación, se muestra una visión general de cómo se organizan los archivos y las subcarpetas en relación con el directorio principal del proyecto.

```
CLI
├── FileServices_pb2.py
├── FileServices_pb2.pyi
├── FileServices_pb2_grpc.py
├── actions.py
├── cli.py
├── file77.txt
├── grpc_client.py
├── loader.py
├── main.py
├── protobufs
│   ├── proto
│   │   └── FileServices.proto
│   └── python
├── proxy_client.py
└── questions.py
└── requirements.txt
```

## Configuración de parámetros del proyecto

Para la configuración de los parámetros del proyecto utilizamos un enfoque basado en variables de entorno. Esto nos brinda la flexibilidad necesaria para adaptar nuestro proyecto a diferentes entornos.

A continuación se muestra el contenido del archivo de configuraciones: ‘.env’. Este archivo controla los aspectos esenciales de la aplicación.

```
NAME_NODE_HOST=http://3.234.34.168
NAME_NODE_PORT=8080
```

## Paquetes y dependencias

Las dependencias requeridas para la correcta ejecución del software desarrollado son las siguientes:

```python
ansicon==1.89.0
blessed==1.20.0
certifi==2023.7.22
charset-normalizer==3.3.0
colorama==0.4.6
grpcio==1.59.0
grpcio-tools==1.59.0
idna==3.4
inquirer==3.1.3
jinxed==1.2.0
protobuf==4.24.4
python-dotenv==1.0.0
python-editor==1.0.4
readchar==4.0.5
requests==2.31.0
six==1.16.0
tabulate==0.9.0
tqdm==4.66.1
urllib3==2.0.6
wcwidth==0.2.8
```

---

# 5. Ambiente de ejecución

## Arquitectura general

En la presente sección se mostrara la arquitectura de referencia recomendada para el proyecto, un primer planteamiento de esta arquitectura, y finalmente, la arquitectura final y los servicios de Amazon Web Services (AWS) y Google Cloud Platform (GCP) empleados para el despliegue eficiente y escalable.

![Arquitectura de referencia recomendad para el proyecto.](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/arquiReferencia.png)

Arquitectura de referencia recomendad para el proyecto.

![Primer planteamiento de la arquitectura para el proyecto.](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/main/docs/arquiPrimerPlanteo.jpg)

Primer planteamiento de la arquitectura para el proyecto.

![Arquitectura final; servicios de AWS y GCP usados.](https://raw.githubusercontent.com/jdprietom03/proyecto1-topicos/68237a0d3fd613aefead4a90fe26735f2076ebe6/docs/arquiFinal.svg)

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
cd proyecto1-topicos/CLI

#instalando librerias necesarias
pip install -r requirements.txt
echo "[x] Librerias necesarias instaladas"
```

### Ejecución del programa

Finalmente podremos ejecutar el programa.

```bash
python3 main.py
```

## Acciones

Los siguientes son los comandos disponibles a usar en el CLI y las acciones permitidas por los mismos.  

### [GET] - Traer archivo (command)

Copia un archivo del Data Node al local.

Nombre

**Archivo a descargar**

Descripción

Dirección (PATH) remoto donde se encuentra el archivo a copiar del Data Node.

Tipo de dato

*string*

### [PUT] - Subir Archivo (command)

Agregar un archivo del local a un Data Node.

Nombre

**Archivo a subir**

Descripción

Dirección local donde se encuentra el archivo a agregar al Data Node.

Tipo de dato

*string*

### [LIST] - Listar archivos (command)

Listar todos los archivos presentes en los Data Nodes.

### [SEARCH] - Buscar archivos (command)

Buscar un archivo en todos los Data Nodes bajo una expresión regular (regex).

Nombre

**Expresión a buscar**

Descripción

Expresión regular para la búsqueda del archivo.

Tipo de dato

*string*

### [SALIR] - Salir

Salir de la linea de comandos.