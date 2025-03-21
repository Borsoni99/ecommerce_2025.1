from azure.cosmos import CosmosClient, PartitionKey

class CosmosConnection:
    def __init__(self):
        # Cosmos DB Emulator default endpoint and key
        url = "https://localhost:8081"
        key = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
        
        # Initialize Cosmos client with SSL verification disabled (for emulator)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.client = CosmosClient(url, credential=key)
        
        # Create or get database
        self.database = self.client.create_database_if_not_exists('ecommerce_db')
        
        # Create containers if they don't exist
        self.containers = {}
        self._ensure_containers()
    
    def _ensure_containers(self):
        # Define containers with their partition keys
        container_configs = {
            'usuarios': PartitionKey(path='/id'),
            'tipos_endereco': PartitionKey(path='/id'),
            'enderecos': PartitionKey(path='/id'),
            'cartoes_credito': PartitionKey(path='/id')
        }
        
        # Create containers if they don't exist
        for container_name, partition_key in container_configs.items():
            self.containers[container_name] = self.database.create_container_if_not_exists(
                id=container_name,
                partition_key=partition_key,
                offer_throughput=400  # Minimum throughput for emulator
            )
    
    def get_container(self, container_name):
        return self.containers.get(container_name) 