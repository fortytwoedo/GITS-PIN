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
        self.in_mode = False
        self.qualified = 0 # the number that are flashing
        self.collected = 0 # the number the player already has
        self.awards = [250000, 500000, 750000, 1000000, 3000000, 5000000]

        pass

    def evt_player_added(self, player):
        player.setState('mode_complex_qualified',0)
        player.setState('mode_complex_collected',0)

    def sw_dropMiss_active(self, sw):
        self.game.score(10)
        self.game.sound.play('sling')	

    def sw_dropG_active(self, sw):
        self.drop_switches[0] = True
        #self.game.lamps.standupMidL.enable()
        self.checkAllSwitches()
        return procgame.game.SwitchStop

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

    def sw_inlaneL_active(self, sw):
        self.drop_count = 0
        if self.drop_switches[0]:
            self.drop_count += 1
        if self.drop_switches[1]:
            self.drop_count += 1
        if self.drop_switches[2]:
            self.drop_count += 1
        if self.drop_switches[3]:
            self.drop_count += 1
        if self.drop_switches[4]:
            self.drop_count += 1
        if self.drop_count == 4:
            self.drop_switches = [True, True, True, True, True]
        #self.game.lamps.standupMidR.enable()
        self.checkAllSwitches()

    def sw_inlaneR_active(self, sw):
        self.drop_count = 0
        if self.drop_switches[0]:
            self.drop_count += 1
        if self.drop_switches[1]:
            self.drop_count += 1
        if self.drop_switches[2]:
            self.drop_count += 1
        if self.drop_switches[3]:
            self.drop_count += 1
        if self.drop_switches[4]:
            self.drop_count += 1
        if self.drop_count == 4:
            self.drop_switches = [True, True, True, True, True]
        #self.game.lamps.standupMidR.enable()
        self.checkAllSwitches()

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
                #self.db_enabled = True
                self.qualified += 1
                self.game.coils.flasherscoopL.schedule(schedule=0xA0FF0AA0, cycle_seconds=0, now=True)
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
        #self.db_enabled = False
        self.drop_switches = [False, False, False, False, False]
        self.qualified = self.game.getPlayerState("mode_complex_qualified")
        self.collected = self.game.getPlayerState("mode_complex_collected")
        self.game.coils.droptarget.pulse()
        if(self.qualified > self.collected):
            self.game.coils.flasherscoopL.schedule(schedule=0xA0FF0AA0, cycle_seconds=0, now=True)

    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.game.setPlayerState("mode_complex_qualified", self.qualified)
        self.game.setPlayerState("mode_complex_collected", self.collected)
        self.game.coils.flasherscoopL.disable()
        self.game.modes.remove(self.game.assemble_team_mode)
        if not (self.game.leftramp_mode in self.game.modes):
            self.game.modes.add(self.game.leftramp_mode)
        #disable assemble team mode enable loop score mode.

    def sw_ScoopL_active_for_500ms(self, sw):
        # advertise and start random award
        #self.game.lamps.database1.disable()
        if((self.qualified > self.collected)and not (self.game.assemble_team_mode in self.game.modes)): # you have qualified and started the ramp mode.  until end of ball or ramp mode is complete.
            self.game.displayText(["Complex Mode Achieved","1,000"])
            self.game.score(1000)
            self.game.sound.play('mode-qualify')
            self.collected += 1
            self.game.coils.flasherscoopL.disable()
            self.db_enabled = True
            self.game.modes.add(self.game.assemble_team_mode)
            self.game.modes.remove(self.game.leftramp_mode)
            #enable assemble team mode disable loop score mode.
        else:
            self.game.displayText("Drop GHOST Targets")
            self.game.score(250)
            self.game.sound.play('modenotready')

    def sw_ScoopL_active_for_1s(self, sw):
        if(not self.db_enabled):
            self.game.coils.scoopL.pulse()

    def sw_ScoopL_active_for_3s(self, sw):
        self.db_enabled = False
        self.game.coils.scoopL.pulse()

