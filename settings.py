from os import environ

SESSION_CONFIGS = [
    dict(
        name='Activity_1_Baseline',
        app_sequence=['Activity_1'],
        num_demo_participants=10,
    ),
    dict(
        name='Activity_2_Passive_Simultaneous',
        app_sequence=['Activity_2'],
        num_demo_participants=10,
    ),
    dict(
        name='Activity_3_Passive_Sequential',
        app_sequence=['Activity_3'],
        num_demo_participants=10,
    ),
    dict(
        name='Activity_4_Non_Passive_Simultaneous',
        app_sequence=['Activity_4'],
        num_demo_participants=10,
    ),
    dict(
        name='Activity_5_Non_Passive_Sequential',
        app_sequence=['Activity_5'],
        num_demo_participants=10,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0,
    
    DEVELOPMENT_TESTING = False,
    CONTROL_FLAG = False,
    control_action_choices = ['Y', 'X'],
    control_player_role = ['Proposer', 'Proposer_2', 'Proposer_1'],
    control_opponent_nature = ['Person', 'Bot', 'Person'],

    showup_fee = 0.5,
    failed_quiz_payoff = 0.10,
    max_bonus = 2.55,
    estimated_time_min = 10,
    IRB_number = '#HRPP-2019-93',
    max_decide_time_sec = 60,
    max_example_page_wait_time_sec = 30,
    max_waiting_time_min = 5,
    follow_up_question_bonus = 1,

    baseline_dg_game_payoff = dict(Action_A=dict(Player_1=6, Receiver=1), 
                                   Action_B=dict(Player_1=5, Receiver=5)),
        
    simultaneous_dg_game_payoff = dict(Action_AA=dict(Player_1=6, Player_2=6, Receiver=1),
                                    Action_AB=dict(Player_1=5, Player_2=5, Receiver=5),
                                    Action_BA=dict(Player_1=5, Player_2=5, Receiver=5),
                                    Action_BB=dict(Player_1=5, Player_2=5, Receiver=5)),
        
    sequential_dg_game_payoff = dict(Action_AA=dict(Player_1=6, Player_2=6, Receiver=1),
                                    Action_AB=dict(Player_1=5, Player_2=5, Receiver=5),
                                    Action_BA=dict(Player_1=5, Player_2=5, Receiver=5),
                                    Action_BB=dict(Player_1=5, Player_2=5, Receiver=5))
)

PARTICIPANT_FIELDS = ['failed_quiz', 'activity_timeout', 'role', 'op_nature', 'submission_code', 'activity_earning']
SESSION_FIELDS = []

DEBUG = False

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7101846635513'
