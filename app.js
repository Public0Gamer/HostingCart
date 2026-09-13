/**
 * ApexHost Client JavaScript — Clean Light Corporate Theme
 * Handles live domain search, pricing switcher, and countdown timers.
 */

// 1. Countdown Timer Simulation
function startCountdown() {
    let seconds = 45;
    let minutes = 28;
    let hours = 4;

    setInterval(() => {
        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
            if (minutes < 0) {
                minutes = 59;
                hours--;
                if (hours < 0) {
                    hours = 4;
                }
            }
        }
        const hEl = document.getElementById('timer-hours');
        const mEl = document.getElementById('timer-mins');
        const sEl = document.getElementById('timer-secs');

        if (hEl) hEl.innerText = String(hours).padStart(2, '0');
        if (mEl) mEl.innerText = String(minutes).padStart(2, '0');
        if (sEl) sEl.innerText = String(seconds).padStart(2, '0');
    }, 1000);
}

// 2. Billing Cycle Switcher
let activeCycle = '48m';

function setBillingCycle(cycle) {
    activeCycle = cycle;

    ['monthly', 'yearly', '48m'].forEach(c => {
        const btn = document.getElementById('btn-cycle-' + c);
        if (!btn) return;
        if (c === cycle) {
            btn.className = 'px-5 py-2.5 rounded-xl text-xs font-extrabold bg-[#6C47FF] text-white shadow transition flex items-center gap-1.5';
        } else {
            btn.className = 'px-5 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900 transition flex items-center gap-1.5';
        }
    });

    document.querySelectorAll('.plan-price').forEach(el => {
        const monthly = el.dataset.monthly;
        const yearly = el.dataset.yearly;
        const fortyEight = el.dataset['48m'];

        const container = el.closest('.rounded-3xl');
        const subtext = container ? container.querySelector('.plan-subtext') : null;
        const regPrice = container ? container.querySelector('.plan-regular-price') : null;

        if (cycle === 'monthly') {
            el.innerText = parseFloat(monthly).toFixed(2);
            if (subtext) subtext.innerText = `Billed ₹${monthly} monthly. Cancel anytime.`;
            if (regPrice) regPrice.innerText = `₹${Math.round(parseInt(monthly) * 1.5)}`;
        } else if (cycle === '48m') {
            el.innerText = parseFloat(fortyEight).toFixed(2);
            const total = parseInt(fortyEight) * 48;
            const regTotal = total * 3;
            if (subtext) subtext.innerText = `Get 48 months for ₹${total.toLocaleString('en-IN')}.00 (regular price ₹${regTotal.toLocaleString('en-IN')}). Cancel anytime.`;
            if (regPrice) regPrice.innerText = `₹${Math.round(parseInt(fortyEight) * 2.5)}`;
        } else {
            el.innerText = parseFloat(yearly).toFixed(2);
            const total = parseInt(yearly) * 12;
            const regTotal = total * 2;
            if (subtext) subtext.innerText = `Get 12 months for ₹${total.toLocaleString('en-IN')}.00 (regular price ₹${regTotal.toLocaleString('en-IN')}). Cancel anytime.`;
            if (regPrice) regPrice.innerText = `₹${Math.round(parseInt(yearly) * 2)}`;
        }
    });

    document.querySelectorAll('.plan-order-link').forEach(link => {
        const slug = link.dataset.slug;
        const promoParam = (window.ACTIVE_PROMO_CODE && window.ACTIVE_PROMO_CODE.trim()) ? `&coupon=${encodeURIComponent(window.ACTIVE_PROMO_CODE.trim())}` : '';
        link.href = `/checkout?plan=${slug}&cycle=${cycle}${promoParam}`;
    });
}

// 3. Live Domain Search in Light Theme
const searchForm = document.getElementById('domain-search-form');
if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('domain-input');
        const query = input.value.trim();
        if (!query) return;

        const btnText = document.getElementById('search-btn-text');
        if (btnText) btnText.innerText = 'Checking...';

        const resultsBox = document.getElementById('domain-results-box');

        try {
            const res = await fetch(`/api/domain-search?domain=${encodeURIComponent(query)}`);
            const data = await res.json();

            if (btnText) btnText.innerText = 'Check Domain';

            if (data.success && resultsBox) {
                resultsBox.classList.remove('hidden');
                
                let html = `<div class="space-y-2.5 pt-2">`;

                data.results.forEach((item) => {
                    const isAvailable = item.available;
                    html += `
                        <div class="p-4 rounded-2xl bg-slate-50 border ${isAvailable ? 'border-primary-200' : 'border-slate-200'} flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <span class="w-3 h-3 rounded-full ${isAvailable ? 'bg-emerald-500' : 'bg-rose-500'}"></span>
                                <div>
                                    <strong class="text-sm font-bold ${isAvailable ? 'text-slate-900' : 'text-slate-400 line-through'} font-mono">${item.domain}</strong>
                                    <span class="text-[11px] block ${isAvailable ? 'text-emerald-700' : 'text-rose-600'} font-bold">
                                        ${isAvailable ? '✓ Available for instant registration' : '✗ Already Registered'}
                                    </span>
                                </div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="text-right">
                                    <span class="text-sm font-bold text-slate-900 font-mono">₹${item.price}</span>
                                    <span class="text-[10px] text-slate-500 block">Renews at ₹${item.renewal}/yr</span>
                                </div>
                                ${isAvailable ? `
                                    <a href="/checkout?plan=premium-hosting&domain=${item.domain}&cycle=yearly" class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1 shadow-sm">
                                        Select & Host &rarr;
                                    </a>
                                ` : `
                                    <button disabled class="px-3 py-1.5 bg-slate-200 text-slate-400 rounded-xl text-xs font-semibold cursor-not-allowed">
                                        Taken
                                    </button>
                                `}
                            </div>
                        </div>
                    `;
                });

                html += `</div>`;
                resultsBox.innerHTML = html;
            }
        } catch (err) {
            console.error(err);
            if (btnText) btnText.innerText = 'Search Failed';
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    startCountdown();
});
