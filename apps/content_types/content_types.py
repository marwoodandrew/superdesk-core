
import superdesk

from apps.auth import get_user_id

CONTENT_TYPE_PRIVILEGE = 'content_type'

DEFAULT_SCHEMA = {
    'slugline': {'maxlength': 24, 'type': 'string'},
    'genre': {'type': 'list'},
    'anpa_take_key': {},
    'place': {'type': 'list'},
    'priority': {},
    'anpa_category': {'type': 'list'},
    'subject': {'type': 'list'},
    'company_codes': {'type': 'list'},
    'ednote': {},
    'headline': {'maxlength': 64, 'type': 'string'},
    'abstract': {'maxlength': 160, 'type': 'string'},
    'body_html': {},
    'byline': {'type': 'string'},
    'dateline': {'type': 'dict'},
    'sign_off': {'type': 'string'},
    'sms': None,
    'footer': None,
    'body_footer': None,
    'media': {},
    'media_description': {},
    'located': {},
}

DEFAULT_EDITOR = {
    'slugline': {'order': 1, 'sdWidth': 'full'},
    'genre': {'order': 2, 'sdWidth': 'half'},
    'anpa_take_key': {'order': 3, 'sdWidth': 'half'},
    'place': {'order': 4, 'sdWidth': 'half'},
    'priority': {'order': 5, 'sdWidth': 'quarter'},
    'anpa_category': {'order': 7, 'sdWidth': 'full'},
    'subject': {'order': 8, 'sdWidth': 'full'},
    'company_codes': {'order': 9, 'sdWidth': 'full'},
    'ednote': {'order': 10, 'sdWidth': 'full'},
    'headline': {'order': 11, 'formatOptions': ['underline', 'anchor', 'bold', 'removeFormat']},
    'sms': {'order': 12},
    'abstract': {'order': 13, 'formatOptions': ['bold', 'italic', 'underline', 'anchor', 'removeFormat']},
    'byline': {'order': 14},
    'dateline': {'order': 15},
    'body_html': {
        'order': 16,
        'formatOptions': ['h2', 'bold', 'italic', 'underline', 'quote', 'anchor', 'embed', 'picture', 'removeFormat']
    },
    'footer': {'order': 17},
    'body_footer': {'order': 18},
    'sign_off': {'order': 19},
    'media': {},
    'media_description': {},
}


class ContentTypesResource(superdesk.Resource):
    schema = {
        '_id': {
            'type': 'string',
            'unique': True,
        },
        'label': {
            'type': 'string',
            'iunique': True,
        },
        'description': {
            'type': 'string',
        },
        'schema': {
            'type': 'dict'
        },
        'editor': {
            'type': 'dict'
        },
        'priority': {
            'type': 'integer',
            'default': 0,
        },
        'enabled': {
            'type': 'boolean',
            'default': False,
        },
        'created_by': superdesk.Resource.rel('users', nullable=True),
        'updated_by': superdesk.Resource.rel('users', nullable=True),
    }

    item_url = 'regex("[\w,.:-]+")'

    privileges = {'POST': CONTENT_TYPE_PRIVILEGE,
                  'PATCH': CONTENT_TYPE_PRIVILEGE,
                  'DELETE': CONTENT_TYPE_PRIVILEGE}

    datasource = {
        'default_sort': [('priority', -1)],
    }


class ContentTypesService(superdesk.Service):
    def _set_updated_by(self, doc):
        doc['updated_by'] = get_user_id()

    def _set_created_by(self, doc):
        doc['created_by'] = get_user_id()

    def on_create(self, docs):
        for doc in docs:
            self._set_updated_by(doc)
            self._set_created_by(doc)
            if 'schema' not in doc and 'editor' not in doc:
                doc['schema'] = DEFAULT_SCHEMA
                doc['editor'] = DEFAULT_EDITOR

    def on_update(self, updates, original):
        self._set_updated_by(updates)
