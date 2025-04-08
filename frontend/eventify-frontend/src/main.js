import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios';

axios.get('http://localhost:8000/api/csrf/').then(() => {
  console.log('CSRF token set');
});

createApp(App).use(router).mount('#app')
