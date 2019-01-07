<template>
    <div>
        <div class="la__book_series">
            <ul class="la__top_set">
                <li class="la__top_set__header">Лучшие подобные книги</li>
                <li v-for="(book, index) in books">
                    <a :href="'/book/' + book.id + '/'">{{ book.title }}</a> ({{ book.year }})
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'

    export default {
        name: "RelatedBooks",
        props: [
            'bookId'
        ],
        data() {
            return {
                books: []
            }
        },
        mounted() {
            axios.post('/books/related/' , {'book_id': this.bookId})
                .then((response) => {
                    this.books = response.data.books
                })
        }
    }
</script>
<style scoped>
    .la__vue__rating_wrap {
        padding-bottom: 10px;
    }
</style>
