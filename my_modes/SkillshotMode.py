import procgame.game   #copied over from T2Master skillshot mode
from procgame.game import AdvancedMode   #copied over from T2Master skillshot

class SkillshotMode(procgame.game.AdvancedMode):

    def __init__(self, game):
        super(SkillshotMode,self).__init__(game=game, priority=20, mode_type=AdvancedMode.Game)

    def evt_ball_starting(self):
        self.game.sound.stop_music()
        #self.game.sound.play_music('skillshot')
        self.game.displayText("Hit the Tachikoma!")
        #self.game.coils.flasherramp.enable()    #flash tachkoma flasher
        self.game.coils.flasherramp.schedule(schedule=0xff00ff00, cycle_seconds=0, now=True)

    def deact(self):
        self.game.coils.flasherramp.disable()
        self.game.displayText("Skill Shot Missed")
        self.cancel_delayed("skilltimeout")
        self.game.modes.remove(self)

    def mode_started(self):
        self.delay(name="skilltimeout", delay=10.5, handler=self.deact)

    def sw_rampLeftHigh_active(self,sw):
        self.game.displayText("SKILL SHOT MADE")
        self.game.score(750) 
        #add 250 for every time this has been done per player.
        self.deact()

    def sw_slingL_active(self,sw):
        self.deact()
        
    def sw_slingR_active(self,sw):
        self.deact()
