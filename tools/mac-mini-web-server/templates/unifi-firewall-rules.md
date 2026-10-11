# UniFi: server VLAN and firewall rules

Recommendation, not mined history: the source project set this up once and it never
caused an incident. Verify menu names against your UniFi Network version.

## Networks
| Name | VLAN | Subnet | DHCP | Notes |
|---|---|---|---|---|
| Default (home) | 1 | 192.168.1.0/24 | on | laptops, phones, TV |
| Servers | 20 | 192.168.20.0/24 | on | the mini; reservation for its Ethernet MAC → 192.168.20.10 |
| IoT (optional) | 30 | 192.168.30.0/24 | on | cameras, plugs |

"Isolate network" stays OFF on Servers — isolation is done by the rules below so you can
allow the one exception you need (e.g. a NAS).

## Firewall rules — LAN In, in this order
1. **Allow** Servers → Servers
2. **Allow** established/related (return traffic)
3. **Drop** Servers → Default, IoT, Guest (every other local network)
4. (optional) **Allow** Default → Servers, TCP 22 only — or skip and admin only over Tailscale (default)
5. Servers → Internet: allowed (the tunnel and Tailscale are outbound-only)

## Port forwarding
None. Nothing in the guide needs an inbound port. A forward you didn't create is a finding.

## Physical
- Mini on wired Ethernet; its switch port native VLAN = Servers (or tag on the Mac side).
- A PoE access point behind a new switch: the switch must be PoE or use an **active**
  802.3af/at injector. A non-PoE switch leaves the AP dark with no link light — looks like
  a dead cable.
- Record the mini's Ethernet MAC at first boot; at a hardware swap move the DHCP
  reservation to the new MAC so the IP follows.

## Gotcha
A NAS on the home LAN is unreachable from the server by design. Reach it over Tailscale
(join the NAS to the tailnet, disable key expiry, turn disk hibernation off), or move the
NAS to the Servers VLAN. Keep one LAN-side recovery path and test it.
