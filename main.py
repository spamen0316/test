import random
from dataclasses import dataclass, field
from typing import List, Tuple

BANNER = r"""
=========================================
       TEXT AUTO-BATTLE ARENA
=========================================
"""


@dataclass
class Skill:
    name: str
    power: int
    accuracy: int
    cooldown: int
    current_cooldown: int = 0

    def ready(self) -> bool:
        return self.current_cooldown == 0

    def trigger(self) -> None:
        self.current_cooldown = self.cooldown

    def tick(self) -> None:
        if self.current_cooldown > 0:
            self.current_cooldown -= 1


@dataclass
class Fighter:
    name: str
    max_hp: int
    attack: int
    defense: int
    speed: int
    skills: List[Skill] = field(default_factory=list)
    hp: int = field(init=False)
    wins: int = 0

    def __post_init__(self) -> None:
        self.hp = self.max_hp

    def alive(self) -> bool:
        return self.hp > 0

    def reset(self) -> None:
        self.hp = self.max_hp
        for skill in self.skills:
            skill.current_cooldown = 0

    def take_damage(self, amount: int) -> int:
        damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        return damage

    def basic_attack(self) -> Tuple[str, int, int]:
        return ("basic", self.attack, 100)

    def choose_action(self) -> Tuple[str, int, int]:
        ready_skills = [skill for skill in self.skills if skill.ready()]
        if ready_skills:
            chosen = max(ready_skills, key=lambda s: s.power)
            chosen.trigger()
            return (chosen.name, chosen.power, chosen.accuracy)
        return self.basic_attack()

    def end_turn(self) -> None:
        for skill in self.skills:
            skill.tick()


@dataclass
class BattleResult:
    winner: Fighter
    loser: Fighter
    rounds: int
    log: List[str]


def generate_fighter(name: str, tier: int = 1) -> Fighter:
    base_hp = random.randint(80, 120) + (tier - 1) * 10
    attack = random.randint(12, 20) + (tier - 1) * 2
    defense = random.randint(4, 8) + (tier - 1)
    speed = random.randint(6, 12) + (tier - 1)
    skills = [
        Skill("Heavy Slash", power=attack + 6, accuracy=85, cooldown=2),
        Skill("Piercing Thrust", power=attack + 4, accuracy=90, cooldown=1),
    ]
    return Fighter(name=name, max_hp=base_hp, attack=attack, defense=defense, speed=speed, skills=skills)


def hit_success(accuracy: int) -> bool:
    return random.randint(1, 100) <= accuracy


def battle(fighter_a: Fighter, fighter_b: Fighter) -> BattleResult:
    log: List[str] = []
    rounds = 0

    while fighter_a.alive() and fighter_b.alive():
        rounds += 1
        log.append(f"-- Round {rounds} --")
        order = sorted([fighter_a, fighter_b], key=lambda f: f.speed, reverse=True)

        for actor in order:
            target = fighter_b if actor is fighter_a else fighter_a
            if not target.alive():
                break
            action_name, power, accuracy = actor.choose_action()
            if hit_success(accuracy):
                damage = target.take_damage(power)
                log.append(
                    f"{actor.name} uses {action_name}! {target.name} takes {damage} damage."
                )
            else:
                log.append(f"{actor.name} uses {action_name}, but misses!")
            log.append(f"{target.name} HP: {target.hp}/{target.max_hp}")
            actor.end_turn()

        log.append("")

    winner = fighter_a if fighter_a.alive() else fighter_b
    loser = fighter_b if winner is fighter_a else fighter_a
    return BattleResult(winner=winner, loser=loser, rounds=rounds, log=log)


def print_fighter_card(fighter: Fighter) -> None:
    print(
        f"{fighter.name} | HP {fighter.max_hp} | ATK {fighter.attack} | "
        f"DEF {fighter.defense} | SPD {fighter.speed}"
    )
    print(" Skills:")
    for skill in fighter.skills:
        print(f"  - {skill.name} (Power {skill.power}, Acc {skill.accuracy}%, CD {skill.cooldown})")


def build_opponent(wins: int) -> Fighter:
    tier = min(1 + wins, 5)
    name = random.choice(["Warden", "Rogue", "Valkyrie", "Titan", "Shade", "Harbinger", "Golem"])
    return generate_fighter(name, tier=tier)


def run_battle(player: Fighter, enemy: Fighter) -> bool:
    player.reset()
    enemy.reset()

    print("\n=== Match Start ===")
    print_fighter_card(player)
    print_fighter_card(enemy)
    print("")

    result = battle(player, enemy)
    for entry in result.log:
        print(entry)
    print(f"Winner: {result.winner.name} after {result.rounds} rounds!")

    if result.winner is player:
        player.wins += 1
        print(f"{player.name} win streak: {player.wins}")
        return True

    print(f"{player.name} was defeated. Win streak reset.")
    player.wins = 0
    return False


def prompt_menu() -> str:
    print("\nChoose an option:")
    print("1) Start Battle")
    print("2) View Fighter")
    print("3) Quit")
    return input("> ").strip()


def main() -> None:
    print(BANNER)
    player_name = input("Enter your fighter name: ").strip() or "Hero"
    player = generate_fighter(player_name)

    print("\nWelcome to the arena!")
    print_fighter_card(player)

    while True:
        choice = prompt_menu()
        if choice == "1":
            enemy = build_opponent(player.wins)
            run_battle(player, enemy)
        elif choice == "2":
            print("")
            print_fighter_card(player)
            print(f"Current win streak: {player.wins}")
        elif choice == "3":
            print("Farewell, champion!")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
