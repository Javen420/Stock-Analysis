<template>
  <section id="features" class="section-pad bg-cream relative overflow-hidden flex flex-col items-center justify-center min-h-[80vh]">
    <!-- Section Header -->
    <div class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 mb-24 text-center">
      <div class="inline-flex flex-col items-center">
        <span class="font-mono text-xs text-clay uppercase tracking-widest flex items-center gap-3 mb-6">
          <span class="inline-block w-6 h-px bg-clay"></span>
          Core Capabilities
          <span class="inline-block w-6 h-px bg-clay"></span>
        </span>
        <h2 class="font-heading text-5xl md:text-7xl lg:text-8xl font-bold tracking-tighter text-charcoal max-w-4xl leading-[0.9]">
          Diagnostic tools for the modern allocator.
        </h2>
      </div>
    </div>

    <div class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 space-y-48">

      <!-- Feature 1: Alternating Left -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-32 2xl:gap-48 items-center">
        <!-- Visual -->
        <div class="relative w-full aspect-[4/5] md:aspect-video lg:aspect-[4/5] rounded-[3rem] overflow-hidden shadow-2xl shadow-charcoal/5 group">
          <div class="absolute inset-0 bg-gradient-to-tr from-charcoal/80 via-transparent to-transparent z-10 opacity-60"></div>
          <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80" alt="Market Data Screen" class="w-full h-full object-cover scale-100 group-hover:scale-105 transition-transform duration-1000 ease-out" />
          <div class="absolute bottom-8 left-8 right-8 z-20 text-cream backdrop-blur-md bg-white/10 p-6 rounded-2xl border border-white/20">
             <div class="text-xs font-mono uppercase tracking-widest text-cream/70 mb-2">Live Factor Models</div>
             <div class="font-heading font-bold text-2xl">Value, Growth, Momentum.</div>
          </div>
        </div>
        <!-- Copy -->
        <div class="space-y-6">
          <div class="font-mono text-[10px] text-moss uppercase tracking-widest font-bold bg-moss/10 px-3 py-1 rounded-full inline-block">01 / Insight Engine</div>
          <h3 class="font-heading text-4xl md:text-5xl font-bold text-charcoal tracking-tight">Institutional-Grade Insights</h3>
          <p class="font-body text-charcoal/60 text-lg leading-relaxed max-w-lg">
            Uncover deep technical metrics and risk-adjusted returns usually reserved for professionals. Our proprietary scoring system analyzes value, growth, and momentum simultaneously to synthesize raw market data into executable conviction.
          </p>
        </div>
      </div>

      <!-- Feature 2: Alternating Right -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-32 2xl:gap-48 items-center">
        <!-- Copy -->
        <div class="space-y-6 order-2 lg:order-1">
          <div class="font-mono text-[10px] text-clay uppercase tracking-widest font-bold bg-clay/10 px-3 py-1 rounded-full inline-block">02 / Asset Radar</div>
          <h3 class="font-heading text-4xl md:text-5xl font-bold text-charcoal tracking-tight">Unified Tracking</h3>
          <p class="font-body text-charcoal/60 text-lg leading-relaxed max-w-lg">
            Monitor your entire portfolio across sectors and markets in a single, streamlined view. Instantly identify overexposure risks and rebalance with clinical precision without wrestling with disjointed brokerage apps.
          </p>
        </div>
        <!-- Visual -->
        <div class="order-1 lg:order-2 relative w-full aspect-[4/5] md:aspect-video lg:aspect-[4/5] rounded-[3rem] overflow-hidden shadow-2xl shadow-charcoal/5 group">
          <div class="absolute inset-0 bg-gradient-to-tr from-clay/40 via-transparent to-transparent z-10 opacity-30"></div>
          <img src="https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=800&q=80" alt="Analytical Overlay" class="w-full h-full object-cover scale-100 group-hover:scale-105 transition-transform duration-1000 ease-out" />
          <div class="absolute bottom-8 left-8 z-20">
             <div class="w-16 h-16 rounded-full bg-cream shadow-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-clay"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>
             </div>
          </div>
        </div>
      </div>

      <!-- Feature 3: Full Width Banner -->
      <div class="relative w-full rounded-[3rem] overflow-hidden bg-charcoal text-cream shadow-2xl">
        <!-- Background element -->
        <div class="absolute inset-0 opacity-20 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white/20 to-transparent pointer-events-none"></div>
        <img src="https://images.unsplash.com/photo-1642790106117-e829e14a795f?auto=format&fit=crop&w=1600&q=80" class="absolute inset-0 w-full h-full object-cover opacity-20 mix-blend-luminosity" />
        
        <div class="relative z-10 px-8 py-24 md:p-32 flex flex-col items-center justify-center text-center max-w-4xl mx-auto">
          <div class="font-mono text-[10px] text-charcoal uppercase tracking-widest font-bold bg-cream px-3 py-1 rounded-full inline-block mb-8">03 / Signal Protocol</div>
          <h3 class="font-heading text-4xl md:text-6xl font-bold tracking-tight mb-6">Data-Driven Conviction</h3>
          <p class="font-body text-cream/70 text-lg md:text-xl leading-relaxed mb-12 max-w-2xl">
            Simulate target allocations before committing capital. Our environment empowers you to stress-test your thesis against historical volatility and sector concentrations.
          </p>
          <router-link to="/portfolio/new" class="bg-moss/20 border border-moss/50 text-moss hover:bg-moss hover:text-cream transition-all px-8 py-4 rounded-full font-bold uppercase tracking-widest text-xs font-mono shadow-xl">
             Try the Simulator
          </router-link>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
</script>
