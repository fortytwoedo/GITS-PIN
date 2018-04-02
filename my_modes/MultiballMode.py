import procgame.game
from procgame.game import AdvancedMode
import logging
import random

class MultiballMode(procgame.game.AdvancedMode):
    def __init__(self, game):
        super(MultiballMode, self).__init__(game=game, priority=50, mode_type=AdvancedMode.Game)
        #self.layer = self.game.animations["HK"]
        self.logger = logging.getLogger('MultiballMode')
        self.mb_switches = [False, False, False]
        self.jackpot_switches = [False, False]
        self.multiball_active = False
        self.jackpot_ready = False
        pass

    def mode_started(self):
        #self.number = random.randint(1,5)
        #self.cancel_delayed(name="MultiballSkillShot")
        #self.game.displayText("Multiball!!"])
        #self.game.lamps["target%d" % self.number].schedule(0xf0f0f0)
        #self.delay(name="MultiballSkillShot", delay=10.0, handler=self.remove_self)
        #self.game.sound.fadeout_music()
        #self.game.sound.play_music('mb-pending-skillshot')
        pass

    def remove_self(self):
        self.game.modes.remove(self)
        self.game.sound.fadeout_music()
        #self.game.sound.play_music('base-music-bgm')

    def mode_stopped(self):
        pass

        
    def evt_single_ball_play(self):
        self.multiball_active = False
        self.game.coils.backboxR.enable()
        self.game.coils.backboxG.enable()
        self.game.coils.backboxB.enable()
        self.jackpot_ready = False
        self.jackpot_switches = [False, False]
        pass

    def launchBallIntoPlay(self, count=1, stealth=True):
        #Added to fix ball save issue
        self.game.trough.callback = None
        self.game.trough.launch_balls(num=count,stealth=stealth,callback=None)

    def sw_lock1_active(self, sw):
        if self.multiball_active:
            self.game.coils.lockdrop.patter(on_time=2, off_time=10, original_on_time=30)
            self.delay(name="disabler3", delay=4.0, handler=self.stop_lock_coil)
    
    def sw_lock1_active_for_300ms(self, sw):
        #lock the first ball play sound animation?
        if not self.mb_switches[0]:
            self.game.trough.num_balls_locked = 1
            self.launchBallIntoPlay()
            self.mb_switches[0] = True
            self.game.coils.flasherlock.schedule(schedule=0xf0f0f000, cycle_seconds=1, now=True)
            logging.info("ball one locked")

    def sw_lock2_active_for_500ms(self, sw):
        #lock the first ball play sound animation?
        if not self.mb_switches[1]:
            self.game.trough.num_balls_locked = 2
            self.launchBallIntoPlay()
            self.mb_switches[1] = True
            self.game.coils.flasherlock.schedule(schedule=0xf0f0f000, cycle_seconds=1, now=True)
            logging.info("ball two locked")

    def sw_lock3_active_for_300ms(self, sw):
        #lock the first ball play sound animation?
        self.mb_switches[2] = True
        self.game.displayText("Multiball!!")
        self.game.coils.flasherlock.schedule(schedule=0xf0f0f0f0, cycle_seconds=10, now=True)

    def sw_lock3_active_for_1s(self, sw): #Start Multiball
        self.multiball_active = True
        self.game.trough.num_balls_locked = 0
        self.game.coils.lockdrop.patter(on_time=2, off_time=10, original_on_time=30)  #self.game.coils['coilName'].patter(on_time=2, off_time=18, original_on_time=25)
        self.delay(name="disabler", delay=8.0, handler=self.stop_lock_coil)
        self.game.coils.backboxR.disable()
        self.game.coils.backboxG.disable()
        self.game.coils.backboxB.enable()
        
    def stop_lock_coil(self):
        self.game.coils.lockdrop.disable()
        self.mb_switches = [False, False, False]
        
    def evt_game_ending(self):
        self.game.coils.lockdrop.patter(on_time=2, off_time=10, original_on_time=30)  #self.game.coils['coilName'].patter(on_time=2, off_time=18, original_on_time=25)
        self.delay(name="disabler2", delay=5.0, handler=self.stop_lock_coil)
        self.game.trough.num_balls_locked = 0
        self.multiball_active = False
        self.game.coils.backboxR.enable()
        self.game.coils.backboxG.enable()
        self.game.coils.backboxB.enable()
        pass

    def sw_rampRight_active(self, sw):
        if self.multiball_active:
            self.jackpot_ready = True

    def sw_lockBashL_active(self, sw):
        if self.jackpot_ready:
            self.jackpot_switches[0] = True
            #self.game.lamps.standupMidL.enable()
            self.checkAllSwitches()
        return procgame.game.SwitchStop
        
    def sw_lockBashR_active(self, sw):
        if self.jackpot_ready:
            self.jackpot_switches[1] = True
            #self.game.lamps.standupMidL.enable()
            self.checkAllSwitches()
        
    def checkAllSwitches(self):
        if self.jackpot_ready and self.jackpot_switches[0] and self.jackpot_switches[1]:
            #award jackpot
            self.game.displayText("JACKPOT!!!")
            self.game.score(5000)
            self.jackpot_ready = False
            self.jackpot_switches[0] = False
            self.jackpot_switches[1] = False
        return procgame.game.SwitchStop