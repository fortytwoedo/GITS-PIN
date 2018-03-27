import procgame.game
from procgame.game import AdvancedMode
import logging

class LaughingManMode(procgame.game.AdvancedMode):
    """
    Example of T2 "Database" functionality
    --random award on lockLeft if database is lit
    knockdown of droptarget awards database

    TODO: Sound effects, other visual feedback??

    """
    def __init__(self, game):
        super(LaughingManMode, self).__init__(game=game, priority=29, mode_type=AdvancedMode.Game)

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('LaughingMan')

        self.db_enabled = False

        self.awards = [250000, 500000, 750000, 1000000, 3000000, 5000000]

        pass

    def evt_player_added(self, player):
        player.setState('mode_complex_qualified',0)	

    def sw_dropMiss_active(self, sw):
        self.game.score(10)
        self.game.sound.play('sling')	
		
    def sw_dropG_active(self, sw):
        self.drop_switches[0] = True
        #self.game.lamps.standupMidL.enable()
        self.checkAllSwitches()
        return procgame.game.SwitchStop
        #self.db_enabled = True
        #self.game.lamps.database1.enable()

    def sw_dropH_active(self, sw):
        self.drop_switches[1] = True
        #self.game.lamps.standupMidL.enable()
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def sw_dropO_active(self, sw):
        self.drop_switches[2] = True
        #self.game.lamps.standupMidC.enable()
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def sw_dropS_active(self, sw):
        self.drop_switches[3] = True
        #self.game.lamps.standupMidR.enable()
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def sw_dropT_active(self, sw):
        self.drop_switches[4] = True
        #self.game.lamps.standupMidR.enable()
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def checkAllSwitches(self):
        """ called by each of the standupMid? handlers to
            determine if the bank has been completed """
        if(self.drop_switches[0] and self.drop_switches[1] and self.drop_switches[2] and self.drop_switches[3] and self.drop_switches[4]): # all three are True
                self.game.displayText("Shoot the Left Scoop!")
                self.game.score(1000)
                self.game.sound.play('target_bank')
                #self.game.lamps.standupMidL.disable()
                #self.game.lamps.standupMidC.disable()
                #self.game.lamps.standupMidR.disable()
                self.db_enabled = True
                #self.qualified += 1
                self.game.coils.droptarget.pulse()
                self.drop_switches = [False, False, False, False, False]
                #self.sync_lamps_to_progress()
        else:
                self.game.score(10)
                self.game.sound.play('target')
#        self.debug()

#    def debug(self):
#        self.logger.info("qualified = %d; collected = %d" % (self.db_enabled))

    def evt_ball_starting(self):
        self.db_enabled = False
        self.drop_switches = [False, False, False, False, False]
        self.modecomplex = self.game.getPlayerState("mode_complex_qualified")		
        self.game.coils.droptarget.pulse()
        #self.game.lamps.database1.disable()

    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.game.setPlayerState("mode_complex_qualified", self.modecomplex)	
        #self.game.coils.droptarget.pulse()
        #self.game.lamps.database1.disable()

    def sw_ScoopL_active_for_500ms(self, sw):
        # advertise and start random award
        #self.game.lamps.database1.disable()
        if(self.db_enabled):
            self.game.displayText(["Complex Mode Achieved","1,000"])
            self.game.score(1000)
            self.game.sound.play('mode-qualify')
        else:
            self.game.displayText("Nothing")
            self.game.score(250)
            self.game.sound.play('modenotready')

    def sw_ScoopL_active_for_1s(self, sw):
        if(not self.db_enabled):
            self.game.coils.scoopL.pulse()

    def sw_ScoopL_active_for_3s(self, sw):
        self.db_enabled = False
        self.game.coils.scoopL.pulse()

