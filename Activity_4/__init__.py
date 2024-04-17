from otree.api import *
import random, time

doc = """
Non-Passive Simultaneous Dictator Game (Two Proposer)
"""

# ---------------------------------------HELPER FUNCTIONS---------------------------------------
def generate_unique_sequence(prefix='SC'):
    # Get current time in milliseconds
    current_time_ms = int(time.time() * 1000)
    # Generate a random number between 1000 and 9999
    random_number = random.randint(1000, 9999)
    # Combine prefix, current time, and random number
    sequence = f'{prefix}{current_time_ms}{random_number}'
    return sequence

def checkQuiz(vals):
    answer_key = ["3", "1", ["2", "3", "4"], ["1"], "2", "2"]

    if(vals == answer_key):
        return True
    
    return False

def positive_normal(mean, sd):
    while True:
        value = random.normalvariate(mean, sd)
        if value > 0:
            return value
        
def set_payoffs(player):    
    #Set Actual Payoff based on Dictator_1 and Dictator_2 Choice
    
    #If Dictator_1 and Dictator_2 chooses action A
    if(player.player_choice == 'X' and player.opponent_random_choice == 'X'):
        player.payoff = player.session.config['simultaneous_dg_game_payoff']['Action_AA']['Player_1']

    #If Dictator_1 chooses action A and Dictator_2 chooses action B
    elif(player.player_choice == 'X' and player.opponent_random_choice == 'Y'):
        player.payoff = player.session.config['simultaneous_dg_game_payoff']['Action_AB']['Player_1']

    #If Dictator_1 chooses action B and Dictator_2 chooses action A
    elif(player.player_choice == 'Y' and player.opponent_random_choice == 'X'):
        player.payoff = player.session.config['simultaneous_dg_game_payoff']['Action_BA']['Player_1']
    
    #If Dictator_1 and Dictator_2 chooses action B
    elif(player.player_choice == 'Y' and player.opponent_random_choice == 'Y'):
        player.payoff = player.session.config['simultaneous_dg_game_payoff']['Action_BB']['Player_1']
# ----------------------------------------------------------------------------------------------

# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'Activity_4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    accept_consent_flag = models.BooleanField(initial = False)
    MTURK_ID = models.StringField(initial= '')
    failed_quiz_count = models.IntegerField(initial= 0)
    player_role = models.StringField(initial='')
    player_choice = models.StringField(choices=['X','Y',], label="Your Choice")
    opponent_random_choice = models.StringField(initial='')
    opponent_nature = models.StringField(initial='')
    showup_fee = models.StringField(initial = None)
    bonus = models.StringField(initial = None)
    total_earnings = models.StringField(initial = None)
    submission_code = models.StringField(initial = None)
    timeout_flag = models.BooleanField(initial = False)

    peq_1 = models.StringField(initial = None)
    peq_2 = models.StringField(initial = None)
    peq_3 = models.StringField(initial = None)
    peq_4 = models.StringField(initial = None)
    peq_5 = models.StringField(initial = None)
    peq_6 = models.StringField(initial = None)
    peq_7 = models.StringField(initial = None)
    peq_8 = models.StringField(initial = None)

# PAGES
class Page1(Page):
    template_name = '_templates/global/Consent_Form.html'

    @staticmethod
    def vars_for_template(player):
        return (dict(failed_compensation = player.session.config['failed_quiz_payoff'], showup_fee = player.session.config['showup_fee'], max_bonus = player.session.config['max_bonus'],
                     estimated_time=player.session.config['estimated_time_min'], irb_number=player.session.config['IRB_number'],
                     max_waiting_time=player.session.config['max_waiting_time_min']))
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.accept_consent_flag = True


class Page2(Page):
    template_name = '_templates/global/Identification.html'
    
    @staticmethod
    def live_method(player, data):
        if(data["type"] == 'MTurk-ID'):
            player.MTURK_ID = data["id"]


class Instructions(Page):
    template_name = '_templates/global/DG-Simultaneous-Instructions.html'
    @staticmethod
    def js_vars(player):
        enable_button_time = 3 if player.session.config['DEVELOPMENT_TESTING'] else 30
        return (dict(enable = enable_button_time))
    
    @staticmethod
    def vars_for_template(player):
        return (dict(
                showup_fee = player.session.config['showup_fee'],
                max_decide_time=player.session.config['max_decide_time_sec'],
                SI_X1 = player.session.config['simultaneous_dg_game_payoff']['Action_AA']['Player_1'],
                SI_Y1 = player.session.config['simultaneous_dg_game_payoff']['Action_AA']['Receiver'],
                SI_X2 = player.session.config['simultaneous_dg_game_payoff']['Action_AB']['Player_1'],
                SI_Y2 = player.session.config['simultaneous_dg_game_payoff']['Action_AB']['Receiver'],
                isPassive = False,
            ))
    
    @staticmethod
    def live_method(player, data):      
        if(data["val"] == 2):
            player.failed_quiz_count = player.failed_quiz_count if checkQuiz(data["answers"]) else (player.failed_quiz_count + 1)
            
            if(player.failed_quiz_count > 1):
                player.participant.failed_quiz = True
            else:
                player.participant.failed_quiz = False
            
            return {player.id_in_group: {"flag" : checkQuiz(data["answers"]), "cnt": player.failed_quiz_count}}
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.failed_quiz_count > 1:
            val_code = generate_unique_sequence("FQ")
            player.participant.submission_code = val_code
            player.submission_code = val_code
            player.participant.failed_quiz = True
            player.total_earnings = str(player.session.config['failed_quiz_payoff'])

class Page4(Page):
    template_name = '_templates/global/Failed_Quiz_Twice.html'

    @staticmethod
    def vars_for_template(player):
        return (dict(failed_quiz_compensation = player.session.config['failed_quiz_payoff'], validation_code = player.participant.submission_code))
    
    @staticmethod
    def is_displayed(player):
        return (True if player.failed_quiz_count > 1 else False)

class WaitRoom(Page):
    template_name = '_templates/global/Waitroom.html'

    @staticmethod
    def is_displayed(player):
        return (player.participant.failed_quiz == False)
   
    @staticmethod
    def js_vars(player):
        rand_wait_time = 5 if(player.session.config['DEVELOPMENT_TESTING'] == True) else positive_normal(9.66, 26.02)
            
        return (dict(wait_time = rand_wait_time, time_left = player.session.config['max_waiting_time_min']))
    
    @staticmethod
    def vars_for_template(player):
        player.player_role = player.session.config['control_player_role'][1] if (player.session.config['CONTROL_FLAG'] == True) else random.choice(["Proposer_1", "Proposer_2"])
        player.participant.role = player.player_role

        return (dict(role = player.player_role))
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.opponent_nature = player.session.config['control_opponent_nature'][1] if (player.session.config['CONTROL_FLAG'] == True) else random.choice(['MTurker', 'Bot'])  


class GamePage(Page):
    template_name = '_templates/global/DG-Simultaneous-GamePage.html'
    timeout_seconds = 60

    form_model = 'player'
    form_fields = ['player_choice']
    
    @staticmethod
    def is_displayed(player):
        p = player.participant
        return (p.failed_quiz == False)
    
    @staticmethod
    def js_vars(player):
        return (dict(timeout = player.session.config['max_decide_time_sec']))
    
    @staticmethod
    def vars_for_template(player):
        return dict(AA_x = player.session.config['simultaneous_dg_game_payoff']['Action_AA']['Player_1'], AA_y = player.session.config['simultaneous_dg_game_payoff']['Action_AA']['Player_2'], AA_z = player.session.config['simultaneous_dg_game_payoff']['Action_AA']['Receiver'],
                    AB_x = player.session.config['simultaneous_dg_game_payoff']['Action_AB']['Player_1'], AB_y = player.session.config['simultaneous_dg_game_payoff']['Action_AB']['Player_2'], AB_z = player.session.config['simultaneous_dg_game_payoff']['Action_AB']['Receiver'],
                    BA_x = player.session.config['simultaneous_dg_game_payoff']['Action_BA']['Player_1'], BA_y = player.session.config['simultaneous_dg_game_payoff']['Action_BA']['Player_2'], BA_z = player.session.config['simultaneous_dg_game_payoff']['Action_BA']['Receiver'],
                    BB_x = player.session.config['simultaneous_dg_game_payoff']['Action_BB']['Player_1'], BB_y = player.session.config['simultaneous_dg_game_payoff']['Action_BB']['Player_2'], BB_z = player.session.config['simultaneous_dg_game_payoff']['Action_BB']['Receiver'],
                    form_label= " ",
                    isPassive = False,
                    op_nature = player.opponent_nature,
                    role = player.player_role,
                    op_role = "Proposer_2" if player.player_role == "Proposer_1" else "Proposer_1"
                    )
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        #Set Actual Payoff based on Dictator Choice
        if(timeout_happened):
            player.timeout_flag = True
            player.participant.activity_timeout = True
            player.participant.activity_earning = 0
            player.participant.op_nature = ''
            
        else:
            player.participant.activity_timeout = False
            player.timeout_flag = False

            opponent_action_choice = player.session.config['control_action_choices'][0] if (player.session.config['CONTROL_FLAG'] == True) else random.choice(['X', 'Y'])
            player.opponent_random_choice = opponent_action_choice

            set_payoffs(player)
            
            participant = player.participant
            participant.activity_earning = float(player.payoff)  
            participant.op_nature = player.opponent_nature



class SOE(Page):
    template_name = '_templates/global/Summary_of_Earnings.html'

    @staticmethod
    def vars_for_template(player):
        return (dict(showup_fee = player.session.config['showup_fee'], timeout_flag = player.participant.activity_timeout, 
                     activity_one = False, bonus = player.session.config['follow_up_question_bonus'], player_action = player.player_choice, 
                     earning = float(player.payoff), t = float(player.payoff), other_proposer_action = player.opponent_random_choice
                     ))
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        total = float(participant.activity_earning)
        player.showup_fee = str(player.session.config["showup_fee"])
        
        # Generate Validation Code
        val_code = ''
        if (player.participant.activity_timeout == True):
            player.bonus = str(0)
            player.total_earnings = str(float(total) + float(player.showup_fee) + float(player.bonus)) 
            val_code = generate_unique_sequence(prefix='TO')
        elif (player.participant.activity_timeout == False):
            player.bonus = str(player.session.config["follow_up_question_bonus"])
            player.total_earnings = str(float(total) + float(player.showup_fee) + float(player.bonus)) 
            val_code = generate_unique_sequence()
        else:
            val_code = 'ER696'
             
        player.submission_code = val_code
        player.participant.submission_code = val_code

class PEQ(Page):
    template_name = '_templates/global/Post_EQ.html'
    
    @staticmethod
    def is_displayed(player):
        return (player.participant.failed_quiz == False and player.participant.activity_timeout == False)
    
    @staticmethod
    def js_vars(player):
        return (dict(activity_one = False))
    
    @staticmethod
    def vars_for_template(player):
        return (dict(activity_one=False))
    
    @staticmethod
    def live_method(player, data):
        if(data["val"] == 3):
            player.peq_1 = data["answers"][0]
            player.peq_2 = data["answers"][1]
            player.peq_3 = data["answers"][2]
            player.peq_4 = data["answers"][3]
            player.peq_5 = data["answers"][4]
            player.peq_6 = data["answers"][5]
            player.peq_7 = data["answers"][6]
            player.peq_8 = data["answers"][7]
        
        return {player.id_in_group: {"flag" : True}}  

class Submission_Code(Page):
    template_name = '_templates/global/Submission_Code.html'

    @staticmethod
    def is_displayed(player):
        return (player.participant.failed_quiz == False)
    
    @staticmethod
    def vars_for_template(player):
        return dict(submission_code = player.participant.submission_code)

page_sequence = [Page1, Page2, Instructions, Page4, WaitRoom, GamePage, SOE, PEQ, Submission_Code]
