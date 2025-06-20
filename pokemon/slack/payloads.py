START_GAME_MODAL = lambda trigger_id, private_metadata: {
    'trigger_id': trigger_id,
    'view': {
        'type': 'modal',
        'title': {
            'type': 'plain_text',
            'text': 'Start your journey!',
        },
        'blocks': [
            {
                'type': 'input',
                'block_id': 'gender',
                'label': {
                    'type': 'plain_text',
                    'text': 'Gender'
                },
                'element': {
                    'type': 'static_select',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': 'Select your gender'
                    },
                    'options': [
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'Male'
                            },
                            'value': 'male'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'Female'
                            },
                            'value': 'female'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'Other'
                            },
                            'value': 'other'
                        },
                    ],
                    'action_id': 'gender'
                }
            },
            {
                'type': 'input',
                'block_id': 'name',
                'label': {
                    'type': 'plain_text',
                    'text': 'Your Name (your Slack name will be used if you leave this blank)',
                },
                'element': {
                    'type': 'plain_text_input',
                    'action_id': 'name',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': 'Enter your name'
                    },
                    'multiline': False,
                },
                'optional': True
            },
            {
                'type': 'input',
                'block_id': 'opponent',
                'label': {
                    'type': 'plain_text',
                    'text': 'Opponent Name (optional, defaults to Gary)',
                },
                'element': {
                    'type': 'plain_text_input',
                    'action_id': 'opponent',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': 'Enter your opponent\'s name'
                    },
                    'multiline': False,
                },
                'optional': True
            }
        ],
        'close': {
            'type': 'plain_text',
            'text': 'Cancel'
        },
        'submit': {
            "type": "plain_text",
            "text": "Start!"
        },
        'callback_id': 'start_game_modal',
        'private_metadata': private_metadata
    }
}
