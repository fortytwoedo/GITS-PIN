import procgame.game
from procgame.game import AdvancedMode
import logging

class BackboxMode(procgame.game.AdvancedMode):
    """
    The mode that is running during "normal" gameplay
    """

    def __init__(self, game):
        """
        The __init__ function is called automatically whenever an instance is created
        """

        # a call to 'super' is required
        # notice we set the mode type and the priority
        super(BackboxMode, self).__init__(game=game, priority=6, mode_type=AdvancedMode.System)

    def mode_started(self):
        """
        the mode_started method is called whenever this mode is added
        to the mode queue; this might happen multiple times per game,
        depending on how the Game itself adds/removes it.  B/C this is
        an advancedMode, we know when it will be added/removed.
        """
        self.game.coils.backboxR.enable()
        self.game.coils.backboxG.enable()
        self.game.coils.backboxB.enable()
        pass

    def mode_stopped(self):
        """
        the mode_stopped method is called whenever this mode is removed
        from the mode queue; this might happen multiple times per game,
        depending on how the Game itself adds/removes it
        """
        pass
