<template>
    <div class="col-12">
        <div class="row" v-if="!showSubscribe">
            <div class="col-12 text-center" v-if="isLoad">
                <img src="/static/images/nav_preloader.gif" />
            </div>
            <div class="col-12 col-lg-4">
                <div class="row">
                    <div class="col-12"><strong>Электронная книга</strong></div>
                    <div class="col-12 la__vue_app__book_item"
                         v-for="partner in partners"
                         v-show="partner.available == true"
                         v-if="partner.type == 'EBOOK'"
                    >
                        <img :src="'https://partners.libs.ru/media/'+partner.partner.logo" width="16"/>
                        <a v-bind:href="partner.url" target="_blank">
                            {{ partner.partner.name }} - <span v-if="partner.currency == 'USD'">$</span> {{ partner.price }}
                            <span v-if="partner.currency == 'RUR'">руб</span>
                        </a>
                    </div>
                    <div class="col-12"><p></p></div>
                </div>
            </div>
            <div class="col-12 col-lg-4">
                <div class="row">
                    <div class="col-12"><strong>Аудиокнига</strong></div>
                    <div class="col-12 la__vue_app__book_item"
                         v-for="partner in partners"
                         v-show="partner.available == true"
                         v-if="partner.type == 'AUDIOBOOK'"
                    >
                        <img :src="'https://partners.libs.ru/media/'+partner.partner.logo" width="16"/>
                        <a v-bind:href="partner.url" target="_blank">
                            {{ partner.partner.name }} - <span v-if="partner.currency == 'USD'">$</span> {{ partner.price }}
                            <span v-if="partner.currency == 'RUR'">руб</span>
                        </a>
                    </div>
                    <div class="col-12"><p></p></div>
                </div>
            </div>
            <div class="col-12 col-lg-4">
                <div class="row">
                    <div class="col-12"><strong>Бумажная книга</strong></div>
                    <div class="col-12 la__vue_app__book_item"
                         v-for="partner in partners"
                         v-show="partner.available == true"
                         v-if="partner.type == 'BOOK'"
                    >
                        <img :src="'https://partners.libs.ru/media/'+partner.partner.logo" width="16"/>
                        <a v-bind:href="partner.url" target="_blank">
                            {{ partner.partner.name }} - <span v-if="partner.currency == 'USD'">$</span> {{ partner.price }}
                            <span v-if="partner.oldprice" class="libs__partner_price_sale">скидка</span>
                            <span v-if="partner.currency == 'RUR'">руб</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="row" v-if="showSubscribe">
            <div class="col-12">
                <notify
                        title="Сообщить о начале продаж"
                        note="Вы получите только один раз уведомление о начале продаж этой книги"
                        :book-id="libsid"
                ></notify>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import { request } from 'graphql-request'
    import Notify from '../../Notify/Notify.vue'

    const query = `query books_price($name: String!, $author: String, $libsid: Int, $litresid: Int) {
      books_price(name:$name, author:$author, libsid: $libsid, litresid: $litresid) {
        type
        available
        url
        price
        oldprice
        currency
        name
        author
        partner {
          name,
          logo
        }
      }
    }`

    export default {
        name: 'partner-price',
        components: {
            'notify': Notify
        },
        props: [
            'title',
            'author',
            'libsid',
            'litresId'
        ],
        data() {
            return {
                partners: [],
                isLoad: true,
                showSubscribe: false
            }
        },
        created() {
            const variables = {
                name: this.title,
                author: this.author,
                libsid: this.libsid,
                litresid: this.litresId
            };

            request('https://partners.libs.ru/api/0.1/graphql', query, variables)
                .then(data => {
                    this.partners = data.books_price
                    this.isLoad = false

                    if (data.books_price.length == 0) {
                        this.showSubscribe = true
                    }

                    axios.post('/book/manager/partner/link/count', {'book_id': this.libsid, 'count_partner_link': data.books_price.length})
                        .then((response) => {
                            // // console.log(response)
                        })
                        .catch((error) => {
                            // // console.log(error)
                        })
                })
        }
    }
</script>
<style scoped>
    .la__vue_app__book_item a {
        padding-left: 3px;
        padding-bottom: 3px;
    }

    .libs__partner_price_sale {
        color: darkred;
    }
</style>
