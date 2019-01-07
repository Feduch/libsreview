import Vue from 'vue'
import StarRating from 'vue-star-rating'
import PartnerPrice from './components/Books/PartnerPrice/PartnerPrice.vue'
import axios from "axios";

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false

new Vue({
    el: '#read-online',
    components: {
        'partner-price': PartnerPrice,
        'star-rating': StarRating
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
