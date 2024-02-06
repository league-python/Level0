<template>
  <div>
    <iframe
      :width="computedWidth"
      :height="computedHeight"
      frameborder="0"
      marginwidth="0"
      marginheight="0"
      allowfullscreen
      :src="iframeSrc"
    ></iframe>
  </div>
</template>

<script>
export default {
  name: 'TrinketEmbed',
  props: {
    type: {
      type: String,
      default: 'python',
    },
    width: {
      type: String,
      default: '100%', // Adjusted to '100%' for responsive design
    },
    height: {
      type: String,
      default: '500',
    },
    code: {
      type: String,
      default: 'print("Hello World!")',
    },
  },
  computed: {
    computedWidth() {
      return this.width; // Use 100% for full width by default or the value passed in props
    },
    computedHeight() {
      return this.height; // Use default height or the value passed in props
    },
    iframeSrc() {
      // Encode the code and create the URL for the iframe
      const baseUrl = 'https://trinket.io/tools/1.0/embed/';
      const encodedCode = encodeURIComponent(this.code.trim());
      return `${baseUrl}${this.type}#code=${encodedCode}`;
    },
  },
  mounted() {
    // Additional JavaScript for iframe manipulation can go here
  },
};
</script>

<style scoped>
/* Your component-specific styles here */
</style>
