"""
Floating cursor overlay — shows a large translucent circle that tracks the
system cursor position. Run as a subprocess; kill it to dismiss the overlay.
"""

import os
import sys

_LOG = open(os.path.join(os.path.dirname(__file__), "overlay.log"), "w", buffering=1)
def _log(msg):
    print(msg, file=_LOG, flush=True)

_log(f"starting pid={os.getpid()} python={sys.executable}")

import objc
from AppKit import (
    NSApplication,
    NSBorderlessWindowMask,
    NSBezierPath,
    NSColor,
    NSEvent,
    NSFloatingWindowLevel,
    NSMakeRect,
    NSScreen,
    NSTimer,
    NSView,
    NSWindow,
    NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSWindowCollectionBehaviorStationary,
)

CIRCLE_RADIUS = 36
OPACITY = 0.75
FILL = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.2, 0.1, 1.0)


class OverlayView(NSView):
    def drawRect_(self, rect):
        _log("drawRect")
        r = NSMakeRect(3, 3, CIRCLE_RADIUS * 2 - 6, CIRCLE_RADIUS * 2 - 6)
        path = NSBezierPath.bezierPathWithOvalInRect_(r)
        FILL.setFill()
        path.fill()
        path.setLineWidth_(3.0)
        NSColor.whiteColor().setStroke()
        path.stroke()


class AppDelegate(objc.lookUpClass("NSObject")):
    def applicationDidFinishLaunching_(self, note):
        for i, s in enumerate(NSScreen.screens()):
            _log(f"  screen {i}: frame={s.frame()} scale={s.backingScaleFactor()}")
        _log("didFinishLaunching")
        size = CIRCLE_RADIUS * 2

        self.win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, size, size),
            NSBorderlessWindowMask,
            2,
            False,
        )
        self.win.setBackgroundColor_(NSColor.clearColor())
        self.win.setOpaque_(False)
        self.win.setAlphaValue_(OPACITY)
        self.win.setLevel_(999)  # just below NSScreenSaverWindowLevel
        self.win.setIgnoresMouseEvents_(True)
        self.win.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces | NSWindowCollectionBehaviorStationary
        )

        view = OverlayView.alloc().initWithFrame_(NSMakeRect(0, 0, size, size))
        self.win.setContentView_(view)
        self.win.orderFrontRegardless()

        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1 / 60.0, self, "tick:", None, True
        )
        _log("window shown, timer scheduled")

    _tick_count = 0

    def tick_(self, timer):
        pos = NSEvent.mouseLocation()
        x = pos.x - CIRCLE_RADIUS
        y = pos.y - CIRCLE_RADIUS
        self.win.setFrameOrigin_((x, y))
        self._tick_count += 1
        if self._tick_count <= 5 or self._tick_count % 60 == 0:
            _log(f"tick #{self._tick_count}: cursor=({pos.x:.0f},{pos.y:.0f}) win=({x:.0f},{y:.0f})")


def main():
    _log("main()")
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(2)
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    _log("app.run()")
    app.run()
    _log("app.run() returned")


if __name__ == "__main__":
    main()
