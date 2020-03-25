#coding:utf-8
import cgi

with open("deathCOVID.csv", "r") as file:
    l = []
    k = []
    m = 0
    data = file.readlines()
    for line in data:
        if m == 0:
            m += 1
            words = line.split(",")
            l.append(words)
        else:
            words = line.split(",")
            k.append(words)


        
    
print("content-type: text/html; charset=utf-8\n")

html = """<!DOCTYPE html>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js"></script>

<head>
    <meta charset="utf-8">
    <title>Ma page web</title>
</head>
<body>
    <h1>Bonjour !</h1>
    <p>bla bla bla bla bla</p>
</body>
<canvas id="myChart" width="400" height="400"></canvas>
<script>
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [{}}],
        datasets: [{
            label: '# of Votes',
            data: {}},
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
</script>
</html>
""".format(l,k)
print(html)
