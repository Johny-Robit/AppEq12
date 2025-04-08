import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios';

axios.get('https://app-eq-12-eventify-29bf10cbb7c2.herokuapp.com/api/csrf/').then(() => {
  console.log('CSRF token set');
});

createApp(App).use(router).mount('#app')
