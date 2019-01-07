<template>
    <table class="table">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Название</th>
            <th scope="col">Автор</th>
            <th scope="col">Статус</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="book in books">
            <th scope="row">{{ book.id }}</th>
            <td>
                <div col="3">
                    <img :src="book.image" v-if="book.image" width="50" />
                    <span v-else>Обложки нет</span>
                </div>
                <div col="9">
                    <a :href="'/book/editor/'+book.id" target="_blank">{{ book.title }}</a>
                </div>
            </td>
            <td><span v-html="book.authors"></span></td>
            <td>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" :id="book.id" checked disabled>
                    <label class="form-check-label" :id="book.id">Не просмотрен</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" @click="setStatus(book.id)" v-model="book.status" value="true">
                    <label class="form-check-label" @click="book.status = true; setStatus(book.id)">Опубликовать</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" @click="setStatus(book.id)" v-model="book.status" value="false">
                    <label class="form-check-label" @click="book.status = false; setStatus(book.id)">Отключить</label>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
</template>
<script>
    import axios from 'axios'

    export default {
        name: 'BookImport',
        props: [],
        components: {
        },
        data() {
            return {
                fields: ['id', 'title', 'authors', 'status', 'show_details'],
                books: []
            }
        },
        methods: {
            setStatus (id) {
                this.$nextTick(function () {
                    for (let key in this.books) {
                        if (this.books[key].id == id) {
                            axios.post('/book/import/status/set', {
                                'id': id,
                                'status': this.books[key].status
                            })
                                .then((response) => {
                                    // console.log(response)
                                })
                                .catch((error) => {
                                    console.log(error)
                                })
                        }
                    }
                })
            }
        },
        mounted () {
            axios.post('/book/import/get')
                .then((response) => {
                    this.books = response.data.books
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
</script>

<style scoped>
</style>
