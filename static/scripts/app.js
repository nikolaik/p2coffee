$(function () {
    /* TODO: poll per second */
    $.getJSON(URLS['stats-events'], function(eventSeries) {
        console.log(eventSeries);
        $('#container').highcharts({
            chart: {
                type: 'column',
                zoomType: 'xy'
            },
            title: {
                text: 'Power in watt over time'
            },
            xAxis: {
                type: 'datetime',
				tickInterval: 3600 * 1000,
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

