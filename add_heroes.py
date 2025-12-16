"""
Seed/update Heroes + their synergies/counters.

Run from backend/:
    py add_heroes.py
"""

import os
import re
from pathlib import Path

import django
from django.conf import settings
from django.core.files import File

# -------------------------
# Django setup (must be before importing models)
# -------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marvel_rivals.settings")
django.setup()

from heroes.models import Hero  # noqa: E402


def safe_name(name: str) -> str:
    """
    Convert hero.name into a filesystem-friendly filename base.

    Examples:
      "Peni-Parker" -> "Peni-Parker"
      "Cloak & Dagger" -> "Cloak_Dagger"
      "Adam Warlock" -> "Adam_Warlock"
    """
    name = name.strip()
    name = name.replace("&", " ")
    name = re.sub(r"\s+", "_", name)          # spaces -> _
    name = re.sub(r"[^A-Za-z0-9_-]", "", name)  # remove weird chars
    return name


def attach_media_if_exists(hero: Hero) -> None:
    base = safe_name(hero.name)

    avatar_filename = f"{base}_Deluxe_Avatar.png"
    banner_filename = f"{base}_banner.png"

    assets_root = Path(settings.BASE_DIR) / "assets" / "heroes"
    avatar_path = assets_root / "avatars" / avatar_filename
    banner_path = assets_root / "banners" / banner_filename

    changed = False

    # FORCE upload once (recommended to fix your current broken DB pointers)
    FORCE_UPLOAD = os.environ.get("FORCE_HERO_MEDIA_UPLOAD", "0") == "1"

    if avatar_path.exists():
        if FORCE_UPLOAD or not hero.image:
            with avatar_path.open("rb") as f:
                hero.image.save(avatar_filename, File(f), save=False)
            changed = True
    else:
        print(f"  ! Missing avatar file for {hero.name}: {avatar_path.name}")

    if banner_path.exists():
        if FORCE_UPLOAD or not hero.banner:
            with banner_path.open("rb") as f:
                hero.banner.save(banner_filename, File(f), save=False)
            changed = True
    else:
        print(f"  ! Missing banner file for {hero.name}: {banner_path.name}")

    if changed:
        hero.save()

#--------------------------
# Data
# -------------------------

heroes_data = [
    # VANGUARDS (Tanks)
    {
        'name': 'Magneto',
        'role': 'VANGUARD',
        'description': 'Master of magnetism. Nice peel and fine burst damage. Creates shields.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'shield', 'area-control', 'peel'],
        'synergies': ['Scarlet Witch', 'Gambit'],
        'counters': ['Iron Man', 'The Punisher', 'Cloak & Dagger'],
    },
    {
        'name': 'Doctor Strange',
        'role': 'VANGUARD',
        'description': 'Sorcerer Supreme. Nice burst damage and best shield for frontline.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'shield', 'teleport', 'utility'],
        'synergies': ['Scarlet Witch', 'Magik'],
        'counters': ['Hela', 'Hawkeye', 'Black Panther', 'Iron Man'],
    },
    {
        'name': 'Venom',
        'role': 'VANGUARD',
        'description': 'Symbiote tank. High sustain and crowd control.',
        'difficulty': 3,
        'playstyle_tags': ['tank', 'sustain', 'dive', 'cc'],
        'synergies': ['Spider-Man', 'Hela', 'Jeff The Land Shark', 'Magneto'],
        'counters': ['Hela', 'Luna Snow', 'Invisible Woman', 'Cloak & Dagger'],
    },
    {
        'name': 'Hulk',
        'role': 'VANGUARD',
        'description': 'Raw power and disruption. Mobile playstyle to dive and get out.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'dive', 'disruption', 'sustain', 'shield'],
        'synergies': ['Luna Snow', 'Rocket Raccoon', 'Magneto', 'Wolverine', 'Daredevil'],
        'counters': ['Mantis', 'Hawkeye', 'Luna Snow',],
    },
        {
        'name': 'Angela',
        'role': 'VANGUARD',
        'description': 'Flying mobile Vanguard. High burst damage with fast capability of getting out.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'dive', 'disruption', 'sustain', 'shield'],
        'synergies': ['Luna Snow', 'Thor',],
        'counters': ['The Punisher', 'Storm', 'Iron Man', 'Groot'],
    },
        {
        'name': 'Emma Frost',
        'role': 'VANGUARD',
        'description': 'Jack of all trades. Has good damage, good shield, AoE ultimate and damage reduction.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'cc', 'disruption', 'sustain', 'shield'],
        'synergies': ['Psylocke', 'Magneto', ],
        'counters': ['Black Panther', 'Spider-Man', 'Psylocke', 'Iron Fist', 'Magik', 'Wolverine', 'Daredevil'],
    },
            {
        'name': 'Peni-Parker',
        'role': 'VANGUARD',
        'description': 'Base.',
        'difficulty': 1,
        'playstyle_tags': ['tank', 'sustain', 'disruption', 'healing', 'cc'],
        'synergies': ['Rocket Raccoon', 'Jeff The Land Shark', 'Mantis'],
        'counters': ['Black Panther', 'Spider-Man', 'Psylocke', 'Iron Fist', 'Magik', 'Wolverine', 'Daredevil'],
    },
            {
        'name': 'The Thing',
        'role': 'VANGUARD',
        'description': 'OG counter for dives. Has high health, high damage and mobility cancelling ability.',
        'difficulty': 1,
        'playstyle_tags': ['tank', 'dive', 'disruption', 'sustain', 'anti-mobility'],
        'synergies': ['Invisible Woman', 'Human Torch', 'Wolverine'],
        'counters': ['Black Panther', 'Spider-Man', 'Psylocke', 'Iron Fist', 'Magik', 'Wolverine', 'Daredevil'],
    },
            {
        'name': 'Groot',
        'role': 'VANGUARD',
        'description': 'High health wall builder AoE enemy stack ultimate Vanguard. Solid frontline presence.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'healing', 'disruption', 'sustain'],
        'synergies': ['Psylocke', 'Magneto', ],
        'counters': ['Black Panther', 'Spider-Man'],
    },
            {
        'name': 'Thor',
        'role': 'VANGUARD',
        'description': 'Damage focused frontline Vanguard. High burst damage and solid crowd control with ultimate.',
        'difficulty': 2,
        'playstyle_tags': ['tank', 'dive', 'disruption', 'sustain', 'cc'],
        'synergies': ['Angela', 'Magneto', ],
        'counters': ['Black Panther', 'Spider-Man', 'Psylocke',  'Magik'],
    },
            {
        'name': 'Captain America',
        'role': 'VANGUARD',
        'description': 'High mobility demon. Has all the stats in high levels making him a solid all-rounder Vanguard.',
        'difficulty': 3,
        'playstyle_tags': ['tank', 'dive', 'disruption', 'sustain', 'cc'],
        'synergies': ['Winter Soldier', 'Magneto', ],
        'counters': ['Black Panther', 'Spider-Man', 'Psylocke', 'Daredevil'],
    },
                {
        'name': 'Rogue',
        'role': 'VANGUARD',
        'description': 'Power absorber. High sustain and disruption with solid damage.',
        'difficulty': 3,
        'playstyle_tags': ['tank', 'dive', 'disruption', 'sustain', 'cc'],
        'synergies': ['Gambit', 'Magneto', ],
        'counters': ['Black Panther', 'Spider-Man', 'Psylocke', 'Captain America'],
    },
    
    
    
    
    
    # DUELISTS (DPS)
    {
        'name': 'Spider-Man',
        'role': 'DUELIST',
        'description': 'Web-slinging flanker. High mobility and burst damage.',
        'difficulty': 3,
        'playstyle_tags': ['flanker', 'mobility', 'dive', 'burst-damage', 'mobile'],
        'synergies': ['Luna Snow', 'Daredevil', 'Venom'],
        'counters': ['Scarlet Witch', 'Iron Man', 'Adam Warlock'],
    },
    {
        'name': 'Iron Man',
        'role': 'DUELIST',
        'description': 'Flying DPS with powerful poke damage.',
        'difficulty': 2,
        'playstyle_tags': ['flyer', 'burst-damage', 'mobility', 'poke'],
        'synergies': ['Magneto', 'Luna Snow', 'Ultron', 'Squirrel Girl'],
        'counters': ['Groot', 'The Thing', 'Venom', 'Peni Parker', 'Ultron', 'Human Torch'],
    },
    {
        'name': 'Scarlet Witch',
        'role': 'DUELIST',
        'description': 'Balance of poke and burst damage. Area damage and crowd control with 1 shot ultimate.',
        'difficulty': 1,
        'playstyle_tags': ['area-control', 'burst-damage', 'zoning', 'cc', 'mobile'],
        'synergies': ['Magneto', 'Doctor Strange'],
        'counters': ['Ultron', 'Iron Fist', 'Star-Lord', 'Human Torch', 'Angela'],
    },
    {
        'name': 'Star-Lord',
        'role': 'DUELIST',
        'description': 'Dual pistols. Consistent damage at range. Fast ultimate farming.',
        'difficulty': 2,
        'playstyle_tags': ['hitscan', 'mobility', 'poke', 'consistent-damage', 'medium burst-damage', 'mobile'],
        'synergies': ['Rocket Raccoon', 'Mantis', 'Luna Snow', 'Gambit'],
        'counters': ['Iron Man', 'Venom', 'Human Torch', 'Ultron', 'Groot'],
    },
    {
        'name': 'Hela',
        'role': 'DUELIST',
        'description': 'Goddess of Death. Powerful ranged poke damage with nice burst damage.',
        'difficulty': 2,
        'playstyle_tags': ['sniper', 'burst-damage', 'backline', 'cc', 'poke'],
        'synergies': ['Loki', 'Venom', 'Mantis', 'Namor'],
        'counters': ['Invisible Woman', 'Venom', 'Doctor Strange', 'The Punisher', 'Iron Man', 'Ultron', 'Human Torch', 'Angela'],
    },
    {
        'name': 'Hawkeye',
        'role': 'DUELIST',
        'description': 'Master archer. Precise long-range eliminations.',
        'difficulty': 3,
        'playstyle_tags': ['sniper', 'burst-damage', 'precision', 'backline'],
        'synergies': ['Luna Snow', 'Mantis', 'Cloak & Dagger'],
        'counters': ['Iron Man', 'Doctor Strange', 'Human Torch', 'Ultron', 'The Punisher', 'Angela', 'Cloak & Dagger'],
    },
    {
        'name': 'Black Widow',
        'role': 'DUELIST',
        'description': 'Sniper. Quick eliminations.',
        'difficulty': 3,
        'playstyle_tags': ['backline', 'stealth', 'burst-damage', 'sniper'],
        'synergies': ['Mantis', 'The Punisher'],
        'counters': ['Hulk', 'Iron Man', 'Ultron', 'Human Torch', 'Angela'],
    },
    {
        'name': 'The Punisher',
        'role': 'DUELIST',
        'description': 'Heavy firepower. Sustained damage dealer.',
        'difficulty': 2,
        'playstyle_tags': ['hitscan', 'consistent-damage', 'backline', 'turret'],
        'synergies': ['Black Widow', 'Magneto', 'Daredevil'],
        'counters': ['The Thing', 'Venom', 'Hulk', 'Iron Man', 'Ultron', 'Human Torch', 'Groot', 'Angela'],
    },
    {
        'name': 'Winter Soldier',
        'role': 'DUELIST',
        'description': 'High burst damage with medium range. Has it all, anti mobility and repetitive ultimate.',
        'difficulty': 2,
        'playstyle_tags': ['constant burst-damage', 'consistent-damage', 'repetitive ultimate', 'anti mobility', 'overshield'],
        'synergies': ['Captain America', 'Mantis', 'Magneto'],
        'counters': ['Black Panther', 'Spider-Man', 'Hulk', 'Iron Man', 'Ultron', 'Human Torch', 'Venom', 'Groot', 'Magneto', 'Angela'],
    },
    {
        'name': 'Psylocke',
        'role': 'DUELIST',
        'description': 'High burst damage ninja flanker. Fast ultimate farm capability with high damage.',
        'difficulty': 2,
        'playstyle_tags': ['burst-damage', 'consistent-damage', 'flanker', 'AoE ultimate', 'mobile'],
        'synergies': ['Emma Frost', 'Magneto', 'Venom'],
        'counters': ['The Thing', 'Venom', 'Invisible Woman', 'Groot'],
    },
    {
        'name': 'Moon Knight',
        'role': 'DUELIST',
        'description': 'Lunar-powered vigilante. Versatile damage dealer with high burst and sustain.',
        'difficulty': 1,
        'playstyle_tags': ['Poke', 'consistent-damage', 'backline', 'burst-damage'],
        'synergies': ['Blade', 'Doctor Strange', 'Groot'],
        'counters': ['The Thing', 'Venom', 'Hulk', 'Loki'],
    },
    {
        'name': 'Squirrel Girl',
        'role': 'DUELIST',
        'description': 'Unbeatable Squirrel Girl. High burst damage and crowd control with squirrel summons.',
        'difficulty': 1,
        'playstyle_tags': ['burst-damage', 'consistent-damage', 'backline', 'cc'],
        'synergies': ['Black Widow', 'Magneto', 'Daredevil'],
        'counters': ['The Thing', 'Venom', 'Hulk', 'Captain America', 'Hela', 'Winter Soldier', 'The Punisher', 'Peni Parker'],
    },
    {
        'name': 'Iron Fist',
        'role': 'DUELIST',
        'description': 'Martial arts master. High burst damage and mobility with healing factor.',
        'difficulty': 3,
        'playstyle_tags': ['dive', 'burst-damage', 'flanker', 'mobile', 'sustain'],
        'synergies': ['Luna Snow', 'Magneto', 'Venom'],
        'counters': ['The Thing', 'Venom', 'Hulk', 'Iron Man', 'Ultron', 'Scarlet Witch', 'Doctor Strange', 'Groot', 'Peni Parker'],
    },
    {
        'name': 'Wolverine',
        'role': 'DUELIST',
        'description': 'Berserker with healing factor. High sustain and melee burst damage.',
        'difficulty': 1,
        'playstyle_tags': ['dive', 'consistent-damage', 'burst-damage', 'sustain'],
        'synergies': ['Hulk', 'The Thing', 'Magneto', 'Rocket Raccoon'],
        'counters': ['Groot', 'Venom', 'Hulk', 'Captain America', 'Doctor Strange', 'Peni Parker'],
    },
    {
        'name': 'Mister Fantastic',
        'role': 'DUELIST',
        'description': 'Stretchable genius. Versatile damage dealer with poke and burst capabilities.',
        'difficulty': 2,
        'playstyle_tags': ['Flexible Playstyle', 'consistent-damage', 'Tank-ish', 'frontline', 'burst-damage'],
        'synergies': ['Invisible Woman', 'Magneto', 'The Thing'],
        'counters': ['The Thing', 'Black Panther', 'Hulk', 'Iron Man',],
    },
    {
        'name': 'Human Torch',
        'role': 'DUELIST',
        'description': 'Flaming speedster. High mobility and area damage dealer.',
        'difficulty': 3,
        'playstyle_tags': ['hitscan', 'consistent-damage', 'backline', 'flying', 'area-damage'],
        'synergies': ['Invisible Woman', 'Spider-Man', 'The Thing'],
        'counters': ['Groot', 'Venom', 'The Thing', 'Emma Frost', 'Doctor Strange', 'Magneto'],
    },
    
    {
        'name': 'Phoenix',
        'role': 'DUELIST',
        'description': 'Cosmic firebird. High burst damage and area control with resurrection ultimate.',
        'difficulty': 2,
        'playstyle_tags': ['hitscan', 'consistent-damage', 'backline', 'area-damage',],
        'synergies': ['Black Widow', 'Wolverine', 'Mantis'],
        'counters': ['The Thing', 'Venom', 'Hulk', 'Iron Man', 'Ultron', 'Human Torch', 'Doctor Strange', 'Captain America', 'Wolverine', 'Spider-Man'],
    },
    {
        'name': 'Blade',
        'role': 'DUELIST',
        'description': 'Vampire hunter. High mobility and melee burst damage.',
        'difficulty': 2,
        'playstyle_tags': ['flexible playstyle', 'consistent-damage', 'heal reduction', 'AoE Ultimate'],
        'synergies': ['Moon Knight', 'Magneto', 'Venom'],
        'counters': ['Phoenix', 'Venom', 'Hulk', 'Wolverine',],
    },
    {
        'name': 'Daredevil',
        'role': 'DUELIST',
        'description': 'Blind vigilante. High mobility and burst damage with crowd control.',
        'difficulty': 2,
        'playstyle_tags': ['dive', 'consistent-damage', 'burst-damage', 'mobile', 'Aoe Ultimate'],
        'synergies': ['The Punisher', 'Magneto',],
        'counters': ['Luna Snow', 'Adam Warlock', 'Gambit', 'Iron Man', 'Black Widow', 'Hawkeye', 'Groot', 'Scarlet Witch'],
    },
    {
        'name': 'Magik',
        'role': 'DUELIST',
        'description': 'Queen of the Limbo. High burst damage and mobility with area control.',
        'difficulty': 3,
        'playstyle_tags': ['teleport', 'burst-damage', 'area-control', 'mobile'],
        'synergies': ['Doctor Strange'],
        'counters': ['Doctor Strange', 'Magneto', 'Groot', 'Venom'],
    },
    {
        'name': 'Namor',
        'role': 'DUELIST',
        'description': 'Atlantean king. Constant damage with Squids while having burst-damage with other skills.',
        'difficulty': 2,
        'playstyle_tags': ['consistent-damage', 'burst-damage', 'area-control', 'sustain'],
        'synergies': ['Hela'],
        'counters': ['Black Panther', 'Spider-Man', 'Wolverine', 'Iron Fist'],
    },
    {
        'name': 'Black Panther',
        'role': 'DUELIST',
        'description': 'Stealthy assassin. High burst damage and mobility.',
        'difficulty': 3,
        'playstyle_tags': ['stealth', 'burst-damage', 'dive', 'mobile', 'flanker'],
        'synergies': ['Hulk'],
        'counters': ['Invisible Woman', 'Jeff The Land Shark'],
    },
    
    
    # STRATEGISTS (Support)
    {
        'name': 'Luna Snow',
        'role': 'STRATEGIST',
        'description': 'K-pop star healer. Solid healing and damage boost with ultimate.',
        'difficulty': 2,
        'playstyle_tags': ['healer', 'damage-boost', 'aoe', 'utility', 'cc'],
        'synergies': ['Spider-Man', 'Iron Man', 'Hulk', 'Venom', 'Star-Lord', 'Hawkeye', 'Iron Fist', 'Captain America', 'Daredevil', 'Black Panther', 'Angela'],
        'counters': ['Doctor Strange', 'Spider-Man', 'Scarlet Witch', 'Black Panther'],
    },
    {
        'name': 'Loki',
        'role': 'STRATEGIST',
        'description': 'Trickster god. Clones, heal and invisibility.',
        'difficulty': 2,
        'playstyle_tags': ['healer', 'stealth', 'utility', 'clones'],
        'synergies': ['Mantis', 'Luna Snow', 'Cloak & Dagger'],
        'counters': ['Scarlet Witch', 'Star-Lord',],
    },
    {
        'name': 'Mantis',
        'role': 'STRATEGIST',
        'description': 'Empath healer. Sleep abilities and damage boost as addition to healing.',
        'difficulty': 3,
        'playstyle_tags': ['healer', 'cc', 'utility', 'damage-boost'],
        'synergies': ['Groot', 'Black Widow', 'Hawkeye', 'Loki'],
        'counters': ['Venom', 'Hulk', 'Spider-Man'],
    },
    {
        'name': 'Rocket Raccoon',
        'role': 'STRATEGIST',
        'description': 'Tech genius. Armor packs and revive station.',
        'difficulty': 1,
        'playstyle_tags': ['armor', 'utility', 'area-denial', 'resurrection', 'Constant healing'],
        'synergies': ['Groot', 'Peni Parker',],
        'counters': ['Spider-Man', 'Hawkeye'],
    },
    {
        'name': 'Adam Warlock',
        'role': 'STRATEGIST',
        'description': 'Cosmic healer. Strong heals, Anti dive skill, Resurrection and poke damage.',
        'difficulty': 2,
        'playstyle_tags': ['burst-healing', 'anti-dive', 'resurrection', 'poke'],
        'synergies': ['Luna Snow',],
        'counters': ['Spider-Man', 'Black Panther', 'Daredevil', 'Iron Fist', 'Magik', 'Psylocke', 'Winter Soldier'],
    },
    {
        'name': 'Jeff The Land Shark',
        'role': 'STRATEGIST',
        'description': 'Adorable shark. Provides healing and crowd control.',
        'difficulty': 2,
        'playstyle_tags': ['healing', 'sustain', 'Devour Ultimate', 'burst-healing', 'Constant healing'],
        'synergies': ['Venom', 'Groot'],
        'counters': ['Spider-Man', 'Black Panther', 'Iron Fist'],
    },
    {
        'name': 'Cloak & Dagger',
        'role': 'STRATEGIST',
        'description': 'Dynamic duo. Area healing and crowd control with stealth capabilities.',
        'difficulty': 1,
        'playstyle_tags': ['area-healing', 'blind', 'stealth', 'utility', 'Long ultimate duration'],
        'synergies': ['Hawkeye'],
        'counters': ['Spider-Man', 'Black Panther'],
    },
    {
        'name': 'Ultron',
        'role': 'STRATEGIST',
        'description': 'AI overlord. Provides armor and healing.',
        'difficulty': 2,
        'playstyle_tags': ['armor', 'utility', 'area-denial', 'flying', 'Constant healing', 'burst-damage'],
        'synergies': ['Iron Man'],
        'counters': ['Peni Parker'],
    },
    {
        'name': 'Invisible Woman',
        'role': 'STRATEGIST',
        'description': 'Force field master. Provides shields, healing and crowd control.',
        'difficulty': 2,
        'playstyle_tags': ['shield', 'healing', 'cc', 'utility'],
        'synergies': ['Mister Fantastic', 'The Thing', 'Human Torch'],
        'counters': ['Spider-Man', 'Doctor Strange', 'Scarlet Witch'],
    },
    {
        'name': 'Gambit',
        'role': 'STRATEGIST',
        'description': 'Card-throwing mutant. Provides healing, damage boost, heal reduction, speed and ult charge speed.',
        'difficulty': 3,
        'playstyle_tags': ['healing', 'damage-boost', 'heal-reduction', 'speed-boost', 'ultimate farm boost'],
        'synergies': ['Magneto'],
        'counters': ['Blade', 'Wolverine'],
    },

]


def main() -> None:
    print(f"Adding {len(heroes_data)} heroes...")

    # First pass: create/update heroes
    hero_objects: dict[str, dict] = {}

    for hero_dict in heroes_data:
        # IMPORTANT: don't mutate the original dict in case you reuse heroes_data
        data = dict(hero_dict)

        synergies = data.pop("synergies", [])
        counters = data.pop("counters", [])

        hero, created = Hero.objects.update_or_create(
            name=data["name"],
            defaults=data,
        )

        attach_media_if_exists(hero)

        hero_objects[hero.name] = {
            "hero": hero,
            "synergies": synergies,
            "counters": counters,
        }

        action = "Created" if created else "Updated"
        print(f"  ✓ {action} {hero.name} ({hero.get_role_display()})")

    # Second pass: relationships
    print("\nAdding synergies and counters...")
    for hero_name, rel in hero_objects.items():
        hero = rel["hero"]

        hero.synergies.clear()
        hero.counters.clear()

        for synergy_name in rel["synergies"]:
            if synergy_name in hero_objects:
                hero.synergies.add(hero_objects[synergy_name]["hero"])

        for counter_name in rel["counters"]:
            if counter_name in hero_objects:
                hero.counters.add(hero_objects[counter_name]["hero"])

        hero.save()
        print(f"  ✓ Updated {hero.name} relationships")

    print(f"\nSuccessfully added {Hero.objects.count()} heroes!")
    print("Admin: http://127.0.0.1:8000/admin/heroes/hero/")


if __name__ == "__main__":
    main()