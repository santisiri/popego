# levanta 3 consumers en puerto 9000-9003
from jq.consumer_startup import createConsumerApplication

application = createConsumerApplication(ports=range(9000,9003))

