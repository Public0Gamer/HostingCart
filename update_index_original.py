import re

print("Updating templates/index.html with 100% Original HostingChahiye Branding...")

with open(r"templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

original_pricing_section = """<!-- Pricing Section: 100% Original HostingChahiye Cloud Architecture -->
<section id="pricing" class="py-20 bg-slate-50 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-14">
            <span class="text-xs font-black uppercase tracking-wider text-blue-600 mb-2 block">Ultra-Fast NVMe Hosting • India Datacenters • 100% Transparent</span>
            <h2 class="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight mb-4">
                Choose the Right Hosting Plan
            </h2>
            <p class="text-slate-600 text-sm sm:text-base">
                Instant automated cloud setup. Free Wildcard SSL, Free Domain with annual billing, and our 30-Day Money-Back Guarantee.
            </p>

            <!-- Billing Cycle Switcher -->
            <div class="inline-flex items-center p-1.5 rounded-2xl bg-white border border-slate-200 mt-8 gap-1 shadow-sm">
                <button type="button" onclick="setBillingCycle('48m')" id="btn-cycle-48m" class="px-5 py-2.5 rounded-xl text-xs font-extrabold bg-blue-600 text-white shadow transition flex items-center gap-1.5">
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
            <!-- ================= CARD 1: SINGLE STARTER ================= -->
            <div class="bg-white rounded-3xl p-7 border border-slate-200 flex flex-col justify-between hover:shadow-xl transition relative">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 rounded-full text-xs font-black bg-blue-50 text-blue-700">Save 84%</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-1">Single Starter</h3>
                    <p class="text-xs text-slate-500 mb-6 h-8 leading-snug">Perfect for personal portfolios, resumes, and simple blogs.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹299</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-600 font-bold">₹</span>
                            <span class="text-4xl font-black text-slate-900 plan-price" data-monthly="49" data-yearly="49" data-48m="49">49.00</span>
                            <span class="text-xs text-slate-500 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-600"></i> 'HOSTINGCHAHIYE' applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=single&cycle=48m" class="plan-order-link w-full py-3 rounded-2xl border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white font-black text-xs text-center block transition shadow-sm mb-3" data-slug="single">
                        Choose Starter
                    </a>
                    <div class="text-[11px] text-slate-500 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹2,352.00 (regular price ₹14,352). Renews at ₹199/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-700 border-t border-slate-100 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>1</strong> Website</span>
                        </li>
                        <li class="flex items-center gap-2 text-slate-400">
                            <i data-lucide="minus" class="w-4 h-4 text-slate-300 flex-shrink-0"></i>
                            <span>Free Domain</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>10 GB</strong> NVMe SSD Storage</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Free Weekly Backups</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Free Wildcard SSL Certificate</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>1-Click WordPress Installer</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>LiteSpeed Enterprise Cache</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>1 Free Business Mailbox</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- ================= CARD 2: PLUS GROWTH ================= -->
            <div class="bg-white rounded-3xl p-7 border border-slate-200 flex flex-col justify-between hover:shadow-xl transition relative">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 rounded-full text-xs font-black bg-blue-50 text-blue-700">Save 78%</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-1">Plus Growth</h3>
                    <p class="text-xs text-slate-500 mb-6 h-8 leading-snug">Best value for growing creators, startups & small businesses.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹499</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-600 font-bold">₹</span>
                            <span class="text-4xl font-black text-slate-900 plan-price" data-monthly="119" data-yearly="119" data-48m="119">119.00</span>
                            <span class="text-xs text-slate-500 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-600"></i> 'HOSTINGCHAHIYE' applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=premium&cycle=48m" class="plan-order-link w-full py-3 rounded-2xl border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white font-black text-xs text-center block transition shadow-sm mb-3" data-slug="premium">
                        Choose Plus Growth
                    </a>
                    <div class="text-[11px] text-slate-500 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹5,712.00 (regular price ₹23,952). Renews at ₹299/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-700 border-t border-slate-100 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>3</strong> Websites</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-orange-600">
                            <i data-lucide="check" class="w-4 h-4 text-orange-600 flex-shrink-0"></i>
                            <span>Free Domain (.IN or .COM)</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>20 GB</strong> NVMe SSD Storage</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Free Weekly Backups</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Free Wildcard SSL Certificate</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>1-Click WordPress & Visual Builder</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>LiteSpeed Enterprise Cache</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>3 Free Business Mailboxes</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- ================= CARD 3: BUSINESS PRO (FEATURED HERO CARD) ================= -->
            <div class="bg-[#0F172A] text-white rounded-3xl p-7 border-2 border-blue-600 shadow-2xl flex flex-col justify-between relative transform lg:-translate-y-2">
                <div class="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-[11px] font-black px-4 py-1 rounded-full uppercase tracking-wider shadow-lg shadow-blue-600/40 flex items-center gap-1.5 whitespace-nowrap">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-300"></i> ⭐ Most Popular • Save 68%
                </div>

                <div>
                    <div class="flex items-center gap-2 mb-1 mt-2">
                        <i data-lucide="zap" class="w-5 h-5 text-blue-400"></i>
                        <h3 class="text-2xl font-black text-white">Business Pro</h3>
                    </div>
                    <p class="text-xs text-slate-300 mb-6 h-8 leading-snug">All-inclusive cloud package for e-commerce, high traffic & agencies.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹599</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-400 font-bold">₹</span>
                            <span class="text-4xl font-black text-white plan-price" data-monthly="199" data-yearly="199" data-48m="199">199.00</span>
                            <span class="text-xs text-slate-400 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-400"></i> 'HOSTINGCHAHIYE' applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=unlimited&cycle=48m" class="plan-order-link w-full py-3.5 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs text-center block shadow-lg shadow-blue-600/40 transition mb-3" data-slug="unlimited">
                        Get Started Now
                    </a>
                    <div class="text-[11px] text-slate-400 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹9,552.00 (regular price ₹28,752). Renews at ₹449/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-200 border-t border-slate-800 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span><strong class="text-white">Unlimited</strong> Websites</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-orange-400">
                            <i data-lucide="check" class="w-4 h-4 text-orange-400 flex-shrink-0"></i>
                            <span>Free Domain Included</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span><strong class="text-white">50 GB</strong> NVMe SSD Storage</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-white">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Daily Backups + 1-Click Restore</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Free Cloud CDN Integration</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>LiteSpeed LSCache Optimized</span>
                        </li>
                        <li class="flex items-center gap-2 text-white font-bold">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Unlimited Business Mailboxes</span>
                        </li>
                        <li class="flex items-center gap-2 text-white font-bold">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-400 flex-shrink-0"></i>
                            <span>Direct Priority WhatsApp Support</span>
                        </li>
                    </ul>

                    <!-- Why this plan? Card -->
                    <div class="mt-6 p-4 rounded-2xl bg-[#1E293B] border border-slate-700 text-xs text-slate-300">
                        <div class="font-black text-white mb-1">Why choose Business Pro?</div>
                        <div class="text-[11px] leading-relaxed">Our flagship package designed for high performance, e-commerce stores, and peace of mind.</div>
                    </div>
                </div>
            </div>

            <!-- ================= CARD 4: ENTERPRISE CLOUD ================= -->
            <div class="bg-white rounded-3xl p-7 border border-slate-200 flex flex-col justify-between hover:shadow-xl transition relative">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 rounded-full text-xs font-black bg-blue-50 text-blue-700">Dedicated Power</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-1">Enterprise Cloud</h3>
                    <p class="text-xs text-slate-500 mb-6 h-8 leading-snug">Dedicated isolated vCPU & NVMe power for mission-critical portals & stores.</p>

                    <!-- Price Box -->
                    <div class="mb-4">
                        <div class="text-xs text-slate-400 line-through font-semibold plan-regular-price">₹1,399</div>
                        <div class="flex items-baseline gap-1 my-0.5">
                            <span class="text-xs text-slate-600 font-bold">₹</span>
                            <span class="text-4xl font-black text-slate-900 plan-price" data-monthly="479" data-yearly="479" data-48m="479">479.00</span>
                            <span class="text-xs text-slate-500 font-semibold">/mo</span>
                        </div>
                        <div class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg mt-1 mb-2">
                            <i data-lucide="tag" class="w-3 h-3 text-emerald-600"></i> 'HOSTINGCHAHIYE' applied
                        </div>
                    </div>

                    <!-- CTA Button -->
                    <a href="/checkout?plan=cloud-startup&cycle=48m" class="plan-order-link w-full py-3 rounded-2xl border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white font-black text-xs text-center block transition shadow-sm mb-3" data-slug="cloud-startup">
                        Choose Enterprise
                    </a>
                    <div class="text-[11px] text-slate-500 mb-6 plan-subtext leading-tight">
                        Get 48 months for ₹22,992.00 (regular price ₹67,152). Renews at ₹899/mo.
                    </div>

                    <!-- Core Features Checklist -->
                    <ul class="space-y-2.5 text-xs text-slate-700 border-t border-slate-100 pt-5 mb-5 font-medium">
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>Unlimited</strong> Websites</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-orange-600">
                            <i data-lucide="check" class="w-4 h-4 text-orange-600 flex-shrink-0"></i>
                            <span>Free Domain Included</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span><strong>100 GB</strong> Dedicated NVMe SSD</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-slate-900">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Daily & On-Demand Snapshots</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Dedicated Isolated vCPU & RAM</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-slate-900">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>Dedicated IP Address Ready</span>
                        </li>
                        <li class="flex items-center gap-2 font-bold text-slate-900">
                            <i data-lucide="check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                            <span>VIP 24/7 Priority Support</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- View All Features Link -->
        <div class="text-center mt-12">
            <a href="#features" class="inline-flex items-center gap-1.5 text-sm font-bold text-blue-600 hover:text-blue-800 transition">
                <span>Compare all hosting features & specifications</span>
                <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </a>
        </div>
    </div>
</section>"""

old_section_pattern = re.compile(r'<!-- Pricing Section.*?-->.*?</section>', re.DOTALL)
if old_section_pattern.search(html):
    html = old_section_pattern.sub(original_pricing_section, html, count=1)
    with open(r"templates/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] templates/index.html updated with 100% original HostingChahiye branding.")
else:
    print("Could not find pricing section in index.html.")
