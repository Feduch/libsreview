import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        globalSettings:{
            genres: []
        },
        smallNavigator: {
            genre: 0,
            years: '',
            name: ''
        },
        globalTimestamp: 0
    },
    mutations: {
        setGlobalSettings (state, payload) {
            state.globalSettings = payload
            state.globalTimestamp = Math.round(Date.now() / 1000)
        },
        setSmallNavigator (state, payload) {
            state.smallNavigator = payload
        },
    },
    actions: {
        setGlobalSettings ({ commit, state }) {
            if (state.globalTimestamp + (24 * 3600) < Math.round(Date.now() / 1000)) {
                axios.get('/api/vue/global/settings')
                    .then((response) => {
                        commit('setGlobalSettings', response.data)
                    })
            }
        },
        setSmallNavigator ({ commit }, payload) {
            commit('setSmallNavigator', payload)
        },
    },
    getters: {
        getSmallNavigator: state => state.smallNavigator,
        getGenres: state => state.globalSettings.genres,
    },
    plugins: [createPersistedState()]
})
