import re
from bs4 import BeautifulSoup

file_path = 'protfolio.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add onclick="openEventModal('Title')" to all portfolio-card elements
soup = BeautifulSoup(html, 'html.parser')
cards = soup.find_all('div', class_='portfolio-card')

for card in cards:
    h3 = card.find('h3')
    if h3:
        title = h3.text.strip()
        # Add or update onclick attribute
        card['onclick'] = f"openEventModal('{title}')"

# We must manually inject the modified cards back, or just use regex to avoid breaking other formatting if bs4 messes it up.
# bs4's str(soup) is usually safe but can mess up `<script>` tags sometimes. Let's stick to bs4 for cards.
# Wait, replacing cards is easy with bs4.
# Actually, the user's HTML is fairly clean, but bs4 might strip some attributes. Let's use regex to be safe.

# Revert to regex for safety:
for card in cards:
    h3 = card.find('h3')
    if h3:
        title = h3.text.strip().replace("'", "\\'")
        # Find the card's original HTML
        card_html = str(card)
        
        # We need to find the start of this specific div in the raw html
        # A simpler way is to just find all <div class="... portfolio-card ..."> 
        pass

# Let's write a better string replacement for cards
import os
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Regex to find <div class="portfolio-card..." and the h3 inside it
# It's better to just replace the first div tag of the card.
# The structure is:
# <div class="portfolio-card masonry-item relative group rounded-xl overflow-hidden cursor-pointer bg-black shadow-sm border border-outline-variant/30" data-tag="tech-summits">
# ... <h3 class="font-h3 text-h3 text-white">Baby Showers</h3>

parts = content.split('portfolio-card masonry-item')
new_content = parts[0]

for part in parts[1:]:
    # Find the h3 tag in this part
    match = re.search(r'<h3[^>]*>(.*?)</h3>', part)
    if match:
        title = match.group(1).strip().replace("'", "\\'")
        # Insert onclick before the closing > of the first tag
        # The part starts with the rest of the class attribute, e.g., " relative group..."
        
        # We want to add onclick="openEventModal('...')" to the div.
        # Find the first >
        first_gt = part.find('>')
        
        # Check if onclick already exists
        div_attrs = part[:first_gt]
        if 'onclick=' not in div_attrs:
            part = div_attrs + f' onclick="openEventModal(\'{title}\')"' + part[first_gt:]
        else:
            # Replace existing onclick
            part = re.sub(r'onclick="[^"]*"', f'onclick="openEventModal(\'{title}\')"', part, count=1)
            
    new_content += 'portfolio-card masonry-item' + part


# 2. Remove visibleCount logic so all cards are shown
# JS block to replace:
old_js = """        let currentFilter = 'all';
        let visibleCount = 3;

        function updateVisibility() {
            let visibleForFilter = 0;
            cards.forEach(card => {
                const tag = card.getAttribute('data-tag');
                if (currentFilter === 'all' || tag === currentFilter) {
                    visibleForFilter++;
                    if (visibleForFilter <= visibleCount) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                } else {
                    card.style.display = 'none';
                }
            });

            if (visibleForFilter > visibleCount) {
                loadMoreBtn.style.display = 'inline-flex';
            } else {
                loadMoreBtn.style.display = 'none';
            }
        }"""

new_js = """        let currentFilter = 'all';

        function updateVisibility() {
            cards.forEach(card => {
                const tag = card.getAttribute('data-tag');
                if (currentFilter === 'all' || tag === currentFilter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });

            if (loadMoreBtn) {
                loadMoreBtn.style.display = 'none';
            }
        }"""

new_content = new_content.replace(old_js, new_js)

# Also remove loadMoreBtn logic from the bottom:
old_load_more_logic = """        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => {
                visibleCount += 3;
                updateVisibility();
            });
        }"""

new_content = new_content.replace(old_load_more_logic, "")

# And in the button click handler:
old_btn_logic = """                currentFilter = btn.getAttribute('data-filter');
                visibleCount = 3;
                updateVisibility();"""

new_btn_logic = """                currentFilter = btn.getAttribute('data-filter');
                updateVisibility();"""

new_content = new_content.replace(old_btn_logic, new_btn_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated protfolio.html successfully.")
