definitions = {
    'Author': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer',
                'format': 'int32',
                'nullable': False,
            },
            'name': {
                'type': 'string',
                'nullable': False,
                'maxLength': 128,
            },
        },
    },
    'Book': {
        'type': 'object',
        'description': 'There is a unique constraint for `name`, `author_id` and `edition`',
        'properties': {
            'id': {
                'type': 'integer',
                'format': 'int32',
                'description': 'Unique ID of each book. It does not mean ISBN.',
                'nullable': False,
            },
            'name': {
                'type': 'string',
                'description': '*Duplicable* book name (Each book is identified by ID or fields of '
                               'unique constraint)',
                'nullable': False,
                'maxLength': 128,
            },
            'edition': {
                'type': 'string',
                'nullable': False,
                'maxLength': 16,
                'description':
                    'Control revision of each book. It can be "9th" or "10th", for example, in the '
                    'case of **Operating System Concepts** 9th edition and 10th edition.',
            },
            'author': {
                '$ref': '#/definitions/Author',
            },
        }
    },
}
