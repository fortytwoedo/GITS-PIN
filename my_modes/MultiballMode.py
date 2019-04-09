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
        self.gameover_delay = 0
        self.jackpot_collected = 0
        self.jackpot_super_collected = 0
        pass

    def evt_player_added(self, player):
        player.setState('jackpot_collected_total',0)
        player.setState('jackpot_super_collected_total',0)
        
    def evt_ball_starting(self):
        self.jackpot_collected = self.game.getPlayerState("jackpot_collected_total")
        self.jackpot_super_collected = self.game.getPlayerState("jackpot_super_collected_total")
        
    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.game.setPlayerState("jackpot_collected_total", self.jackpot_collected)
        self.game.setPlayerState("jackpot_super_collected_total", self.jackpot_super_collected)
        
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
        if self.multiball_active: #IF MB was active reset settings, otherwise leave alone aka add a ball was active
            self.game.modes.add(self.game.laughingman_mode)#enable LaughingManMode
            self.multiball_active = False
            self.game.coils.backboxR.enable()
            self.game.coils.backboxG.enable()
            self.game.coils.backboxB.enable()
            self.jackpot_ready = False
            self.jackpot_switches = [False, False]
            self.mb_switches = [False, False, False]
            self.game.sound.fadeout_music()
            self.game.sound.play_music('base-music-bgm',-1)
        pass

    def launchBallIntoPlay(self, count=1, stealth=True):
        #Added to fix ball save issue
        self.game.trough.callback = None
        self.game.trough.launch_balls(num=count,stealth=stealth,callback=None)

    def sw_lock1_active(self, sw):
        if self.multiball_active:
            self.game.coils.lockdrop.patter(on_time=1, off_time=5, original_on_time=20)
            self.delay(name="disabler3", delay=4.0, handler=self.stop_lock_coil)
    
    def sw_lock1_active_for_1s(self, sw):
        #lock the first ball play sound animation?
        if not self.mb_switches[0]:
            self.game.trough.num_balls_locked = 1
            self.launchBallIntoPlay()
            self.mb_switches[0] = True
            self.game.coils.flasherlock.schedule(schedule=0xf0f0f000, cycle_seconds=1, now=True)
            logging.info("ball one locked")
            self.game.sound.play('tachleft')

    def sw_lock2_active_for_2s(self, sw):
        #lock the second ball play sound animation?
        if not self.mb_switches[1]:
            self.game.trough.num_balls_locked = 2
            self.launchBallIntoPlay()
            self.mb_switches[1] = True
            self.game.coils.flasherlock.schedule(schedule=0xf0f0f000, cycle_seconds=1, now=True)
            logging.info("ball two locked")
            self.game.sound.play('tachright')

    def sw_lock3_active_for_500ms(self, sw):
        #lock the first ball play sound animation?
        self.mb_switches[2] = True
        self.game.displayText("Multiball!!")
        self.game.coils.flasherlock.schedule(schedule=0xf0f0f0f0, cycle_seconds=10, now=True)
        self.game.sound.play('rightleftready')

    def sw_lock3_active_for_1s(self, sw): #Start Multiball
        self.launchBallIntoPlay()  #launch 4th ball into play
        #self.launchBallIntoPlay()  #launch 5th ball into play

    def sw_lock3_active_for_2s(self, sw): #Start Multiball
        self.game.modes.remove(self.game.laughingman_mode)#disable LaughingManMode
        self.multiball_active = True
        self.game.trough.num_balls_locked = 0
        self.game.coils.lockdrop.patter(on_time=1, off_time=5, original_on_time=18)  #self.game.coils['coilName'].patter(on_time=2, off_time=18, original_on_time=25)
        self.delay(name="disabler", delay=8.0, handler=self.stop_lock_coil)
        self.game.coils.backboxR.disable()
        self.game.coils.backboxG.disable()
        self.game.coils.backboxB.enable()
        self.game.sound.fadeout_music()
        self.game.sound.play_music('multiball',-1)
        self.game.enable_ball_saver()
        self.launchBallIntoPlay()  #launch 5th ball into play
        
    def stop_lock_coil(self):
        self.game.coils.lockdrop.disable()
        self.mb_switches = [False, False, False]
        
    def clear_scoop(self):
        self.game.coils.scoopR.pulse()

    def evt_balls_missing(self):
        self.game.coils.lockdrop.patter(on_time=1, off_time=5, original_on_time=18)  #self.game.coils['coilName'].patter(on_time=2, off_time=18, original_on_time=25)
        self.delay(name="disabler", delay=4.0, handler=self.stop_lock_coil)
        self.delay(name="scoopcoil", delay=5.0, handler=self.clear_scoop)
        self.mb_switches = [False, False, False]
        self.game.trough.num_balls_locked = 0
    
    def evt_game_ending(self):
        self.game.trough.num_balls_locked = 0
        #self.game.modes.add(self.game.laughingman_mode)#enable LaughingManMode
        self.multiball_active = False
        self.mb_switches = [False, False, False]
        self.game.coils.backboxR.enable()
        self.game.coils.backboxG.enable()
        self.game.coils.backboxB.enable()
        if (self.game.switches.lock1.is_active() or self.game.switches.lock2.is_active() or self.game.switches.lock2.is_active()): #new code
            self.game.coils.lockdrop.patter(on_time=1, off_time=5, original_on_time=18)  #self.game.coils['coilName'].patter(on_time=2, off_time=18, original_on_time=25)
            self.delay(name="disabler2", delay=4.0, handler=self.stop_lock_coil)
            self.delay(name="scoopcoil", delay=5.0, handler=self.clear_scoop)
            self.gameover_delay = 7 #do something
        else:
            self.gameover_delay = 0
        return self.gameover_delay # dont know if this is correct

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
            self.jackpot_ready = False
            self.jackpot_switches[0] = False
            self.jackpot_switches[1] = False
            self.jackpot_collected + 1
            if (self.jackpot_collected >= 10):
                self.game.displayText("SUPER JACKPOT!!!")
                self.game.score(20000)
                self.jackpot_collected = 0
            else:
                self.game.displayText("BETTER JACKPOT!!!")
                self.game.score(5000)
        return procgame.game.SwitchStop

    def sw_ScoopL_active_for_1s(self, sw):
        if self.multiball_active:
            self.game.displayText("OK JACKPOT")
            self.game.score(3000)
            self.game.coils.scoopL.pulse()

#    def sw_ScoopL_active_for_3s(self, sw):
#        self.db_enabled = False
#        self.game.coils.scoopL.pulse()