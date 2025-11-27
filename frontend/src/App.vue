<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  template: `<button class="btn btn-primary"> Click me</button>`,
  components: {
    Navbar,
    Footer,
  },
};
</script>

<template>
  <Navbar />
  <router-view />
  <button class="btn btn-primary">Click Me</button>
  <Footer />
</template>

<style scoped></style>