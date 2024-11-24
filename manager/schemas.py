student_info_config = {
    "class": "StudentInfo",
    "vectorizer": "none",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"],
        },
        {
            "name": "code",
            "dataType": ["text"],
            "indexSearchable": True,
            "indexFilterable": True
        },
        {
            'name': 'gender',
            'dataType': ['boolean'], # 0 for man, 1 for woman
        },
    ]
}

student_embedding_left_config = {
    "class": "StudentEmbeddingLeft",
    "vectorizer": "none",
    "properties": [
        {
            "name": "code",
            "dataType": ["text"],
            "indexSearchable": True,
            "indexFilterable": True
        },
        {
            "name": "embedding",
            "dataType": ["text"],
        },
    ]
}

student_embedding_middle_config = {
    "class": "StudentEmbeddingMiddle",
    "vectorizer": "none",
    "properties": [
        {
            "name": "code",
            "dataType": ["text"],
            "indexSearchable": True,
            "indexFilterable": True
        },
        {
            "name": "embedding",
            "dataType": ["text"],
        },
    ]
}

student_embedding_right_config = {
    "class": "StudentEmbeddingRight",
    "vectorizer": "none",
    "properties": [
        {
            "name": "code",
            "dataType": ["text"],
            "indexSearchable": True,
            "indexFilterable": True
        },
        {
            "name": "embedding",
            "dataType": ["text"],
        },
    ]
}