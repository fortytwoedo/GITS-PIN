import procgame.game
from procgame.game import AdvancedMode
import logging

class LeftRampLoop(procgame.game.AdvancedMode):
    """
    Mode that tracks both forward and backward shots on left "loop" ramp.
    This ramp will also track combo shots between the left ramp forward and reverse and orbit
    """
    def __init__(self, game):
        super(LeftRampLoop, self).__init__(game=game, priority=44, mode_type=AdvancedMode.Game)
        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('LeftRampLoop')

        self.forward_ramp_ready = False
        self.reverse_ramp_ready = False
        self.combo_shots = [False, False, False, False] #track last event used for combo orbit, left forward, left reverse, Right Ramp
        self.combo_made = 0 # track what shot your on.
        self.rampfrenzy = 1 # ramp frenzy combo score multiplier 1 is normal score
        self.total_ramps_made = 0 # total game counter for loops for ramp frenzy mode
        self.loopscompleted = 0 # total concequitive ramps made, max looping done
        pass

    def evt_player_added(self, player):
        player.setState('Max_loops_completed',0)
        player.setState('Total_ramps_made',0)

    def sw_rampLeftLow_active(self, sw):
        if(self.game.switches.rampLeftHigh.hw_timestamp == None):
            self.game.score(10)
        else:
            if(((self.game.switches.rampLeftLow.hw_timestamp - self.game.switches.rampLeftHigh.hw_timestamp) < 700) and
                (self.game.switches.rampLeftLow.hw_timestamp > self.game.switches.rampLeftHigh.hw_timestamp)):
                if (self.reverse_ramp_ready): # completed Tachkoma ramp
                    self.loopcompletedtt += 1
                    self.loopscompleted += 1
                    self.game.score(100)
                else:
                    self.game.score(10)
                self.game.sound.play('letsroll')
                self.total_ramps_made += 1
                #self.game.displayText("Think Tank Loop " + str(self.loopcompletedtt))
                self.cancel_delayed(name="disabler")
                self.delay(name="disabler", delay=2.0, handler=self.disable_ramp_readiness)
                self.forward_ramp_ready = True
                self.reverse_ramp_ready = True
                if self.combo_shots[2]: #combo  code
                    self.combo_made = 0
                self.combo_shots = [False, False, True, False]
                self.combo_switch_check()
            else:
                self.game.score(10)

    def sw_rampLeftHigh_active(self, sw):        
        if(self.game.switches.rampLeftLow.hw_timestamp == None):
            self.game.score(10)
        else:
            if (((self.game.switches.rampLeftHigh.hw_timestamp - self.game.switches.rampLeftLow.hw_timestamp) < 700) and
                (self.game.switches.rampLeftHigh.hw_timestamp > self.game.switches.rampLeftLow.hw_timestamp)):
                if (self.reverse_ramp_ready): # completed section 9 ramp
                    self.loopcompleteds9 += 1
                    self.loopscompleted += 1
                    self.game.score(100)
                else:
                    self.game.score(10)
                self.game.sound.play('letsroll')
                self.total_ramps_made += 1
                #self.game.displayText("Section 9 Loop " + str(self.loopcompleteds9))
                self.cancel_delayed(name="disabler")
                self.delay(name="disabler", delay=2.0, handler=self.disable_ramp_readiness)
                self.forward_ramp_ready = True
                self.reverse_ramp_ready = True
                if self.combo_shots[1]: #combo code
                    self.combo_made = 0
                self.combo_shots = [False, True, False, False]
                self.combo_switch_check()
            else:
                self.game.score(10)
                
    def disable_combo_readiness(self):
        self.combo_made = 0
        self.combo_shots = [False, False, False, False]
    
    def combo_switch_check(self):
        self.combo_made += 1
        if self.combo_made > 1:
            self.game.displayText(str(self.combo_made) + " Way Combo")
            self.game.score(300 * self.combo_made * self.rampfrenzy) #reward
            if self.rampfrenzy > 1:
                self.game.sound.play("frenzy")
            else:
                self.game.sound.play("combo")
        self.cancel_delayed(name="combo")
        self.delay(name="combo", delay=3.5, handler=self.disable_combo_readiness)
        if self.total_ramps_made == 42 :
            self.game.displayText(str(self.total_ramps_made) + " ramps made... RAMP FRENZY make combos for super score")
            self.game.sound.play("frenzycombo")
            self.rampfrenzy = 3
            self.delay(name="rampdisabler", delay=20.0, handler=self.disable_ramp_frenzy)
        elif self.total_ramps_made < 42:
            self.game.displayText(str(self.total_ramps_made) + " ramps made... try to get to 42")

    def disable_ramp_frenzy(self):
        self.rampfrenzy = 1
        self.game.displayText("RAMP FRENZY ENDED")
        
    def sw_orbit_active(self, sw): 
        self.game.score(100)    
        self.game.coils.gate.patter(on_time=4, off_time=2, original_on_time=10)
        self.delay(name="orbit_disabler", delay=1.5, handler=self.stop_gate_coil)
        #combo code
        if self.combo_shots[0]:
            self.combo_made = 0
        self.combo_shots = [True, False, False, False]
        self.combo_switch_check()
        #play sound
        
    def sw_rampRight_active(self, sw):
        #combo code
        self.total_ramps_made += 1
        if self.combo_shots[3]:
            self.combo_made = 0
        self.combo_shots = [False, False, False, True]
        self.combo_switch_check()
        
    def stop_gate_coil(self):
        self.game.coils.gate.disable()
        
    def evt_ball_starting(self):
        self.loopscompleted = 0
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()
        self.total_ramps_made = self.game.getPlayerState("Total_ramps_made")

    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.cancel_delayed(name="disabler")
        self.cancel_delayed(name="rampdisabler")
        self.disable_ramp_readiness()
        self.game.setPlayerState("Total_ramps_made", self.total_ramps_made)

    def disable_ramp_readiness(self):
        self.forward_ramp_ready = False
        self.reverse_ramp_ready = False
        self.loopcompletedtt = 0
        self.loopcompleteds9 = 0
        if (self.game.getPlayerState("Max_loops_completed") < self.loopscompleted) :
            self.game.setPlayerState("Max_loops_completed", self.loopscompleted)
            self.game.displayText("New Max Loops")
        else:
            self.game.displayText("Looping Ended")
        self.loopscompleted = 0
        #self.game.lamps.rampL.disable()
        #self.game.lamps.rampRight.disable()
