$(function () {
    /* TODO */
    $.getJSON(URLS['stats-events'], function(eventSeries) {
        console.log(eventSeries);
        $('#container').highcharts({
            chart: {
                type: 'scatter',
                zoomType: 'xy'
            },
            title: {
                text: 'Power in watt over time'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Watt'
                }
            },
            plotOptions: {
            },
            series: eventSeries
        });
    });
});

