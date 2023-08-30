# Wireshark
Une CheatSheet pour wireshark

## Filtering
```
ip.addr == <ip>
ip.src == <src ip> and ip.dst == <dst ip>
tcp.port eq <Port> or <Protocol Name>
udp.port eq <Port> or <Portocol Name>
apr.opcode==2      : Marque les reply ARP
arp.dst.proto_ipv4 : Marque les requeêtes ARP et réponses IPv4
```
