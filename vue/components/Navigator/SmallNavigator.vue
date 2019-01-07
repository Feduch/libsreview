<template>
    <form>
        <div class="form-group">
            <label for="exampleSelect1">Лучшие книги</label>
            <select class="form-control form-control-sm"  name="genre" v-model="selectedGenre">
                <option value="">Выберите один из жанров</option>
                <option v-for="genre in genres" :value="genre.id">{{ genre.name }}</option>
            </select>
        </div>
        <div class="form-group">
            <label for="exampleSelect1">Книги года</label>
            <input class="form-control form-control-sm" v-model="years" type="text">
        </div>
        <div class="form-group">
            <button type="button" class="btn btn-secondary btn-sm" @click="toNavigator">Показать книги</button>
        </div>
    </form>
</template>

<script>
    import { mapGetters } from 'vuex'

    export default {
        name: 'SmallNavigator',
        components: {
        },
        data() {
            return {
                selectedGenre: 116,
                years: '2017-2018'
            }
        },
        methods: {
            toNavigator () {
                this.$store.dispatch('setSmallNavigator', {
                    genre: this.selectedGenre,
                    years: this.years,
                    name: this.genres.find(genre => genre.id === this.selectedGenre).name
                })
                    .then((result) => {
                        window.location.replace("/nav/")
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        },
        mounted() {
            this.$store.dispatch('setGlobalSettings')
            const smallNavigator = this.$store.getters.getSmallNavigator

            if (smallNavigator.genre > 0) {
                this.selectedGenre = smallNavigator.genre
                this.years = smallNavigator.years
            }
        },
        computed: {
            ...mapGetters({
                genres: 'getGenres'
            })
        }
    }
</script>

<style scoped>
</style>
