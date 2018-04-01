import procgame.game
from procgame.game import AdvancedMode
import logging

class AssembleTeamMode(procgame.game.AdvancedMode):
    """
    Mode that tracks both forward and backward shots on left "loop" ramp.
    Assemble the team by looping the loop forward 8 times and backward 3 times.
    started from Laughing man mode, when running LeftRamp Mode is not running
    """
    def __init__(self, game):
        super(AssembleTeamMode, self).__init__(game=game, priority=45, mode_type=AdvancedMode.Manual)
        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('AssembleTeamMode')

        self.forward_ramp_ready = False
        self.reverse_ramp_ready = False
        self.loopscompleted = 0
        self.complete_tt = False
        self.complete_s9 = False
        self.loopcompletedtt = 0
        self.loopcompleteds9 = 0
        pass

    def evt_player_added(self, player):
        #player.setState('max_loops_completed',0)
        pass

    def sw_rampLeftLow_active(self, sw):
        if(self.game.switches.rampLeftHigh.hw_timestamp == None):
            self.game.score(10)
        else:
            if(((self.game.switches.rampLeftLow.hw_timestamp - self.game.switches.rampLeftHigh.hw_timestamp) < 700) and
                (self.game.switches.rampLeftLow.hw_timestamp > self.game.switches.rampLeftHigh.hw_timestamp)):
                if True: #(self.reverse_ramp_ready):
                    self.loopcompletedtt += 1
                    self.loopscompleted += 1
                    #self.game.score(100)
                else:
                    self.game.score(50)
                #self.game.displayText("Think Tank Loop " + str(self.loopcompletedtt))
                self.cancel_delayed(name="disabler")
                self.delay(name="disabler", delay=2.5, handler=self.disable_ramp_readiness)
                self.forward_ramp_ready = True
                self.reverse_ramp_ready = True
            else:
                self.game.score(10)
            self.check_progress_tt()

    def sw_rampLeftHigh_active(self, sw):        
        if(self.game.switches.rampLeftLow.hw_timestamp == None):
            self.game.score(10)
        else:
            if (((self.game.switches.rampLeftHigh.hw_timestamp - self.game.switches.rampLeftLow.hw_timestamp) < 700) and
                (self.game.switches.rampLeftHigh.hw_timestamp > self.game.switches.rampLeftLow.hw_timestamp)):
                if True: #(self.reverse_ramp_ready):
                    self.loopcompleteds9 += 1
                    self.loopscompleted += 1
                    #self.game.score(100)
                else:
                    self.game.score(50)
                self.game.displayText("Section 9 Loop " + str(self.loopcompleteds9))
                self.cancel_delayed(name="disabler")
                self.delay(name="disabler", delay=2.5, handler=self.disable_ramp_readiness)
                self.forward_ramp_ready = True
                self.reverse_ramp_ready = True
            else:
                self.game.score(10)
            self.check_progress_s9()

    def check_progress_tt(self):
        #add pictures or video and sound
        if self.loopcompletedtt == 1 and not self.complete_tt:
            self.game.displayText("1 of 3")
            self.game.score(500)
        if self.loopcompletedtt == 2 and not self.complete_tt:
            self.game.displayText("2 of 3")
            self.game.score(2000)
        if self.loopcompletedtt == 3 and not self.complete_tt:
            self.game.displayText("Tachikomas collected")
            self.game.score(4500)
            self.complete_tt = True
            self.game.coils.flasherramp.disable()
        if self.loopcompletedtt > 3 or self.complete_tt:
            self.game.score(10)
        self.check_total_progress()
        pass

    def check_progress_s9(self):
        #add pictures or video and sound
        if self.loopcompleteds9 == 1 and not self.complete_s9:
            self.game.displayText("1 of 8")
            self.game.score(100)
        if self.loopcompleteds9 == 2 and not self.complete_s9:
            self.game.displayText("2 of 8")
            self.game.score(400)
        if self.loopcompleteds9 == 3 and not self.complete_s9:
            self.game.displayText("3 of 8")
            self.game.score(900)
        if self.loopcompleteds9 == 4 and not self.complete_s9:
            self.game.displayText("4 of 8")
            self.game.score(1600)
        if self.loopcompleteds9 == 5 and not self.complete_s9:
            self.game.displayText("5 of 8")
            self.game.score(2500)
        if self.loopcompleteds9 == 6 and not self.complete_s9:
            self.game.displayText("6 of 8")
            self.game.score(3600)
        if self.loopcompleteds9 == 7 and not self.complete_s9:
            self.game.displayText("7 of 8")
            self.game.score(4900)
        if self.loopcompleteds9 == 8 and not self.complete_s9:
            self.game.displayText("Section 9 Team collected")
            self.game.score(6400)
            self.complete_s9 = True
            self.game.coils.flasherscoopL.disable()
        if self.loopcompleteds9 > 3 or self.complete_tt:
            self.game.score(10)
        self.check_total_progress()
    pass

    def check_total_progress(self):
        if self.complete_s9 and self.complete_tt:
            self.game.modes.remove(self)
    
    def mode_started(self):
        self.loopscompleted = 0
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()
        self.complete_tt = False
        self.complete_s9 = False
        self.loopcompletedtt = 0
        self.loopcompleteds9 = 0
        self.game.coils.flasherscoopL.enable()
        self.game.coils.flasherramp.enable()
        
    def mode_stopped(self): 
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()
        self.game.modes.add(self.game.leftramp_mode)
        #def evt_ball_ending(self, (shoot_again, last_ball)):
        #self.cancel_delayed(name="disabler")
        #self.disable_ramp_readiness()
        self.game.coils.flasherscoopL.disable()
        self.game.coils.flasherramp.disable()

    def disable_ramp_readiness(self):
        self.forward_ramp_ready = False
        self.reverse_ramp_ready = False
        self.loopcompletedtt = 0
        self.loopcompleteds9 = 0
        self.game.displayText("Looping Ended")
        self.loopscompleted = 0
        #self.game.lamps.rampL.disable()
        #self.game.lamps.rampRight.disable()
