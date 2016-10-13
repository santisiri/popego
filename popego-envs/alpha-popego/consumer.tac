from jq.consumer_startup import createConsumerApplication

application = createConsumerApplication(ports=range(9000,9006))
