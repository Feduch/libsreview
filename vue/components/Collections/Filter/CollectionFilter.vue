<template>
    <div class="libs__collection_filter">
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
        </form>
        <div class="col-12 text-center" v-if="isLoad">
            <img src="/static/images/nav_preloader.gif" />
        </div>
        <div v-if="!isLoad">
            <div v-for="(book, index) in books" :key="index">
                <book-item :book="book"></book-item>
            </div>
        </div>
    </div>
</template>
<script>
    import BookItem from '../../Books/Book/BookItem.vue'
    import axios from 'axios'

    export default {
        name: 'CollectionFilter',
        props: [
            'collectionId'
        ],
        components: {
            'book-item': BookItem
        },
        data() {
            return {
                sort: '-rating',
                books:[],
                isLoad: false
            }
        },
        methods: {
            getBooks () {
                $('#libs__books').remove()
                this.isLoad = true
                axios.post('/collections/books/get', {
                    collection_id: this.collectionId,
                    sort: this.sort
                })
                    .then((response) => {
                        this.books = response.data.books
                        this.isLoad = false
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        }
    }
</script>
<style scoped>
    .libs__collection_filter form {
        padding-bottom: 20px;
    }
</style>
