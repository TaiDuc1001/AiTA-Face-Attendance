from weaviate import Client
from rich import print

def create_class(config: dict, 
                 client: Client,
                 verbose: bool = True) -> None:
    if client.schema.exists(class_name=config['class']):
        client.schema.delete_class(class_name=config['class'])
    client.schema.create_class(config)
    if verbose:
        print(f'[bold green]Created class {config["class"]}[/bold green]')

def create_data_object(
        class_name: str, 
        data_object: dict, 
        identifier: str,
        client: Client) -> None:
    schema = client.schema.get()
    class_names = [c['class'] for c in schema['classes']]
    if class_name not in class_names:
        raise ValueError(
            f"[bold red]Class {class_name} does not exist[/bold red]. "
            f"Please choose from {class_names}")

    identifier = identifier.lower()
    schema = client.schema.get()[class_name]
    properties = [p['name'] for p in schema['properties']]
    if identifier not in properties:
        raise ValueError(
            f"[bold red]Property {identifier} does not exist in "
            f"{class_name}[/bold red]. Please choose from {properties}")

    where_filter = {
        'path': [identifier],
        'operator': 'Equal',
        'valueText': data_object[identifier]
    }
    results = client.query.get(
        class_name, [identifier, '_additional {id}']
    ).with_where(where_filter).do()
    
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
    