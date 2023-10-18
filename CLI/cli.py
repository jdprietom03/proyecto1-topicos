import json
import inquirer
from tqdm import tqdm
import time
from actions import Action
from proxy_client import APIClient
from loader import SubscriberSingleton
import re
import asyncio
from questions import *
from grpc_client import FileClient
import os
from tabulate import tabulate



class Wrapper:
    def __init__(self):
        self.content = None

    def __str__(self):
        return f"{self.content}"

class CLI:
    def __init__(self, **kwargs):
        NAME_NODE_HOST = os.getenv('NAME_NODE_HOST')
        NAME_NODE_PORT = os.getenv('NAME_NODE_PORT')

        self.client = APIClient(f"{NAME_NODE_HOST}:{NAME_NODE_PORT}")
        
        self.loader = SubscriberSingleton

    def value_of(self, action):
        action = action.upper()

        if Action.GET.value == action:
            asyncio.run(self.GET())
        elif Action.PUT.value == action:
            asyncio.run(self.PUT())
        elif Action.LIST.value == action:
            asyncio.run(self.LIST())
        elif Action.SEARCH.value == action:
            asyncio.run(self.SEARCH())

    async def GET(self):
        response = Wrapper()

        do_request = False

        while not do_request:
            questions = [
                InputQuestion()\
                .with_id("file")\
                .with_message("Archivo a descargar: ")\
                .build(),

                ValidationQuestion()\
                .with_id("do_request")\
                .with_message("¿Deseas realizar esta operación?")\
                .build()
            ]

            answers = inquirer.prompt(questions)
            filename = answers["file"]
            do_request = answers["do_request"]

        self.__assign(response, self.client.get("get", {
            "payload": filename
        }))
        
        grpc_client = FileClient.set_host(response.content[0][0])

        await asyncio.gather(
            self.loader.add(3, "GET Request", lambda: self.__assign(response, grpc_client.get_file(filename)))
        )

        if response.content["status"] != 500:
            with open(response.content["filename"], 'wb') as file:
                file.write(response.content["data"])

    def __assign(self, wrapper, content):
        wrapper.content = content

    async def PUT(self):
        response = Wrapper()

        do_request = False

        while not do_request:
            questions = [
                InputQuestion()\
                .with_id("file")\
                .with_message("Archivo a subir: ")\
                .build(),

                ValidationQuestion()\
                .with_id("do_request")\
                .with_message("¿Deseas realizar esta operación?")\
                .build()
            ]

            answers = inquirer.prompt(questions)
            filename = answers["file"]
            do_request = answers["do_request"]

        self.__assign(response, self.client.put("put", {
            "payload": filename
        }))

        grpc_client = FileClient.set_host(response.content)

        await asyncio.gather(
            self.loader.add(1, "PUT Request", lambda: self.__assign(response, grpc_client.put_file(filename)))
        )

        print(response.content)

    async def LIST(self):
        response = Wrapper()

        await asyncio.gather(
            self.loader.add(3, "Listing files", lambda: self.__assign(response, self.client.list("list", data={"payload": "."})))
        )

        headers = ['Ruta']

        unique = [[j] for j in set(i[1] for i in response.content)]

        table = tabulate(unique, headers, tablefmt="pretty")

        print(table)

    async def SEARCH(self):
        response = Wrapper()

        do_request = False

        while not do_request:
            questions = [
                InputQuestion()\
                .with_id("search")\
                .with_message("Expresión a buscar: ")\
                .build(),

                ValidationQuestion()\
                .with_id("do_request")\
                .with_message("¿Deseas realizar esta operación?")\
                .build()
            ]

            answers = inquirer.prompt(questions)
            search = answers["search"]
            do_request = answers["do_request"]


        await asyncio.gather(
            self.loader.add(3, "GET Request", lambda: self.__assign(response, self.client.search("search", data = {
                "payload":  search
            })))
        )

        headers = ['Ruta']
        unique = [[j] for j in set(i[1] for i in response.content)]

        table = tabulate(unique, headers, tablefmt="pretty")

        print(table)

    def run(self):
        print("CLI: DFS System")

        while True:

            questions = [
                MultipleChoicesQuestion()\
                .with_id("action")\
                .with_message("Seleccionar el tipo de petición: ")\
                .with_action("[GET] - Traer archivo")\
                .with_action("[PUT] - Subir Archivo")\
                .with_action("[LIST] - Listar archivos")\
                .with_action("[SEARCH] - Buscar archivos")\
                .with_action("[SALIR] - Salir")\
                .build(),

                ValidationQuestion()\
                .with_id("do_request")\
                .with_message("¿Deseas realizar esta operación?")\
                .build()
            ]

            answers = inquirer.prompt(questions)
            action = answers["action"]
            do_request = answers["do_request"]
            action = self.__get_action(action)

            if do_request and action == "SALIR": break

            if do_request:
                self.value_of(action)
       

    def __get_action(self, action):
        resultados = re.findall(r'\[([^]]+)\]', action)

        return resultados[0]
