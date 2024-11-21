student_info_config = {
    "class": "StudentInfo",
    "vectorizer": "none",
    "properties": [
        {
            "name": "name",
            "dataType": ['text'],
        },
        {
            'name': 'gender',
            'dataType': ['boolean'],
        },
    ]
}

student_embedding_left_config = {
    "class": "StudentEmbeddingLeft",
    "vectorizer": "none",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"],
        },
        {
            "name": "embedding",
            "dataType": ["blob"],
        },
    ]
}

student_embedding_middle_config = {
    "class": "StudentEmbeddingMiddle",
    "vectorizer": "none",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"],
        },
        {
            "name": "embedding",
            "dataType": ["blob"],
        },
    ]
}

student_embedding_right_config = {
    "class": "StudentEmbeddingRight",
    "vectorizer": "none",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"],
        },
        {
            "name": "embedding",
            "dataType": ["blob"],
        },
    ]
}