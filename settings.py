from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# mTurk settings. Do not change!
mTurk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Rely or Verify',
    'description': 'This HIT is an academic experiment where you will be interacting with another person on mTurk and make a range of decisions. Your payoff is dependent on your performance.',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 24*7, # 0.01 days
    'grant_qualification_id': 'XXXXX', # to prevent retakes
    'qualification_requirements': [
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
        {
            'QualificationTypeId': "XXXX",
            'Comparator': "DoesNotExist",
        },
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThan",
            'IntegerValues': [25] # taking in new people, and people with high approval rate
        },
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': 'GreaterThan',
            'IntegerValues': [95]
        }
    ]
}


SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.05,
    'participation_fee': 0.50,
    'doc': "",
    'mturk_hit_settings': mTurk_hit_settings,
}


SESSION_CONFIGS = [
    {
        'name': 'Leadership_Corruption_Game',
        'display_name': 'Rely or Verify',
        'num_demo_participants': 3,
        'app_sequence': ['LCG']
    },
    {
        'name': 'public_Goods_Game_exoEN',
        'display_name': "Jedrek's game",
        'real_world_currency_per_point': 0.10,
        'participation_fee': 5.00,
        'num_demo_participants': 2,
        'app_sequence': ['PGGRegiEN', 'PGGexoEN']
    }
]



# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 2

ROOMS = [
]

# Do not change any of the following!

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.


AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """
Choose a study design to demo it.
"""

# don't share this with anybody.
SECRET_KEY = 'ahssood=cw(3!ls+*^6opq6t9u&ss40lcekefxbv#57=b!s3mb'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'otree_tools','captcha']
EXTENSION_APPS = ['otree_tools']

# for mTurk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# for Captcha
RECAPTCHA_PUBLIC_KEY = '6Ldf7bcUAAAAAMzBo1iTCUFmMEFK-HGmLMEYNnBl'
RECAPTCHA_PRIVATE_KEY = '6Ldf7bcUAAAAAJk0sqe3wwMX1yBZ34BT_ABkP3vo'
# RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True
