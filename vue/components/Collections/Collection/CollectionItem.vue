<template>
    <div class="card">
        <div class="card-body">
            <div class="row">
                <div class="col-lg-2 col-md-2 col-sm-2 col-xs-12">
                    <div class="product-wrapper-2">
                        <div class="product-img">
                            <a :href="collection.url" v-if="collection.image">
                                <img
                                        :src="collection.image"
                                        :title="collection.title"
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
                                    :rating="parseFloat(collection.rating)"
                                    @rating-selected="setCollectionRating($event, collection.id)"
                            >
                            </star-rating>
                        </div>
                        <div class="libs__views">
                            <span title="Просмотры"><img src="/static/images/eye.png" alt="Количество просмотров"> {{ collection.showCounter }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-10 col-md-10 col-sm-10 col-xs-12">
                    <div class="libs__author_name">
                        <a :href="'/collections/editor/'+collection.id" target="_blank">Редактировать</a><br />
                        <a :href="collection.url">{{ collection.title }}</a>
                    </div>
                    <div class="libs__author_birthday">
                        Дата обновления: {{ dateUpdate }}
                    </div>
                    <div class="libs__author_book_count">
                        Всего книг: {{ collection.books }}
                    </div>
                    <div class="libs__author_description">
                        {{ collection.text | striptags | truncate }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import moment from 'moment'
    import StarRating from 'vue-star-rating'

    export default {
        name: 'CollectionItem',
        props: [
            'collection'
        ],
        components: {
            'star-rating': StarRating
        },
        data() {
            return {
            }
        },
        methods: {
            setCollectionRating: function(rating, collectionId){
                axios.post('/ratings/author/set', {
                    'collection_id': collectionId,
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
                last = last || length - clamp.length;
                tcText =  tcText.slice(0, last);
                return tcText + clamp;
            }
        },
        computed: {
            dateUpdate: function() {
                return moment(this.collection.dateUpdate).format('DD.MM.YYYY, hh:mm:ss')
            }
        }
    }
</script>
<style scoped>
    .card {
        margin-bottom: 18px;
    }
</style>
