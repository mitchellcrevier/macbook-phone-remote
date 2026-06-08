import SwiftUI

struct ConnectView: View {
    @Binding var ip: String
    let failed: Bool
    let onConnect: () -> Void

    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            VStack(spacing: 32) {
                VStack(spacing: 8) {
                    Text("Mac Remote")
                        .font(.system(size: 28, weight: .semibold))
                        .foregroundColor(.white)
                    if failed {
                        Text("Couldn't reach your Mac. Check the IP and make sure `python app.py` is running.")
                            .font(.system(size: 13))
                            .foregroundColor(Color(red: 1.0, green: 0.35, blue: 0.35))
                            .multilineTextAlignment(.center)
                    } else {
                        Text("Enter your Mac's IP — both devices must be on the same Wi-Fi.")
                            .font(.system(size: 14))
                            .foregroundColor(Color(white: 0.5))
                            .multilineTextAlignment(.center)
                    }
                }

                VStack(spacing: 12) {
                    TextField(
                        "",
                        text: $ip,
                        prompt: Text("192.168.1.x").foregroundColor(Color(white: 0.3))
                    )
                    .keyboardType(.numbersAndPunctuation)
                    .autocorrectionDisabled()
                    .textInputAutocapitalization(.never)
                    .padding()
                    .background(Color(white: 0.1))
                    .cornerRadius(12)
                    .foregroundColor(.white)
                    .font(.system(size: 17, design: .monospaced))

                    Text("Find your Mac IP: open Terminal and run `ipconfig getifaddr en0`")
                        .font(.system(size: 12))
                        .foregroundColor(Color(white: 0.3))
                        .multilineTextAlignment(.center)
                }

                Button(action: onConnect) {
                    Text("Connect")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(.black)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(Color.white)
                        .cornerRadius(12)
                }
                .disabled(ip.isEmpty)
                .opacity(ip.isEmpty ? 0.4 : 1.0)
            }
            .padding(.horizontal, 28)
        }
    }
}
