import Vue from 'vue'
import store from './store'
import StarRating from 'vue-star-rating'
import Navigator from './components/Navigator/Navigator.vue'
import axios from "axios/index";

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false


new Vue({
    el: '#vue-books-navigator',
    store: store,
    components: {
        'star-rating': StarRating,
        'navigator': Navigator
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


