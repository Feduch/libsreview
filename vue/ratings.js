import Vue from 'vue'
import StarRating from 'vue-star-rating'
import axios from "axios/index";

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false

new Vue({
    el: '#libs-rating-books',
    components: {
        'star-rating': StarRating
    },
    methods: {
        setBookRating: function(rating, bookId){
            axios.post('/ratings/book/set', {
                'book_id': bookId,
                'rating': rating
            })
                .then((response) => {

                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
})


