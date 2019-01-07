<template>
    <div class="libs__publication_editor">
        <div class="row">
            <div class="col-12">
                <div class="card mb-3" v-if="imagePreview">
                    <img class="card-img-top" :src="imagePreview">
                </div>
            </div>
            <div class="col-12">
                <b-form-file
                        accept="image/jpeg, image/png, image/gif"
                        v-model="image" :state="Boolean(image)" placeholder="Обложка для поста"
                ></b-form-file>
            </div>
            <div class="col-12">
                <label>Название</label>
                <input type="text" class="form-control" v-model="title"/>
            </div>
            <div class="col-12">
                <label>Текст</label>
                <textarea type="text" class="form-control" rows="5" v-model="text"></textarea>
            </div>
            <div class="col-12">
                <label>Книги</label>
                <multiselect
                        v-model="selectedBooks"
                        :options="books"
                        :multiple="true"
                        :clear-on-select="true"
                        :close-on-select="false"
                        :hide-selected="true"
                        :preserve-search="true"
                        :preselect-first="true"
                        label="title"
                        track-by="id"
                        placeholder="Введите название книги"
                        selectLabel="Выбрать"
                        selectedLabel="Выбрана"
                        deselectLabel="Отменить выбор"
                        open-direction="bottom"
                        :searchable="true"
                        :loading="isLoadingBook"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFindBook"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет книг в списке</span>
                </multiselect>
            </div>
            <div class="col-12">
                <label>Авторы</label>
                <multiselect
                        v-model="selectedAuthors"
                        :options="authors"
                        :multiple="true"
                        :clear-on-select="true"
                        :close-on-select="false"
                        :hide-selected="true"
                        :preserve-search="true"
                        :preselect-first="true"
                        label="name"
                        track-by="id"
                        placeholder="Введите автора"
                        selectLabel="Выбрать"
                        selectedLabel="Выбрана"
                        deselectLabel="Отменить выбор"
                        open-direction="bottom"
                        :searchable="true"
                        :loading="isLoadingAuthor"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFindBookAuthor"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет автора в списке</span>
                </multiselect>
            </div>
            <div class="col-12">
                <label>Серия</label>
                <multiselect
                        v-model="selectedSeries"
                        :options="series"
                        :multiple="true"
                        :clear-on-select="true"
                        :close-on-select="false"
                        :hide-selected="true"
                        :preserve-search="true"
                        :preselect-first="true"
                        label="title"
                        track-by="id"
                        placeholder="Введите название серии"
                        selectLabel="Выбрать"
                        selectedLabel="Выбрана"
                        deselectLabel="Отменить выбор"
                        open-direction="bottom"
                        :searchable="true"
                        :loading="isLoadingSeries"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFindSeries"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет серии в списке</span>
                </multiselect>
            </div>
            <div class="col-12 text-right">
                <button type="button" class="btn btn-secondary" @click="savePublication">Сохранить</button>
            </div>
        </div>
        <vue-snotify></vue-snotify>
    </div>
</template>
<script>
    import Multiselect from 'vue-multiselect'
    import axios from 'axios'

    export default {
        name: 'PublicationEditor',
        props: [
            'publicationId'
        ],
        components: {
            Multiselect
        },
        data() {
            return {
                selectedBooks: [],
                selectedAuthors: [],
                selectedSeries: [],
                books:[],
                authors:[],
                series:[],
                isLoadingBook: false,
                isLoadingAuthor: false,
                isLoadingSeries: false,
                title: '',
                text: '',
                image: null,
                imagePreview: null
            }
        },
        methods: {
            asyncFindBook (query) {
                if (query.length) {
                    this.isLoadingBook = true
                    return axios.post('/book/editor/books/get', {'title': query})
                        .then((response) => {
                            this.books = response.data.books
                            this.isLoadingBook = false
                        })
                        .catch((error) => {
                            this.$snotify.error('Попробуйте позже', 'Ошибка')
                        })
                }
            },
            asyncFindBookAuthor (query) {
                if (query.length) {
                    this.isLoadingAuthor = true
                    return axios.post('/book/editor/authors/get', {'name': query})
                        .then((response) => {
                            this.authors = response.data.authors
                            this.isLoadingAuthor = false
                        })
                        .catch((error) => {
                            this.$snotify.error('Попробуйте позже', 'Ошибка')
                        })
                }
            },
            asyncFindSeries (query) {
                if (query.length) {
                    this.isLoadingSeries = true
                    return axios.post('/book/editor/series/get', {'title': query})
                        .then((response) => {
                            this.series = response.data.series
                            this.isLoadingSeries = false
                        })
                        .catch((error) => {
                            this.$snotify.error('Попробуйте позже', 'Ошибка')
                        })
                }
            },
            savePublication () {
                let book_list = []
                let author_list = []
                let series_list = []

                for (let key in this.selectedBooks) {
                    book_list.push(this.selectedBooks[key].id)
                }

                for (let key in this.selectedAuthors) {
                    author_list.push(this.selectedAuthors[key].id)
                }

                for (let key in this.selectedSeries) {
                    series_list.push(this.selectedSeries[key].id)
                }

                let rowData = {
                    'id': this.publicationId,
                    'title': this.title,
                    'text': this.text,
                    'books': book_list,
                    'authors': author_list,
                    'series': series_list
                }

                var data = new FormData()
                // data.append('image', this.image, this.image.data)
                data.append('image', this.image)
                data.append('data', JSON.stringify(rowData))

                const config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }

                return axios.post('/publication/editor/save', data, config)
                    .then((response) => {

                        if (this.publicationId) {
                            this.$snotify.success('Пост сохранен', 'Изменение')
                        } else {
                            this.$snotify.success('Пост добавлен', 'Новая')
                        }

                        this.publicationId = response.data.id
                        this.imagePreview = response.data.image
                    })
                    .catch((error) => {
                        this.$snotify.error('Попробуйте позже', 'Ошибка')
                    })
            },
            countDownChanged (dismissCountDown) {
                this.dismissCountDown = dismissCountDown
            }
        },
        mounted () {
            if (this.publicationId) {
                axios.post('/publication/editor/get', {'id': this.publicationId})
                    .then((response) => {
                        if (response.data.error.length) {
                            this.$snotify.error(response.data.error, 'Ошибка')
                        } else {
                            this.title = response.data.publication.title
                            this.text = response.data.publication.text
                            this.image = response.data.publication.image
                            this.imagePreview = response.data.publication.image
                            this.selectedBooks = response.data.publication.books
                            this.selectedAuthors = response.data.publication.authors
                            this.selectedSeries = response.data.publication.series
                        }
                    })
                    .catch((error) => {
                        this.$snotify.error('Попробуйте позже', 'Ошибка')
                    })
            }
        }
    }
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
    .libs__publication_editor .col-12 {
        padding-bottom: 10px;
    }
</style>
