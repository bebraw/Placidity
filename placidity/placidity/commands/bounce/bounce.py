from __future__ import absolute_import
from threads import RepeatingTimer
from visual import *

class Bounce:
    aliases = 'bounce'
    description = 'Amazing bouncing ball!'

    def __init__(self):
        self.timer = RepeatingTimer(0.01, self._update)
        self._init_done = False

    def _update(self):
        delta = 0.01
        self.ball.pos += self.ball.velocity * delta

        if self.ball.y < 1:
            self.ball.velocity.y *= -1
        else:
            self.ball.velocity.y -= 9.8 * delta

    def _init(self):
        self.floor = visual.box(length=4, height=0.5, width=4,
            color=visual.color.blue)

        self.ball = visual.sphere(pos=(0,4,0), color=visual.color.red)
        self.ball.velocity = visual.vector(0,-1,0)

        self._init_done = True

    def execute(self, expression, context):
        expression = expression.strip()

        if expression == 'quit':
            context.release()
            visual.scene.visible = False

            self.timer.cancel()

            return 'Quitting bounce!'
        elif context.owner != self:
            context.claim_for(self)
            visual.scene.visible = True

            if not self._init_done:
                self._init()

            self.timer.start()
