import SwiftUI

struct ContentView: View {
    @AppStorage("serverIP") private var serverIP = ""
    @State private var pendingIP = ""
    @State private var isConnected = false
    @State private var loadFailed = false

    var body: some View {
        if isConnected && !loadFailed, let url = URL(string: "http://\(serverIP):5050") {
            WebView(url: url, onError: {
                isConnected = false
                loadFailed = true
            })
            .ignoresSafeArea()
        } else {
            ConnectView(ip: $pendingIP, failed: loadFailed) {
                serverIP = pendingIP
                loadFailed = false
                isConnected = true
            }
            .onAppear {
                pendingIP = serverIP
                if !serverIP.isEmpty && !loadFailed {
                    isConnected = true
                }
            }
        }
    }
}
