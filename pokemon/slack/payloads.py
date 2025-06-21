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

GAME_BLOCKS = lambda file_url: {
    'blocks': [
        {
            'type': 'image',
            'alt_text': 'Game Scene',
            'image_url': file_url,
            'title': {
                'type': 'plain_text',
                'text': 'Game Scene'
            },
            'block_id': 'game_scene_image'
        },
        {
            'type': 'actions',
            'block_id': 'movement_buttons',
            'elements': [
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Left'
                    },
                    'value': 'left',
                    'action_id': 'left_button'
                },
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Up'
                    },
                    'value': 'up',
                    'action_id': 'up_button'
                },
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Down'
                    },
                    'value': 'down',
                    'action_id': 'down_button'
                },
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Right'
                    },
                    'value': 'right',
                    'action_id': 'right_button'
                },
            ]
        },
        {
            'type': 'actions',
            'block_id': 'action_buttons',
            'elements': [
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'A'
                    },
                    'value': 'a',
                    'action_id': 'a_button'
                },
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'B'
                    },
                    'value': 'b',
                    'action_id': 'b_button'
                },
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'X'
                    },
                    'value': 'x',
                    'action_id': 'x_button'
                },
                {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Y'
                    },
                    'value': 'y',
                    'action_id': 'y_button'
                }
            ]
        },
        {
            'dispatch_action': True,
            'type': 'input',
            'block_id': 'mass_input',
            'element': {
                'type': 'plain_text_input',
                'action_id': 'mass_input',
                'placeholder': {
                    'type': 'plain_text',
                    'text': 'Mass input (use w a s d for movement, and a b x y for actions. e.g: w a s d a b x y)',
                },
            },
            'label': {
                'type': 'plain_text',
                'text': 'Mass Input'
            },
        },
    ],
    'response_type': 'in_channel'
}
