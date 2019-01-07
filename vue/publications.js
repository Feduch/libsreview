import Vue from 'vue'
import { FormFile } from 'bootstrap-vue/es/components'
import Snotify, { SnotifyPosition } from 'vue-snotify'
import "vue-snotify/styles/material.css"
import PublicationEditor from './components/Publications/Editor/PublicationEditor.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false
Vue.use(FormFile)

const options = {
  toast: {
    position: SnotifyPosition.rightTop,
      timeout: 3000
  }
}
Vue.use(Snotify, options)

new Vue({
    el: '#libs-app',
    components: {
        'publication-editor': PublicationEditor
    }
})


