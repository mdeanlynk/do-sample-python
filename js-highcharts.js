<script src="https://code.highcharts.com/highcharts.js"></script>
<script>
    // Define the chart options
    var options = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Alert Event'
        },
        xAxis: {
            type: 'category',
            title: {
                text: 'Cause Type'
            }
        },
        yAxis: {
            title: {
                text: 'Count'
            }
        },
        series: [{
            name: 'Cause Type',
            data: []
        }]
    };
    // Request data from the API endpoint
    fetch('https://api-generator.retool.com/8mjKBi/alert_event?cause_type=CLOUD')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Update the chart data
            options.series[0].data = data;
            // Create the chart
            Highcharts.chart('container', options);
        });
</script>
<div id="container"></div>
