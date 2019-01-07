<template>
    <div class="card libs__book">
        <div class="card-body">
            <div class="row">
                <div class="col-lg-2 col-md-2 col-sm-2 col-xs-12">
                    <div class="product-wrapper-2">
                        <div class="product-img">
                            <a :href="book.url">
                                <img v-if="book.image"
                                     :src="book.image"
                                     :title="book.title"
                                     class="figure-img img-fluid"
                                />
                                <img v-else
                                     src="/static/mages/no_book_cover.png"
                                     :title="book.title"
                                     class="figure-img img-fluid"
                                />
                            </a>
                        </div>
                        <div class="libs__rating">
                            <star-rating
                                    v-bind:increment="1" :round-start-rating="false"
                                    v-bind:max-rating="5"
                                    inactive-color="#ccc"
                                    active-color="#45a6f3"
                                    v-bind:star-size="15"
                                    :read-only="false"
                                    :rating="parseFloat(book.rating)"
                                    @rating-selected="setBookRating($event, book.id)"
                            >
                            </star-rating>
                        </div>
                        <div class="libs__user_rating " v-if="book.userRating">
                            Ваша оценка: {{book.userRating}}
                        </div>
                        <div class="libs__views">
                            <span title="Просмотры"><img src="/static/images/eye.png" alt="Количество просмотров"> {{ book.show_counter }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-10 col-md-10 col-sm-10 col-xs-12">
                    <div class="libs__book_title">
                        Книга: <a :href="book.url">{{ book.title }}</a>
                    </div>
                    <div class="libs__book_author">
                        Автор(ы): <span v-html="book.authors"></span>
                    </div>
                    <div class="libs__book_genres">
                        Жанр(ы): <span v-html="book.genres"></span>
                    </div>
                    <div class="libs__book_year" v-if="book.year">
                        Год издания: {{ book.year }}
                    </div>
                    <div class="libs__book_description">
                        {{ book.description | striptags | truncate }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import StarRating from 'vue-star-rating'

    export default {
        name: 'BookItem',
        props: [
            'book'
        ],
        components: {
            'star-rating': StarRating
        },
        data() {
            return {
            }
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
        },
        filters: {
            striptags(value) {
                if (!value) return ''
                value = value.toString()
                return  value.replace(/<[^>]+>/gm, '');
            },
            truncate(text) {
                var clamp = '...';
                var length = 80;

                if (text.length <= length) return text;

                var tcText = text.slice(0, length - clamp.length);
                var last = tcText.length - 1;

                while (last > 0 && tcText[last] !== ' ' && tcText[last] !== clamp[0]) last -= 1;

                // Fix for case when text dont have any `space`
                last = last || length - clamp.length;

                tcText =  tcText.slice(0, last);

                return tcText + clamp;
            }
        }
    }
</script>
<style scoped>
    .libs__user_rating {
        font-size: 14px;
    }
</style>
