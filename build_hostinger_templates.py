import re

print("1. Updating templates/index.html with Hostinger Exact 4-Tier Pricing Grid...")

with open(r"C:\Users\at781\.gemini\antigravity\scratch\apexhost-platform\templates\index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_pricing_section = """<!-- Pricing Section: Hostinger Exact 4-Card Matching Architecture -->
<section id="pricing" class="py-20 bg-[#F8F9FA] border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-14">
            <span class="text-xs font-black uppercase tracking-wider text-[#6C47FF] mb-2 block">Enterprise Speed • ₹0 Server Costs • 100% Automated</span>
            <h2 class="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight mb-4">
                Choose the Right Hosting Plan
            </h2>
            <p class="text-slate-600 text-sm sm:text-base">
                Instant automated activation. Cheaper than Hostinger, with Free SSL, Domain, and 30-Day Money-Back Guarantee.
            </p>

            <!-- Billing Cycle Switcher -->
            <div class="inline-flex items-center p-1.5 rounded-2xl bg-white border border-slate-200 mt-8 gap-1 shadow-sm">
                <button type="button" onclick="setBillingCycle('48m')" id="btn-cycle-48m" class="px-5 py-2.5 rounded-xl text-xs font-extrabold bg-[#6C47FF] text-white shadow transition flex items-center gap-1.5">
                    48 Months <span class="bg-emerald-500 text-[10px] text-white px-2 py-0.5 rounded-full font-black uppercase">Best Value</span>
                </button>
                <button type="button" onclick="setBillingCycle('yearly')" id="btn-cycle-yearly" class="px-5 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900 transition flex items-center gap-1.5">
                    12 Months <span class="text-orange-600 text-[10px] font-bold bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">Free Domain</span>
                </button>
                <button type="button" onclick="setBillingCycle('monthly')" id="btn-cycle-monthly" class="px-5 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900 transition">
                    1 Month
                </button>
            </div>
        </div>

        <!-- 4 Plans Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
            <!-- ================= CARD 1: SINGLE ================= -->
            <div class="bg-white rounded-3xl p-7 border border-slate-200 flex flex-col justify-between hover:shadow-xl transition relative">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 rounded-full text-xs font-black bg-[#EDE9FE] text-[#6C47FF]">84% off</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-1">Single</h3>
                    <p class="text-xs text-slate-500 mb-6 h-8 leading-snug">Get your first website online. Best for beginners or simple projects.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹299</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-600 font-bold">₹</span>
                            <span class="text-4xl font-black text-slate-900 plan-price" data-monthly="49" data-yearly="49" data-48m="49">49.00</span>
                            <span class="text-xs text-slate-500 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-600"></i> 'HOSTINGPRO' coupon applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=single&cycle=48m" class="plan-order-link w-full py-3 rounded-2xl border-2 border-[#6C47FF] text-[#6C47FF] hover:bg-[#6C47FF] hover:text-white font-black text-xs text-center block transition shadow-sm mb-3" data-slug="single">
                        Choose plan
                    </a>
                    <div class="text-[11px] text-slate-500 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹2,352.00 (regular price ₹14,352). Renews at ₹199/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-700 border-t border-slate-100 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>1</strong> website</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>Free domain</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>10 GB</strong> SSD storage</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Free weekly backups</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Ecommerce available</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>CDN</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>AI tools</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>Priority 24/7 expert support</span>
                        </li>
                    </ul>

                    <!-- Build With Section -->
                    <div class="border-t border-slate-100 pt-4 mb-4 text-xs">
                        <span class="text-[11px] font-bold text-slate-900 block mb-2">Build with:</span>
                        <ul class="space-y-2 text-slate-600">
                            <li class="flex items-center gap-2">
                                <i data-lucide="cpu" class="w-3.5 h-3.5 text-[#6C47FF]"></i>
                                <span>AI Builder (5 credits)</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="globe" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>WordPress</span>
                            </li>
                            <li class="flex items-center gap-2 text-slate-400">
                                <i data-lucide="minus" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>Node.js</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Communicate & Grow -->
                    <div class="border-t border-slate-100 pt-4 text-xs">
                        <span class="text-[11px] font-bold text-slate-900 block mb-2">Communicate & grow:</span>
                        <ul class="space-y-2 text-slate-600">
                            <li class="flex items-center gap-2">
                                <i data-lucide="mail" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>Free mailbox</span>
                            </li>
                            <li class="flex items-center gap-2 text-slate-400">
                                <i data-lucide="minus" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>AI email marketing</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- ================= CARD 2: PREMIUM ================= -->
            <div class="bg-white rounded-3xl p-7 border border-slate-200 flex flex-col justify-between hover:shadow-xl transition relative">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 rounded-full text-xs font-black bg-[#EDE9FE] text-[#6C47FF]">78% off</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-1">Premium</h3>
                    <p class="text-xs text-slate-500 mb-6 h-8 leading-snug">Run websites smoothly. Great for creators and small brands.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹499</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-600 font-bold">₹</span>
                            <span class="text-4xl font-black text-slate-900 plan-price" data-monthly="119" data-yearly="119" data-48m="119">119.00</span>
                            <span class="text-xs text-slate-500 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-600"></i> 'HOSTINGPRO' coupon applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=premium&cycle=48m" class="plan-order-link w-full py-3 rounded-2xl border-2 border-[#6C47FF] text-[#6C47FF] hover:bg-[#6C47FF] hover:text-white font-black text-xs text-center block transition shadow-sm mb-3" data-slug="premium">
                        Choose plan
                    </a>
                    <div class="text-[11px] text-slate-500 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹5,712.00 (regular price ₹23,952). Renews at ₹299/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-700 border-t border-slate-100 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>3</strong> websites</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-emerald-700">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Domain - free for 1 year</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>20 GB</strong> SSD storage</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Free weekly backups</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Ecommerce available</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>CDN</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>AI tools</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>Priority 24/7 expert support</span>
                        </li>
                    </ul>

                    <!-- Build With Section -->
                    <div class="border-t border-slate-100 pt-4 mb-4 text-xs">
                        <span class="text-[11px] font-bold text-slate-900 block mb-2">Build with:</span>
                        <ul class="space-y-2 text-slate-600">
                            <li class="flex items-center gap-2">
                                <i data-lucide="cpu" class="w-3.5 h-3.5 text-[#6C47FF]"></i>
                                <span>AI Builder (5 credits)</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="globe" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>WordPress</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="shopping-bag" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>Build or manage store with AI</span>
                            </li>
                            <li class="flex items-center gap-2 text-slate-400">
                                <i data-lucide="minus" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>Node.js</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Communicate & Grow -->
                    <div class="border-t border-slate-100 pt-4 text-xs">
                        <span class="text-[11px] font-bold text-slate-900 block mb-2">Communicate & grow:</span>
                        <ul class="space-y-2 text-slate-600">
                            <li class="flex items-center gap-2 text-emerald-700 font-bold">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i>
                                <span>2 mailboxes / site - free 1 yr</span>
                            </li>
                            <li class="flex items-center gap-2 text-slate-400">
                                <i data-lucide="minus" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>AI email marketing</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- ================= CARD 3: UNLIMITED (FEATURED DARK HERO) ================= -->
            <div class="bg-[#111026] text-white rounded-3xl p-7 border-2 border-[#6C47FF] shadow-2xl flex flex-col justify-between relative transform lg:-translate-y-2">
                <div class="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-[#6C47FF] text-white text-[11px] font-black px-4 py-1 rounded-full uppercase tracking-wider shadow-lg shadow-[#6C47FF]/40 flex items-center gap-1.5 whitespace-nowrap">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-300"></i> Special offer &bull; 68% off
                </div>

                <div>
                    <div class="flex items-center gap-2 mb-1 mt-2">
                        <i data-lucide="sparkles" class="w-5 h-5 text-[#8B6FFF]"></i>
                        <h3 class="text-2xl font-black text-white">Unlimited</h3>
                    </div>
                    <p class="text-xs text-slate-300 mb-6 h-8 leading-snug">Unlimited websites and mailboxes, plus AI tools and priority support for maximum flexibility.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹599</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-400 font-bold">₹</span>
                            <span class="text-4xl font-black text-white plan-price" data-monthly="199" data-yearly="199" data-48m="199">199.00</span>
                            <span class="text-xs text-slate-400 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-400"></i> 'HOSTINGPRO' coupon applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=unlimited&cycle=48m" class="plan-order-link w-full py-3.5 rounded-2xl bg-[#6C47FF] hover:bg-[#5835E5] text-white font-extrabold text-xs text-center block shadow-lg shadow-[#6C47FF]/40 transition mb-3" data-slug="unlimited">
                        Choose plan
                    </a>
                    <div class="text-[11px] text-slate-400 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹9,552.00 (regular price ₹28,752). Renews at ₹449/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-200 border-t border-slate-800 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span><strong class="text-white">Unlimited</strong> websites</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-emerald-400">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Domain - free for 1 year</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span><strong class="text-white">50 GB</strong> NVMe storage</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Daily backups + easy data restore</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>CDN included</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Ecommerce available</span>
                        </li>
                        <li class="flex items-center gap-2 text-white font-bold">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>AI tools</span>
                        </li>
                        <li class="flex items-center gap-2 text-white font-bold">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Priority 24/7 expert support</span>
                        </li>
                    </ul>

                    <!-- Build With Section -->
                    <div class="border-t border-slate-800 pt-4 mb-4 text-xs">
                        <span class="text-[11px] font-bold text-white block mb-2">Build with:</span>
                        <ul class="space-y-2 text-slate-300">
                            <li class="flex items-center gap-2">
                                <i data-lucide="cpu" class="w-3.5 h-3.5 text-[#8B6FFF]"></i>
                                <span class="font-bold text-white">AI Builder (15 credits)</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="globe" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>WordPress</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="shopping-bag" class="w-3.5 h-3.5 text-slate-300"></i>
                                <span>Build or manage store with AI assistant</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="terminal" class="w-3.5 h-3.5 text-[#8B6FFF]"></i>
                                <span>Node.js</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Communicate & Grow -->
                    <div class="border-t border-slate-800 pt-4 text-xs">
                        <span class="text-[11px] font-bold text-white block mb-2">Communicate & grow:</span>
                        <ul class="space-y-2 text-slate-300">
                            <li class="flex items-center gap-2 text-emerald-400 font-bold">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i>
                                <span>Unlimited mailboxes / site - free 1 yr</span>
                            </li>
                            <li class="flex items-center gap-2 text-emerald-400 font-bold">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i>
                                <span>AI email marketing - free 1 yr</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Why this plan? Card (From Hostinger Screenshot) -->
                    <div class="mt-6 p-4 rounded-2xl bg-[#1B1938] border border-[#2F2C59] text-xs text-slate-300">
                        <div class="font-black text-white mb-1">Why this plan?</div>
                        <div class="text-[11px] leading-relaxed">A complete solution for long-term projects. Everything included.</div>
                    </div>
                </div>
            </div>

            <!-- ================= CARD 4: CLOUD STARTUP ================= -->
            <div class="bg-white rounded-3xl p-7 border border-slate-200 flex flex-col justify-between hover:shadow-xl transition relative">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 rounded-full text-xs font-black bg-[#EDE9FE] text-[#6C47FF]">68% off</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-1">Cloud Startup</h3>
                    <p class="text-xs text-slate-500 mb-6 h-8 leading-snug">Dedicated power for agencies or high-traffic projects.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹1,399</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-600 font-bold">₹</span>
                            <span class="text-4xl font-black text-slate-900 plan-price" data-monthly="479" data-yearly="479" data-48m="479">479.00</span>
                            <span class="text-xs text-slate-500 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-600"></i> 'HOSTINGPRO' coupon applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=cloud-startup&cycle=48m" class="plan-order-link w-full py-3 rounded-2xl border-2 border-[#6C47FF] text-[#6C47FF] hover:bg-[#6C47FF] hover:text-white font-black text-xs text-center block transition shadow-sm mb-3" data-slug="cloud-startup">
                        Choose plan
                    </a>
                    <div class="text-[11px] text-slate-500 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹22,992.00 (regular price ₹67,152). Renews at ₹899/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-700 border-t border-slate-100 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>Unlimited</strong> websites</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-emerald-700">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Domain - free for 1 year</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>100 GB</strong> NVMe storage</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Daily and on demand backups</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>CDN included</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Ecommerce available</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-slate-900">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>AI tools</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-slate-900">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Priority 24/7 expert support</span>
                        </li>
                    </ul>

                    <!-- Build With Section -->
                    <div class="border-t border-slate-100 pt-4 mb-4 text-xs">
                        <span class="text-[11px] font-bold text-slate-900 block mb-2">Build with:</span>
                        <ul class="space-y-2 text-slate-600">
                            <li class="flex items-center gap-2">
                                <i data-lucide="cpu" class="w-3.5 h-3.5 text-[#6C47FF]"></i>
                                <span class="font-bold">AI Builder (15 credits)</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="globe" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>WordPress</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="shopping-bag" class="w-3.5 h-3.5 text-slate-700"></i>
                                <span>Build or manage store with AI</span>
                            </li>
                            <li class="flex items-center gap-2">
                                <i data-lucide="terminal" class="w-3.5 h-3.5 text-[#6C47FF]"></i>
                                <span>Node.js</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Communicate & Grow -->
                    <div class="border-t border-slate-100 pt-4 text-xs">
                        <span class="text-[11px] font-bold text-slate-900 block mb-2">Communicate & grow:</span>
                        <ul class="space-y-2 text-slate-600">
                            <li class="flex items-center gap-2 text-emerald-700 font-bold">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i>
                                <span>Unlimited mailboxes / site - free 1 yr</span>
                            </li>
                            <li class="flex items-center gap-2 text-emerald-700 font-bold">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i>
                                <span>AI email marketing - free 1 yr</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- View All Features Link (From Hostinger Screenshot) -->
        <div class="text-center mt-12">
            <a href="#features" class="inline-flex items-center gap-1.5 text-sm font-bold text-[#6C47FF] hover:text-[#5835E5] transition">
                <span>View all features</span>
                <i data-lucide="arrow-up-right" class="w-4 h-4"></i>
            </a>
        </div>
    </div>
</section>"""

# Replace old pricing section with new pricing section
old_section_pattern = re.compile(r'<!-- Pricing Section -->.*?</section>', re.DOTALL)
if old_section_pattern.search(html):
    html = old_section_pattern.sub(new_pricing_section, html, count=1)
    with open(r"C:\Users\at781\.gemini\antigravity\scratch\apexhost-platform\templates\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] templates/index.html updated successfully with Hostinger pricing.")
else:
    print("Could not find old pricing section.")
