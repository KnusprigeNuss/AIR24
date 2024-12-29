import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'

// In flask-vue-app/frontend directory, run:
// npm install

// In flask-vue-app/backend-server directory, run:
// flask run --port=5001 --debug

// In flask-vue-app/frontend directory, run:
// npm run dev

// http://localhost:5173/

const app = createApp(App)

app.use(router)

app.mount('#app')
