<template>
    <div class="libs__navigator">
        <form>
            <div class="form-row">
                <div class="form-group col-12 col-md-6">
                    <label>Жанры</label>
                    <multiselect
                            v-model="genreValues"
                            :options="genres"
                            :multiple="true"
                            :close-on-select="false"
                            :clear-on-select="false"
                            :hide-selected="true"
                            :preserve-search="true"
                            placeholder="Все жанры"
                            label="name"
                            track-by="name"
                            :preselect-first="true"
                            @select="updateYears"
                            @remove="updateYears"
                    >
                    </multiselect>
                </div>
                <div class="form-group col-12 col-md-6">
                    <label>Сортировка</label>
                    <select v-model="sort" class="form-control">
                        <option value="-rating">Рейтинг</option>
                        <option value="-show_counter">Просмотров</option>
                        <option value="title">по алфавиту</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group col-md-6">
                    <label>Интервал годов</label>
                    <div class="row">
                        <div class="col-6">
                            <select v-model="startYear" class="form-control" @change="resetYear">
                                <option value="">-</option>
                                <option v-for="year in years" :value="year">{{ year }}</option>
                            </select>
                        </div>
                        <div class="col-6">
                            <select v-model="endYear" class="form-control" @change="resetYear">
                                <option value="">-</option>
                                <option v-for="year in years" :value="year">{{ year }}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="form-group col-12 col-md-6">
                    <label>или год публикации</label>
                    <select v-model="year" class="form-control col-4 col-md-4" @change="resetRangeYear">
                        <option value="">-</option>
                        <option v-for="year in years" :value="year">{{ year }}</option>
                    </select>
                </div>
            </div>
            <button type="button" class="btn btn-secondary" @click="getBooks">Найти</button>
        </form>

        <div class="row libs__book_list">
            <div class="col-12 text-center" v-if="isLoad">
                <img src="/static/images/nav_preloader.gif" />
            </div>
            <div class="col-12">
                <div class="libs__book" v-for="book in books">
                    <book-item :book="book"></book-item>
                </div>
                <p v-if="message">{{message}}</p>
                <infinite-loading
                        @infinite="infiniteHandler"
                        :distance="600"
                        force-use-infinite-wrapper="true"
                        spinner="bubbles"
                        v-if="showLoadmore"
                        ref="infiniteLoading"
                >
                    <span slot="no-more">
                      Это все книги :(
                    </span>
                </infinite-loading>
            </div>
        </div>
    </div>
</template>

<script>
    import InfiniteLoading from 'vue-infinite-loading'
    import Multiselect from 'vue-multiselect'
    import BookItem from '../Books/Book/BookItem.vue'
    import axios from 'axios'

    export default {
        name: 'Navigator',
        components: {
            'book-item': BookItem,
            Multiselect,
            InfiniteLoading
        },
        data() {
            return {
                genreValues: [],
                genres: [],
                currentPage: 1,
                sort: '-rating',
                isLoad: false,
                books: [],
                years: [],
                showLoadmore: false,
                year: '',
                startYear: '',
                endYear: '',
                genreId: [],
                message: ''
            }
        },
        methods: {
            getBooks () {
                this.currentPage = 1

                let genreIds = []
                for (let key in this.genreValues) {
                    genreIds.push(this.genreValues[key].id)
                }

                this.isLoad = true
                this.books = []
                axios.post('/nav/books/get', {
                    page: this.currentPage,
                    genre_id: genreIds,
                    sort: this.sort,
                    start_year: this.startYear,
                    end_year: this.endYear,
                    year: this.year
                })
                    .then((response) => {
                        if (response.data.books.length) {
                            this.books = response.data.books
                            this.showLoadmore = true
                            this.currentPage = 2
                            this.$nextTick(() => {
                                this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset')
                            })
                        } else if (this.currentPage == 1) {
                            if (this.genreValues.length > 1) {
                                this.message = 'В выбранных жанрах книг нет :('
                            } else {
                               this.message = 'В жанре '+this.genreValues[0].name+' в '+this.year+' году нет книг :('
                            }
                        }
                        this.isLoad = false

                    })
                    .catch((error) => {
                        console.log(error)
                    })
            },
            updateYears () {
                this.$nextTick(function () {
                    let genreIds = []
                    for (let key in this.genreValues) {
                        genreIds.push(this.genreValues[key].id)
                    }

                    axios.post('/nav/years/get', {genre_id: genreIds})
                        .then((response) => {
                            this.years = response.data.years
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                })
            },
            infiniteHandler($state) {
                let genreIds = []
                for (let key in this.genreValues) {
                    genreIds.push(this.genreValues[key].id)
                }

                axios.post('/nav/books/get', {
                    page: this.currentPage,
                    genre_id: genreIds,
                    sort: this.sort,
                    start_year: this.startYear,
                    end_year: this.endYear,
                    year: this.year
                })
                    .then((response) => {
                        if (response.data.books.length) {
                            this.books = this.books.concat(response.data.books)
                            $state.loaded()
                            if (this.books.length / 10 === 10) {
                                $state.complete()
                            }
                        } else {
                            $state.complete()
                        }
                        this.currentPage += 1
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            },
            resetRangeYear () {
                this.startYear = ''
                this.endYear = ''
            },
            resetYear () {
                this.year = ''
            }
        },
        created () {
        },
        mounted() {
            this.genres = this.$store.getters.getGenres
            const smallNavigator = this.$store.getters.getSmallNavigator

            if (smallNavigator.genre > 0) {
                this.genreValues.push({
                    'id': smallNavigator.genre,
                    'name': smallNavigator.name
                })
                this.genreId.push(smallNavigator.genre)

                if (smallNavigator.years.length == 9) {
                    const years = smallNavigator.years.split('-')
                    this.startYear = years[0]
                    this.endYear = years[1]

                } else if (smallNavigator.years.length == 4) {
                    this.year = smallNavigator.years
                }

                this.getBooks()

                this.$store.dispatch('setSmallNavigator', {
                    genre: 0,
                    years: ''
                })
            }

            this.updateYears()
        }
    }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
    .libs__book_list {
        padding-top: 10px;
    }
</style>
