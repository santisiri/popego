# EXAMPLE consumer.tac
# levanta 1 consumidor en puerto 9000
from jq.consumer_startup import createConsumerApplication

application = createConsumerApplication(ports=[9000,9001])

