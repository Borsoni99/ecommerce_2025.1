from database.cosmos_connection import CosmosConnection
import json

def test_cosmos_connection():
    try:
        print("1. Initializing Cosmos DB connection...")
        cosmos = CosmosConnection()
        
        print("\n2. Getting 'produtos' container...")
        container = cosmos.get_container('produtos')
        
        print("\n3. Testing container read...")
        container_properties = container.read()
        print(f"Container properties: {json.dumps(container_properties, indent=2)}")
        
        print("\n4. Testing item creation...")
        test_item = {
            'id': 'test-item-1',
            'productCategory': 'Test',
            'productName': 'Test Product',
            'price': 10.99,
            'imageUrl': 'https://example.com/test.jpg',
            'productDescription': 'Test product description'
        }
        
        created_item = container.create_item(body=test_item)
        print(f"Created item: {json.dumps(created_item, indent=2)}")
        
        print("\n5. Testing item read...")
        read_item = container.read_item(
            item=test_item['id'],
            partition_key=test_item['productCategory']
        )
        print(f"Read item: {json.dumps(read_item, indent=2)}")
        
        print("\n6. Testing item deletion...")
        container.delete_item(
            item=test_item['id'],
            partition_key=test_item['productCategory']
        )
        print("Item deleted successfully")
        
        print("\nAll tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_cosmos_connection() 