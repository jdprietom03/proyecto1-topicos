# Proyecto No 1.

| Información |  |
| --- | --- |
| Materia | Tópicos especiales en Telemática |
| Curso | ST0263 |
| Estudiantes | Juan David Echeverri (mailto:jdecheverv@eafit.edu.co) |
|  | Juan Sebastián Guerra (mailto:jsguerrah@eafit.edu.co) |
|  | Juan David Prieto (mailto:jdprietom@eafit.edu.co) |
|  | Santiago Puerta (mailto:spuertaf@eafit.edu.co) |
| Profesor | Edwin Nelson Montoya Munera (mailto:emontoya@eafit.edu.co) |

# 1. Objetivo

Diseñar e implementar un sistema de archivos distribuido minimalista.

---

# 2. Aspectos solucionados y no solucionados

- [x]  La escritura de los archivos debe de ser directamente realizada entre el Cliente y el Data Node.
- [x]  La lectura de los archivos debe de ser directamente realizada entre el Cliente y el Data Node.
- [x]  Operación ‘list’ funcional.
- [x]  Operación ‘search’ funcional.
- [x]  Operación ‘get’ funcional.
- [x]  Operación ‘put’ funcional.
- [x]  Un archivo debe de estar en al menos dos (2) Data Nodes.
- [x]  Al solicitar un archivo el Name Node deberá de realizar un acercamiento de round robin hacia los Data Nodes.
- [x]  Puesta en marcha de Name Node Replica.
- [ ]  Puesta en marcha de Data Node Replica.
- [ ]  Aquel Data Node que reciba un archivo del cliente tendrá la responsabilidad de transferirlo al Data Node replica.
- [ ]  Implementación de método GETBATCH para poder descargar mas de un archivo.
- [x]  Implementación de una interfaz de cliente para la comunicación con el Name Node y Data Nodes.

---

# 3. Información general del diseño

## Sobre los servicios

En esta sección, se explican los servicios implementados para dar solución al reto propuesto, explicado en la sección: 1. Objetivo.

| Nombre del servicio | Rol que desempeña | IP y puertos de escucha |
| --- | --- | --- |
| Command-line Interface (CLI) Client | Permite a los usuarios dar instrucciones e interactuar con el Name Node y los Data Nodes. | local |
| Name Node | Recibe y resuelve las solicitudes de los clientes, busca en el índice de archivos de los Data Nodes el archivo solicitado por el cliente y le redirige al Data Node que lo almacena; administra el índice de archivos de los Data Nodes.     | 3.234.34.168: 8080 & 80 |
| Data Node 1 | Almacena los archivos subidos por los clientes; notifica al Name Node en caso de que un nuevo archivo haya sido creado.  | 3.223.88.22: 50051 & 80  |
| Data Node 2 | Almacena los archivos subidos por los clientes; notifica al Name Node en caso de que un nuevo archivo haya sido creado. | 44.208.106.154: 50051 & 80 |

---

# 4. Ambiente de desarrollo

En esta sección se proporciona una visión general fundamental para el desarrollo del proyecto. En ella, se detalla la "Estructura del Código", delineando la organización jerárquica de archivos y directorios que sustenta el proyecto. Además, se exploran aspectos clave de la "Configuración de Parámetros del Proyecto", destacando cómo ajustar y personalizar los elementos esenciales que guiarán el desarrollo y funcionamiento del software.

## Estructura del código

En esta sección se explora la disposición de archivos y carpetas de los diferentes servicios estipulados en la Sección 3: Informacion general del diseño - Sobre los servicios. Se muestra una visión general de como se organizan los archivos y las subcarpetas.

[💻 Command-line Interface (CLI) Client](https://github.com/jdprietom03/proyecto1-topicos/tree/main/CLI#estructura-del-c%C3%B3digo)

[🗄️ Name Node](https://github.com/jdprietom03/proyecto1-topicos/tree/main/NAMENODE#estructura-del-c%C3%B3digo)

[📂 Data Nodes](https://github.com/jdprietom03/proyecto1-topicos/tree/main/DATANODE#estructura-del-c%C3%B3digo)

## Configuración de parámetros del proyecto

La presente sección detalla que enfoque se tomo para la configuración de los parámetros del proyecto, como se configuran, y el contenido de los archivos dedicados para esto.

[💻 Command-line Interface (CLI) Client](https://github.com/jdprietom03/proyecto1-topicos/tree/main/CLI#configuraci%C3%B3n-de-par%C3%A1metros-del-proyecto)

[🗄️ Name Node](https://github.com/jdprietom03/proyecto1-topicos/tree/main/NAMENODE#configuraci%C3%B3n-de-par%C3%A1metros-del-proyecto)

[📂 Data Nodes](https://github.com/jdprietom03/proyecto1-topicos/tree/main/DATANODE#configuraci%C3%B3n-de-par%C3%A1metros-del-proyecto)

## Paquetes y dependencias

Se detallan las dependencias requeridas para una correcta ejecución del software desarrollado para cada uno de los servicios estipulados en la Sección 3: Informacion general del diseño - Sobre los servicios.

[💻 Command-line Interface (CLI) Client](https://github.com/jdprietom03/proyecto1-topicos/tree/main/CLI#paquetes-y-dependencias)

[🗄️ Name Node](https://github.com/jdprietom03/proyecto1-topicos/tree/main/NAMENODE#paquetes-y-dependencias)

[📁 Data Nodes](https://github.com/jdprietom03/proyecto1-topicos/tree/main/DATANODE#paquetes-y-dependencias)

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

## Guías de uso

Las siguientes guías brindará los pasos a seguir para un correcto funcionamiento y ejecución del software desarrollado para cada uno de los servicios estipulados en la Sección 3: Informacion general del diseño - Sobre los servicios.

[💻 Command-line Interface (CLI) Client](https://github.com/jdprietom03/proyecto1-topicos/tree/main/CLI#gu%C3%ADa-de-uso)

[🗄️ Name Node](https://github.com/jdprietom03/proyecto1-topicos/blob/main/NAMENODE/README.md#gu%C3%ADa-de-uso)

[📂 Data Nodes](https://github.com/jdprietom03/proyecto1-topicos/tree/main/DATANODE#gu%C3%ADa-de-uso)

## Acciones

Los siguientes son los endpoints y comandos disponibles a y las acciones permitidas por cada uno de los servicios estipulados en la Sección 3: Informacion general del diseño - Sobre los servicios.

[💻 Command-line Interface (CLI) Client](https://github.com/jdprietom03/proyecto1-topicos/tree/main/CLI#acciones)

[🗄️ Name Node](https://github.com/jdprietom03/proyecto1-topicos/blob/main/NAMENODE/README.md#acciones)

[📂 Data Nodes](https://github.com/jdprietom03/proyecto1-topicos/tree/main/DATANODE#acciones)