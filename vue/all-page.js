import Vue from 'vue'
import store from './store'
import SmallNavigator from './components/Navigator/SmallNavigator.vue'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.config.devtools=false

new Vue({
    el: '#vue-small-navigator-top',
    store: store,
    components: {
        'small-navigator': SmallNavigator
    }
})

new Vue({
    el: '#vue-small-navigator-right',
    store: store,
    components: {
        'small-navigator': SmallNavigator
    }
})

new Vue({
    el: '#vue-small-navigator-bottom',
    store: store,
    components: {
        'small-navigator': SmallNavigator
    }
})


