import Vue from 'vue'
import { FormFile } from 'bootstrap-vue/es/components'
import Snotify, { SnotifyPosition } from 'vue-snotify'
import "vue-snotify/styles/material.css"
import StarRating from 'vue-star-rating'
import CollectionFilter from './components/Collections/Filter/CollectionFilter.vue'
import CollectionEditor from './components/Collections/Editor/CollectionEditor.vue'
import Notify from './components/Notify/Notify.vue'
import axios from "axios"
import VueQuillEditor from 'vue-quill-editor'

// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'

Vue.use(VueQuillEditor)

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
        'star-rating': StarRating,
        'collection-filter': CollectionFilter,
        'collection-editor': CollectionEditor,
        'notify': Notify
    },
    methods: {
        setCollectionRating: function(rating, collectionId){
            axios.post('/ratings/collection/set', {
                'collection_id': collectionId,
                'rating': rating
            })
                .then((response) => {
                    if (!response.data.auth) {
                        $('#LogInModal').modal('show')
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
})


