<template>
    <div>
        <form>
            <div class="form-row">
                <div class="form-group col-md-9">
                    <select v-model="genre" class="form-control form-control-sm">
                        <option value="">Выберите один из жанров</option>
                        <option v-for="genre in genres" v-bind:value="genre.id">
                            {{ genre.name }}
                        </option>
                    </select>
                </div>
                <div class="form-group col-md-3">
                    <select v-model="sort" class="form-control form-control-sm">
                        <option value="-rating">Рейтинг</option>
                        <option value="-show_counter">Просмотров</option>
                        <option value="title">по алфавиту</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group col-md-5">
                    <input type="text" class="form-control form-control-sm" placeholder="год с" v-model="startYear">
                </div>
                <div class="form-group col-md-5">
                    <input type="text" class="form-control form-control-sm" placeholder="по" v-model="endYear">
                </div>
                <div class="form-group col-md-2">
                    <button type="button" class="btn btn-secondary btn-sm" @click="getBooks">Показать книги</button>
                </div>
            </div>
        </form>
        <div class="col-12 text-center" v-if="isLoad">
            <img src="/static/images/nav_preloader.gif" />
        </div>
        <div class="la__vue_app"></div>
        <div class="la__vue_app__book" v-for="book in books">
            <book-item :book="book"></book-item>
        </div>
        <b-pagination size="md"
                      v-model="currentPage"
                      :total-rows="totalRows"
                      :per-page="30"
                      :limit="10"
                      :hide-goto-end-buttons="true"
                      @input="getBooks"
                      v-if="showPagination">
        </b-pagination>
    </div>
</template>
<script>
    import BookItem from '../../Books/Book/BookItem.vue'
    import axios from 'axios'
    import { request } from 'graphql-request'

    const query = `{
          genres {
            name
            id
          }
        }`

    export default {
        name: 'BookFilter',
        props: [
        ],
        components: {
            'book-item': BookItem
        },
        data() {
            return {
                startYear: null,
                endYear: null,
                sort: '-rating',
                genre: '',
                genres: [],
                books:[],
                currentPage: 1,
                isLoad: false,
                showPagination: false,
                totalRows: 0
            }
        },
        methods: {
            getBooks () {
                window.scrollTo(0, 0)
                $('#libs__books').remove()
                this.isLoad = true
                this.showPagination = false
                axios.post('/books/get', {
                    page: this.currentPage,
                    genre_id: this.genre,
                    sort: this.sort,
                    start_year: this.startYear,
                    end_year: this.endYear,
                })
                    .then((response) => {
                        this.books = response.data.books
                        this.totalRows = response.data.count
                        this.isLoad = false
                        this.showPagination = true
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        },
        mounted() {
            request('/api/0.1/graphql', query).
            then(data => {
                this.genres = data.genres
            })
        }
    }
</script>
<style scoped>
    .la__vue_app__book_filter {
        padding: 15px 0 30px 0;
        font-size: 14px;
    }

    .la__vue_app__book_filter .form-inline {
        padding-bottom: 5px;
    }

    .la__vue_app {
        padding-top: 15px;
    }
</style>
