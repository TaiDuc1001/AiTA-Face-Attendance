from weaviate import Client

def create_class(config: dict, client: Client) -> None:
    if client.schema.exists(class_name=config['class']):
        client.schema.delete_class(class_name=config['class'])
    client.schema.create_class(config)
    print(f"Class {config['class']} created")

def create_data_object(
        class_name: str, 
        data_object: dict, 
        identifier: str,
        client: Client) -> None:
    schema = client.schema.get()
    class_names = [c['class'] for c in schema['classes']]
    assert class_name in class_names, f'Please choose a class from {class_names}'

    identifier = identifier.lower()
    schema = client.schema.get()[class_name]
    properties = [p['name'] for p in schema['properties']]
    assert identifier in properties, f'Please choose an identifier from {properties}'

    name = data_object[identifier]
    results = client.query.get(
        class_name, [identifier, '_additional {id}']
    ).with_where({
        'path': [identifier],
        'operator': 'Equal',
        'valueText': name
    }).do()
    
    if len(results['data']['Get'][class_name]) != 0:
        toDelID = results['data']['Get'][class_name][0]['_additional']['id']
        client.data_object.delete(
            uuid=toDelID,
            class_name=class_name
        )
        
    client.data_object.create(
        class_name=class_name,
        data_object=data_object
    )
    