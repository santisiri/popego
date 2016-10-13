from twisted.application import internet, service
from jq.consumer.server import JobConsumerFactory
import os


def attachConsumerService(processPath, port, app):
    service =  internet.TCPServer(port, JobConsumerFactory(processPath))
    service.setServiceParent(app)

def createConsumerApplication(name='JobConsumer Application',
                              ports=[9000]):
    
    # path del proceso consumer a ejecutar
    from jq import consumer
    consumerExecutable = os.path.join(os.path.dirname(consumer.__file__),
                                      'agent_dispatcher.py')

    # conexion a la base de la aplicacion
    if 'POPEGO_CONF' not in os.environ:
        raise Exception("Falta la variable POPEGO_CONF")

    # Creacion del application
    application = service.Application(name)
    
    for port in ports:
        attachConsumerService(consumerExecutable, port, application)

    return application
                              
