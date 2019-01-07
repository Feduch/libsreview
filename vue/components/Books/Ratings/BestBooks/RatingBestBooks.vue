<template>
    <div>
        <div class="col-12">
            <ul class="la__main__lenta">
                <li class="la__main__lenta_header">
                    {{title}}
                    <a :href="'/rating/days/'+ days +'/'">(все книги за этот период)</a>
                </li>
            </ul>
            <div class="row la__vue__rating_wrap" itemscope="" itemtype="http://schema.org/Book">
                <div class="col-3 la__book_item" v-for="book in books" v-cloak>
                    <div class="la__book_cover">
                        <a v-bind:href="'/book/' + book.id + '/'">
                            <span v-if="book.image !== ''">
                                <img class="img-thumbnail" v-bind:src="book.image" v-bind:alt="book.title">
                            </span>
                            <span v-else><img class="img-thumbnail" src="{% static 'images/no_book_cover.png' %}" v-bind:alt="book.title"></span>
                        </a>
                    </div>
                    <div class="la__book_title">
                        {{ book.title }}
                    </div>
                    <div class="la__book_author">
                    <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
                        <a v-bind:href="'/a/'+ author.id + '/'" itemprop="url" v-for="author in book.author">
                            <span itemprop="name">{{ author.name }}</span>
                        </a>
                    </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import { request } from 'graphql-request'
    const query = `query book_rating($days: Int, $month: Int) {
                      book_rating(days:$days, month: $month) {
                        id
                        title
                        image
                        author {
                          id
                          name
                        }
                      }
                    }`

    export default {
        name: 'RatingBestBooks',
        props: [
            'days',
            'title'
        ],
        data() {
            return {
                books: []
            }
        },
        mounted() {
            request('/api/0.1/graphql', query, {'days': this.days, 'month': this.month}).
            then(data => {
                this.books = data['book_rating']
            })
        }
    }
</script>
<style scoped>
    .la__vue__rating_wrap {
        padding-bottom: 10px;
    }
</style>
