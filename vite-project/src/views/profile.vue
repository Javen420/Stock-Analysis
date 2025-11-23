<!-- profile page, shows different portfolios, liked stocks and total earnngs? profits, ytd? -->
 <template>
    <div id="main_container" class="row">
        <div id="header">
            <h2>Profile</h2>
        </div>
        <div id="stats_section" class="col">
            <div>
                <p>Total Assets</p>
                <p>{{ total_assets }}</p>
            </div>
            <div>
                <p>Lifetime P/L</p>
                <p>{{ lt_pl }}</p>
            </div>
            <div>
                <p>Daily P/L</p>
                <p>{{ daily_pl }}</p>
            </div>
            <div>
                <p>IDK yet</p>
                <p></p>
            </div>
            <div>
                <p>Idk yet</p>
                <p></p>
            </div>
        </div>
        <div>
            <h3>Portfolios</h3>
        </div>
        <div id="dashboard">
            <div id="individual stocks">
                <div v-for="stock in stocks">

                </div>
            </div>
            <div id="charts">
                <div v-for="chart in charts">

                </div>
            </div>
        </div>
    </div>
 </template>

 <script>
</script>

<style scoped>
</style>