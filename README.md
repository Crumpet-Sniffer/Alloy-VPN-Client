Welcome to Alloy!

Alloy was officially started on 13/03/2026.

I made alloy because I use linux on my laptop, and I use multiple VPNs for different use cases. It's often hard to keep track of which one I'm using. Also turning on/off each one is a pain, especially as 2/3 of the ones I use have no GUI in linux. So I made Alloy, a 100% python VPN GUI where I can manage all my VPNs in one place.

As of V0.3:
I have added support for these VPNs:

Cloudflare Warp

Tailscale

Mullvad

Wireguard (Not in all versions*)

Just because it's not in this list doesn't mean I don't want to/can't add it. If you can let me know, I can try to add support for it! My discord is at the bottom if you have any requests!

No GUI yet
I know I know, the point was a GUI... but this is better than nothing and it's pretty easy to use. I will add a GUI in an update soon, I just need to learn tkinter first.

*As of V0.3, I have added support for wireguard .conf files. The CLI syntax to use wireguard configs is different between linux and windows, and so I had to make seperate branches for linux and windows. They will share the exact same features going forwards, but it was necessarry to make multiple versions. You also need admin access in windows to add wireguard configs, so I created a seperate branch for this it's not ideal but while admin is necessary, I will keep them in seperate branches.

For any enquiries regarding Alloy, you can reach me on my discord @crumpet_sniffer
