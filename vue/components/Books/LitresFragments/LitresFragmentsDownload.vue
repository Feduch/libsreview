<template>
    <div class="col-12">
        <div v-if="litres_book_id">
            <a class="btn btn-secondary btn-sm" :href="'https://www.litres.ru/gettrial/?art='+litres_book_id+'&format=fb2&lfrom=16315930'">fb2</a>
            <a class="btn btn-secondary btn-sm" :href="'https://www.litres.ru/gettrial/?art='+litres_book_id+'&format=rtf&lfrom=16315930'">rtf</a>
            <a class="btn btn-secondary btn-sm" :href="'https://www.litres.ru/gettrial/?art='+litres_book_id+'&format=txt&lfrom=16315930'">txt</a>
            <a class="btn btn-secondary btn-sm" :href="'https://www.litres.ru/gettrial/?art='+litres_book_id+'&format=epub&lfrom=16315930'">epub</a>
            <div>
                (будет легально скачан большой фрагмент книги, Вы сможете понять, нравится ли она Вам, и если да, то легально купить)
            </div>
        </div>
        <div v-else>Нет возможности скачать фрагмент книги</div>
    </div>
</template>
<script>
    import axios from 'axios'
    import { request } from 'graphql-request'
    const query = `query litres_fragments($name: String!, $author: String, $litresid: Int, $isbn: String, $libsid: Int) {
          litres_fragments(name: $name, author: $author, litresid: $litresid, isbn: $isbn, libsid: $libsid) {
            id
            partner_book_id
            isbn
          }
        }`

    export default {
        name: 'LitresFragmentsDownload',
        props: [
            'name',
            'author',
            'litresId',
            'isbn',
            'bookId'
        ],
        data() {
            return {
                litres_book_id: 0,
                url: null,
                isbn: null
            }
        },
        mounted() {
            request('https://partners.libs.ru/api/0.1/graphql', query, {
                'name': this.name,
                'author': this.author,
                'isbn': this.isbn,
                'libsid': this.bookId,
                'litresid': this.litresId
            }).
            then(data => {
                if (data['litres_fragments'] == null || data['litres_fragments'].length == 0) {
                    $('#litres-fragment-read').hide()
                    this.litres_book_id = 0
                } else {
                    if (data['litres_fragments'][0]['partner_book_id'].length > 0) {
                        this.litres_book_id = data['litres_fragments'][0]['partner_book_id']
                        let url = '//www.litres.ru/pages/quickread/?art=' + this.litres_book_id + '&amp;lfrom=16315930'
                        $('#litres_fragment_link').attr('src', url)
                        this.isbn = data['litres_fragments'][0]['isbn']
                        this.setLitesId()
                    } else {
                        this.litres_book_id = 0
                        $('#litres-fragment-read').hide()
                    }
                }
            })
        },
        computed: {
        },
        methods: {
            setLitesId () {
                axios.post('/book/litres/set', {
                    'litres_book_id': this.litres_book_id,
                    'book_id': this.bookId,
                    'isbn': this.isbn
                })
                    .then((response) => {
                        // console.log(response)
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        }
    }
</script>
<style>
    .la__litres_fragment {
        padding-bottom: 10px;
    }
</style>
