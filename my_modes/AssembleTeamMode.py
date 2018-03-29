import procgame.game
from procgame.game import AdvancedMode
import logging

class AssembleTeamMode(procgame.game.AdvancedMode):
    """
    Mode that tracks both forward and backward shots on left "loop" ramp.

    """
    def __init__(self, game):
        super(AssembleTeamMode, self).__init__(game=game, priority=45, mode_type=AdvancedMode.Manual)
        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('AssembleTeamMode')

        self.forward_ramp_ready = False
        self.reverse_ramp_ready = False
        self.loopscompleted = 0
        pass

    def evt_player_added(self, player):
        player.setState('max_loops_completed',0)

    def sw_rampLeftLow_active(self, sw):
        if(self.game.switches.rampLeftHigh.hw_timestamp == None):
            self.game.score(10)
        else:
            if(((self.game.switches.rampLeftLow.hw_timestamp - self.game.switches.rampLeftHigh.hw_timestamp) < 700) and
                (self.game.switches.rampLeftLow.hw_timestamp > self.game.switches.rampLeftHigh.hw_timestamp)):
                if (self.reverse_ramp_ready):
                    self.loopcompletedtt += 1
                    self.loopscompleted += 1
                    self.game.score(100 * self.loopcompletedtt * self.loopscompleted )
                else:
                    self.game.score(50)
                self.game.displayText("Think Tank Loop " + str(self.loopcompletedtt))
                self.cancel_delayed(name="disabler")
                self.delay(name="disabler", delay=2.0, handler=self.disable_ramp_readiness)
                self.forward_ramp_ready = True
                self.reverse_ramp_ready = True
            else:
                self.game.score(10)

    def sw_rampLeftHigh_active(self, sw):        
        if(self.game.switches.rampLeftLow.hw_timestamp == None):
            self.game.score(10)
        else:
            if (((self.game.switches.rampLeftHigh.hw_timestamp - self.game.switches.rampLeftLow.hw_timestamp) < 700) and
                (self.game.switches.rampLeftHigh.hw_timestamp > self.game.switches.rampLeftLow.hw_timestamp)):
                if (self.reverse_ramp_ready):
                    self.loopcompleteds9 += 1
                    self.loopscompleted += 1
                    self.game.score((100 * self.loopscompleted * self.loopcompleteds9))
                else:
                    self.game.score(50)
                self.game.displayText("Section 9 Loop " + str(self.loopcompleteds9))
                self.cancel_delayed(name="disabler")
                self.delay(name="disabler", delay=2.0, handler=self.disable_ramp_readiness)
                self.forward_ramp_ready = True
                self.reverse_ramp_ready = True
            else:
                self.game.score(10)

    def evt_ball_starting(self):
        self.loopscompleted = 0
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()


    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()
#        player.setState('max_loops_completed',self.loopscompleted)

    def disable_ramp_readiness(self):
        self.forward_ramp_ready = False
        self.reverse_ramp_ready = False
        self.loopcompletedtt = 0
        self.loopcompleteds9 = 0
        if (self.game.getPlayerState("max_loops_completed") < self.loopscompleted) :
            self.game.setPlayerState("max_loops_completed", self.loopscompleted)
            self.game.displayText("New Max Loops")
        else:
            self.game.displayText("Looping Ended")
        self.loopscompleted = 0
        #self.game.lamps.rampL.disable()
        #self.game.lamps.rampRight.disable()
