import procgame.game   #copied over from T2Master skillshot mode
from procgame.game import AdvancedMode   #copied over from T2Master skillshot

class SkillshotMode(procgame.game.AdvancedMode):

    def __init__(self, game):
        super(SkillshotMode,self).__init__(game=game, priority=20, mode_type=AdvancedMode.Ball)
        self.skill_made = 0 #
        self.LIONMAN = True
        self.flag = False
    
    def evt_player_added(self, player):
        player.setState('skill_shot_completed',0)

    def evt_ball_starting(self):
        self.skill_shot_made = False
        self.skill_made = self.game.getPlayerState("skill_shot_completed")
        self.game.sound.stop_music()
        self.game.sound.play_music('gameintro')
        self.game.displayText("Hit the Tachikoma!")
        self.game.coils.flasherramp.schedule(schedule=0x80808080, cycle_seconds=0, now=True)

    def deact(self):
        if self.skill_shot_made:
            self.game.displayText("SKILL SHOT MADE")
            self.skill_score = 750 + (self.skill_made * 250) # add 250 for every time this has been done per player.  
            self.game.score(self.skill_score)
            self.game.setPlayerState("skill_shot_completed", self.skill_made + 1)
            self.game.sound.play('skillshotmade')
            if self.LIONMAN:
                self.game.displayText("LIONMAN!!!!!!")
        else:
            self.game.displayText("Skill Shot Missed")
            self.game.sound.play('skillshotfail')
        self.game.coils.flasherramp.disable()
        self.cancel_delayed("skilltimeout")
        self.game.modes.remove(self)
        self.game.sound.stop_music()
        self.game.sound.play_music('base-music-bgm',-1)

    def mode_started(self):
        #self.delay(name="skilltimeout", delay=10.5, handler=self.deact)
        self.flag = False
        #self.game.sound.stop_music()
        #self.game.sound.play_music('gameintro',-1)
        pass

    def sw_shooter_inactive_for_250ms(self, sw):
        # ball saver syntax has changed.  We no longer need to supply a callback
        # method instead, evt_ball_saved() will be called if a ball is saved.
        # to enable it, use this 
        # (defaults are 1 ball, save time length is based on service mode setting)
        self.game.enable_ball_saver()
        if not self.flag:
            self.delay(name="skilltimeout", delay=10.5, handler=self.deact)
            self.flag = True

    def sw_rampLeftHigh_active(self,sw):
        self.skill_shot_made = True
        self.deact()

    def sw_inlaneL_active(self,sw):
        self.skill_shot_made = True
        self.deact()

    def sw_inlaneR_active(self,sw):
        self.deact()

    def sw_outlaneL_active(self,sw):
        self.deact()

    def sw_outlaneR_active(self,sw):
        self.deact()

    def sw_rampLeftLow_active(self,sw):
        self.deact()
        
    def sw_slingL_active(self,sw):
        self.deact()
        
    def sw_slingR_active(self,sw):
        self.deact()
