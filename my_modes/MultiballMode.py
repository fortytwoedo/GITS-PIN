import procgame.game
from procgame.game import AdvancedMode
import logging
import random

class MultiballMode(procgame.game.AdvancedMode):
    def __init__(self, game):
        super(MultiballMode, self).__init__(game=game, priority=50, mode_type=AdvancedMode.Game)
        #self.layer = self.game.animations["HK"]
        self.logger = logging.getLogger('MultiballMode')
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
        pass

    def launchBallIntoPlay(self, count=1, stealth=True):
        #Added to fix ball save issue
        self.game.trough.callback = None
        self.game.trough.launch_balls(num=count,stealth=stealth,callback=None)

    def sw_lock1_active_for_50ms(self, sw):
        #lock the first ball play sound animation?
        self.game.trough.num_balls_locked = 1
        self.launchBallIntoPlay()

    def sw_lock2_active_for_50ms(self, sw):
        #lock the first ball play sound animation?
        self.game.trough.num_balls_locked = 2
        self.launchBallIntoPlay()

    def sw_lock3_active_for_50ms(self, sw):
        #lock the first ball play sound animation?
        self.game.trough.num_balls_locked = 0
        self.game.displayText("Multiball!!")
        self.game.coils.lockdrop.pulsed_patter(5,2,100)
        


