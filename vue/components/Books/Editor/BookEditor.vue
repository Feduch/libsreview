<template>
    <div class="libs__book_editor">
        <div class="row">
            <div class="col-3">
                <div class="card mb-3" v-if="imagePreview">
                    <img class="card-img-top" :src="imagePreview">
                </div>
            </div>
            <div class="col-12">
                <b-form-file
                        accept="image/jpeg, image/png, image/gif"
                        v-model="image" placeholder="Обложка для книги"
                ></b-form-file>
            </div>
            <div class="col-12">
                <label>Статус</label>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="inlineRadio1" v-model="status" value="true">
                    <label class="form-check-label" for="inlineRadio1"><span class="badge badge-success">Опубликована</span></label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="inlineRadio2" v-model="status" value="false">
                    <label class="form-check-label" for="inlineRadio2"><span class="badge badge-dark">Отключена</span></label>
                </div>
            </div>
            <div class="col-12">
                <label>Название</label>
                <input type="text" class="form-control" v-model="title"/>
            </div>
            <div class="col-12">
                <label>Описание</label>
                <textarea type="text" class="form-control" rows="5" v-model="description"></textarea>
            </div>
            <div class="col-12">
                <label>Жанры</label>
                <multiselect
                        v-model="selectedGenres"
                        :options="genres"
                        :multiple="true"
                        :clear-on-select="true"
                        :close-on-select="false"
                        :hide-selected="true"
                        :preserve-search="true"
                        :preselect-first="true"
                        label="name"
                        track-by="id"
                        placeholder="Введите название жанра"
                        selectLabel="Выбрать"
                        selectedLabel="Выбрана"
                        deselectLabel="Отменить выбор"
                        open-direction="bottom"
                        :searchable="true"
                        :loading="isLoading"
                        :internal-search="true"
                        :show-no-results="true"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет жанра в списке</span>
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
                        placeholder="Введите имя автора"
                        selectLabel="Выбрать"
                        selectedLabel="Выбрана"
                        deselectLabel="Отменить выбор"
                        open-direction="bottom"
                        :searchable="true"
                        :loading="isLoading"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFindAuthors"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет автора в списке</span>
                </multiselect>
            </div>
            <div class="col-12">
                <label>Возрастное ограничение</label>
                <input type="text" class="form-control" v-model="age"/>
            </div>
            <div class="col-12">
                <label>Год публикации</label>
                <input type="text" class="form-control" v-model="year"/>
            </div>
            <div class="col-12">
                <label>Серия</label>
                <multiselect
                        v-model="selectedSeries"
                        :options="series"
                        :multiple="false"
                        :clear-on-select="true"
                        :close-on-select="true"
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
                        :loading="isLoading"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFindSeries"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет серии в списке</span>
                </multiselect>
            </div>
            <div class="col-12">
                <label>Номер в серии</label>
                <input type="text" class="form-control" v-model="nrSeries"/>
            </div>
            <div class="col-12">
                <label>Премии</label>
                <multiselect
                        v-model="selectedAwards"
                        :options="awards"
                        :multiple="true"
                        :clear-on-select="true"
                        :close-on-select="false"
                        :hide-selected="true"
                        :preserve-search="true"
                        :preselect-first="true"
                        label="name"
                        track-by="id"
                        placeholder="Введите название премии"
                        selectLabel="Выбрать"
                        selectedLabel="Выбрана"
                        deselectLabel="Отменить выбор"
                        open-direction="bottom"
                        :searchable="true"
                        :loading="isLoadingAwards"
                        :internal-search="false"
                        :show-no-results="true"
                        @search-change="asyncFindAwards"
                        :block-keys="['Tab']"
                >
                    <span slot="noResult">Нет премии в списке</span>
                </multiselect>
            </div>
            <div class="col-6">
                <label>Рейтинг:</label>
                <input type="text" class="form-control" v-model="rating" disabled="disabled"/>
            </div>
            <div class="col-6">
                <label>Рейтинг ручной</label>
                <input type="text" class="form-control" v-model="manualRating"/>
            </div>
            <div class="col-12">&nbsp;</div>
            <div class="col-12">
                <b-alert :show="dismissCountDown"
                         dismissible
                         variant="success"
                         @dismissed="dismissCountDown=0"
                         @dismiss-count-down="countDownChanged">
                    <p>Книгу сохранил {{ dismissCountDown }}</p>
                    <b-progress variant="success"
                                :max="dismissSecs"
                                :value="dismissCountDown"
                                height="4px">
                    </b-progress>
                </b-alert>
            </div>
            <div class="col-12">
                <button type="button" class="btn btn-secondary" @click="saveBook(true)">Сохранить и продолжить редактирование</button>
                <button type="button" class="btn btn-secondary" @click="saveBook(false)">Сохранить и добавить новую</button>
            </div>
        </div>
    </div>
</template>
<script>
    import Multiselect from 'vue-multiselect'
    import axios from 'axios'

    export default {
        name: 'BookEditor',
        props: [
            'bookId'
        ],
        components: {
            Multiselect
        },
        data() {
            return {
                selectedGenres: [],
                selectedAuthors: [],
                selectedSeries: [],
                selectedAwards: [],
                authors:[],
                genres:[],
                series:[],
                awards:[],
                isLoading: false,
                isLoadingAwards: false,
                title: '',
                description: '',
                age: '',
                year: '',
                nrSeries: '',
                rating: '',
                manualRating: '',
                image: null,
                imagePreview: null,
                dismissSecs: 3,
                dismissCountDown: 0,
                showDismissibleAlert: false,
                status: null
            }
        },
        methods: {
            asyncFindAuthors (query) {
                if (query.length) {
                    this.isLoading = true
                    return axios.post('/book/editor/authors/get', {'name': query})
                        .then((response) => {
                            this.authors = response.data.authors
                            this.isLoading = false
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                }
            },
            asyncFindAwards (query) {
                if (query.length) {
                    this.isLoadingAwards = true
                    return axios.post('/awards/get', {'name': query})
                        .then((response) => {
                            this.awards = response.data.awards
                            this.isLoadingAwards = false
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                }
            },
            asyncFindSeries (query) {
                if (query.length) {
                    this.isLoading = true
                    return axios.post('/book/editor/series/get', {'title': query})
                        .then((response) => {
                            this.series = response.data.series
                            this.isLoading = false
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                }
            },
            saveBook (flag) {
                let author_list = []

                for (let key in this.selectedAuthors) {
                    author_list.push(this.selectedAuthors[key].id)
                }

                let genres_list = []

                for (let key in this.selectedGenres) {
                    genres_list.push(this.selectedGenres[key].id)
                }

                let awards_list = []

                for (let key in this.selectedAwards) {
                    awards_list.push(this.selectedAwards[key].id)
                }

                let rowData = {
                    'id': this.bookId,
                    'title': this.title,
                    'description': this.description,
                    'authors': author_list,
                    'genres': genres_list,
                    'awards': awards_list,
                    'age': this.age,
                    'year': this.year,
                    'nr_series': this.nrSeries,
                    'manual_rating': this.manualRating,
                    'status': this.status
                }

                if (this.selectedSeries) {
                    rowData['series'] =  this.selectedSeries.id
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

                return axios.post('/book/editor/save', data, config)
                    .then((response) => {
                        this.dismissCountDown = this.dismissSecs

                        if (flag) {
                            this.bookId = response.data.id
                        } else {
                            this.bookId = null
                            this.title = null
                            this.description = null
                            this.image = null
                            this.imagePreview = null
                            this.selectedAuthors = []
                            this.selectedGenres = []
                            this.selectedAwards = []
                            this.age = null
                            this.year = null
                            this.selectedSeries = null
                            this.nrSeries = null
                            this.rating = null
                            this.manualRating = 0
                            this.status = null
                        }

                    })
                    .catch((error) => {
                        console.log(error)
                    })
            },
            countDownChanged (dismissCountDown) {
                this.dismissCountDown = dismissCountDown
            }
        },
        mounted () {
            axios.post('/book/editor/get', {'id': this.bookId})
                .then((response) => {
                    this.title = response.data.book.title
                    this.description = response.data.book.description
                    this.image = response.data.book.image
                    this.imagePreview = response.data.book.image
                    this.selectedAuthors = response.data.book.authors
                    this.selectedGenres = response.data.book.genres
                    this.selectedAwards = response.data.book.awards
                    this.age = response.data.book.age
                    this.year = response.data.book.year
                    this.selectedSeries = response.data.book.series
                    this.nrSeries = response.data.book.nr_series
                    this.rating = response.data.book.rating
                    this.manualRating = response.data.book.manual_rating
                    this.genres = response.data.genres
                    this.status = response.data.book.status
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
    .libs__book_editor .col-12 {
        padding-bottom: 10px;
    }
</style>
