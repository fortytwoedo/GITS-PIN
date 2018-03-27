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

        pass

    def evt_player_added(self, player):
        player.setState('mode_complex_qualified',0)		

    def sw_StandUp2_active(self, sw):
        self.S2501_switches[0] = True
        #self.game.lamps.standupMidL.enable()
        self.game.sound.play('target-2')
        self.game.displayText('2')
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def sw_StandUp5_active(self, sw):
        self.S2501_switches[1] = True
        #self.game.lamps.standupMidL.enable()
        self.game.sound.play('target-5')
        self.game.displayText('5')
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def sw_StandUp0_active(self, sw):
        self.S2501_switches[2] = True
        #self.game.lamps.standupMidL.enable()
        self.game.sound.play('target-0')
        self.game.displayText('0')
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def sw_StandUp1_active(self, sw):
        self.S2501_switches[3] = True
        #self.game.lamps.standupMidL.enable()
        self.game.sound.play('target-1')
        self.game.displayText('1')
        self.checkAllSwitches()
        return procgame.game.SwitchStop

    def checkAllSwitches(self):
        """ called by each of the standupMid? handlers to
            determine if the bank has been completed """
        if(self.S2501_switches[0] and self.S2501_switches[1] and self.S2501_switches[2] and self.S2501_switches[3]): # all three are True
            self.game.displayText("Hurry-up and Dive into the PuppetMaster")
            self.game.score(1000)
            self.game.sound.play('puppetmaster2501')
            #self.layer = self.game.animations['puppet2']
            #self.game.lamps.standupMidL.disable()
            #self.game.lamps.standupMidC.disable()
            #self.game.lamps.standupMidR.disable()
            self.S2501_complete = True
            #self.qualified += 1
            #self.game.coils.droptarget.pulse()
            self.S2501_switches = [False, False, False, False]
            self.delay(name="pupdelay",delay=10.0, handler=self.reset_puppet_huryup)
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
            self.game.displayText("Puppetmaster Brain Dived")
            self.game.score(3000)
        else:
            self.game.score(100)

    def reset_puppet_huryup(self):			
        self.S2501_complete = False

    def evt_ball_starting(self):
        self.S2501_complete = False
        self.S2501_switches = [False, False, False, False]		
        #self.modecomplex = self.game.getPlayerState("mode_complex_qualified")		
        #self.game.coils.droptarget.pulse()
        #self.game.lamps.database1.disable()

    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.S2501_complete = False
        #self.game.setPlayerState("mode_complex_qualified", self.modecomplex)	
        #self.game.coils.droptarget.pulse()
        #self.game.lamps.database1.disable()

