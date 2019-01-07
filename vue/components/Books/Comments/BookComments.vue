<template>
    <div class="libs__reviews">
        <ul class="la__top_set">
            <li class="la__top_set__header">Отзывы о книге ({{commentCount}})</li>
        </ul>
        <div class="libs__comment" v-for="comment in comments">
            <span v-if="comment.url">
                <a :href="comment.url" >{{ comment.username }}</a>:
                <span v-html="comment.text"></span>
            </span>
            <span v-else>
                <strong>{{ comment.response_author }}</strong> <span v-html="comment.response_text"></span>
            </span>
        </div>
        <div class="libs__comment_more" v-if="isMore">
            <a @click="get">показать еще >></a>
        </div>
        <div class="libs__reviews_button" id="libs-add-comments">
        </div>
        <form>
            <div class="form-group">
                <label for="message-text" class="col-form-label">Ваш отзыв:</label>
                <quill-editor v-model="reviewText"
                              :options="editorOption"
                >
                </quill-editor>
            </div>
            <button v-if="!isAuth" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#LogInModal">Оставить отзыв</button>
            <button
                    type="button"
                    class="btn btn-primary"
                    role="button"
                    v-if="isAuth"
                    @click="set"
            >Отправить</button>
        </form>
        <vue-snotify></vue-snotify>
    </div>
</template>
<script>
    import axios from 'axios'
    import {request} from 'graphql-request'

    const query = `query book_comments($libs_book_id: Int, $book_name: String) {
                  book_comments(libs_book_id: $libs_book_id, book_name: $book_name) {
                    id
                    response_author
                    response_date
                    response_text
                  }
                }`

    export default {
        name: 'Comments',
        props: [
            'bookId',
            'bookName'
        ],
        data() {
            return {
                page: 1,
                count: 10,
                comments: [],
                reviewText: '',
                isAuth: false,
                commentCount: 0,
                isMore: false,
                editorOption: {
                    placeholder: 'Ваш отзыв ...',
                    theme: 'snow',
                    modules: {
                        toolbar: [
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote']
                        ],
                        syntax: {
                            highlight: text => hljs.highlightAuto(text).value
                        }
                    }
                }
            }
        },
        methods: {
            set () {
                if (this.reviewText.length == 0) {
                    this.$snotify.error('Напишите ваш отзыв', 'Ошибка')
                    return false
                }

                axios.post('/comments/set', {
                    'book_id': this.bookId,
                    'text': this.reviewText
                })
                    .then((response) => {
                        this.comments.push(response.data.comment)
                        this.reviewText = ''
                        this.commentCount += 1
                    })
                    .catch((error) => {
                        this.$snotify.error('Попробуйте позже', 'Ошибка')
                    })
                yaCounter15891616.reachGoal('libsbtn-add-comment-bottom')
            },
            get () {
                axios.post('/comments/get', {
                    'book_id': this.bookId,
                    'count': this.count,
                    'page': this.page
                })
                    .then((response) => {
                        if (response.data.comments.length) {
                            if (this.comments.length) {
                                this.comments = this.comments.concat(response.data.comments)
                            } else {
                                this.comments = response.data.comments
                                this.commentCount = response.data.commentCount

                                if (this.commentCount > 10) {
                                    this.isMore = true
                                }

                                if (this.commentCount) {
                                    $('.libs__book_comment_list').show()
                                }
                            }
                        } else {
                            this.isMore = false
                        }
                        this.isAuth = response.data.isAuth
                        this.page += 1
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        },
        created () {
            this.get()
        },
        mounted () {
            if (this.comments.length == 0) {
                request('https://agregator.libs.ru/api/0.1/graphql', query, {
                    'libs_book_id': this.bookId,
                    'book_name': this.bookName,
                    'count': this.count,
                    'page': this.page
                }).
                then(data => {
                    if (data.book_comments.length) {
                        this.comments = data.book_comments
                        $('.libs__book_comment_list').show()
                    }
                })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        },
        computed: {}
    }
</script>
<style>
    .libs__reviews,
    .libs__comment {
        padding-bottom: 5px;
    }

    .libs__reviews_button {
        padding-top: 10px;
    }
    .libs__comment_more {
        text-align: right;
    }

    .quill-editor >>> .ql-container {
        min-height: 3rem!important;
    }
</style>
