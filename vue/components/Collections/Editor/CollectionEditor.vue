<template>
    <div class="libs__collection_editor">
        <div class="row">
            <div class="col-12">
                <div class="card mb-3" v-if="imagePreview">
                    <img class="card-img-top" :src="imagePreview">
                </div>
            </div>
            <div class="col-12">
                <b-form-file
                        accept="image/jpeg, image/png, image/gif"
                        v-model="image" :state="Boolean(image)" placeholder="Обложка для коллекции"
                ></b-form-file>
            </div>
            <div class="col-12">
                <label>Название</label>
                <input type="text" class="form-control" v-model="title"/>
            </div>
            <div class="col-12">
                <label>Описание</label>
                <quill-editor v-model="text"
                              :options="editorOption"
                >
                </quill-editor>
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
                        :loading="isLoading"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFind"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет книг в списке</span>
                </multiselect>
            </div>
            <div class="col-12 text-right">
                <button type="button" class="btn btn-secondary" @click="saveCollection">Сохранить</button>
            </div>
        </div>
        <vue-snotify></vue-snotify>
    </div>
</template>
<script>
    import Multiselect from 'vue-multiselect'
    import axios from 'axios'

    export default {
        name: 'CollectionEditor',
        props: [
            'collectionId'
        ],
        components: {
            Multiselect
        },
        data() {
            return {
                selectedBooks: [],
                books:[],
                isLoading: false,
                title: '',
                text: '',
                image: null,
                imagePreview: null,
                editorOption: {
                    placeholder: 'Введите описание коллекции...',
                    theme: 'snow',
                    modules: {
                        toolbar: [
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote'],
                            ['clean']
                        ],
                        syntax: {
                            highlight: text => hljs.highlightAuto(text).value
                        }
                    }
                }
            }
        },
        methods: {
            asyncFind (query) {
                if (query.length) {
                    this.isLoading = true
                    return axios.post('/book/editor/books/get', {'title': query})
                        .then((response) => {
                            this.books = response.data.books
                            this.isLoading = false
                        })
                        .catch((error) => {
                            this.$snotify.error('Попробуйте позже', 'Ошибка')
                        })
                }
            },
            saveCollection () {
                let book_list = []

                for (let key in this.selectedBooks) {
                    book_list.push(this.selectedBooks[key].id)
                }

                let rowData = {
                    'id': this.collectionId,
                    'title': this.title,
                    'text': this.text,
                    'books': book_list
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

                return axios.post('/collections/editor/save', data, config)
                    .then((response) => {

                        if (this.collectionId) {
                            this.$snotify.success('Коллекция сохранена', 'Изменение')
                        } else {
                            this.$snotify.success('Коллекция добавлена', 'Новая')
                        }

                        this.collectionId = response.data.id
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
            if (this.collectionId) {
                axios.post('/collections/editor/get', {'id': this.collectionId})
                    .then((response) => {
                        if (response.data.error.length) {
                            this.$snotify.error(response.data.error, 'Ошибка')
                        } else {
                            this.title = response.data.collection.title
                            this.text = response.data.collection.text
                            this.image = response.data.collection.image
                            this.imagePreview = response.data.collection.image
                            this.selectedBooks = response.data.collection.books
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
    .libs__collection_editor .col-12 {
        padding-bottom: 10px;
    }

    .quill-editor >>> .ql-container {
        min-height: 13rem!important;
    }
</style>
