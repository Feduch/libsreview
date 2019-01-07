import Vue from 'vue'
import axios from 'axios'
import StarRating from 'vue-star-rating'
import AuthorBookFilter from './components/Authors/Filter/AuthorBookFilter.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false

new Vue({
    el: '#vue-author-detail',
    components: {
        'star-rating': StarRating,
        'author-books-filter': AuthorBookFilter
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
        },
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


