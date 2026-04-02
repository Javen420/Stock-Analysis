<template>
  <div class="bg-cream">
    <!-- ═══ HERO ═══ -->
    <HeroSection />

    <!-- ═══ EXPANDED LANDING TEASER ═══ -->
    <section class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 pb-32 pt-16">
      <!-- Trusted By / Value Prop -->
      <div class="border-y border-charcoal/10 py-16 text-center space-y-6 mb-32 hidden md:block">
        <p class="font-mono text-sm uppercase tracking-widest text-charcoal/40 font-bold mb-8">Integrated Data Providers</p>
        <div class="flex flex-wrap justify-center items-center gap-12 md:gap-24 opacity-40 grayscale">
          <div class="font-heading font-black text-2xl tracking-tighter">DATA<span class="font-drama italic font-normal">stream</span></div>
          <div class="font-mono text-xl font-bold tracking-widest">QUANT//NET</div>
          <div class="font-body text-2xl font-bold">Alpaca</div>
          <div class="font-heading font-bold text-2xl">Polygon.io</div>
        </div>
      </div>

      <!-- Mini Vision UNBOXED -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 md:gap-24 items-center">
        <div class="space-y-8 order-2 lg:order-1">
          <span class="font-mono text-xs text-moss uppercase tracking-widest font-bold bg-moss/10 px-3 py-1 rounded-full text-moss">The Edge</span>
          <h2 class="font-heading font-bold text-4xl md:text-6xl text-charcoal tracking-tight leading-[1]">Stop guessing.<br />Start knowing.</h2>
          <p class="text-xl text-charcoal/50 leading-relaxed max-w-lg">
            Stop relying on scattered spreadsheets and delayed financial news. We bring Wall Street's quantitative muscle directly to your browser.
          </p>
          <router-link to="/features" class="inline-flex items-center gap-2 font-mono font-bold text-clay uppercase tracking-widest text-sm hover:text-clay-dark transition-colors group pb-1 border-b border-clay/30 hover:border-clay">
            Explore Capabilities
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="transform group-hover:translate-x-1 transition-transform"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </router-link>
        </div>
        
        <!-- Massive visual representation -->
        <div class="order-1 lg:order-2 w-full aspect-[4/3] rounded-[3rem] overflow-hidden shadow-2xl relative group">
          <div class="absolute inset-0 bg-charcoal/10 mix-blend-multiply group-hover:opacity-0 transition-opacity duration-700 z-10"></div>
          <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80" alt="Analytical Terminal View" class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-1000 ease-out" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import HeroSection from '../components/HeroSection.vue'
</script>
