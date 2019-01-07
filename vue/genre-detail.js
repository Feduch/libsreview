import Vue from 'vue'
import { Pagination } from 'bootstrap-vue/es/components'
import StarRating from 'vue-star-rating'
import GenreFilter from './components/Genres/Filter/GenreFilter.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false
Vue.use(Pagination)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from 'axios'


new Vue({
    el: '#vue-genre-detail',
    components: {
        'star-rating': StarRating,
        'genre-filter': GenreFilter
    },
    methods: {
        setBookRating: function(rating, bookId){
            axios.post('/ratings/book/set', {
                'book_id': bookId,
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


