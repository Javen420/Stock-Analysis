<template>
  <section class="min-h-screen flex items-center justify-center pt-24 overflow-hidden bg-cream text-charcoal">
    <div class="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 md:grid-cols-2 gap-12 lg:gap-24 items-center">
      
      <!-- Copy -->
      <div class="relative z-10 space-y-8">
        <h1 class="font-drama text-5xl md:text-7xl lg:text-8xl leading-[0.9] tracking-tighter">
          Decode the
          <span class="block text-moss">Market's DNA.</span>
        </h1>
        <p class="font-body text-lg md:text-xl text-charcoal/70 max-w-lg leading-relaxed">
          Institutional-grade analytics wrapped in a clinical, organic interface. Stop guessing. Start knowing.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-wrap items-center gap-4 pt-4">
          <router-link to="/dashboard" class="btn-magnetic px-8 py-4 rounded-full bg-clay text-cream hover:bg-clay-dark transition-all duration-300 font-heading font-semibold text-sm shadow-xl shadow-clay/20 flex items-center gap-3 group">
            Start Analysing
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="transform group-hover:translate-x-1 transition-transform"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </router-link>
        </div>

        <div class="flex items-center gap-6 pt-8 border-t border-charcoal/10 max-w-sm">
          <div>
            <div class="font-mono text-2xl tracking-tighter font-bold text-moss">3.4M+</div>
            <div class="font-mono text-[10px] uppercase tracking-widest text-charcoal/50">Data points</div>
          </div>
          <div class="w-px h-8 bg-charcoal/10"></div>
          <div>
            <div class="font-mono text-2xl tracking-tighter font-bold text-clay">14</div>
            <div class="font-mono text-[10px] uppercase tracking-widest text-charcoal/50">Proprietary Models</div>
          </div>
        </div>
      </div>

      <!-- Abstract Graphic -->
      <div class="relative h-[400px] md:h-[600px] w-full origin-center">
        <!-- SVG Canvas (Organic Tech Motif) -->
        <svg viewBox="0 0 500 500" class="w-full h-full opacity-90 drop-shadow-2xl">
          <defs>
            <linearGradient id="mossGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="var(--color-moss-light)" />
              <stop offset="100%" stop-color="var(--color-moss)" />
            </linearGradient>
            <linearGradient id="clayGrad" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="var(--color-clay)" />
              <stop offset="100%" stop-color="var(--color-clay-dark)" />
            </linearGradient>
            <filter id="blur">
              <feGaussianBlur stdDeviation="8" />
            </filter>
          </defs>
          
          <g transform="translate(250 250)">
            <circle cx="0" cy="0" r="180" fill="none" stroke="var(--color-charcoal)" stroke-opacity="0.05" stroke-width="1" />
            <circle cx="0" cy="0" r="120" fill="none" stroke="var(--color-clay)" stroke-opacity="0.2" stroke-width="1" stroke-dasharray="4 8" />
            <path d="M -80,-80 L 120,-40 L 80,100 L -100,60 Z" fill="url(#mossGrad)" opacity="0.9" style="mix-blend-mode: multiply;" />
            <circle cx="40" cy="-20" r="140" fill="url(#clayGrad)" opacity="0.8" style="mix-blend-mode: multiply;" />
            <path d="M -150,0 Q 0,-150 150,0 T -150,0" fill="none" stroke="var(--color-charcoal)" stroke-opacity="0.1" stroke-width="2" />
          </g>
        </svg>
      </div>

    </div>
  </section>
</template>

<script setup>
</script>
