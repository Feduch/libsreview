<template>
    <div class="col-12 libs__genre_filter">
        <form class="form-inline">
            <div class="form-check form-check-inline">
                <label class="form-check-label" for="sort">Cортировать:</label>
            </div>
            <div class="form-check form-check-inline">
                <input class="form-check-input"
                       v-model="sort"
                       type="radio"
                       value="-rating"
                       id="rating"
                       @change="getBooks"
                >
                <label class="form-check-label" for="rating" @change="getBooks">
                    по рейтингу
                </label>
            </div>
            <div class="form-check form-check-inline">
                <input class="form-check-input"
                       v-model="sort"
                       type="radio"
                       value="title"
                       id="title"
                       @change="getBooks"
                >
                <label class="form-check-label" for="title" @change="getBooks">
                    по алфавиту
                </label>
            </div>
            <div class="form-check form-check-inline">
                <input class="form-check-input"
                       v-model="sort"
                       type="radio"
                       id="date_create"
                       value="-date_create"
                       @change="getBooks"
                >
                <label class="form-check-label" for="date_create" @change="getBooks">
                    по дате поступления
                </label>
            </div>
        </form>
        <div class="col-12 text-center" v-if="isLoad">
            <img src="/static/images/nav_preloader.gif" />
        </div>
        <div class="elevator-button" ref="elevatorup"></div>
        <div v-if="!isLoad">
            <div v-for="(book, index) in books" :key="index">
                <book-item :book="book"></book-item>
            </div>
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

    export default {
        name: 'GenreFilter',
        props: [
            'genreId'
        ],
        components: {
            'book-item': BookItem
        },
        data() {
            return {
                sort: '-rating',
                currentPage: 1,
                books:[],
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
                    genre_id: this.genreId,
                    sort: this.sort
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
        }
    }
</script>
<style scoped>
    .libs__genre_filter form {
        padding-bottom: 20px;
    }
</style>
