<template>
    <span>
        <p v-html="formattedString">{{ text }}</p>
        <span v-show="text.length > maxChars">
            <a :href="link" v-show="!isReadMore" class="btn btn-secondary btn-sm" v-on:click="triggerReadMore($event, true)">{{moreButtonValue}}</a>
            <a :href="link" v-show="isReadMore" class="btn btn-secondary btn-sm" v-on:click="triggerReadMore($event, false)">{{lessButtonValue}}</a>
        </span>
    </span>
</template>
<script>
    export default {
        name: 'read-more',
        props: {
            moreButtonValue: {
                type: String,
                default: 'больше текста'
            },
            lessButtonValue: {
                type: String,
                default: 'скрыть текст'
            },
            text: {
                type: String,
                default: ''
            },
            maxChars: {
                type: Number,
                default: 400
            },
            link: {
                type: String,
                default: '#'
            },
        },
        data() {
            return {
                isReadMore: false
            }
        },
        computed: {
            formattedString() {
                let val_container = this.text;
                if(!this.isReadMore && this.text.length > this.maxChars){
                    val_container = val_container.substring(0,this.maxChars) + '...';
                }
                return(val_container);
            }
        },
        methods: {
            triggerReadMore(e, b){
                if(this.link == '#'){
                    e.preventDefault();
                }
                if(this.lessButtonValue !== null || this.lessButtonValue !== '')
                    this.isReadMore = b;
            }
        }
    }
</script>
<style scoped>
    p {
        font-size: 14px;
        line-height: 1.5em;
    }
</style>
