<!-- displays all the portfolios/stocks that the user has saved.
will only appear if user is logged in -->

<template>
    <div id="main_container" class="container">
        <h1 class="text-center">
            My stocks
        </h1>
        <div id="individual stocks">
            <div v-for="stock in stocks" id="indi_stock">
                <img :src="stock.img"></img>
                <p>
                    {{ stock.name }}
                </p>
                <p>
                    {{ stock.description }}
                </p>
            </div>
        </div>
    </div>
</template>

<script>

</script>

<style>
    
</style>