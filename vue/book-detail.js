import Vue from 'vue'
import StarRating from 'vue-star-rating'
import Snotify, { SnotifyPosition } from 'vue-snotify'
import "vue-snotify/styles/material.css"
import LitresFragmentsDownload from './components/Books/LitresFragments/LitresFragmentsDownload.vue'
import PartnerPrice from './components/Books/PartnerPrice/PartnerPrice.vue'
import RatingBestBooks from './components/Books/Ratings/BestBooks/RatingBestBooks.vue'
import BookGenrePlace from './components/Books/Genre/Place/BookGenrePlace.vue'
import BookYearPlace from './components/Books/Genre/Place/BookYearPlace.vue'
import BookGenreYearPlace from './components/Books/Genre/Place/BookGenreYearPlace.vue'
import Comments from './components/Books/Comments/BookComments.vue'
import axios from 'axios'
import VueQuillEditor from 'vue-quill-editor'

import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'

Vue.use(VueQuillEditor)

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false

const options = {
  toast: {
    position: SnotifyPosition.rightTop,
      timeout: 3000
  }
}
Vue.use(Snotify, options)

new Vue({
    el: '#litres-fragment-download',
    components: {
        'litres-fragment-download': LitresFragmentsDownload
    }
})

new Vue({
    el: '#partner-price',
    components: {
        'partner-price': PartnerPrice
    }
})

new Vue({
    el: '#libs-comments-mobile',
    components: {
        'libs-comments': Comments
    }
})

new Vue({
    el: '#libs-comments',
    components: {
        'libs-comments': Comments
    }
})

new Vue({
    el: '#book-ratings',
    components: {
        'rating-best-books': RatingBestBooks,
        'star-rating': StarRating,
        'genre-place': BookGenrePlace,
        'year-place': BookYearPlace,
        'genre-year-place': BookGenreYearPlace
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
    el: '#series_books',
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
