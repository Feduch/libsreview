import Vue from 'vue'
import axios from "axios/index"
import StarRating from 'vue-star-rating'

Vue.config.productionTip = false
Vue.config.silent = false
Vue.config.devtools=false


new Vue({
    el: '#vue-books-list',
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

new Vue({
    el: '#vue-authors-list',
    components: {
        'star-rating': StarRating
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


