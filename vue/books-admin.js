import Vue from 'vue'
import { FormFile, Alert, Progress } from 'bootstrap-vue/es/components'
import BookEditor from './components/Books/Editor/BookEditor.vue'
import BookImport from './components/Books/Editor/BookImport.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false
Vue.use(FormFile)
Vue.use(Alert)
Vue.use(Progress)


new Vue({
    el: '#libs-app',
    components: {
        'book-editor': BookEditor,
        'book-import': BookImport
    }
})


