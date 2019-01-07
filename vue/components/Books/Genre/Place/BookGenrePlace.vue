<template>
    <span>
        {{ place }}
    </span>
</template>
<script>
    import axios from 'axios'

    export default {
        name: 'BookGenrePlace',
        props: [
            'bookId',
            'genreId'
        ],
        data() {
            return {
                place: ''
            }
        },
        mounted() {
            axios.post('/book/genre/place/', {
                'book_id': this.bookId,
                'genre_id': this.genreId,
            })
                .then((response) => {
                    this.place = response.data.place
                })
        }
    }
</script>
<style scoped>
</style>
