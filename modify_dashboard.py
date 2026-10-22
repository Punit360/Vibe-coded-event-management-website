import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Sidebar
sidebar_original = '''<a class="flex items-center gap-3 px-4 py-3 bg-primary text-on-primary rounded-lg mx-2 active:scale-95 transition-transform shadow-sm" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
<span class="font-body-md font-medium">Dashboard</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all active:scale-95" href="#">
<span class="material-symbols-outlined">analytics</span>
<span class="font-body-md font-medium">Analytics</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all active:scale-95" href="#">
<span class="material-symbols-outlined">group</span>
<span class="font-body-md font-medium">Team</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all active:scale-95" href="#">
<span class="material-symbols-outlined">campaign</span>
<span class="font-body-md font-medium">Marketing</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all active:scale-95" href="#">
<span class="material-symbols-outlined">settings</span>
<span class="font-body-md font-medium">Settings</span>
</a>'''

sidebar_new = '''<a id="nav-dashboard" class="flex items-center gap-3 px-4 py-3 bg-primary text-on-primary rounded-lg mx-2 active:scale-95 transition-transform shadow-sm cursor-pointer" onclick="showSection('dashboard-section')">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
<span class="font-body-md font-medium">Dashboard</span>
</a>
<a id="nav-orders" class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all active:scale-95 cursor-pointer" onclick="showSection('orders-section')">
<span class="material-symbols-outlined">receipt_long</span>
<span class="font-body-md font-medium">Orders</span>
</a>'''

html = html.replace(sidebar_original, sidebar_new)

# Remove Upgrade Pro and Support
upgrade_pro_html = '''<div class="px-6 mb-6">
<button class="w-full py-3 px-4 rounded-lg bg-secondary text-on-secondary font-body-md font-medium shadow-sm hover:shadow-md transition-all duration-300 hover:bg-secondary/90">
                Upgrade Pro
            </button>
</div>'''
html = html.replace(upgrade_pro_html, '')

support_html = '''<a class="flex items-center gap-3 px-4 py-2 text-on-surface-variant hover:bg-surface-container mx-2 rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">help</span>
<span class="font-body-md">Support</span>
</a>'''
html = html.replace(support_html, '')

# 2. Update Stats
html = html.replace('data-target="84250" data-prefix="$">$0</p>', 'data-target="0" data-prefix="₹">₹0</p>')
html = html.replace('data-target="32">0</p>', 'data-target="5">5</p>')
html = html.replace('data-target="156">0</p>', 'data-target="15">15</p>')
html = html.replace('data-target="4.8" data-decimals="1">0.0</p>', 'data-target="4.5" data-decimals="1">4.5</p>')

# 3. Add Orders section and wrap main content in dashboard-section
main_content_start = '<section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter mb-stack-lg">'
main_content_replacement = '''
<div id="dashboard-section">
<section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter mb-stack-lg">
'''

html = html.replace(main_content_start, main_content_replacement)

# End of dashboard section is after the grid grid-cols-1 lg:grid-cols-3...
# Let's find </main> and insert the orders section before it
end_main_idx = html.find('</main>')

orders_section = '''
</div> <!-- End dashboard-section -->

<div id="orders-section" class="hidden">
    <div class="bg-surface border border-outline-variant/40 rounded-2xl flex flex-col overflow-hidden shadow-sm">
        <div class="p-6 border-b border-outline-variant/30 bg-surface-container-lowest flex justify-between">
            <h3 class="font-h3 text-h3 text-on-surface font-semibold">Customer Event Orders</h3>
            <button onclick="fetchOrders()" class="text-primary text-sm flex items-center gap-1"><span class="material-symbols-outlined text-[18px]">refresh</span> Refresh</button>
        </div>
        <div class="overflow-x-auto bg-surface">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-surface-container-low border-b border-outline-variant/30">
                        <th class="p-4 font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">ID</th>
                        <th class="p-4 font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">Customer</th>
                        <th class="p-4 font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">Email</th>
                        <th class="p-4 font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">Event</th>
                        <th class="p-4 font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">Date</th>
                        <th class="p-4 font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">Details</th>
                    </tr>
                </thead>
                <tbody id="orders-tbody" class="divide-y divide-outline-variant/20">
                    <tr><td colspan="6" class="p-4 text-center text-on-surface-variant">Loading...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
'''

html = html[:end_main_idx] + orders_section + html[end_main_idx:]

# 4. Add JS for switching sections and fetching orders
js_addition = '''
    window.showSection = function(sectionId) {
        document.getElementById('dashboard-section').classList.add('hidden');
        document.getElementById('orders-section').classList.add('hidden');
        document.getElementById(sectionId).classList.remove('hidden');
        
        document.getElementById('nav-dashboard').classList.remove('bg-primary', 'text-on-primary');
        document.getElementById('nav-dashboard').classList.add('text-on-surface-variant');
        document.getElementById('nav-orders').classList.remove('bg-primary', 'text-on-primary');
        document.getElementById('nav-orders').classList.add('text-on-surface-variant');
        
        if(sectionId === 'dashboard-section') {
            document.getElementById('nav-dashboard').classList.add('bg-primary', 'text-on-primary');
            document.getElementById('nav-dashboard').classList.remove('text-on-surface-variant');
        } else {
            document.getElementById('nav-orders').classList.add('bg-primary', 'text-on-primary');
            document.getElementById('nav-orders').classList.remove('text-on-surface-variant');
            fetchOrders();
        }
    };

    window.fetchOrders = async function() {
        const tbody = document.getElementById('orders-tbody');
        tbody.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-on-surface-variant">Loading orders...</td></tr>';
        try {
            const res = await fetch((window.location.hostname ? `http://${window.location.hostname}:3000` : 'http://localhost:3000') + '/api/orders');
            const data = await res.json();
            if(data.orders && data.orders.length > 0) {
                tbody.innerHTML = '';
                data.orders.forEach(order => {
                    let detailsStr = '';
                    try {
                        const details = JSON.parse(order.details || '{}');
                        detailsStr = `Guests: ${details.guests || 'N/A'}<br>Reqs: ${details.additional || 'None'}`;
                    } catch(e) {
                        detailsStr = order.details;
                    }
                    tbody.innerHTML += `
                    <tr class="hover:bg-surface-container-low/50 transition-colors group">
                        <td class="p-4 text-sm text-on-surface">#${order.id}</td>
                        <td class="p-4 font-medium text-on-surface">${order.user_name || 'N/A'}</td>
                        <td class="p-4 text-sm text-on-surface-variant">${order.user_email || 'N/A'}</td>
                        <td class="p-4 text-sm text-on-surface">${order.event_name}</td>
                        <td class="p-4 text-sm text-on-surface-variant">${order.order_date}</td>
                        <td class="p-4 text-xs text-on-surface-variant">${detailsStr}</td>
                    </tr>`;
                });
                
                // Update revenue based on orders (Optional, e.g. each order = 15000 INR)
                // document.querySelector('.counter[data-prefix="₹"]').setAttribute('data-target', data.orders.length * 15000);
            } else {
                tbody.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-on-surface-variant">No orders found.</td></tr>';
            }
        } catch(e) {
            tbody.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-error">Error loading orders.</td></tr>';
        }
    };
'''

script_end_idx = html.find('});\n</script>')
if script_end_idx != -1:
    html = html[:script_end_idx] + js_addition + html[script_end_idx:]


with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
