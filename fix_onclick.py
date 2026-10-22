import re

with open('protfolio.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The incorrect format is: > onclick="openEventModal('Name')"
# We need to change it to: onclick="openEventModal('Name')">
content = re.sub(r'(<div class="portfolio-card[^>]+)>( onclick="openEventModal\(\'.*?\'\)")', r'\1\2>', content)

with open('protfolio.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed protfolio.html onclick")
