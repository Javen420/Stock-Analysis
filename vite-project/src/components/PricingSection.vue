<template>
  <section id="pricing" ref="sectionRef" class="section-pad bg-cream relative overflow-hidden">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div ref="headerRef" class="text-center mb-16 md:mb-20 opacity-0">
        <span class="font-mono text-xs text-clay uppercase tracking-widest flex items-center justify-center gap-3 mb-4">
          <span class="inline-block w-6 h-px bg-clay"></span>
          Start Analysing
          <span class="inline-block w-6 h-px bg-clay"></span>
        </span>
        <h2 class="font-heading font-bold text-3xl md:text-5xl text-charcoal tracking-tight leading-tight mb-4">
          Choose your<br>
          <span class="font-drama text-moss text-4xl md:text-6xl">instrument.</span>
        </h2>
        <p class="font-body text-charcoal/50 text-lg max-w-xl mx-auto">
          Every plan is built for investors who take data seriously. Start free, scale when you're ready.
        </p>
      </div>

      <!-- Pricing Cards -->
      <div class="grid md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto">

        <!-- Essential -->
        <div ref="price1" class="card-organic bg-cream-dark p-8 flex flex-col opacity-0">
          <div class="mb-6">
            <span class="font-mono text-[10px] text-moss/50 uppercase tracking-widest">Essential</span>
            <div class="mt-2 flex items-baseline gap-1">
              <span class="font-heading font-bold text-4xl text-charcoal">$0</span>
              <span class="font-body text-charcoal/40 text-sm">/mo</span>
            </div>
            <p class="font-body text-charcoal/50 text-sm mt-2">Core analytics for getting started.</p>
          </div>

          <ul class="space-y-3 mb-8 flex-1">
            <li v-for="f in essentialFeatures" :key="f" class="flex items-start gap-3 text-sm font-body text-charcoal/70">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-moss flex-shrink-0 mt-0.5"><polyline points="20 6 9 17 4 12"/></svg>
              {{ f }}
            </li>
          </ul>

          <button class="btn-magnetic w-full py-3.5 rounded-full font-heading font-semibold text-sm border border-moss/20 text-moss bg-transparent">
            <span class="btn-bg bg-moss/10 rounded-full"></span>
            <span class="btn-content">Get Started Free</span>
          </button>
        </div>

        <!-- Performance (Featured) -->
        <div ref="price2" class="card-organic bg-moss p-8 flex flex-col ring-2 ring-clay/30 opacity-0 relative">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-clay text-cream font-mono text-[10px] uppercase tracking-widest px-4 py-1 rounded-full">
            Most Popular
          </div>
          <div class="mb-6">
            <span class="font-mono text-[10px] text-cream/50 uppercase tracking-widest">Performance</span>
            <div class="mt-2 flex items-baseline gap-1">
              <span class="font-heading font-bold text-4xl text-cream">$49</span>
              <span class="font-body text-cream/40 text-sm">/mo</span>
            </div>
            <p class="font-body text-cream/50 text-sm mt-2">Full analytics suite for serious investors.</p>
          </div>

          <ul class="space-y-3 mb-8 flex-1">
            <li v-for="f in performanceFeatures" :key="f" class="flex items-start gap-3 text-sm font-body text-cream/80">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-clay flex-shrink-0 mt-0.5"><polyline points="20 6 9 17 4 12"/></svg>
              {{ f }}
            </li>
          </ul>

          <button class="btn-magnetic w-full py-3.5 rounded-full font-heading font-semibold text-sm bg-clay text-cream">
            <span class="btn-bg bg-clay-dark rounded-full"></span>
            <span class="btn-content">Start Analysing</span>
          </button>
        </div>

        <!-- Enterprise -->
        <div ref="price3" class="card-organic bg-cream-dark p-8 flex flex-col opacity-0">
          <div class="mb-6">
            <span class="font-mono text-[10px] text-moss/50 uppercase tracking-widest">Enterprise</span>
            <div class="mt-2 flex items-baseline gap-1">
              <span class="font-heading font-bold text-4xl text-charcoal">Custom</span>
            </div>
            <p class="font-body text-charcoal/50 text-sm mt-2">Tailored infrastructure for funds &amp; institutions.</p>
          </div>

          <ul class="space-y-3 mb-8 flex-1">
            <li v-for="f in enterpriseFeatures" :key="f" class="flex items-start gap-3 text-sm font-body text-charcoal/70">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-moss flex-shrink-0 mt-0.5"><polyline points="20 6 9 17 4 12"/></svg>
              {{ f }}
            </li>
          </ul>

          <button class="btn-magnetic w-full py-3.5 rounded-full font-heading font-semibold text-sm border border-moss/20 text-moss bg-transparent">
            <span class="btn-bg bg-moss/10 rounded-full"></span>
            <span class="btn-content">Contact Sales</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const sectionRef = ref(null)
const headerRef = ref(null)
const price1 = ref(null)
const price2 = ref(null)
const price3 = ref(null)

let ctx

const essentialFeatures = [
  'Up to 10 tracked assets',
  'Basic risk metrics (Sharpe, Beta)',
  'Daily portfolio snapshot',
  'Community support',
]

const performanceFeatures = [
  'Unlimited tracked assets',
  'Full risk-adjusted analytics suite',
  'Real-time portfolio monitoring',
  '60-second signal refresh',
  'Factor analysis & correlation maps',
  'Priority support',
]

const enterpriseFeatures = [
  'Everything in Performance',
  'API access & white-label',
  'Custom factor models',
  'Dedicated account manager',
  'SOC 2 compliance',
  'SLA-backed uptime',
]

onMounted(() => {
  ctx = gsap.context(() => {
    gsap.fromTo(headerRef.value, { y: 30, opacity: 0 }, {
      y: 0, opacity: 1, duration: 0.8, ease: 'power3.out',
      scrollTrigger: { trigger: headerRef.value, start: 'top 80%' }
    })

    const cards = [price1.value, price2.value, price3.value]
    cards.forEach((card, i) => {
      gsap.fromTo(card, { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.8, delay: i * 0.15, ease: 'power3.out',
        scrollTrigger: { trigger: card, start: 'top 85%' }
      })
    })
  }, sectionRef.value)
})

onUnmounted(() => {
  if (ctx) ctx.revert()
})
</script>
