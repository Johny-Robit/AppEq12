import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Login from '../pages/Login.vue'
import Signup from '../pages/Signup.vue'
import Events from '../pages/Events.vue'
import MyEvents from '../pages/MyEvents.vue'
import CreateEvent from '../pages/CreateEvent.vue'
import EditEvent from '../pages/EditEvent.vue'
import Profile from '../pages/Profile.vue'
import EditProfile from '../pages/EditProfile.vue'
import Event from '../pages/Event.vue'
import { isLoggedIn } from '../store/user.js'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/events', component: Events },
  {
    path: '/my-events',
    component: MyEvents,
  },
  {
    path: '/create-event',
    component: CreateEvent,
    beforeEnter: (to, from, next) => {
      if (!isLoggedIn.value) {
        next({ path: '/login', query: { redirect: to.fullPath } })
      } else {
        next()
      }
    },
  },
  {
    path: '/edit-event/:id',
    component: EditEvent,
    beforeEnter: (to, from, next) => {
      if (!isLoggedIn.value) {
        next({ path: '/login', query: { redirect: to.fullPath } })
      } else {
        next()
      }
    },
  },
  { path: '/profile', component: Profile },
  {
    path: '/edit-profile',
    component: EditProfile,
    beforeEnter: (to, from, next) => {
      if (!isLoggedIn.value) {
        next({ path: '/login', query: { redirect: to.fullPath } })
      } else {
        next()
      }
    },
  },
  {
    path: '/event/:id',
    name: 'Event',
    component: Event
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
