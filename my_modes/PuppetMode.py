import procgame.game
from procgame.game import AdvancedMode
import logging

class PuppetMode(procgame.game.AdvancedMode):
    """
    Example of T2 "Database" functionality
    --random award on lockLeft if database is lit
    knockdown of droptarget awards database

    TODO: Sound effects, other visual feedback??

    """
    def __init__(self, game):
        super(PuppetMode, self).__init__(game=game, priority=42, mode_type=AdvancedMode.Game)

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('puppetmode')

        self.S2501_complete = False
        self.awards = [250000, 500000, 750000, 1000000, 3000000, 5000000]
        self.cyborg_defeated = 0

        pass

    def evt_player_added(self, player):
        player.setState('Cyborg_Defeated',0)

    def sw_StandUpC_active(self, sw):
        if self.S2501_switches[0] == False:
            self.S2501_switches[0] = True
            #self.game.lamps.standupMidL.enable()
            self.game.sound.play('target-C')
            self.game.displayText('C')
            self.checkAllSwitches()
        else:
            self.game.sound.play('miss')
        return procgame.game.SwitchStop
        
    def sw_StandUpY_active(self, sw):
        if self.S2501_switches[1] == False:
            self.S2501_switches[1] = True
            #self.game.lamps.standupMidL.enable()
            self.game.sound.play('target-Y')
            self.game.displayText('Y')
            self.checkAllSwitches()
        else:
            self.game.sound.play('miss')
        return procgame.game.SwitchStop
        
    def sw_StandUpB_active(self, sw):
        if self.S2501_switches[2] == False:
            self.S2501_switches[2] = True
            #self.game.lamps.standupMidL.enable()
            self.game.sound.play('target-B')
            self.game.displayText('B')
            self.checkAllSwitches()
        else:
            self.game.sound.play('miss')
        return procgame.game.SwitchStop

    def sw_StandUpO_active(self, sw):
        if self.S2501_switches[3] == False:
            self.S2501_switches[3] = True
            #self.game.lamps.standupMidL.enable()
            self.game.sound.play('target-O')
            self.game.displayText('O')
            self.checkAllSwitches()
        else:
            self.game.sound.play('miss')
        return procgame.game.SwitchStop

    def sw_StandUpR_active(self, sw):
        if self.S2501_switches[4] == False:
            self.S2501_switches[4] = True
            #self.game.lamps.standupMidL.enable()
            self.game.sound.play('target-R')
            self.game.displayText('R')
            self.checkAllSwitches()
        else:
            self.game.sound.play('miss')
        return procgame.game.SwitchStop

    def sw_StandUpG_active(self, sw):
        if self.S2501_switches[5] == False:
            self.S2501_switches[5] = True
            #self.game.lamps.standupMidL.enable()
            self.game.sound.play('target-G')
            self.game.displayText('G')
            self.checkAllSwitches()
        else:
            self.game.sound.play('miss')
        return procgame.game.SwitchStop

    def checkAllSwitches(self):
        """ called by each of the standupMid? handlers to
            determine if the bank has been completed """
        if(self.S2501_switches[0] and self.S2501_switches[1] and self.S2501_switches[2] and self.S2501_switches[3] and self.S2501_switches[4] and self.S2501_switches[5]): # all six are True
            self.game.displayText("Cyborg BATTLE!")
            self.game.score(1000)
            self.game.sound.play('cyborgbattle')
            self.delay(name="sounddelay",delay=1.0, handler=self.play_next_sound)
            #self.layer = self.game.animations['puppet2']
            #self.game.lamps.standupMidL.disable()
            #self.game.lamps.standupMidC.disable()
            #self.game.lamps.standupMidR.disable()
            self.S2501_complete = True
            #self.qualified += 1
            #self.game.coils.droptarget.pulse()
            self.S2501_switches = [False, False, False, False, False, False]
            self.delay(name="pupdelay",delay=15.0, handler=self.reset_puppet_huryup)
            self.game.coils.flasherlock.enable()
        else:
            self.game.score(10)
            #self.game.sound.play('target')
            #        self.debug()

            #    def debug(self):
            #        self.logger.info("qualified = %d; collected = %d" % (self.db_enabled))

    def sw_rampRight_active(self, sw):
        if(self.S2501_complete):
            #self.game.sound.play('target-0')
            self.S2501_complete = False
            self.game.displayText("Cyborg Brain Dived")
            self.cyborg_defeated += 1
            self.game.score(3000 * self.cyborg_defeated)
            self.game.sound.play('pm-complete')
        else:
            self.game.score(100)
            self.game.sound.play('door')

    def reset_puppet_huryup(self): 
        self.S2501_complete = False
        self.game.coils.flasherlock.disable()

    def play_next_sound(self): #play instruction sounds
        self.game.sound.play('shootdiveramp')

    def evt_ball_starting(self):
        self.S2501_complete = False
        self.S2501_switches = [False, False, False, False, False, False]
        self.cyborg_defeated = self.game.getPlayerState("Cyborg_Defeated")
        #self.modecomplex = self.game.getPlayerState("mode_complex_qualified")
        #self.game.coils.droptarget.pulse()
        #self.game.lamps.database1.disable()

    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.S2501_complete = False
        self.game.setPlayerState("Cyborg_Defeated", self.cyborg_defeated)
        #self.game.setPlayerState("mode_complex_qualified", self.modecomplex)
        #self.game.coils.droptarget.pulse()
        #self.game.lamps.database1.disable()

