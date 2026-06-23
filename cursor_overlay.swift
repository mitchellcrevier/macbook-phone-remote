import Cocoa
import QuartzCore

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var circleLayer: CAShapeLayer!
    let size: CGFloat = 72
    var lastX: CGFloat = -9999
    var lastY: CGFloat = -9999

    func applicationDidFinishLaunching(_ n: Notification) {
        guard let screen = NSScreen.main else { return }
        let screenFrame = screen.frame

        window = NSWindow(
            contentRect: screenFrame,
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

        // Explicitly assign the root layer before the view goes into the window —
        // this guarantees it exists when we add the circle sublayer below.
        let rootLayer = CALayer()
        let contentView = NSView(frame: NSRect(origin: .zero, size: screenFrame.size))
        contentView.wantsLayer = true
        contentView.layer = rootLayer
        window.contentView = contentView
        window.orderFrontRegardless()

        // Build the circle once as a GPU shape layer — no CPU draw() on any future frame.
        circleLayer = CAShapeLayer()
        let r = CGRect(x: 0, y: 0, width: size, height: size).insetBy(dx: 3, dy: 3)
        circleLayer.path = CGPath(ellipseIn: r, transform: nil)
        circleLayer.fillColor = NSColor(red: 1, green: 0.2, blue: 0.05, alpha: 0.85).cgColor
        circleLayer.strokeColor = NSColor.white.cgColor
        circleLayer.lineWidth = 3
        circleLayer.bounds = CGRect(x: 0, y: 0, width: size, height: size)
        circleLayer.anchorPoint = CGPoint(x: 0.5, y: 0.5)
        circleLayer.isHidden = true  // hide until first position is set
        rootLayer.addSublayer(circleLayer)

        // Only update the layer position — zero window server cost per frame.
        // anchorPoint(0.5,0.5) means position = center of the circle.
        Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            let p = NSEvent.mouseLocation
            guard p.x != self.lastX || p.y != self.lastY else { return }
            self.lastX = p.x
            self.lastY = p.y
            CATransaction.begin()
            CATransaction.setDisableActions(true)
            self.circleLayer.isHidden = false
            // NSEvent.mouseLocation is in screen coordinates (origin = bottom-left of primary screen).
            // The content view layer has the same origin as the window, so subtract the screen offset.
            self.circleLayer.position = CGPoint(
                x: p.x - screenFrame.origin.x,
                y: p.y - screenFrame.origin.y
            )
            CATransaction.commit()
        }
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.accessory)
let delegate = AppDelegate()
app.delegate = delegate
app.run()
