<template>
    <div>
        <button class="btn btn-danger btn-sm"
                v-if="!showEmailForm"
                @click="showEmailForm = true"
        >
            <i class="far fa-envelope"></i> {{ title }}
        </button>
        <small id="btnHelp"
               class="form-text text-info"
               v-if="!showEmailForm"
        >{{note}}</small>
        <div class="form-group">
            <div class="input-group input-group-sm mb-3" v-if="showEmailForm">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="basic-addon1">@</span>
                </div>
                <input type="email"
                       class="form-control"
                       placeholder="Введите Email"
                       aria-label="Введите Email"
                       aria-describedby="button-addon1"
                       v-model="email"
                >
                <div class="input-group-append">
                    <button
                            class="btn btn-outline-secondary"
                            type="button"
                            id="button-addon2"
                            @click="setSubscribe"
                    >{{ buttonTitle }}</button>
                </div>
            </div>
            <small id="emailHelp"
                   class="form-text text-info"
                   :class="{ 'text-info': !hasError,  'text-danger': hasError}"
            >{{result}}</small>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'

    export default {
        name: 'Notify',
        props: [
            'title',
            'note',
            'bookId',
            'authorId',
            'collectionId'
        ],
        components: {
        },
        data() {
            return {
                showEmailForm: false,
                showResult: false,
                email: '',
                result: '',
                buttonTitle: 'подписаться',
                buttonAction: true,
                hasError: false
            }
        },
        methods: {
            setSubscribe () {
                if (this.validateEmail(this.email)) {
                    this.hasError = false

                    if (this.buttonAction) {
                        axios.post('/api/subscribe', {
                            'email': this.email,
                            'book_id': this.bookId,
                            'authorId': this.authorId,
                            'collection_id': this.collectionId
                        })
                            .then((response) => {
                                this.result = response.data.info
                                this.hasError = false
                                if (response.data.isIsset) {
                                    this.buttonTitle = 'отписаться'
                                    this.buttonAction = false
                                }
                            })
                            .catch((error) => {
                                this.result = 'Ошибка, попробуйте позже.'
                                this.hasError = true
                            })
                    } else {
                        axios.delete('/api/subscribe', {
                            data: {
                                'email': this.email,
                                'book_id': this.bookId,
                                'authorId': this.authorId,
                                'collection_id': this.collectionId
                            }
                        })
                            .then((response) => {
                                this.result = response.data.info
                                this.hasError = false
                                this.buttonTitle = 'подписаться'
                                this.buttonAction = true
                            })
                            .catch((error) => {
                                this.result = 'Ошибка, попробуйте позже.'
                                this.hasError = true
                            })
                    }
                } else {
                    this.result = 'Укажите email'
                    this.hasError = true
                }
            },
            validateEmail(email) {
                var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return re.test(String(email).toLowerCase())
            }
        }
    }
</script>
<style scoped>
</style>
