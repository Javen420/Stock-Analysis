<template>
  <section id="protocol" class="bg-cream text-charcoal w-full">
    <div class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 flex flex-col justify-center">
      
      <!-- Header unboxed -->
      <div class="mb-24 md:mb-32">
        <span class="font-mono text-xs text-clay uppercase tracking-widest flex items-center gap-3 mb-6">
          <span class="inline-block w-6 h-px bg-clay"></span>
          The Pipeline
        </span>
        <h2 class="font-heading text-6xl md:text-8xl font-bold tracking-tighter max-w-4xl leading-[0.9]">
          How it works.
        </h2>
      </div>

      <!-- Protocol Flow Unboxed -->
      <div class="space-y-24 md:space-y-32">

        <!-- Phase 1 -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-16 items-start border-t border-charcoal/10 pt-12">
          <div class="md:col-span-3">
            <div class="font-mono text-sm text-moss font-bold uppercase tracking-widest">Phase 01</div>
          </div>
          <div class="md:col-span-9 space-y-6">
            <h3 class="font-heading text-4xl md:text-5xl font-bold text-charcoal tracking-tight">Global Market Sync</h3>
            <p class="font-body text-charcoal/60 text-xl leading-relaxed max-w-3xl">
              The system continuously fetches tick-level market data, parsing standard fundamentals alongside complex price-action histories to feed the proprietary engine. No data is left unparsed.
            </p>
          </div>
        </div>

        <!-- Phase 2 -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-16 items-start border-t border-charcoal/10 pt-12">
          <div class="md:col-span-3">
            <div class="font-mono text-sm text-clay font-bold uppercase tracking-widest">Phase 02</div>
          </div>
          <div class="md:col-span-9 space-y-6">
            <h3 class="font-heading text-4xl md:text-5xl font-bold text-charcoal tracking-tight">Algorithmic Scoring</h3>
            <p class="font-body text-charcoal/60 text-xl leading-relaxed max-w-3xl">
              Moving away from human bias, assets are aggressively graded across Value, Growth, and Momentum axes to produce the unified Q-Score. This happens in real-time, instantly adjusting to market volatility.
            </p>
          </div>
        </div>

        <!-- Phase 3 -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-16 items-start border-t border-charcoal/10 pt-12">
          <div class="md:col-span-3">
            <div class="font-mono text-sm text-charcoal font-bold uppercase tracking-widest">Phase 03</div>
          </div>
          <div class="md:col-span-9 space-y-6">
            <h3 class="font-heading text-4xl md:text-5xl font-bold text-charcoal tracking-tight">Portfolio Construction</h3>
            <p class="font-body text-charcoal/60 text-xl leading-relaxed max-w-3xl">
              The final layer analyzes cross-asset correlation, penalizing concentrated risk and rewarding true diversification, delivering a holistic institutional grade across your entire allocation block.
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
</script>
