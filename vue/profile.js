import Vue from 'vue'
import Snotify, { SnotifyPosition } from 'vue-snotify'
import "vue-snotify/styles/material.css"
import Profile from './views/profile/Profile.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false

const options = {
  toast: {
    position: SnotifyPosition.rightTop,
      timeout: 3000
  }
}
Vue.use(Snotify, options)

new Vue({
    el: '#vue-user-profile',
    components: {
        'profile': Profile
    }
})


