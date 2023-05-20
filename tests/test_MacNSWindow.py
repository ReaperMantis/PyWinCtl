#!/usr/bin/env python
# encoding: utf-8

# Lawrence Akka - https://sourceforge.net/p/pyobjc/mailman/pyobjc-dev/thread/0B4BC391-6491-445D-92D0-7B1CEF6F51BE%40me.com/#msg27726282

# We need to import the relevant object definitions from PyObjC

import sys
assert sys.platform == "darwin"

import time

from AppKit import (
    NSApp, NSObject, NSApplication, NSMakeRect, NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable, NSBackingStoreBuffered)

import pywinctl


# Cocoa prefers composition to inheritance. The members of an object's
# delegate will be called upon the happening of certain events. Once we define
# methods with particular names, they will be called automatically
class Delegate(NSObject):

    npw = None
    demoMode = False

    def getDemoMode(self):
        return self.demoMode

    def setDemoMode(self):
        self.demoMode = True

    def unsetDemoMode(self):
        self.demoMode = False

    def applicationDidFinishLaunching_(self, aNotification: None):
        '''Called automatically when the application has launched'''
        # Set it as the frontmost application
        NSApp().activateIgnoringOtherApps_(True)
        for win in NSApp().orderedWindows():
            print(win.title(), win.frame(), type(win.frame().origin))

        if self.demoMode:

            if not self.npw:
                self.npw = pywinctl.getActiveWindow(NSApp())

                if self.npw:
                    print("ACTIVE WINDOW:", self.npw.title)

                    def moveChanged(pos):
                        print("CHANGED!!!", pos, self.npw.box if self.npw is not None else "", self.npw.rect if self.npw is not None else "")

                    self.npw.watchdog.start(movedCB=moveChanged)

                else:
                    print("NO ACTIVE WINDOW FOUND")
                    return

            wait = True
            timelap = 0.3

            self.npw.maximize(wait=wait)
            time.sleep(timelap)
            assert self.npw.isMaximized
            self.npw.restore(wait=wait)
            time.sleep(timelap)
            assert not self.npw.isMaximized

            self.npw.minimize(wait=wait)
            time.sleep(timelap)
            assert self.npw.isMinimized
            self.npw.restore(wait=wait)
            time.sleep(timelap)
            assert not self.npw.isMinimized

            self.npw.hide(wait=wait)
            time.sleep(timelap)
            assert not self.npw.visible
            self.npw.show(wait=wait)
            time.sleep(timelap)
            assert self.npw.visible

            # Test resizing
            print("RESIZE", self.npw.size)
            self.npw.resizeTo(600, 400, wait=wait)
            time.sleep(timelap)
            assert self.npw.size == (600, 400)
            assert self.npw.width == 600
            assert self.npw.height == 400

            print("RESIZEREL", self.npw.size)
            self.npw.resizeRel(10, 20, wait=wait)
            time.sleep(timelap)
            assert self.npw.size == (610, 420)
            assert self.npw.width == 610
            assert self.npw.height == 420

            # Test moving
            print("MOVE", self.npw.topleft)
            self.npw.moveTo(600, 300, wait=wait)
            time.sleep(timelap)
            assert self.npw.topleft == (600, 300)
            assert self.npw.left == 600
            assert self.npw.top == 300
            assert self.npw.right == 1210
            assert self.npw.bottom == 720
            assert self.npw.bottomright == (1210, 720)
            assert self.npw.bottomleft == (600, 720)
            assert self.npw.topright == (1210, 300)

            print("MOVEREL", self.npw.topleft)
            self.npw.moveRel(1, 2, wait=wait)
            time.sleep(timelap)
            assert self.npw.topleft == (601, 302)
            assert self.npw.left == 601
            assert self.npw.top == 302
            assert self.npw.right == 1211
            assert self.npw.bottom == 722
            assert self.npw.bottomright == (1211, 722)
            assert self.npw.bottomleft == (601, 722)
            assert self.npw.topright == (1211, 302)

            # Move via the properties
            print("RESIZE", self.npw.size)
            self.npw.resizeTo(601, 401, wait=wait)
            time.sleep(timelap)
            print("MOVE moveTo(100, 600)", self.npw.box, self.npw.rect)
            self.npw.moveTo(100, 600, wait=wait)
            time.sleep(timelap)

            print("MOVE left = 200", self.npw.box, self.npw.rect)
            self.npw.left = 200
            time.sleep(timelap)
            assert self.npw.left == 200

            print("MOVE right = 200", self.npw.box, self.npw.rect)
            self.npw.right = 200
            time.sleep(timelap)
            assert self.npw.right == 200

            print("MOVE top = 200", self.npw.box, self.npw.rect)
            self.npw.top = 200
            time.sleep(timelap)
            assert self.npw.top == 200

            print("MOVE bottom = 800", self.npw.box, self.npw.rect)
            self.npw.bottom = 800
            time.sleep(timelap)
            assert self.npw.bottom == 800

            print("MOVE topleft = (300, 400)", self.npw.box, self.npw.rect)
            self.npw.topleft = (300, 400)
            time.sleep(timelap)
            assert self.npw.topleft == (300, 400)

            print("MOVE topright = (300, 400)", self.npw.box, self.npw.rect)
            self.npw.topright = (300, 400)
            time.sleep(timelap)
            assert self.npw.topright == (300, 400)

            print("MOVE bottomleft = (300, 700)", self.npw.box, self.npw.rect)
            self.npw.bottomleft = (300, 700)
            time.sleep(timelap)
            assert self.npw.bottomleft == (300, 700)

            print("MOVE bottomright = (300, 900)", self.npw.box, self.npw.rect)
            self.npw.bottomright = (300, 900)
            time.sleep(timelap)
            assert self.npw.bottomright == (300, 900)

            print("MOVE midleft = (300, 400)", self.npw.box, self.npw.rect)
            self.npw.midleft = (300, 400)
            time.sleep(timelap)
            assert self.npw.midleft == (300, 400)

            print("MOVE midright = (300, 400)", self.npw.box, self.npw.rect)
            self.npw.midright = (300, 400)
            time.sleep(timelap)
            assert self.npw.midright == (300, 400)

            print("MOVE midtop = (300, 400)", self.npw.box, self.npw.rect)
            self.npw.midtop = (300, 400)
            time.sleep(timelap)
            assert self.npw.midtop == (300, 400)

            print("MOVE midbottom = (300, 700)", self.npw.box, self.npw.rect)
            self.npw.midbottom = (300, 700)
            time.sleep(timelap)
            assert self.npw.midbottom == (300, 700)

            print("MOVE center = (300, 400)", self.npw.box, self.npw.rect)
            self.npw.center = (300, 400)
            time.sleep(timelap)
            assert self.npw.center == (300, 400)

            print("MOVE centerx = 1000", self.npw.box, self.npw.rect)
            self.npw.centerx = 1000
            time.sleep(timelap)
            assert self.npw.centerx == 1000

            print("MOVE centery = 300", self.npw.box, self.npw.rect)
            self.npw.centery = 300
            time.sleep(timelap)
            assert self.npw.centery == 300

            print("RESIZE width = 600", self.npw.size)
            self.npw.width = 600
            time.sleep(timelap)
            assert self.npw.width == 600

            print("RESIZE height = 400", self.npw.size)
            self.npw.height = 400
            time.sleep(timelap)
            assert self.npw.height == 400

            print("RESIZE size = (810, 610)", self.npw.size)
            self.npw.size = (810, 610)
            time.sleep(timelap)
            assert self.npw.size == (810, 610)

            # Test lower and raise window
            print("LOWER")
            self.npw.lowerWindow()
            time.sleep(timelap)
            print("RAISE")
            self.npw.raiseWindow()
            time.sleep(timelap)

            # Test managing window stacking
            print("ALWAYS ON TOP")
            self.npw.alwaysOnTop()
            time.sleep(timelap)
            print("DEACTIVATE AOT")
            self.npw.alwaysOnTop(aot=False)
            time.sleep(timelap)
            print("ALWAYS AT BOTTOM")
            self.npw.alwaysOnBottom()
            time.sleep(timelap)
            print("DEACTIVATE AOB")
            self.npw.alwaysOnBottom(aob=False)
            time.sleep(timelap)
            print("SEND BEHIND")
            self.npw.sendBehind()
            time.sleep(timelap)
            print("BRING FROM BEHIND")
            self.npw.sendBehind(sb=False)
            time.sleep(timelap)

            # Test parent methods
            print("GET PARENT")
            parent = self.npw.getParent()
            assert self.npw.isChild(parent)

            # Test visibility
            print("HIDE")
            self.npw.hide()
            time.sleep(timelap)
            assert not self.npw.isVisible
            assert self.npw.isAlive
            print("SHOW")
            self.npw.show()
            time.sleep(timelap)
            assert self.npw.isVisible
            assert self.npw.isAlive

            # Test ClientFrame (called twice to assure no re-registration)
            print("CLIENT FRAME", self.npw.getClientFrame())
            print("CLIENT FRAME", self.npw.getClientFrame())

            # Test closing
            print("CLOSE")
            self.npw.watchdog.stop()
            self.npw.close()
            assert not self.npw.isVisible
            assert not self.npw.isAlive

    def windowWillClose_(self, aNotification: None):
        '''Called automatically when the window is closed'''
        print("Window has been closed")
        # Terminate the application
        NSApp().terminate_(self)

    def windowDidBecomeKey_(self, aNotification: None):
        print("Now I'm ACTIVE")


def demo():
    # Create a new application instance ...
    a = NSApplication.sharedApplication()
    # ... and create its delegate.  Note the use of the
    # Objective C constructors below, because Delegate
    # is a subclass of an Objective C class, NSObject
    delegate = Delegate.alloc().init()
    delegate.setDemoMode()
    # Tell the application which delegate object to use.
    a.setDelegate_(delegate)

    # Now we can start to create the window ...
    frame = NSMakeRect(400, 400, 250, 100)
    # (Don't worry about these parameters for the moment. They just specify
    # the type of window, its size and position etc)
    mask = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable
    w = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(frame, mask, NSBackingStoreBuffered, False)

    # ... tell it which delegate object to use (here it happens
    # to be the same delegate as the application is using)...
    w.setDelegate_(delegate)
    # ... and set some properties. Unicode strings are preferred.
    w.setTitle_(u'Hello, World!')
    # All set. Now we can show the window ...
    w.orderFrontRegardless()

    # ... and start the application
    a.run()
    #AppHelper.runEventLoop()


if __name__ == '__main__':
    demo()
