<template>
    <div class="container">
        <div class="row my-2">
            <div class="col-lg-9 order-lg-2">
                <ul class="nav nav-tabs">
                    <li class="nav-item">
                        <a href="" data-target="#profile" data-toggle="tab" class="nav-link active">Активность</a>
                    </li>
                    <li class="nav-item">
                        <a href="" data-target="#edit" data-toggle="tab" class="nav-link">Профайл</a>
                    </li>
                </ul>
                <div class="tab-content py-4">
                    <div class="tab-pane active" id="profile">
                        <div class="row" v-if="isLoad">
                            <div class="col-12 text-center">
                                <img src="/static/images/nav_preloader.gif" />
                            </div>
                        </div>
                        <div class="row" v-if="!isLoad">
                            <div class="col-sm-12">
                                <a class="btn btn btn-primary" href="/publication/editor/" role="button">+ Добавить пост</a>
                                <a class="btn btn btn-primary" href="/collections/editor/" role="button">+ Добавить коллекцию</a>
                            </div>

                            <div class="col-md-12">
                                <h4 class="mt-2">Активность на сайте</h4>
                            </div>

                            <div class="col-md-12">
                                <h5>Ваши посты</h5>
                            </div>
                            <div class="col-md-12" v-if="!posts.length">
                                тут пока пусто
                            </div>
                            <div class="col-md-12"
                                 v-for="post in posts">
                                <post-item :post="post"></post-item>
                            </div>

                            <div class="col-md-12">
                                <h5>Ваши коллекции</h5>
                            </div>
                            <div class="col-md-12" v-if="!collections.length">
                                тут пока пусто
                            </div>
                            <div class="col-md-12"
                                 v-for="collection in collections">
                                <collection-item :collection="collection"></collection-item>
                            </div>

                            <div class="col-md-12">
                                <h5>Книги которые Вы оценили</h5>
                            </div>
                            <div class="col-md-12" v-if="!books.length">
                                тут пока пусто
                            </div>
                            <div class="col-md-12"
                                 v-for="book in books">
                                <book-item :book="book"></book-item>
                            </div>
                        </div>
                        <!--/row-->
                    </div>
                    <div class="tab-pane" id="edit">
                        <form role="form">
                            <div class="form-group row">
                                <label class="col-lg-3 col-form-label form-control-label">Имя пользователя</label>
                                <div class="col-lg-9">
                                    <div class="input-group mb-2">
                                        <div class="input-group-prepend">
                                            <div class="input-group-text">@</div>
                                        </div>
                                        <input type="text" v-model="profile.username" aria-describedby="usernameHelp" class="form-control" id="inlineFormInputGroup" placeholder="Имя пользователя">
                                    </div>
                                    <small id="usernameHelp" class="form-text text-muted">Публичная страница https://libs.ru/users/{{profile.username}}</small>
                                </div>
                            </div>
                            <div class="form-group row">
                                <label class="col-lg-3 col-form-label form-control-label">Email</label>
                                <div class="col-lg-9">
                                    <input class="form-control" v-model="profile.email" aria-describedby="emailHelp" type="email" disabled="disabled">
                                    <small id="emailHelp" class="form-text text-muted">Ваш логин</small>
                                </div>
                            </div>
                            <div class="form-group row">
                                <label class="col-lg-3 col-form-label form-control-label">Пароль</label>
                                <div class="col-lg-9">
                                    <input class="form-control"
                                           v-model="password"
                                           type="password"
                                    >
                                </div>
                            </div>
                            <div class="form-group row">
                                <label class="col-lg-3 col-form-label form-control-label">Повторите пароль</label>
                                <div class="col-lg-9">
                                    <input class="form-control"
                                           v-model="rePassword"
                                           type="password"
                                    >
                                </div>
                            </div>
                            <div class="form-group row">
                                <label class="col-lg-3 col-form-label form-control-label"></label>
                                <div class="col-lg-9">
                                    <input type="button" class="btn btn-primary" @click="saveProfile" value="Сохранить">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 order-lg-1 text-center" v-if="!isLoad">
                <img :src="profile.avatar" class="mx-auto img-fluid rounded-circle d-block" alt="avatar">
                <h6 class="mt-2">Загрузите новое фото</h6>
                <form>
                    <label class="custom-file">
                        <input type="file" accept="image/jpeg, image/png" ref="avatar" @change="saveAvatar" id="file" class="custom-file-input">
                        <span class="custom-file-control btn btn-secondary">Выбрать аватар (jpg, png)</span>
                    </label>
                </form>
            </div>
        </div>
        <vue-snotify></vue-snotify>
    </div>
</template>
<script>
    import axios from 'axios'
    import CollectionItem from '../../components/Collections/Collection/CollectionItem.vue'
    import PostItem from '../../components/Posts/Post/PostItem.vue'
    import BookItem from '../../components/Books/Book/BookItem.vue'

    export default {
        name: 'Profile',
        components: {
            'collection-item': CollectionItem,
            'post-item': PostItem,
            'book-item': BookItem
        },
        data() {
            return {
                profile: {
                    username: null,
                    email: null,
                    avatar: null
                },
                posts: [],
                collections: [],
                books: [],
                avatar: null,
                password: null,
                rePassword: null,
                isLoad: true
            }
        },
        methods: {
            getProfile () {
                axios.post('/accounts/profile/get', {})
                    .then((response) => {
                        this.profile = response.data.profile
                        this.posts = response.data.posts
                        this.collections = response.data.collections
                        this.books = response.data.books
                        this.isLoad = false
                    })
                    .catch((error) => {
                        console.log(error)
                    })

            },
            saveProfile () {
                if (this.password === this.rePassword) {
                    axios.post('/accounts/profile/save', {
                        'profile': this.profile,
                        'password': this.password
                    })
                        .then((response) => {
                            for (let key in response.data.result) {
                                let type = response.data.result[key].type
                                let title = response.data.result[key].title
                                let text = response.data.result[key].text

                                if (type === 'success') {
                                    this.$snotify.success(text, title)
                                }

                                if (type === 'error') {
                                    this.$snotify.error(text, title)
                                }
                            }
                        })
                        .catch((error) => {
                            this.$snotify.error('Попробуйте позже', 'Ошибка')
                        })
                } else {
                    this.$snotify.error('Пароли не совпадают', 'Ошибка')
                }
            },
            saveAvatar () {
                var data = new FormData()
                data.append('avatar', this.$refs.avatar.files[0])

                const config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }

                axios.post('/accounts/profile/avatar/save', data, config)
                    .then((response) => {

                        this.profile.avatar = response.data.avatar

                        for (let key in response.data.result) {
                            let type = response.data.result[key].type
                            let title = response.data.result[key].title
                            let text = response.data.result[key].text

                            if (type === 'success') {
                                this.$snotify.success(text, title)
                            }

                            if (type === 'error') {
                                this.$snotify.error(text, title)
                            }
                        }
                    })
                    .catch((error) => {
                        this.$snotify.error('Попробуйте позже', 'Ошибка')
                    })
            },
        },
        created: function () {
            this.getProfile()
        },
        mounted () {
        }
    }
</script>
<style scoped>
</style>
