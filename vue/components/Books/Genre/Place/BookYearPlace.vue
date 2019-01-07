<template>
    <span>
        {{ place }}
    </span>
</template>
<script>
    import axios from 'axios'

    export default {
        name: 'BookYearPlace',
        props: [
            'bookId',
            'bookYear'
        ],
        data() {
            return {
                place: ''
            }
        },
        mounted() {
            axios.post('/book/year/place/', {
                'book_id': this.bookId,
                'year': this.bookYear,
            })
                .then((response) => {
                    this.place = response.data.place
                })
        }
    }
</script>
<style scoped>
</style>
