from dataclasses import dataclass, field
from typing import List


@dataclass
class Player:
    """描述球员的类, 记录球员的信息"""

    name: str
    number: int
    position: str
    age: int


@dataclass
class Team:
    """描述球队的类， 球队包括队名称、队成员"""

    name: str
    players: List[Player]


james = Player("Lebron James", 23, "SF", 25)  # 实例化一个球员james
davis = Player("Anthony Davis", 3, "PF", 21)  # 实例化一个球员davis

lal = Team("Los Angeles Lakers", [james, davis])  # 实例化一个球队，将两个球员加入队中
print("Team name:{0},\nTeam members:{1}".format(lal.name, lal.players))
