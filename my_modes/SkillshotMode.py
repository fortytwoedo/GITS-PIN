import procgame.game   #copied over from T2Master skillshot mode
from procgame.game import AdvancedMode   #copied over from T2Master skillshot

class SkillshotMode(procgame.game.AdvancedMode):

    def __init__(self, game):
        super(SkillshotMode,self).__init__(game=game, priority=20, mode_type=AdvancedMode.Ball)
        self.skill_made = 0 #
    
    def evt_player_added(self, player):
        player.setState('skill_shot_completed',0)

    def evt_ball_starting(self):
        self.skill_shot_made = False
        self.skill_made = self.game.getPlayerState("skill_shot_completed")
        self.game.sound.stop_music()
        #self.game.sound.play_music('skillshot')
        self.game.displayText("Hit the Tachikoma!")
        self.game.coils.flasherramp.schedule(schedule=0x80808080, cycle_seconds=0, now=True)

    def deact(self):
        if self.skill_shot_made:
            self.game.displayText("SKILL SHOT MADE")
            self.skill_score = 750 + (self.skill_made * 250) # add 250 for every time this has been done per player.  
            self.game.score(self.skill_score)
            self.game.setPlayerState("skill_shot_completed", self.skill_made + 1)
        else:
            self.game.displayText("Skill Shot Missed")
        self.game.coils.flasherramp.disable()
        self.cancel_delayed("skilltimeout")
        self.game.modes.remove(self)

    def mode_started(self):
        self.delay(name="skilltimeout", delay=10.5, handler=self.deact)

    def sw_rampLeftHigh_active(self,sw):
        self.skill_shot_made = True
        self.deact()

    def sw_slingL_active(self,sw):
        self.deact()
        
    def sw_slingR_active(self,sw):
        self.deact()
