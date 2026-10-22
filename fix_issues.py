import re
import sys

# 1. Fix home.html: move cards from hero to gallery
try:
    with open('home.html', 'r', encoding='utf-8') as f:
        home_html = f.read()
    
    # Extract the 4 cards from hero section
    cards_start_str = '''<div class="group relative overflow-hidden rounded-xl glass-card aspect-[4/5] cursor-pointer" onclick="openEventModal('Corporate Summits')">'''
    cards_end_str = '''<p class="font-label-caps text-[10px] text-secondary-fixed-dim uppercase tracking-widest mb-1">Launch</p>
<h4 class="font-h3 text-body-lg font-semibold text-white">Product Launches</h4>
</div>
</div>'''
    
    start_idx = home_html.find(cards_start_str)
    end_idx = home_html.find(cards_end_str) + len(cards_end_str)
    
    if start_idx != -1 and end_idx != -1:
        extracted_cards = home_html[start_idx:end_idx]
        # Remove from hero section
        home_html = home_html[:start_idx] + home_html[end_idx:]
        
        # Insert at the end of Event Gallery
        gallery_end_str = '''<p class="font-label-caps text-[10px] text-secondary-fixed-dim uppercase tracking-widest mb-1">University Fests</p>
<h4 class="font-h3 text-body-lg font-semibold text-white">University Fests</h4>
</div>
</div>
</div>
</section>'''
        
        gal_idx = home_html.find(gallery_end_str)
        if gal_idx != -1:
            replacement = gallery_end_str.replace('</div>\n</div>\n</div>\n</section>', '</div>\n</div>\n' + extracted_cards + '\n</div>\n</section>')
            home_html = home_html.replace(gallery_end_str, replacement)
            
            with open('home.html', 'w', encoding='utf-8') as f:
                f.write(home_html)
                print("home.html fixed.")
except Exception as e:
    print(f"Error fixing home.html: {e}")

# 2. Fix dashboard.html: logout button, logo, name
try:
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        dash_html = f.read()

    # Logo and name from home.html
    new_logo_html = '''<img alt="Organization Logo" class="w-12 h-12 rounded-lg object-cover ring-1 ring-outline-variant/30 shadow-sm" data-alt="A sleek, modern corporate logo icon" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB74tu0gNSsRrHYz3jimltx9TKUoPAmD19Ry56o3gL5XekmACwex4Lz4IBodqfuQHXw1hOAjCKjvumnOwVCf2SJLpiRfCi_OhUT2At7Hr5rGgUwNgOvUx1yfl_Sree9BjgNEVwLxUJ5H8F4wLOSe7b5INbaNmkED5exSHxN2Wbpl7Rnx1yALEHs_Q8JcwYXdyUoXCYXz8mVMG9YoFLpzXQwDghx0yaxDCyM3lRch-CtXT465w8wnyiWK5_BN8ByLLQOCx_w5D-2tcZC"/>
<div>
<div class="font-h2 text-h2 font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">EventPro</div>
<p class="font-label-caps text-label-caps text-on-surface-variant mt-1">Enterprise Suite</p>
</div>'''

    old_logo_start = dash_html.find('<img alt="Organization Logo"')
    old_logo_end = dash_html.find('</div>', old_logo_start)
    old_logo_end = dash_html.find('</div>', old_logo_end + 1) + 6 # end of the inner div
    
    if old_logo_start != -1 and old_logo_end != -1:
        dash_html = dash_html[:old_logo_start] + new_logo_html + dash_html[old_logo_end:]

    # Logout logic
    logout_script = '''
    document.getElementById('dashboard-logout-btn').addEventListener('click', function() {
        localStorage.removeItem('eventpro_auth');
        localStorage.removeItem('eventpro_user');
        localStorage.removeItem('eventpro_email');
        window.location.href = 'home.html';
    });
'''
    if 'localStorage.removeItem(\'eventpro_auth\');' not in dash_html:
        script_end_idx = dash_html.rfind('</script>')
        dash_html = dash_html[:script_end_idx] + logout_script + dash_html[script_end_idx:]

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dash_html)
        print("dashboard.html fixed.")
except Exception as e:
    print(f"Error fixing dashboard.html: {e}")

# 3. Fix about.html: remove create event button
try:
    with open('about.html', 'r', encoding='utf-8') as f:
        about_html = f.read()
    
    create_event_btn = '''<a class="btn-primary text-white font-medium py-2 px-6 rounded-full transition-all duration-300 ease-in-out hover:scale-[1.02] inline-flex items-center justify-center" href="create-event.html">
                    Create Event
                </a>'''
    about_html = about_html.replace(create_event_btn, '')
    
    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(about_html)
        print("about.html fixed.")
except Exception as e:
    print(f"Error fixing about.html: {e}")
