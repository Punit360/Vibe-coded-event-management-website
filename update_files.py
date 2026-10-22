import re

# 1. Update protfolio.html with modal and onclicks
with open('protfolio.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract modal from home.html
with open('home.html', 'r', encoding='utf-8') as f:
    home_content = f.read()

modal_match = re.search(r'<!-- Event Details Modal -->.*?</script>', home_content, re.DOTALL)
if modal_match and '<!-- Event Details Modal -->' not in content:
    modal_code = modal_match.group(0)
    content = content.replace('</body>', f'{modal_code}\n</body>')

# Add onclick to portfolio cards
def repl(m):
    full_match = m.group(0)
    card_div = m.group(1)
    if 'onclick' in card_div:
        return full_match
    
    # Extract the h3 text
    h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', full_match)
    if h3_match:
        event_name = h3_match.group(1).strip()
        new_card_div = card_div + f' onclick="openEventModal(\'{event_name}\')"'
        return full_match.replace(card_div, new_card_div)
    return full_match

pattern = r'(<div class="portfolio-card masonry-item relative group rounded-xl overflow-hidden cursor-pointer bg-black shadow-sm border border-outline-variant/30"[^>]*>)(.*?</div>\s*</div>\s*</div>)'
content = re.sub(pattern, repl, content, flags=re.DOTALL)

with open('protfolio.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update dashboard.html with active events logic and replace logo
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Logo replacement
new_logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 160" class="w-10 h-8">
        <defs>
            <linearGradient id="brand-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#2563EB;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
            </linearGradient>
        </defs>
        <path d="M40 60 L100 140 L160 60" fill="none" stroke="url(#brand-grad)" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M70 60 L100 100 L130 60" fill="none" stroke="url(#brand-grad)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
    </svg>"""
    
old_logo = r'<img alt="Organization Logo" class="w-12 h-12 rounded-lg object-cover ring-1 ring-outline-variant/30 shadow-sm".*?/>'
dash_content = re.sub(old_logo, new_logo, dash_content, flags=re.DOTALL)

# Active events logic
active_events_js = """
        const res = await fetch((window.location.hostname ? `http://${window.location.hostname}:3000` : 'http://localhost:3000') + '/api/orders');
        const data = await res.json();
        if(data.orders && data.orders.length > 0) {
            
            // UPDATE ACTIVE EVENTS
            const baseEvents = 5;
            const newEvents = baseEvents + data.orders.length;
            const activeEventsCounter = document.querySelector('.counter[data-target="5"]');
            if (activeEventsCounter) {
                activeEventsCounter.setAttribute('data-target', newEvents);
                activeEventsCounter.innerText = newEvents;
            }
"""

dash_content = dash_content.replace("const res = await fetch((window.location.hostname ? `http://${window.location.hostname}:3000` : 'http://localhost:3000') + '/api/orders');\n            const data = await res.json();\n            if(data.orders && data.orders.length > 0) {", active_events_js)

dash_content = dash_content.replace("document.addEventListener('DOMContentLoaded', () => {", "document.addEventListener('DOMContentLoaded', () => {\n    fetchOrders();")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("Files updated successfully.")
