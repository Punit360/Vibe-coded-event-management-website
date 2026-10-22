import os
import re

auth_html = '''<div id="auth-container" class="flex items-center gap-3">
    <div id="unauth-actions" class="flex items-center gap-3">
        <a href="login.html" class="bg-surface-container border border-primary/20 text-primary font-medium py-2 px-6 rounded-full hover:bg-primary/5 transition-all">Sign Up</a>
    </div>
    
    <div id="auth-actions" class="relative hidden">
        <button id="profile-btn" class="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white font-bold text-lg border border-outline-variant/30 hover:shadow-md transition-all">
            U
        </button>
        
        <div id="profile-dropdown" class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-outline-variant/20 py-2 hidden opacity-0 transition-opacity duration-200 z-50">
            <div class="px-4 py-2 border-b border-outline-variant/10 mb-1">
                <p class="text-sm font-semibold text-on-surface" id="dropdown-username">User</p>
            </div>
            <a href="dashboard.html" id="dropdown-dashboard" class="hidden block px-4 py-2 text-sm text-on-surface-variant hover:bg-surface-container hover:text-primary transition-colors">Dashboard</a>
            <button id="logout-btn" class="w-full text-left block px-4 py-2 text-sm text-error hover:bg-error/5 transition-colors">Logout</button>
        </div>
    </div>
</div>'''

auth_js = '''<script>
    document.addEventListener('DOMContentLoaded', () => {
        const unauthActions = document.getElementById('unauth-actions');
        const authActions = document.getElementById('auth-actions');
        const profileBtn = document.getElementById('profile-btn');
        const profileDropdown = document.getElementById('profile-dropdown');
        const logoutBtn = document.getElementById('logout-btn');
        const dropdownUsername = document.getElementById('dropdown-username');
        const dropdownDashboard = document.getElementById('dropdown-dashboard');

        const isLoggedIn = localStorage.getItem('eventpro_auth') === 'true';
        const userName = localStorage.getItem('eventpro_user') || 'User';
        const role = localStorage.getItem('eventpro_role') || 'user';

        if (isLoggedIn) {
            unauthActions.classList.add('hidden');
            authActions.classList.remove('hidden');
            profileBtn.innerText = userName.charAt(0).toUpperCase();
            dropdownUsername.innerText = userName;
            if (role === 'admin' && dropdownDashboard) {
                dropdownDashboard.classList.remove('hidden');
            }
        } else {
            unauthActions.classList.remove('hidden');
            authActions.classList.add('hidden');
        }

        if(profileBtn) {
            profileBtn.addEventListener('click', () => {
                if (profileDropdown.classList.contains('hidden')) {
                    profileDropdown.classList.remove('hidden');
                    setTimeout(() => profileDropdown.classList.remove('opacity-0'), 10);
                } else {
                    profileDropdown.classList.add('opacity-0');
                    setTimeout(() => profileDropdown.classList.add('hidden'), 200);
                }
            });
        }

        document.addEventListener('click', (e) => {
            if (authActions && !authActions.contains(e.target) && profileDropdown) {
                profileDropdown.classList.add('opacity-0');
                setTimeout(() => profileDropdown.classList.add('hidden'), 200);
            }
        });

        if(logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                localStorage.removeItem('eventpro_auth');
                localStorage.removeItem('eventpro_user');
                localStorage.removeItem('eventpro_role');
                window.location.reload();
            });
        }
    });
</script>'''

# 1. FIX ABOUT.HTML
try:
    with open('about.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the flex items-center gap-4 block and replace contents
    pattern = re.compile(r'<div class="flex items-center gap-4">\s*<button[^>]*>Create Event</button>\s*<img[^>]*>\s*</div>', re.DOTALL)
    if pattern.search(html):
        html = pattern.sub('<div class="flex items-center gap-4">\n' + auth_html + '\n</div>', html)
    else:
        print("Could not find about.html navbar elements to replace")

    if 'eventpro_auth' not in html:
        html = html.replace('</body></html>', auth_js + '\n</body></html>')

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("about.html fixed")
except Exception as e:
    print("Error fixing about.html:", e)


# 2. FIX PROTFOLIO.HTML
try:
    with open('protfolio.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change auth keys
    html = html.replace('eventvantage_auth', 'eventpro_auth')
    html = html.replace('eventvantage_user', 'eventpro_user')
    html = html.replace('eventvantage_role', 'eventpro_role')

    # Remove the search button
    search_btn_pattern = re.compile(r'<button class="p-2 text-primary hover:bg-surface-variant/50 rounded-full transition-colors duration-300">\s*<span class="material-symbols-outlined">search</span>\s*</button>', re.DOTALL)
    html = search_btn_pattern.sub('', html)
    
    # Remove Create Event button
    create_btn_pattern = re.compile(r'<button class="hidden md:block btn-primary-gradient px-4 py-2 rounded-lg font-label-caps text-label-caps">\s*Create Event\s*</button>', re.DOTALL)
    html = create_btn_pattern.sub('', html)

    with open('protfolio.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("protfolio.html fixed")
except Exception as e:
    print("Error fixing protfolio.html:", e)


# 3. FIX DASHBOARD.HTML
try:
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Re-insert the sidebar nav
    bad_nav_pattern = re.compile(r'</div>\s*<div class="px-4 space-y-2 pt-4 border-t border-outline-variant/30">', re.DOTALL)
    replacement = '''</div>
</a>
<div class="flex-1 px-4 space-y-2 overflow-y-auto">
<a id="nav-dashboard" class="flex items-center gap-3 px-4 py-3 bg-primary text-on-primary rounded-lg mx-2 active:scale-95 transition-transform shadow-sm cursor-pointer" onclick="showSection('dashboard-section')">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
<span class="font-body-md font-medium">Dashboard</span>
</a>
<a id="nav-orders" class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all active:scale-95 cursor-pointer" onclick="showSection('orders-section')">
<span class="material-symbols-outlined">receipt_long</span>
<span class="font-body-md font-medium">Orders</span>
</a>
</div>
<div class="px-4 space-y-2 pt-4 border-t border-outline-variant/30">'''

    if bad_nav_pattern.search(html):
        html = bad_nav_pattern.sub(replacement, html)
        with open('dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("dashboard.html fixed")
    else:
        print("Could not find the broken nav block in dashboard.html")
except Exception as e:
    print("Error fixing dashboard.html:", e)

