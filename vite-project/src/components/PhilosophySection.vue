<template>
  <section id="philosophy" class="bg-cream text-charcoal w-full">
    <div class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 flex flex-col lg:flex-row gap-16 lg:gap-32 2xl:gap-48 items-center justify-center">
      
      <!-- Philosophy text -->
      <div class="flex-1 space-y-12">
        <span class="font-mono text-xs text-clay uppercase tracking-widest flex items-center gap-3">
          <span class="inline-block w-6 h-px bg-clay"></span>
          The Manifesto
        </span>
        <h2 class="font-drama text-6xl md:text-8xl leading-[0.9] tracking-tighter">
          Markets are chaotic.<br />
          <span class="font-heading font-black text-transparent bg-clip-text bg-gradient-to-r from-moss to-clay tracking-tight">Your conviction shouldn't be.</span>
        </h2>
        
        <div class="space-y-6 text-charcoal/70 text-xl md:text-2xl font-body leading-relaxed max-w-3xl border-l-4 border-charcoal/10 pl-8">
          <p>
            Retail investors navigate the market with blindfolds—relying on fragmented sentiment, emotional narratives, and delayed fundamentals.
          </p>
          <p>
            We built Quantalyze to cut out the noise. Designed to arm you with the same ruthless, algorithmic clarity used by systematic funds, wrapped in an interface that doesn't require a Ph.D. in mathematics to interpret.
          </p>
        </div>
      </div>

      <!-- Stats unboxed -->
      <div class="w-full md:w-1/3 flex flex-col gap-16 pt-16">
        <div>
          <div class="font-mono text-7xl md:text-8xl text-charcoal font-bold tracking-tighter mb-4 text-moss">0.14s</div>
          <div class="w-12 h-1 bg-charcoal/10 mb-4"></div>
          <div class="text-sm font-mono text-charcoal/50 uppercase tracking-widest font-bold">Average Latency</div>
          <p class="text-charcoal/40 mt-2 text-sm max-w-xs">Data streams are updated relentlessly from top exchanges.</p>
        </div>
        <div>
          <div class="font-mono text-7xl md:text-8xl text-charcoal font-bold tracking-tighter mb-4 text-clay">99.9%</div>
          <div class="w-12 h-1 bg-charcoal/10 mb-4"></div>
          <div class="text-sm font-mono text-charcoal/50 uppercase tracking-widest font-bold">Model Uptime</div>
          <p class="text-charcoal/40 mt-2 text-sm max-w-xs">Our proprietary analytics engines run 24/7, processing global shifts.</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>
