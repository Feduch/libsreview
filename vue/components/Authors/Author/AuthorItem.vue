<template>
    <div class="card libs__author">
        <div class="card-body">
            <div class="row">
                <div class="col-lg-2 col-md-2 col-sm-2 col-xs-12">
                    <div class="product-wrapper-2">
                        <div class="product-img">
                            <a :href="author.url">
                                <img v-if="author.photo"
                                     :src="author.photo"
                                     :title="author.name"
                                     class="figure-img img-fluid"
                                />
                                <img v-else
                                     src="/static/images/no_book_cover.png"
                                     :title="author.photo"
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
                                    :rating="parseFloat(author.rating)"
                                    @rating-selected="setAuthorRating($event, author.id)"
                            >
                            </star-rating>
                        </div>
                        <div class="libs__views">
                            <span title="Просмотры"><img src="/static/images/eye.png" alt="Количество просмотров"> {{ author.show_counter }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-10 col-md-10 col-sm-10 col-xs-12">
                    <div class="libs__author_name">
                        Автор: <a :href="author.url">{{ author.name }}</a>
                    </div>
                    <div class="libs__author_birthday">
                        Дата рождения: {{ author.birthday }}
                    </div>
                    <div class="libs__author_book_count">
                         Всего книг: {{ author.book_count }}
                    </div>
                    <div class="libs__author_description">
                        {{ author.description | striptags | truncate }}
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
        name: 'AuthorItem',
        props: [
            'author'
        ],
        components: {
            'star-rating': StarRating
        },
        data() {
            return {
            }
        },
        methods: {
            setAuthorRating: function(rating, authorId){
                axios.post('/ratings/author/set', {
                    'author_id': authorId,
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
</style>
