<template>
    <div class="app-container">
        <Header />
        <main class="main-content">
          <router-view />
        </main>
        <Footer />
    </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>


<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background: #f8f9fa;
}
</style>