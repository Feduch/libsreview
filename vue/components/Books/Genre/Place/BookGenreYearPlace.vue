<template>
    <span>
        {{ place }}
    </span>
</template>
<script>
    import axios from 'axios'

    export default {
        name: 'BookGenreYearPlace',
        props: [
            'bookId',
            'genreId',
            'bookYear'
        ],
        data() {
            return {
                place: ''
            }
        },
        mounted() {
            axios.post('/book/genre/year/place/',{
                    'book_id': this.bookId,
                    'genre_id': this.genreId,
                    'year': this.bookYear
                })
                .then((response) => {
                    this.place = response.data.place
                })
        }
    }
</script>
<style scoped>
</style>
