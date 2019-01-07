import Vue from 'vue'
import { Pagination } from 'bootstrap-vue/es/components'
import StarRating from 'vue-star-rating'
import BookFilter from './components/Books/Filter/BookFilter.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false
Vue.use(Pagination)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from "axios/index";


new Vue({
    el: '#vue-books-list',
    components: {
        'star-rating': StarRating,
        'book-filter': BookFilter
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


