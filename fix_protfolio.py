import re

try:
    with open('protfolio.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove Create Event button
    create_event_btn = '''<a class="btn-primary text-white font-medium py-2 px-6 rounded-full transition-all duration-300 ease-in-out hover:scale-[1.02] inline-flex items-center justify-center" href="create-event.html">
                    Create Event
                </a>'''
    html = html.replace(create_event_btn, '')

    # 2. Remove search bar
    search_bar = '''<div class="hidden lg:flex items-center bg-surface-container rounded-full px-4 py-2 border border-outline-variant/30 focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/20 transition-all w-64">
<span class="material-symbols-outlined text-on-surface-variant mr-2 text-[20px]">search</span>
<input class="bg-transparent border-none outline-none text-sm w-full font-body-md text-on-surface placeholder:text-on-surface-variant/60" placeholder="Search events, venues..." type="text"/>
</div>'''
    html = html.replace(search_bar, '')
    
    search_btn_mobile = '''<button class="md:hidden w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container transition-colors">
<span class="material-symbols-outlined">search</span>
</button>'''
    html = html.replace(search_btn_mobile, '')

    # 3. Add onclick to all cards
    # We can find all <div class="group relative overflow-hidden rounded-xl glass-card aspect-[4/5] cursor-pointer">
    # and we need to pass the event title to openEventModal.
    # The title is in <h4 class="font-h3 text-body-lg font-semibold text-white">TITLE</h4>
    
    # regex to find cards and their titles
    pattern = re.compile(r'(<div class="group relative overflow-hidden rounded-xl glass-card aspect-\[4/5\] cursor-pointer[^>]*>.*?<h4[^>]*>)(.*?)(</h4>)', re.DOTALL)
    
    def repl(match):
        start_html = match.group(1)
        title = match.group(2).strip()
        end_html = match.group(3)
        
        # If it already has onclick, don't add it again
        if 'onclick=' not in start_html:
            start_html = start_html.replace('cursor-pointer"', f'cursor-pointer" onclick="openEventModal(\'{title}\')"')
            
        return start_html + title + end_html

    html = pattern.sub(repl, html)

    # 4. Inject Modal HTML and JS at the end of body
    modal_html = '''
<!-- Event Details Modal -->
<div id="event-modal" class="fixed inset-0 z-[100] flex items-center justify-center hidden">
    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" onclick="closeEventModal()"></div>
    <div class="relative bg-surface w-[90%] max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl p-8 transform scale-95 opacity-0 transition-all duration-300" id="event-modal-content">
        <button onclick="closeEventModal()" class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-surface-container hover:bg-surface-variant transition-colors">
            <span class="material-symbols-outlined">close</span>
        </button>
        <h2 id="modal-event-title" class="font-h1 text-h2 mb-2 text-on-surface">Event Title</h2>
        <div class="flex gap-4 text-sm text-on-surface-variant mb-6 pb-4 border-b border-outline-variant/30">
            <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[18px]">calendar_today</span> Oct 15 - 18, 2024</span>
            <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[18px]">schedule</span> 10:00 AM - 6:00 PM</span>
        </div>
        
        <p class="font-body-md text-on-surface-variant mb-6">Experience an immersive, world-class event designed by the industry's leading professionals. We take care of everything from start to finish to ensure an unforgettable experience.</p>
        
        <h3 class="font-h3 text-[18px] mb-3 text-on-surface">Services Provided</h3>
        <ul class="list-disc list-inside text-sm text-on-surface-variant mb-6 grid grid-cols-2 gap-2">
            <li>VIP Management</li>
            <li>Real-time Analytics</li>
            <li>Spatial Planning</li>
            <li>Gourmet Catering</li>
        </ul>

        <div class="bg-surface-container-low p-4 rounded-xl mb-6 border border-outline-variant/20">
            <div class="flex gap-1 text-amber-400 mb-2">
                <span class="material-symbols-outlined text-[16px] fill-current">star</span><span class="material-symbols-outlined text-[16px] fill-current">star</span><span class="material-symbols-outlined text-[16px] fill-current">star</span><span class="material-symbols-outlined text-[16px] fill-current">star</span><span class="material-symbols-outlined text-[16px] fill-current">star</span>
            </div>
            <p class="italic text-sm text-on-surface-variant">"Absolutely stunning experience. The EventVantage team went above and beyond to make our event flawless."</p>
            <p class="text-xs font-semibold text-on-surface mt-2">- Sarah Jenkins, Nexus Corp</p>
        </div>

        <div id="modal-booking-form" class="hidden mt-6 border-t border-outline-variant/30 pt-6">
            <h3 class="font-h3 text-[18px] mb-4 text-on-surface">Complete Your Booking</h3>
            
            <div id="booking-pricing-info" class="bg-primary/5 p-4 rounded-xl mb-4 border border-primary/20">
                <div class="flex justify-between text-sm mb-1 text-on-surface-variant"><span>Base Price:</span> <span id="pricing-base" class="font-medium text-on-surface">$0</span></div>
                <div class="flex justify-between text-sm mb-1 text-on-surface-variant"><span>Discount:</span> <span id="pricing-discount" class="font-medium text-emerald-600">-$0 (0%)</span></div>
                <div class="flex justify-between text-base font-bold mt-2 pt-2 border-t border-outline-variant/20 text-on-surface"><span>Total:</span> <span id="pricing-total" class="text-primary">$0</span></div>
            </div>

            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-1">Date</label>
                    <input type="date" id="booking-date" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm">
                    <p id="err-booking-date" class="text-red-500 text-xs mt-1 hidden">This field is required.</p>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Number of Guests</label>
                    <input type="number" id="booking-guests" placeholder="e.g. 150" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm">
                    <p id="err-booking-guests" class="text-red-500 text-xs mt-1 hidden">This field is required.</p>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Special Requirements</label>
                    <textarea id="booking-details" rows="2" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm" placeholder="Any dietary restrictions or VIP needs..."></textarea>
                    <p id="err-booking-details" class="text-red-500 text-xs mt-1 hidden">This field is required.</p>
                </div>
                <button type="button" onclick="goToPayment()" class="w-full btn-primary text-white font-medium py-3 rounded-lg">Next: Payment Details</button>
            </div>
        </div>

        <div id="modal-payment-form" class="hidden mt-6 border-t border-outline-variant/30 pt-6">
            <div class="flex items-center mb-4">
                <button type="button" onclick="goBackToBooking()" class="mr-2 text-on-surface-variant hover:text-primary transition-colors flex items-center">
                    <span class="material-symbols-outlined text-sm">arrow_back</span>
                </button>
                <h3 class="font-h3 text-[18px] text-on-surface">Payment Details</h3>
            </div>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-1">Select Bank</label>
                    <select id="payment-bank" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm">
                        <option value="">Choose your bank...</option>
                        <option value="sbi">State Bank of India (SBI)</option>
                        <option value="hdfc">HDFC Bank</option>
                        <option value="icici">ICICI Bank</option>
                        <option value="axis">Axis Bank</option>
                        <option value="pnb">Punjab National Bank (PNB)</option>
                        <option value="bob">Bank of Baroda</option>
                        <option value="kotak">Kotak Mahindra Bank</option>
                        <option value="indusind">IndusInd Bank</option>
                        <option value="yes">Yes Bank</option>
                        <option value="union">Union Bank of India</option>
                        <option value="canara">Canara Bank</option>
                        <option value="idfc">IDFC FIRST Bank</option>
                    </select>
                    <p id="err-payment-bank" class="text-red-500 text-xs mt-1 hidden">This field is required.</p>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Card / Account Number</label>
                    <input type="text" id="payment-account" placeholder="XXXX-XXXX-XXXX-XXXX" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm">
                    <p id="err-payment-account" class="text-red-500 text-xs mt-1 hidden">This field is required.</p>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium mb-1">Expiry</label>
                        <input type="text" id="payment-expiry" placeholder="MM/YY" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm">
                        <p id="err-payment-expiry" class="text-red-500 text-xs mt-1 hidden">Required.</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">CVV</label>
                        <input type="password" id="payment-cvv" placeholder="123" class="w-full rounded-lg border-outline-variant/50 p-2 text-sm">
                        <p id="err-payment-cvv" class="text-red-500 text-xs mt-1 hidden">Required.</p>
                    </div>
                </div>
                <button type="button" onclick="submitBooking()" class="w-full btn-primary text-white font-medium py-3 rounded-lg flex justify-center items-center gap-2">
                    <span class="material-symbols-outlined text-[20px]">lock</span> Pay & Book
                </button>
                <p id="booking-success" class="text-emerald-600 bg-emerald-50 p-2 rounded text-center text-sm hidden">Payment successful! Booking confirmed.</p>
            </div>
        </div>

        <div id="modal-action-buttons" class="mt-6">
            <button onclick="handleOrderClick()" class="w-full btn-primary text-white font-medium py-3 rounded-lg">Order / Book Event</button>
        </div>
    </div>
</div>

<script>
    let currentEventName = '';
    
    function clearErrors() {
        ['booking-date', 'booking-guests', 'booking-details', 'payment-bank', 'payment-account', 'payment-expiry', 'payment-cvv'].forEach(id => {
            const errEl = document.getElementById('err-' + id);
            if (errEl) errEl.classList.add('hidden');
        });
    }
    
    // Check if we came back from login to book an event
    document.addEventListener('DOMContentLoaded', () => {
        const urlParams = new URLSearchParams(window.location.search);
        const autoOpen = urlParams.get('auto_open');
        if (autoOpen) {
            openEventModal(autoOpen);
            // clean up url
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    });

    function openEventModal(eventName) {
        currentEventName = eventName;
        document.getElementById('modal-event-title').innerText = eventName;
        const modal = document.getElementById('event-modal');
        const content = document.getElementById('event-modal-content');
        
        modal.classList.remove('hidden');
        // trigger animation
        setTimeout(() => {
            content.classList.remove('scale-95', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
        }, 10);

        // Reset form state
        clearErrors();
        document.getElementById('booking-success').classList.add('hidden');
        document.getElementById('booking-date').value = '';
        document.getElementById('booking-guests').value = '';
        document.getElementById('booking-details').value = '';
        
        const bankEl = document.getElementById('payment-bank');
        if (bankEl) bankEl.value = '';
        const accEl = document.getElementById('payment-account');
        if (accEl) accEl.value = '';
        const expEl = document.getElementById('payment-expiry');
        if (expEl) expEl.value = '';
        const cvvEl = document.getElementById('payment-cvv');
        if (cvvEl) cvvEl.value = '';
        
        const modalPaymentForm = document.getElementById('modal-payment-form');
        if (modalPaymentForm) modalPaymentForm.classList.add('hidden');

        // Calculate pricing
        let basePrice = 300000;
        const nameLower = eventName.toLowerCase();
        if (nameLower.includes('wedding') || nameLower.includes('shower')) {
            basePrice = 500000;
        } else if (nameLower.includes('sports')) {
            basePrice = 1000000;
        } else if (nameLower.includes('summit') || nameLower.includes('lab') || nameLower.includes('conference')) {
            basePrice = 800000;
        }
        
        // Random discount between 5% and 25%
        const discountPercent = Math.floor(Math.random() * 21) + 5;
        const discountAmount = (basePrice * discountPercent) / 100;
        const total = basePrice - discountAmount;
        
        const priceBaseEl = document.getElementById('pricing-base');
        if (priceBaseEl) priceBaseEl.innerText = '₹' + basePrice.toLocaleString('en-IN');
        
        const priceDiscountEl = document.getElementById('pricing-discount');
        if (priceDiscountEl) priceDiscountEl.innerText = '-₹' + discountAmount.toLocaleString('en-IN') + ' (' + discountPercent + '%)';
        
        const priceTotalEl = document.getElementById('pricing-total');
        if (priceTotalEl) priceTotalEl.innerText = '₹' + total.toLocaleString('en-IN');
        
        const isLoggedIn = localStorage.getItem('eventpro_auth') === 'true';
        if (isLoggedIn) {
            document.getElementById('modal-action-buttons').classList.add('hidden');
            document.getElementById('modal-booking-form').classList.remove('hidden');
        } else {
            document.getElementById('modal-action-buttons').classList.remove('hidden');
            document.getElementById('modal-booking-form').classList.add('hidden');
        }
    }

    function closeEventModal() {
        const modal = document.getElementById('event-modal');
        const content = document.getElementById('event-modal-content');
        
        content.classList.remove('scale-100', 'opacity-100');
        content.classList.add('scale-95', 'opacity-0');
        
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    }

    function handleOrderClick() {
        const isLoggedIn = localStorage.getItem('eventpro_auth') === 'true';
        if (!isLoggedIn) {
            // Redirect to login
            const redirectUrl = encodeURIComponent(window.location.pathname + '?auto_open=' + currentEventName);
            window.location.href = 'login.html?redirect=' + redirectUrl;
        }
    }

    function goToPayment() {
        clearErrors();
        let isValid = true;
        ['booking-date', 'booking-guests', 'booking-details'].forEach(id => {
            const val = document.getElementById(id).value;
            if (!val || !val.trim()) {
                document.getElementById('err-' + id).classList.remove('hidden');
                isValid = false;
            }
        });
        
        if (!isValid) return;

        document.getElementById('modal-booking-form').classList.add('hidden');
        document.getElementById('modal-payment-form').classList.remove('hidden');
    }

    function goBackToBooking() {
        document.getElementById('modal-payment-form').classList.add('hidden');
        document.getElementById('modal-booking-form').classList.remove('hidden');
    }

    async function submitBooking() {
        clearErrors();
        let isValid = true;
        ['payment-bank', 'payment-account', 'payment-expiry', 'payment-cvv'].forEach(id => {
            const val = document.getElementById(id)?.value;
            if (!val || !val.trim()) {
                const errEl = document.getElementById('err-' + id);
                if (errEl) errEl.classList.remove('hidden');
                isValid = false;
            }
        });
        
        if (!isValid) return;

        const date = document.getElementById('booking-date').value;
        const guests = document.getElementById('booking-guests').value;
        const detailsText = document.getElementById('booking-details').value;
        const userName = localStorage.getItem('eventpro_user') || 'User';
        const userEmail = localStorage.getItem('eventpro_email') || 'user@example.com'; 
        
        try {
            const res = await fetch((window.location.hostname ? `http://${window.location.hostname}:3000` : 'http://localhost:3000') + '/api/orders', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_name: userName,
                    user_email: userEmail,
                    event_name: currentEventName,
                    order_date: date,
                    details: { guests, additional: detailsText }
                })
            });
            const data = await res.json();
            if (res.ok) {
                document.getElementById('booking-success').classList.remove('hidden');
                setTimeout(() => {
                    closeEventModal();
                }, 4000);
            } else {
                alert(data.error);
            }
        } catch (err) {
            alert('Failed to place order: ' + err.message);
        }
    }
</script>
'''
    if 'event-modal' not in html:
        html = html.replace('</body></html>', modal_html + '\n</body></html>')

    with open('protfolio.html', 'w', encoding='utf-8') as f:
        f.write(html)
        print("protfolio.html fixed.")
except Exception as e:
    print(f"Error fixing protfolio.html: {e}")
