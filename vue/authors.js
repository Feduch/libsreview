import Vue from 'vue'
import { Pagination } from 'bootstrap-vue/es/components'
import StarRating from 'vue-star-rating'
import AuthorFilter from './components/Authors/Filter/AuthorFilter.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false
Vue.use(Pagination)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from "axios/index";


new Vue({
    el: '#vue-authors-list',
    components: {
        'star-rating': StarRating,
        'author-filter': AuthorFilter
    },
    methods: {
        setAuthorRating: function(rating, authorId){
            axios.post('/ratings/author/set', {
                'author_id': authorId,
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


