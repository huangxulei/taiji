class Router:
    def __init__(self, name, mode, number):
        self.name = name
        self.mode = mode
        self.number = number
        self.l3protocol = "arp, static, rip, eigrp, ospf, isis, bgp"

    def desc(self):
        print(f"This is {self.name}_{self.mode}_{self.number}router")
        print(f"l3func: {self.l3protocol}")


class Switch(Router):

    def __init__(self, name, mode, number, zone):
        self.zone = zone
        super().__init__(name, mode, number)

    def desc(self):
        print(
            f"This is {self.name}_{self.mode}_{self.number} switch. made in {self.zone}"
        )
        print(f"New feature: {self.l3protocol}")


class Firewall(Switch):

    def __init__(self, name, mode, number, zone):
        super().__init__(name, mode, number, zone)


if __name__ == "__main__":
    cisco = Router("CISCO", "NEXUS", "7010")
    cisco.desc()
    huawei = Switch("HUAWEI", "CE", "12808", "China")
    huawei.l3protocol = "css, vxlan, evpn, mbgp, srv6"
    huawei.desc()
    hillstone = Firewall("HILLSTONE", "SG", "5060", "China")
    hillstone.desc()
