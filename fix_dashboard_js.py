import re

# Fix dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add ID to active events counter
content = re.sub(
    r'(<p class="[^"]*counter"[^>]*data-target="5"[^>]*>5</p>)',
    r'<p id="active-events-counter" class="font-display text-display font-bold text-on-surface counter" data-target="5">5</p>',
    content
)

# Fix the JS query selector
content = content.replace(
    "const activeEventsCounter = document.querySelector('.counter[data-target=\"5\"]');",
    "const activeEventsCounter = document.getElementById('active-events-counter');"
)

# And wait! The orders-section might not open. The user said "in admin panel i can not open order section".
# Why? In dashboard.html:
# window.showSection = function(sectionId) { ... }
# The a tag has: onclick="showSection('orders-section')"
# The orders-section div is: <div id="orders-section" class="hidden">
# If it doesn't open, maybe there's a JS error preventing showSection from running?
# Ah! Let's look at the fetchOrders call.
# If I changed `document.addEventListener('DOMContentLoaded', () => {`
# to `document.addEventListener('DOMContentLoaded', () => { fetchOrders(); ...`
# But fetchOrders is defined INSIDE the DOMContentLoaded? No, it's defined inside DOMContentLoaded but assigned to window!
# Wait! In the original code, fetchOrders was assigned to window INSIDE DOMContentLoaded.
# If I added fetchOrders() at the TOP of DOMContentLoaded, before it was defined, it throws an error!
# Yes! That's why the JS breaks and showSection doesn't work!
# Let's fix that.
content = content.replace(
    "document.addEventListener('DOMContentLoaded', () => {\\n    fetchOrders();",
    "document.addEventListener('DOMContentLoaded', () => {"
)
# We need to call fetchOrders() AFTER it is defined!
# It is defined near the end of DOMContentLoaded. We can just add it right after window.fetchOrders = ...
fetch_orders_def = "window.fetchOrders = async function() {"
content = content.replace(
    "});\\n\\n    document.getElementById('dashboard-logout-btn')",
    "    fetchOrders();\n});\n\n    document.getElementById('dashboard-logout-btn')"
)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix Stop Server.bat to not use /F so node can exit gracefully
with open('Stop Server.bat', 'r', encoding='utf-8') as f:
    bat_content = f.read()

bat_content = bat_content.replace('taskkill /F /IM node.exe', 'taskkill /IM node.exe')

with open('Stop Server.bat', 'w', encoding='utf-8') as f:
    f.write(bat_content)

# Fix server.js to gracefully exit and use WAL mode
with open('backend/server.js', 'r', encoding='utf-8') as f:
    server_content = f.read()

# Add WAL mode
if 'PRAGMA journal_mode=WAL;' not in server_content:
    server_content = server_content.replace(
        "console.log('Connected to SQLite database.');",
        "console.log('Connected to SQLite database.');\n        db.run('PRAGMA journal_mode=WAL;');\n        db.run('PRAGMA synchronous=NORMAL;');"
    )

# Add graceful shutdown
graceful_shutdown = """
process.on('SIGINT', () => {
    console.log('Closing database connection...');
    db.close((err) => {
        if (err) {
            console.error(err.message);
        }
        console.log('Database connection closed.');
        process.exit(0);
    });
});
process.on('SIGTERM', () => {
    console.log('Closing database connection...');
    db.close((err) => {
        if (err) {
            console.error(err.message);
        }
        console.log('Database connection closed.');
        process.exit(0);
    });
});
"""
if 'process.on(\'SIGINT\'' not in server_content:
    server_content = server_content.replace("app.listen(PORT", graceful_shutdown + "\napp.listen(PORT")

with open('backend/server.js', 'w', encoding='utf-8') as f:
    f.write(server_content)

print("Dashboard JS, Stop Server.bat, and server.js fixed")
