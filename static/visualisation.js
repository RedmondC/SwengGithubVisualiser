window.onload = function() {
  window.myChart = new Chart(document.getElementById("myChart"), {
      type: 'bar',
      data: {
        labels: ["one","two","three","four","five"],
        datasets: [
          {
            label: "test chart",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: [1,2,3,4,5]
          }
        ]
      },
      options: {
        legend: { display: true },
        title: {
          display: true,
          text: 'Total commits by repository'
        },
        responsive:true
      }
  })
};