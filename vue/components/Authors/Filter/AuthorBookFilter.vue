<template>
    <div class="la__vue_app__author_filter" id="la__vue_app__author_filter">
        <div class="libs__badge">
            <p><span class="badge badge-info">Совет!</span> Чтобы вывести список лучших книг автора просто рассортируйте их по рейтингу.</p>
        </div>
        <form class="form-inline">
            <div class="form-check form-check-inline">
                <label class="form-check-label" for="sort">сортировать по:</label>&nbsp;
                <select v-model="sort" @change="getBooks" class="form-control form-control-sm" id="sort">
                    <option value="-rating">рейтингу</option>
                    <option value="-show_counter">просмотрам</option>
                    <option value="title">алфавиту</option>
                </select>
            </div>
            <div class="form-check form-check-inline">
                <select v-model="genre" @change="getBooks" class="form-control form-control-sm">
                    <option value="0">все жанры</option>
                    <option v-for="(genre, index) in genres" :key="index" :value="genre.id">
                        {{ genre.name }}
                    </option>
                </select>
            </div>
            <div class="form-check form-check-inline">
                <label class="form-check-label" for="group">группировать по:</label>&nbsp;
                <input class="form-check-input" type="checkbox" v-model="groupBySeries" value="true" @change="getBooks" checked="checked">
                <label class="form-check-label" for="group">сериям</label>
            </div>
        </form>
        <div class="row libs__author_books_vue" v-for="(series, index) in books" v-if="groupBySeries" :key="index">
            <div class="col-12">
                <span v-if="index != '0'">
                    Серия <a :href="'/book/series/'+index+'.html'">{{ getSeriesTitle(index) }}</a>
                </span>
                <span v-else>
                    Книги без серии
                </span>
            </div>
            <div class="col-12" v-for="(book, index) in series" :key="index">
                <div class="row libs__book_light">
                    <div class="col-1 libs__numer">{{ getIndex(index) }}</div>
                    <div class="col-7">
                        <div class="row">
                            <div class="col-12">
                                <a :href="'/book/'+book.book_id+'/'">{{ book.book_title }} <span v-if="book.book_year"></span></a>
                            </div>
                            <div class="col-12 libs__book_genres">
                                Жанры:
                                <a v-for="(genre, index) in book.book_genres"
                                   :key="index"
                                   :href="'/genre/'+genre.slug+'/'">{{ genre.name }}</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-3 libs__rating">
                        <star-rating
                                v-bind:increment="1" :round-start-rating="false"
                                v-bind:max-rating="5"
                                inactive-color="#ccc"
                                active-color="#45a6f3"
                                v-bind:star-size="15"
                                :read-only="false"
                                :rating="parseFloat(book.book_rating)"
                                @rating-selected="setBookRating($event, book.book_id)"
                        >
                        </star-rating>
                    </div>
                </div>
            </div>
        </div>
        <div class="row libs__author_books_vue" v-if="!groupBySeries">
            <div class="col-12" v-for="(book, index) in booksList" :key="index">
                <div class="row libs__book_light">
                    <div class="col-1 libs__numer">{{ getIndex(index) }}</div>
                    <div class="col-7">
                        <div class="row">
                            <div class="col-12">
                                <a :href="book.url">{{ book.title }} <span v-if="book.year"></span></a>
                            </div>
                            <div class="col-12 libs__book_genres">
                                Жанры: <span v-html="book.genres"></span>
                            </div>
                        </div>
                    </div>
                    <div class="col-3 libs__rating">
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
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import flow from 'lodash/fp/flow'
    import groupBy from 'lodash/fp/groupBy'
    import StarRating from 'vue-star-rating'
    import axios from 'axios'

    export default {
        name: 'AuthorBookFilter',
        components: {
            'star-rating': StarRating
        },
        props: [
            'authorId',
            'genresIds'
        ],
        data() {
            return {
                books: [],
                booksList: [],
                series: [],
                groupBySeries: true,
                sort: '-rating',
                genres: [],
                genre: 0
            }
        },
        methods: {
            getBooks () {
                axios.post('/author/books/get', {
                    is_group: this.groupBySeries,
                    sort: this.sort,
                    genre: this.genre,
                    author_id: this.authorId
                })
                    .then((response) => {
                        let books = response.data.books

                        if (this.groupBySeries) {
                            this.books = flow(
                                groupBy('series_id')
                            )(books)

                            this.series = response.data.series
                        } else {
                            this.booksList = books
                        }

                        $('.libs__author_books').remove()
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            },
            getSeriesTitle (seriesId) {
                return this.series[seriesId].title
            },
            getIndex (index) {
                return index + 1
            }
        },
        mounted() {
            if (this.genresIds.length) {
                axios.post('/author/genres/get', {
                    genres_ids: this.genresIds
                })
                    .then((response) => {
                        this.genres = response.data.genres
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        }
    }
</script>
<style scoped>
</style>
