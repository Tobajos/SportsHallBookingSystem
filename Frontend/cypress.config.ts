import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:4200', // URL aplikacji Angular
    setupNodeEvents(on, config) {
      // Możesz zdefiniować tutaj eventy Node.js
    },
  },
});