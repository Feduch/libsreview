import Vue from 'vue'
import Snotify, { SnotifyPosition } from 'vue-snotify'
import "vue-snotify/styles/material.css"
import Auth from './components/Auth/Auth.vue'

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
    el: '#vue-auth',
    components: {
        'auth': Auth
    }
})


