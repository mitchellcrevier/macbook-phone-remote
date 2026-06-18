import Cocoa

class CircleView: NSView {
    override func draw(_ dirtyRect: NSRect) {
        let r = bounds.insetBy(dx: 3, dy: 3)
        let path = NSBezierPath(ovalIn: r)
        NSColor(red: 1, green: 0.2, blue: 0.05, alpha: 0.85).setFill()
        path.fill()
        path.lineWidth = 3
        NSColor.white.setStroke()
        path.stroke()
    }
    override var isOpaque: Bool { false }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    let size: CGFloat = 72

    func applicationDidFinishLaunching(_ n: Notification) {
        window = NSWindow(
            contentRect: NSRect(x: 100, y: 100, width: size, height: size),
            styleMask: .borderless,
            backing: .buffered,
            defer: false
        )
        window.backgroundColor = .clear
        window.isOpaque = false
        window.hasShadow = false
        window.ignoresMouseEvents = true
        window.level = NSWindow.Level(rawValue: 999)
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .ignoresCycle]
        window.contentView = CircleView(frame: NSRect(x: 0, y: 0, width: size, height: size))
        window.orderFrontRegardless()

        Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { _ in
            let p = NSEvent.mouseLocation
            self.window.setFrameOrigin(NSPoint(x: p.x - self.size / 2, y: p.y - self.size / 2))
        }
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.accessory)
let delegate = AppDelegate()
app.delegate = delegate
app.run()
