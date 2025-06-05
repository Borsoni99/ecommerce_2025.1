from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError
import os
from dotenv import load_dotenv
import base64

class CosmosConnection:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get credentials from environment variables
        self.endpoint = os.getenv('COSMOS_DB_ENDPOINT')
        key = os.getenv('COSMOS_DB_KEY', '')
        
        # Ensure proper base64 padding
        padding = 4 - (len(key) % 4)
        if padding != 4:
            key = key + ('=' * padding)
        self.key = key
        
        if not self.endpoint or not self.key:
            raise ValueError("Cosmos DB credentials not found in environment variables")
        
        # Initialize the Cosmos client
        self.client = CosmosClient(self.endpoint, self.key)
        
        # Create database and container if they don't exist
        self._ensure_database()
        self._ensure_containers()
    
    def _ensure_database(self):
        """
        Creates the database if it doesn't exist
        """
        try:
            self.database = self.client.create_database_if_not_exists('ecommerce_db')
        except Exception as e:
            print(f"Error creating database: {str(e)}")
            raise
    
    def _ensure_containers(self):
        """
        Creates containers if they don't exist
        """
        try:
            # Define container configurations
            containers_config = {
                'produtos': {
                    'partition_key': PartitionKey(path='/productCategory'),
                    'offer_throughput': 400
                }
            }
            
            # Create containers if they don't exist
            for container_id, config in containers_config.items():
                try:
                    container = self.database.create_container_if_not_exists(
                        id=container_id,
                        partition_key=config['partition_key'],
                        offer_throughput=config['offer_throughput']
                    )
                    print(f"Container {container_id} ensured")
                except Exception as e:
                    print(f"Error creating container {container_id}: {str(e)}")
                    raise
        except Exception as e:
            print(f"Error in _ensure_containers: {str(e)}")
            raise
    
    def get_container(self, container_id):
        """
        Gets a container by ID, creates it if it doesn't exist
        """
        try:
            container = self.database.get_container_client(container_id)
            # Test if container exists by reading its properties
            container.read()
            return container
        except CosmosResourceNotFoundError:
            print(f"Container {container_id} not found, creating it...")
            self._ensure_containers()
            return self.database.get_container_client(container_id) 