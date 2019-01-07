<template>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                <a :href="post.url"><span>{{ post.title }}</span></a>
            </h5>
            <img :src="post.image" :alt="post.title" v-if="post.image" />
            <p class="card-text">
                <span>{{ post.previewText }}</span>
            </p>
            <a :href="post.url" class="btn btn-primary">Читать дальше</a>
        </div>
        <div class="card-footer text-muted">
            <span title="Просмотры"><img src="/static/images/eye.png" alt="Количество просмотров"> {{ post.showCounter }}</span>
            последнее обновление <span >{{ dateUpdate }}</span>
        </div>
    </div>
</template>
<script>
    import moment from 'moment'

    export default {
        name: 'PostItem',
        props: [
            'post'
        ],
        components: {
        },
        data() {
            return {
            }
        },
        methods: {
        },
        computed: {
            dateUpdate: function() {
                return moment(this.post.dateUpdate).format('DD.MM.YYYY, hh:mm:ss')
            }
        }
    }
</script>
<style scoped>
    .card {
        margin-bottom: 18px;
    }
</style>
