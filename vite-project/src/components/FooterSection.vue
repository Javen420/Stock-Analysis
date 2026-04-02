<template>
  <footer class="relative overflow-hidden" style="background-color: var(--color-charcoal); border-radius: 4rem 4rem 0 0;">
    <div class="section-pad pb-8">
      <div class="max-w-7xl mx-auto">
        <!-- Main Footer Grid -->
        <div class="grid md:grid-cols-4 gap-12 md:gap-8 mb-16">
          <!-- Brand Column -->
          <div class="md:col-span-1">
            <h3 class="font-heading font-bold text-xl text-cream mb-3">Quantalyze</h3>
            <p class="font-body text-cream/40 text-sm leading-relaxed mb-6">
              Institutional-grade investment analytics for the modern investor.
            </p>
            <!-- Status Indicator -->
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-emerald-400 pulse-dot"></div>
              <span class="font-mono text-[10px] text-cream/40 uppercase tracking-wider">System Operational</span>
            </div>
          </div>

          <!-- Product -->
          <div>
            <h4 class="font-heading font-semibold text-sm text-cream/60 uppercase tracking-wider mb-4">Product</h4>
            <ul class="space-y-2.5">
              <li v-for="link in productLinks" :key="link">
                <a href="#" class="font-body text-sm text-cream/35 hover:text-cream transition-colors duration-300 hover-lift inline-block">{{ link }}</a>
              </li>
            </ul>
          </div>

          <!-- Company -->
          <div>
            <h4 class="font-heading font-semibold text-sm text-cream/60 uppercase tracking-wider mb-4">Company</h4>
            <ul class="space-y-2.5">
              <li v-for="link in companyLinks" :key="link">
                <a href="#" class="font-body text-sm text-cream/35 hover:text-cream transition-colors duration-300 hover-lift inline-block">{{ link }}</a>
              </li>
            </ul>
          </div>

          <!-- Connect -->
          <div>
            <h4 class="font-heading font-semibold text-sm text-cream/60 uppercase tracking-wider mb-4">Connect</h4>
            <ul class="space-y-2.5">
              <li v-for="link in connectLinks" :key="link">
                <a href="#" class="font-body text-sm text-cream/35 hover:text-cream transition-colors duration-300 hover-lift inline-block">{{ link }}</a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Bottom Bar -->
        <div class="pt-8 border-t border-cream/8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p class="font-mono text-[10px] text-cream/25 uppercase tracking-wider">
            &copy; 2026 Quantalyze. All rights reserved.
          </p>
          <div class="flex items-center gap-6">
            <a href="#" class="font-mono text-[10px] text-cream/25 hover:text-cream/50 uppercase tracking-wider transition-colors">Privacy</a>
            <a href="#" class="font-mono text-[10px] text-cream/25 hover:text-cream/50 uppercase tracking-wider transition-colors">Terms</a>
            <a href="#" class="font-mono text-[10px] text-cream/25 hover:text-cream/50 uppercase tracking-wider transition-colors">Security</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const productLinks = ['Analysis Tool', 'API Docs', 'Changelog', 'Status']
const companyLinks = ['About', 'Blog', 'Careers', 'Press']
const connectLinks = ['Twitter / X', 'LinkedIn', 'Discord', 'Support']
</script>
