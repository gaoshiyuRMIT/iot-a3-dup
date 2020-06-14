
/*
* line chart with date as x-axis
* param `data` example: [
*   {x: "2019-01-01", y: 30},
*   {x: "2020-01-01", y: 91}
* ]
*/
function generate_date_bar_chart(canvas_id, data) {
    const canvas = document.getElementById(canvas_id);
    const ctx = canvas.getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                label: '# of cars used each day',
                data: data,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    }
                }],
                xAxes: [{
                    type: "time",
                    time: {
                        "unit": "day",
                        "displayFormats": {
                            "day": "DD MMM YYYY"
                        },
                        "parser": "YYYY-MM-DD"
                    }
                }]
            }
        }
    });
    return myChart;
}

function generate_date_revenue_line_chart(canvas_id, data) {
    const canvas = document.getElementById(canvas_id);
    const ctx = canvas.getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'revenue',
                data: data,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 0.1
                    }
                }],
                xAxes: [{
                    type: "time",
                    time: {
                        "unit": "day",
                        "displayFormats": {
                            "day": "DD MMM YYYY"
                        },
                        "parser": "YYYY-MM-DD"
                    }
                }]
            }
        }
    });
    return myChart;
}

function generate_activity_polar_area(canvas_id, data, labels) {
    const canvas = document.getElementById(canvas_id);
    const ctx = canvas.getContext('2d');
    const colors = [];
    labels.forEach(function(item, index, array) {
        colors.push(getRandomColor());
    });
    const myChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'user activities',
                data: data,
                borderWidth: 1,
                backgroundColor: colors
            }]
        },
        options: {
            scale: {
                ticks: {
                    stepSize: 1
                }
            }
        }
    });
    return myChart;
}

