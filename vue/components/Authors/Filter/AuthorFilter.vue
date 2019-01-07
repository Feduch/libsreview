<template>
    <div class="la__vue_app__author_filter" id="la__vue_app__author_filter" v-cloak>
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
                       @change="getAuthors"
                >
                <label class="form-check-label" for="rating" @change="getAuthors">
                    по рейтингу
                </label>
            </div>
            <div class="form-check form-check-inline">
                <input class="form-check-input"
                       v-model="sort"
                       type="radio"
                       value="name"
                       id="name"
                       @change="getAuthors"
                >
                <label class="form-check-label" for="name" @change="getAuthors">
                    по алфавиту
                </label>
            </div>
            <div class="form-check form-check-inline">
                <input class="form-check-input"
                       v-model="sort"
                       type="radio"
                       value="-date_create"
                       id="date_create"
                       @change="getAuthors"
                >
                <label class="form-check-label" for="date_create" @change="getAuthors">
                    по дате поступления
                </label>
            </div>
        </form>
        <div class="la__vue_app"></div>
        <div class="la__vue_app__author" v-for="author in authors">
            <author-item :author="author"></author-item>
        </div>
        <div class="col-12 text-center" v-if="isLoad">
            <img src="/static/images/nav_preloader.gif" />
        </div>
        <b-pagination size="md"
                      v-model="currentPage"
                      :total-rows="totalRows"
                      :per-page="30"
                      :limit="10"
                      :hide-goto-end-buttons="true"
                      @input="getAuthors"
                      v-if="showPagination">
        </b-pagination>
    </div>
</template>
<script>
    import AuthorItem from '../../Authors/Author/AuthorItem.vue'
    import axios from 'axios'
    import { request } from 'graphql-request'

    const query = `{
              genres {
                name
                id
              }
            }`

    export default {
        name: 'AuthorFilter',
        components: {
            'author-item': AuthorItem
        },
        data() {
            return {
                sort: '-rating',
                authors: []
            }
        },
        methods: {
            getAuthors () {
                window.scrollTo(0, 0)
                $('#libs__authors').remove()
                this.isLoad = true
                this.showPagination = false
                axios.post('/authors/get', {
                    page: this.currentPage,
                    sort: this.sort
                })
                    .then((response) => {
                        this.authors = response.data.authors
                        this.totalRows = response.data.count
                        this.isLoad = false
                        this.showPagination = true
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        },
        mounted() {
            request('/api/0.1/graphql', query).
            then(data => {
                this.genres = data.genres
            })
        }
    }
</script>
<style scoped>
    .la__vue_app__author_filter {
        padding-top: 15px;
        padding-bottom: 15px;
    }

    .la__vue_app {
        padding-top: 15px;
    }

    [v-cloak] {
        display: none;
    }
    .la__vue_app__book_filter {
        padding: 15px 0 30px 0;
        font-size: 14px;
    }

    .la__vue_app__book_filter .form-inline {
        padding-bottom: 5px;
    }

    .la__vue_app__book_filter_button {
        padding-right: 58px;
    }

</style>
