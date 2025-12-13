import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marvel_rivals.settings')
django.setup()

from heroes.models import Hero

# Path to banners folder
BANNER_FOLDER = 'media/heroes/banners/'

# Get all banner files
banner_files = []
if os.path.exists(BANNER_FOLDER):
    banner_files = [f for f in os.listdir(BANNER_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Found {len(banner_files)} banner files in {BANNER_FOLDER}")
else:
    print(f"Error: {BANNER_FOLDER} not found!")
    exit()

# Map of hero names to their banner filenames
# This helps match different naming conventions
hero_name_mappings = {
    'Cloak & Dagger': ['Cloak__Dagger', 'Cloak_&_Dagger', 'Cloak_and_Dagger'],
    'Jeff The Land Shark': ['Jeff_the_Land_Shark', 'Jeff_The_Land_Shark'],
    'Mister Fantastic': ['Mister_Fantastic', 'Mr_Fantastic'],
    'The Punisher': ['The_Punisher', 'Punisher'],
    'The Thing': ['The_Thing', 'Thing'],
}

def find_banner_for_hero(hero_name, banner_files):
    """Try to find a matching banner file for a hero"""
    # Clean hero name for comparison
    clean_name = hero_name.replace(' ', '_').replace('&', '_')
    
    # Try exact match first
    for banner_file in banner_files:
        if clean_name.lower() in banner_file.lower():
            return f'heroes/banners/{banner_file}'
    
    # Try alternative names
    if hero_name in hero_name_mappings:
        for alt_name in hero_name_mappings[hero_name]:
            for banner_file in banner_files:
                if alt_name.lower() in banner_file.lower():
                    return f'heroes/banners/{banner_file}'
    
    return None

# Update all heroes
heroes = Hero.objects.all()
updated_count = 0
not_found = []

for hero in heroes:
    banner_path = find_banner_for_hero(hero.name, banner_files)
    
    if banner_path:
        hero.banner = banner_path
        hero.save()
        print(f"✓ Updated {hero.name} with banner: {banner_path}")
        updated_count += 1
    else:
        not_found.append(hero.name)
        print(f"✗ No banner found for {hero.name}")

print("\n" + "="*50)
print(f"Updated {updated_count} heroes with banners")
print(f"Could not find banners for {len(not_found)} heroes")

if not_found:
    print("\nHeroes without banners:")
    for name in not_found:
        print(f"  - {name}")
