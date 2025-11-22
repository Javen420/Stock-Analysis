<!-- displays all the portfolios/stocks that the user has saved.
will only appear if user is logged in -->

<template>
    <div id="main_container" class="container">

        <!-- Portfolio Section -->
        <div id="port_section">
            <h1 class="text-center">
                portfolios
            </h1>
            <div id="Portfolios">
                <div v-for="portfolio in portfolios" id="portfolio">
                    <img :src="portfolio.img"></img>
                    <p>
                        {{ portfolio.name }}
                    </p>
                    <p>
                        {{ portfolio.description }}
                    </p>
                </div>
            </div>
        </div>

        <!-- wishlist section -->
        <div>
            <h1 class="text-center">
                Wish list
            </h1>
            <div id="individual stocks">
                <div v-for="stock in wishlist" id="indi_stock">
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
    </div>
</template>

<script>
    export default{
        name: "my_stocks"
    }
</script>

<style></style>