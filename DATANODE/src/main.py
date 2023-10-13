import argparse

# Configura el parser de argumentos
parser = argparse.ArgumentParser(
    description='Ejecuta componentes del proyecto. Por lo pronto, solo esta el DataNode.')

parser.add_argument('component',
                    type=str,
                    choices=['datanode'],
                    help='Especifica el componente a ejecutar. "datanode" para correr el servidor DataNode')

args = parser.parse_args()

if args.component == 'datanode':

    from server.grpc import server
    server.run()
